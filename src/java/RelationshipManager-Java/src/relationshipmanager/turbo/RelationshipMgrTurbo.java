/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package relationshipmanager.turbo;

import java.util.ArrayList;
import java.util.Hashtable;
import java.util.List;
import javax.naming.spi.DirStateFactory.Result;

/**
 *
 * @author Tarik
 */
public class RelationshipMgrTurbo implements IRelationshipManager {
    
    // region Data Structures
    
    private Links forwardLinks;
    private Links backLinks;
    private Hashtable<String, Cardinality> constraintsCardinality = new Hashtable<String, Cardinality>();
    private Hashtable<String, Directionality> constraintsDirectionality = new Hashtable<String, Directionality>();

    private enum RelationshipOp {

        Add,
        Remove,
        CountAll,
        CountRelIds
    };
    
    private enum CountingOp {
        All,
        MatchRelId
    };

    public RelationshipMgrTurbo() {
        forwardLinks = new Links(this, LinksDirection.Forward);
        backLinks = new Links(this, LinksDirection.Backward);
    }

    // endregion

    // region Flags to Control Implementation Behaviour

    private boolean autoCompactHashTables = true;
    private boolean maintainBackLinks = true;
    private boolean enforceConstraints = true;
    public boolean optimiseOneToOne = true;

    // endregion

    public String Dump()
    {
        String result = "";
        result += "NUMBER OF RELATIONSHIPS " + this.Count() + "\n";
        result += "forwardLinks:\n" + DumpLinks(forwardLinks);
        result += "backLinks:\n" + DumpLinks(backLinks);
        return result;
    }
    
    private String DumpLinks(Links links)
    {
        String result = "";
        RelIds relIds;
        
        // for each FROM object in the forward links dictionary
        for (Object o : links.Value.keySet()) {
            
            // index in on FROM o and get the TO relids dictionary
            relIds = forwardLinks.GetRelIdsHashTable(o, false);

            // print each relationship in the relIds TO dictionary
            for (String relId : relIds.Value.keySet()) {
                
                IToObjs toArray = relIds.FindToObjs(relId);
                
                // for each TO object in the array (each belongs to the same relid)
                for (Object to : toArray.ToArray()) {
                    result += "ENTRY: " + o.toString() + " [" + relId.toString() + "] " + to.toString() + "\n";
                }
            }
            //result += "\n";
        }
        result += "--------\n";
        
        return result;
    }
    
    // region Caching
    private CallCacheObjStrObj cacheCallFindObjectPointedToByMe = new CallCacheObjStrObj();
    private CallCacheObjStrObj cacheCallFindObjectPointingToMe = new CallCacheObjStrObj();
    private CallCacheInt cacheCallCount = new CallCacheInt();
    private CallCacheStrInt cacheCallCountRelationships = new CallCacheStrInt();

    private void InvalidateCaches() {
        cacheCallFindObjectPointedToByMe.Invalidate();
        cacheCallFindObjectPointingToMe.Invalidate();
        cacheCallCount.Invalidate();
        cacheCallCountRelationships.Invalidate();
    }

    // endregion

    // region Add and Remove Relationship
    public void Clear() {
        forwardLinks.Clear();
        backLinks.Clear();
        InvalidateCaches();
    }

    /// 
    /// <param name="fromObj">Can be any Object e.g. an Object, String, char etc. Not sure about numbers</param>
    /// <param name="toObj">Any Object</param>
    /// <param name="relId">A String describing the relationship e.g. "rel1" or "C->A" or "CustomerOrders"</param>
    public void AddRelationship(Object fromObj, Object toObj, String relId) {
        RelationshipOperation(RelationshipOp.Add, fromObj, toObj, relId, false);

        if (EnforceBidirectionality(relId)) {
            RelationshipOperation(RelationshipOp.Add, toObj, fromObj, relId, true);
        }
    }

    private boolean EnforceBidirectionality(String relId) {
        return enforceConstraints &&
                constraintsDirectionality.containsKey(relId) &&
                constraintsDirectionality.get(relId) == Directionality.DoubleDirectional;
    }

    public void AddRelationship(Object fromObj, Object toObj) {
        AddRelationship(fromObj, toObj, "");
    }

    /// 
    /// <param name="fromObj"></param>
    /// <param name="toObj"></param>
    /// <param name="relId"></param>
    public void RemoveRelationship(Object fromObj, Object toObj, String relId, Optimize optimization) {
        RelationshipOperation(RelationshipOp.Remove, fromObj, toObj, relId, false, optimization);

        if (EnforceBidirectionality(relId)) {
            RelationshipOperation(RelationshipOp.Remove, toObj, fromObj, relId, true);
        }  // not sure if safe to pass optimization in here.
    }

    public void RemoveRelationship(Object fromObj, Object toObj, String relId) {
        RemoveRelationship(fromObj, toObj, relId, Optimize.DontOptimize);
    }

    private void RelationshipOperation(RelationshipOp operation, Object fromObj, Object toObj, String relId, boolean isBi) {
        RelationshipOperation(operation, fromObj, toObj, relId, isBi, Optimize.DontOptimize);
    }

    private void RelationshipOperation(RelationshipOp operation, Object fromObj, Object toObj, String relId, boolean isBi, Optimize optimization) {
        IToObjs rhs;

        if (fromObj == null || toObj == null) {
            return;
        }

        if (enforceConstraints && operation == RelationshipOp.Add && !isBi) {
            RemoveExistingRelationships(fromObj, toObj, relId);
        }


        if (optimiseOneToOne && operation == RelationshipOp.Remove && optimization == Optimize.SkipForwardlinkRemoval) {
        // skip
        } else {
            rhs = forwardLinks.GetToObjs(fromObj, relId);
            if (operation == RelationshipOp.Add) {
                rhs.Add(toObj);
            } else {
                rhs.Remove(toObj);
                CompactRelIdHashtable(forwardLinks, fromObj, relId, rhs);
            }
        }


        if (optimiseOneToOne && operation == RelationshipOp.Remove && optimization == Optimize.SkipBacklinkRemoval) {
        // skip
        } else {
            if (maintainBackLinks) {
                rhs = backLinks.GetToObjs(toObj, relId);
                if (operation == RelationshipOp.Add) {
                    rhs.Add(fromObj);
                } else {
                    rhs.Remove(fromObj);
                    CompactRelIdHashtable(backLinks, toObj, relId, rhs);
                }
            }
        }

        InvalidateCaches();
    }

    // endregion

    // region Utility (Compaction)
    private void CompactRelIdHashtable(Links rootLinks, Object fromObj, String relId, IToObjs rhs) {
        if (autoCompactHashTables && rhs.getCount() == 0) {
            RelIds relIdsHashtable = rootLinks.FindRelIds(fromObj);
            relIdsHashtable.Remove(relId);
        }
    }

    private void CompactRootLinksHashtable(Links rootLinks, Object obj, RelIds relIds) {
        if (autoCompactHashTables && relIds.getCount() == 0) {
            rootLinks.Remove(obj);
        }
    }

    // endregion

    // region Enforcement
    public Cardinality LookUpCardinality(String relId) {
        if (!constraintsCardinality.containsKey(relId)) {
            return Cardinality.ManyToMany;
        }
        return constraintsCardinality.get(relId);
    }

    private void RemoveExistingRelationships(Object fromObj, Object toObj, String relId) {
        switch (LookUpCardinality(relId)) {
            case OneToOne:
                ExtinguishOldFrom(toObj, relId);
                ExtinguishOldTo(fromObj, relId);
                break;

            case OneToMany:
                ExtinguishOldFrom(toObj, relId);
                break;

            case ManyToOne:
                ExtinguishOldTo(fromObj, relId);
                break;

            case ManyToMany:
                break;
            }
    }

    /*
     * Its ok to be calling RemoveRelationship within
     *   ExtinguishOldFrom
     *   ExtinguishOldTo
     * even though this seems to be potentially 
     * infinitely recursive, since:
     * 
     * AddRel 
     *  calls - RelationshipOp(opAdd) **
     *    calls - RemoveOld 
     *      calls - RemoveRel 
     *        calls - RelationshipOp(opRemove) **
     * 
     * But the second call to RelationshipOp has a
     * opRemove parameter, and in cases of removal 
     * operations, RemoveOld is not called, thus 
     * avoiding infinite recursion.
     * 
     */

    /// <summary>
    /// Remove anything with the same relId pointing to 'toObj'.  
    /// 
    /// This is strictness.  If you didn't enforce this then
    /// one to one's would become many to ones.  And one to manys
    /// would become many to many.
    /// 
    /// Philosophical point.  This enforces the 'one' on the lhs
    /// of a one to one and a one to many.  It removes what WAS 
    /// pointing to the 'toObj' (the old 'from') before we wire in
    /// the new thing pointing to the 'toObj'.  Thus only one thing
    /// will ever be pointing to the 'toObj'.
    /// </summary>
    /// <param name="toObj"></param>
    /// <param name="relId"></param>
    private void ExtinguishOldFrom(Object toObj, String relId) {
        Object oldFrom = FindObjectPointingToMe(toObj, relId);
        if (oldFrom != null) {
            RemoveRelationship(oldFrom, toObj, relId, Optimize.SkipBacklinkRemoval);
        }
    }

    private void ExtinguishOldTo(Object fromObj, String relId) {
        if (fromObj == null) {
            // throw new Exception("null cannot point to anything!");
            return;
        }
        Object oldTo = FindObjectPointedToByMe(fromObj, relId);
        if (oldTo != null) {
            RemoveRelationship(fromObj, oldTo, relId, Optimize.SkipForwardlinkRemoval);
        }
    }

    /// 
    /// <param name="relId"></param>
    /// <param name="cardinality"></param>
    public void EnforceRelationship(String relId, Cardinality cardinality) {
        constraintsCardinality.put(relId, cardinality);
    }

    /// 
    /// <param name="relId"></param>
    /// <param name="cardinality"></param>
    /// <param name="directionality"></param>
    public void EnforceRelationship(String relId, Cardinality cardinality, Directionality directionality) {
        constraintsCardinality.put(relId, cardinality);
        constraintsDirectionality.put(relId, directionality);
    }

    // endregion

    // region Find (Singular)

    /// 
    /// <param name="fromObj"></param>
    /// <param name="relId"></param>
    public Object FindObjectPointedToByMe(Object fromObj, String relId) {
        Object result;
        CallCacheObjStrObj cache = cacheCallFindObjectPointedToByMe;

        if (CallCache.cacheEnabled && cache.CallMatches(fromObj, relId)) {
            return cache.getResult();
        }

        IToObjs rhsObjs = forwardLinks.GetToObjs(fromObj, relId);
        result = rhsObjs.GetFirstHashKey();

        if (CallCache.cacheEnabled) {
            cache.SetData(fromObj, relId, result);
        }
        return result;
    }

    /// 
    /// <param name="toObj"></param>
    /// <param name="relId"></param>
    public Object FindObjectPointingToMe(Object toObj, String relId) {
        Object result;
        CallCacheObjStrObj cache = cacheCallFindObjectPointingToMe;

        if (CallCache.cacheEnabled && cache.CallMatches(toObj, relId)) {
            return cache.getResult();
        }

        IToObjs rhsObjs = backLinks.GetToObjs(toObj, relId);
        result = rhsObjs.GetFirstHashKey();

        if (CallCache.cacheEnabled) {
            cache.SetData(toObj, relId, result);
        }
        return result;
    }

    // endregion

    // region Find (Plural)
    /// 
    /// <param name="fromObj"></param>
    /// <param name="relId"></param>
    public List FindObjectsPointedToByMe(Object fromObj, String relId) {
        ArrayList result = forwardLinks.GetToObjs(fromObj, relId).ToArray();
        return result;
    }

    /// 
    /// <param name="toObj"></param>
    /// <param name="relId"></param>
    public List FindObjectsPointingToMe(Object toObj, String relId) {
        ArrayList result = backLinks.GetToObjs(toObj, relId).ToArray();
        return result;
    }

    // endregion

    // region Remove All

    /// 
    /// <param name="obj"></param>
    /// <param name="relId"></param>
    public void RemoveAllRelationshipsInvolving(Object obj, String relId) {
        RemoveAll(forwardLinks, obj, relId);
        if (maintainBackLinks) {
            RemoveAll(backLinks, obj, relId);
        }
        InvalidateCaches();
    }

    private void RemoveAll(Links rootLinks, Object obj, String relId) {
        RemoveRelationshipsHash(rootLinks, obj, relId);
        RemoveOtherReferencesTo(rootLinks, obj, relId);
    }

    private void RemoveRelationshipsHash(Links rootLinks, Object obj, String relId) {
        RelIds relIds = rootLinks.GetRelIdsHashTable(obj, false);
        relIds.Remove(relId);

        CompactRootLinksHashtable(rootLinks, obj, relIds);
    }

    private void RemoveOtherReferencesTo(Links rootLinks, Object obj, String relId) {
        // Now need to find all possible relationships involving the 'obj'
        for (Object o : rootLinks.Value.keySet()) {
            RelIds relIdsHashTable = rootLinks.FindRelIds(o);
            if (relIdsHashTable.Contains(relId)) {
                ((IToObjs) relIdsHashTable.FindToObjs(relId)).Remove(obj);
            }
        }
    }

    // endregion

    // region Counting Relationships
    public int Count() {
        CallCacheInt cache = cacheCallCount;
        int result;

        if (CallCache.cacheEnabled && cache.CallMatches()) {
            return cache.getResult();
        }

        result = CountOperation(CountingOp.All, null);

        if (CallCache.cacheEnabled) {
            cache.SetData(result);
        }
        return result;
    }

    public int CountRelationships(String relId) {
        CallCacheStrInt cache = cacheCallCountRelationships;
        int result;

        if (CallCache.cacheEnabled && cache.CallMatches(relId)) {
            return cache.getResult();
        }

        result = CountOperation(CountingOp.MatchRelId, relId);

        if (CallCache.cacheEnabled) {
            cache.SetData(relId, result);
        }
        return result;
    }

    private int CountOperation(CountingOp op, String matchingRelId) {
        RelIds relIds;
        int result = 0;

        for (Object o : forwardLinks.Value.keySet()) {
            relIds = forwardLinks.GetRelIdsHashTable(o, false);
            for (String relId : relIds.Value.keySet()) {
                if ((op == CountingOp.MatchRelId && relId.equals(matchingRelId)) || op == CountingOp.All) {
                    result += ((IToObjs) relIds.FindToObjs(relId)).getCount();
                }
            }
        }
        return result;
    }

    // endregion

    // region Misc Relationship Querying

    /// <summary>
    /// Does the specified relationship exist
    /// </summary>
    /// <param name="fromObj"></param>
    /// <param name="toObj"></param>
    /// <param name="relId"></param>
    /// <returns>True or False</returns>
    public boolean DoesRelIdExistBetween(Object fromObj, Object toObj, String relId) {
        return forwardLinks.GetToObjs(fromObj, relId).Contains(toObj);
    }

    public List FindRelIdsBetween(Object fromObj, Object toObj) {
        IToObjs toObjs;
        ArrayList result = new ArrayList();

        RelIds relIds = forwardLinks.GetRelIdsHashTable(fromObj, false);
        for (String relId : relIds.Value.keySet()) {
            toObjs = relIds.FindToObjs(relId);
            if (toObjs.Contains(toObj)) {
                result.add(relId);
            }
        }
        return result;
    }

    // endregion
}
