/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package relationshipmanager.turbo;

import java.util.List;

/**
 *
 * @author Tarik
 */
public interface IRelationshipManager {
    public void AddRelationship(Object fromObj, Object toObj, String relId);
    public Object FindObjectPointedToByMe(Object fromObj, String relId);
    public List FindObjectsPointedToByMe(Object fromObj, String relId);
    public void RemoveRelationship(Object fromObj, Object toObj, String relId);
    public void RemoveAllRelationshipsInvolving(Object obj, String relId);
    public Object FindObjectPointingToMe(Object toObj, String relId);
    public List FindObjectsPointingToMe(Object toObj, String relId);
    public int Count();
    public int CountRelationships(String relId);
    public void Clear();
    public void EnforceRelationship(String relId, Cardinality cardinality);
    public boolean DoesRelIdExistBetween(Object fromObj, Object toObj, String relId);
    public List FindRelIdsBetween(Object fromObj, Object toObj);
    public String Dump();
}
