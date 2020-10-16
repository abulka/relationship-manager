using System;
using System.Collections;
using System.Text;

using RelationshipManager.Interfaces;

namespace RelationshipManager.Turbo
{
    public enum Optimize
    {
        SkipBacklinkRemoval,
        SkipForwardlinkRemoval,
        DontOptimize
    }

	public class RelationshipMgrTurbo : IRelationshipManager
    {
        #region Data Structures

        private Links forwardLinks;
        private Links backLinks;
        private Hashtable constraintsCardinality = new Hashtable();
        private Hashtable constraintsDirectionality = new Hashtable();
        private enum RelationshipOp { Add, Remove, CountAll, CountRelIds };
        private enum CountingOp { All, MatchRelId };

        public RelationshipMgrTurbo()
        {
            forwardLinks = new Links(this, LinksDirection.Forward);
            backLinks = new Links(this, LinksDirection.Backward);
        }

        #endregion

        # region Flags to Control Implementation Behaviour

        private bool autoCompactHashTables = true;
        private bool maintainBackLinks = true;
        private bool enforceConstraints = true;
        public bool optimiseOneToOne = true;

        #endregion

        #region Caching

        private CallCacheObjStrObj cacheCallFindObjectPointedToByMe = new CallCacheObjStrObj();
        private CallCacheObjStrObj cacheCallFindObjectPointingToMe = new CallCacheObjStrObj();
        private CallCacheInt cacheCallCount = new CallCacheInt();
        private CallCacheStrInt cacheCallCountRelationships = new CallCacheStrInt();

        private void InvalidateCaches()
        {
            cacheCallFindObjectPointedToByMe.Invalidate();
            cacheCallFindObjectPointingToMe.Invalidate();
            cacheCallCount.Invalidate();
            cacheCallCountRelationships.Invalidate();
        }

        #endregion

        #region Add and Remove Relationship

        public void Clear()
		{
			forwardLinks.Clear();
			backLinks.Clear();
            InvalidateCaches();
		}

		/// 
		/// <param name="fromObj">Can be any object e.g. an object, string, char etc. Not sure about numbers</param>
		/// <param name="toObj">Any object</param>
		/// <param name="relId">A string describing the relationship e.g. "rel1" or "C->A" or "CustomerOrders"</param>
		public void AddRelationship(object fromObj, object toObj, string relId)
		{
			RelationshipOperation(RelationshipOp.Add, fromObj, toObj, relId, false);

            if (EnforceBidirectionality(relId))
		        RelationshipOperation(RelationshipOp.Add, toObj, fromObj, relId, true);
		}

        private bool EnforceBidirectionality(string relId)
        {
            return enforceConstraints && 
                constraintsDirectionality.Contains(relId) &&
                (Directionality)constraintsDirectionality[relId] == Directionality.DoubleDirectional;
        }

        public void AddRelationship(object fromObj, object toObj)
        {
            AddRelationship(fromObj, toObj, "");
        }
        
        /// 
		/// <param name="fromObj"></param>
		/// <param name="toObj"></param>
		/// <param name="relId"></param>
        public void RemoveRelationship(object fromObj, object toObj, string relId, Optimize optimization)
		{
            RelationshipOperation(RelationshipOp.Remove, fromObj, toObj, relId, false, optimization);

            if (EnforceBidirectionality(relId))
                RelationshipOperation(RelationshipOp.Remove, toObj, fromObj, relId, true);  // not sure if safe to pass optimization in here.
		}
        public void RemoveRelationship(object fromObj, object toObj, string relId)
        {
            RemoveRelationship(fromObj, toObj, relId, Optimize.DontOptimize);
        }


        private void RelationshipOperation(RelationshipOp operation, object fromObj, object toObj, string relId, bool isBi)
        {
            RelationshipOperation(operation, fromObj, toObj, relId, isBi, Optimize.DontOptimize);
        }
		private void RelationshipOperation(RelationshipOp operation, object fromObj, object toObj, string relId, bool isBi, Optimize optimization)
		{
			IToObjs rhs;

            if (fromObj == null || toObj == null)
                return;

            if (enforceConstraints && operation == RelationshipOp.Add && !isBi)
                RemoveExistingRelationships(fromObj, toObj, relId);


            if (optimiseOneToOne && operation == RelationshipOp.Remove && optimization == Optimize.SkipForwardlinkRemoval)
            {
                // skip
            }
            else
            {
                rhs = forwardLinks.GetToObjs(fromObj, relId);
                if (operation == RelationshipOp.Add)
                    rhs.Add(toObj);
                else
                {
                    rhs.Remove(toObj);
                    CompactRelIdHashtable(forwardLinks, fromObj, relId, rhs);
                }
            }


            if (optimiseOneToOne && operation == RelationshipOp.Remove && optimization == Optimize.SkipBacklinkRemoval)
            {
                // skip
            }
            else
            {
                if (maintainBackLinks)
                {
                    rhs = backLinks.GetToObjs(toObj, relId);
                    if (operation == RelationshipOp.Add)
                        rhs.Add(fromObj);
                    else
                    {
                        rhs.Remove(fromObj);
                        CompactRelIdHashtable(backLinks, toObj, relId, rhs);
                    }
                }
            }

            InvalidateCaches();
        }

		#endregion

		#region Utility (Compaction)

		private void CompactRelIdHashtable(Links rootLinks, object fromObj, string relId, IToObjs rhs)
		{
			if (autoCompactHashTables && rhs.Count == 0)
			{
                RelIds relIdsHashtable = rootLinks.FindRelIds(fromObj);
				relIdsHashtable.Remove(relId);
			}
		}

		private void CompactRootLinksHashtable(Links rootLinks, object obj, RelIds relIds)
		{
			if (autoCompactHashTables && relIds.Count == 0)
				rootLinks.Remove(obj);
		}

		#endregion

		#region Enforcement

        public Cardinality LookUpCardinality(string relId)
        {
            if (!constraintsCardinality.Contains(relId))
                return Cardinality.ManyToMany;
            return (Cardinality)constraintsCardinality[relId];
        }

        private void RemoveExistingRelationships(object fromObj, object toObj, string relId)
        {
            switch (LookUpCardinality(relId))
            {
                case Cardinality.OneToOne:
                    ExtinguishOldFrom(toObj, relId);
                    ExtinguishOldTo(fromObj, relId);
                    break;

                case Cardinality.OneToMany:
                    ExtinguishOldFrom(toObj, relId);
                    break;

                case Cardinality.ManyToOne:
                    ExtinguishOldTo(fromObj, relId);
                    break;

                case Cardinality.ManyToMany:
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
        private void ExtinguishOldFrom(object toObj, string relId)
        {
		    object oldFrom = FindObjectPointingToMe(toObj, relId);
            if (oldFrom != null)
                RemoveRelationship(oldFrom, toObj, relId, Optimize.SkipBacklinkRemoval);
        }

        private void ExtinguishOldTo(object fromObj, string relId)
        {
            if (fromObj == null)
                throw new Exception("null cannot point to anything!");
		    object oldTo = FindObjectPointedToByMe(fromObj, relId);
            if (oldTo != null)
                RemoveRelationship(fromObj, oldTo, relId, Optimize.SkipForwardlinkRemoval);
        }

		/// 
		/// <param name="relId"></param>
		/// <param name="cardinality"></param>
        public void EnforceRelationship(string relId, Cardinality cardinality)
        {
            constraintsCardinality[relId] = cardinality;
		}

		/// 
		/// <param name="relId"></param>
		/// <param name="cardinality"></param>
		/// <param name="directionality"></param>
        public void EnforceRelationship(string relId, Cardinality cardinality, Directionality directionality)
		{
            constraintsCardinality[relId] = cardinality;
            constraintsDirectionality[relId] = directionality;
		}

		#endregion

		#region Find (Singular)

		/// 
		/// <param name="fromObj"></param>
		/// <param name="relId"></param>
		public object FindObjectPointedToByMe(object fromObj, string relId)
		{
            object result;
            CallCacheObjStrObj cache = cacheCallFindObjectPointedToByMe;

            if (CallCache.cacheEnabled && cache.CallMatches(fromObj, relId))
                return cache.Result;
            
			IToObjs rhsObjs = forwardLinks.GetToObjs(fromObj, relId);
            result = rhsObjs.GetFirstHashKey();

            if (CallCache.cacheEnabled)
                cache.SetData(fromObj, relId, result);
            return result;
		}

		/// 
		/// <param name="toObj"></param>
		/// <param name="relId"></param>
		public object FindObjectPointingToMe(object toObj, string relId)
		{
            object result;
            CallCacheObjStrObj cache = cacheCallFindObjectPointingToMe;

            if (CallCache.cacheEnabled && cache.CallMatches(toObj, relId))
                return cache.Result;

			IToObjs rhsObjs = backLinks.GetToObjs(toObj, relId);
            result = rhsObjs.GetFirstHashKey();

            if (CallCache.cacheEnabled)
                cache.SetData(toObj, relId, result);
            return result;
		}

		#endregion

		#region Find (Plural)
		/// 
		/// <param name="fromObj"></param>
		/// <param name="relId"></param>
		public IList FindObjectsPointedToByMe(object fromObj, string relId)
		{
			ArrayList result = forwardLinks.GetToObjs(fromObj, relId).ToArray();
			return result;
		}

		/// 
		/// <param name="toObj"></param>
		/// <param name="relId"></param>
		public IList FindObjectsPointingToMe(object toObj, string relId){
			ArrayList result = backLinks.GetToObjs(toObj, relId).ToArray();
			return result;
		}

		#endregion

		#region Remove All

		/// 
		/// <param name="obj"></param>
		/// <param name="relId"></param>
		public void RemoveAllRelationshipsInvolving(object obj, string relId){
			RemoveAll(forwardLinks, obj, relId);
			if (maintainBackLinks)
				RemoveAll(backLinks, obj, relId);
            InvalidateCaches();
		}

        private void RemoveAll(Links rootLinks, object obj, string relId)
		{
			RemoveRelationshipsHash(rootLinks, obj, relId);
			RemoveOtherReferencesTo(rootLinks, obj, relId);
		}

		private void RemoveRelationshipsHash(Links rootLinks, object obj, string relId)
		{
            RelIds relIds = rootLinks.GetRelIdsHashTable(obj, false);
			relIds.Remove(relId);

			CompactRootLinksHashtable(rootLinks, obj, relIds);
		}

        private void RemoveOtherReferencesTo(Links rootLinks, object obj, string relId)
		{
			// Now need to find all possible relationships involving the 'obj'
			foreach (object o in rootLinks.Value.Keys)
			{
                RelIds relIdsHashTable = rootLinks.FindRelIds(o);
				if (relIdsHashTable.Contains(relId))
					((IToObjs)relIdsHashTable.FindToObjs(relId)).Remove(obj);
			}
		}

		#endregion

		#region Counting Relationships

		public int Count()
		{
            CallCacheInt cache = cacheCallCount;
            int result;

            if (CallCache.cacheEnabled && cache.CallMatches())
                return cache.Result;

			result = CountOperation(CountingOp.All, null);

            if (CallCache.cacheEnabled)
                cache.SetData(result);
            return result;
		}

		public int CountRelationships(string relId)
		{
            CallCacheStrInt cache = cacheCallCountRelationships;
            int result;

            if (CallCache.cacheEnabled && cache.CallMatches(relId))
                return cache.Result;

			result = CountOperation(CountingOp.MatchRelId, relId);

            if (CallCache.cacheEnabled)
                cache.SetData(relId, result);
            return result;
		}

		private int CountOperation(CountingOp op, string matchingRelId)
		{
            RelIds relIds;
			int result = 0;

			foreach (object o in forwardLinks.Value.Keys)
			{
				relIds = forwardLinks.GetRelIdsHashTable(o, false);
				foreach (string relId in relIds.Value.Keys)
				{
					if ((op == CountingOp.MatchRelId && relId == matchingRelId) || op == CountingOp.All)
						result += ((IToObjs)relIds.FindToObjs(relId)).Count;
				}
			}
			return result;
		}

		#endregion

        #region Misc Relationship Querying

        /// <summary>
        /// Does the specified relationship exist
        /// </summary>
        /// <param name="fromObj"></param>
        /// <param name="toObj"></param>
        /// <param name="relId"></param>
        /// <returns>True or False</returns>
        public bool DoesRelIdExistBetween(object fromObj, object toObj, string relId)
        {
            return forwardLinks.GetToObjs(fromObj, relId).Contains(toObj);
        }

        public IList FindRelIdsBetween(object fromObj, object toObj)
        {
            IToObjs toObjs;
            ArrayList result = new ArrayList();

            RelIds relIds = forwardLinks.GetRelIdsHashTable(fromObj, false);
            foreach (string relId in relIds.Value.Keys)
            {
                toObjs = relIds.FindToObjs(relId);
                if (toObjs.Contains(toObj))
                    result.Add(relId);
            }
            return result;
        }

        #endregion

    }

    public class RM : RelationshipMgrTurbo, IRM {
        public void ER(string relId, Cardinality cardinality) {
		    this.EnforceRelationship(relId, cardinality); }

        public void ER(string relId, Cardinality cardinality, Directionality directionality) {
		    this.EnforceRelationship(relId, cardinality, directionality); }

	    public void R(object fromObj, object toObj, string relId) {
		    this.AddRelationship(fromObj, toObj, relId); }

	    public IList PS(object fromObj, string relId) {
		    return this.FindObjectsPointedToByMe(fromObj, relId); }

	    public object P(object fromObj, string relId) {
		    return this.FindObjectPointedToByMe(fromObj, relId); }

	    public IList BS(object toObj, string relId) {
	 	    return this.FindObjectsPointingToMe(toObj, relId); }

	    public object B(object toObj, string relId) {
		    return this.FindObjectPointingToMe(toObj, relId); }

	    public void NR(object fromObj, object toObj, string relId) {
		    this.RemoveRelationship(fromObj, toObj, relId); }

	    public void NRS(object obj, string relId) {
		    this.RemoveAllRelationshipsInvolving(obj, relId); }

        public bool QR(object fromObj, object toObj, string relId) {
            return this.DoesRelIdExistBetween(fromObj, toObj, relId); }

    }

}
