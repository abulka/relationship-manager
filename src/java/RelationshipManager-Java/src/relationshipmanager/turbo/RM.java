package relationshipmanager.turbo;

import java.util.List;

/**
 *
 * @author Tarik
 */
public class RM extends RelationshipMgrTurbo implements IRM {

    public void ER(String relId, Cardinality cardinality) {
        this.EnforceRelationship(relId, cardinality);
    }

    public void ER(String relId, Cardinality cardinality, Directionality directionality) {
        this.EnforceRelationship(relId, cardinality, directionality);
    }

    public void R(Object fromObj, Object toObj, String relId) {
        this.AddRelationship(fromObj, toObj, relId);
    }

    public List PS(Object fromObj, String relId) {
        return this.FindObjectsPointedToByMe(fromObj, relId);
    }

    public Object P(Object fromObj, String relId) {
        return this.FindObjectPointedToByMe(fromObj, relId);
    }

    public List BS(Object toObj, String relId) {
        return this.FindObjectsPointingToMe(toObj, relId);
    }

    public Object B(Object toObj, String relId) {
        return this.FindObjectPointingToMe(toObj, relId);
    }

    public void NR(Object fromObj, Object toObj, String relId) {
        this.RemoveRelationship(fromObj, toObj, relId);
    }

    public void NRS(Object obj, String relId) {
        this.RemoveAllRelationshipsInvolving(obj, relId);
    }

    public boolean QR(Object fromObj, Object toObj, String relId) {
        return this.DoesRelIdExistBetween(fromObj, toObj, relId);
    }
    
    public String D() {
        return this.Dump();
    }
}
