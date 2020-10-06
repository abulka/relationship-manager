/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package relationshipmanager.turbo;

/**
 *
 * @author Tarik
 */
public class Links extends HashColl {

    RelIds result;
    private RelationshipMgrTurbo rm;
    private LinksDirection linksDirection;

    public Links(RelationshipMgrTurbo rm, LinksDirection linksDirection) {
        this.rm = rm;
        this.linksDirection = linksDirection;
    }

    public RelIds FindRelIds(Object fromObj) {
        result = (RelIds) Value.get(fromObj);
        return result;
    }

    public RelIds GetRelIdsHashTable(Object fromObj, boolean repairIfNotThere) {
        RelIds relIds;
        if (this.Contains(fromObj)) {
            relIds = this.FindRelIds(fromObj);
        } else {
            relIds = new RelIds();
            if (repairIfNotThere) {
                this.SetEntry(fromObj, relIds);
            }
        }
        return relIds;

    }

    public IToObjs GetToObjs(Object fromObj, String relId) {
        RelIds relIds;
        IToObjs toObjs;

        relIds = this.GetRelIdsHashTable(fromObj, true);

        if (relIds.Contains(relId)) {
            toObjs = relIds.FindToObjs(relId);
        } else {
            Cardinality cardinality = rm.LookUpCardinality(relId);

            if (rm.optimiseOneToOne) {
                if (cardinality == Cardinality.OneToOne ||
                        cardinality == Cardinality.OneToMany && this.linksDirection == LinksDirection.Backward ||
                        cardinality == Cardinality.ManyToOne && this.linksDirection == LinksDirection.Forward) {
                    toObjs = new ToObjsSingle();
                } else {
                    toObjs = new ToObjs();
                }
            } else {
                toObjs = new ToObjs();
            }

            relIds.SetEntry(relId, toObjs);
        }

        return toObjs;
    }

    public void SetEntry(Object fromObj, RelIds relIds) {
        Value.put(fromObj, relIds);
    }
}
