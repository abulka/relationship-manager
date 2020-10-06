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
public interface IRM {
    public void ER(String relId, Cardinality cardinality);
    public void ER(String relId, Cardinality cardinality, Directionality directionality);
    public void R(Object fromObj, Object toObj, String relId);
    public List PS(Object fromObj, String relId);
    public Object P(Object fromObj, String relId);
    public List BS(Object toObj, String relId);
    public Object B(Object toObj, String relId);
    public void NR(Object fromObj, Object toObj, String relId);
    public void NRS(Object obj, String relId);
    public boolean QR(Object fromObj, Object toObj, String relId);
    public int Count();
    public int CountRelationships(String relId);
    public void EnforceRelationship(String relId, Cardinality cardinality);
    public boolean DoesRelIdExistBetween(Object fromObj, Object toObj, String relId);
    public String D();
}
