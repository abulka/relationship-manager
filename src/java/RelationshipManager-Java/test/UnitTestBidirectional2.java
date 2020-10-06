/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

import java.util.List;
import org.junit.Before;
import org.junit.Test;
import relationshipmanager.turbo.IRM;
import relationshipmanager.turbo.RM;
import relationshipmanager.turbo.RelationshipMgrTurbo;
import static org.junit.Assert.*;

/**
 *
 * @author Tarik
 */
public class UnitTestBidirectional2 {

    public IRM RM;

    @Before
    public void SetUp() {
        RM = new RM();
        BO.SetRm(RM);
    }

    @Test
    public void BidirectionalBug1a() {
        RelationshipMgrTurbo rm = (RelationshipMgrTurbo) RM;

        X x1;
        Y y1, y2;
        x1 = new X();
        y1 = new Y();
        y2 = new Y();
        x1.addY(y1);
        assertEquals(2, RM.Count());
        assertEquals(2, RM.CountRelationships("xtoy"));

        x1.addY(y2);
        assertEquals(4, RM.Count());
        assertEquals(4, RM.CountRelationships("xtoy"));

        List result = x1.getAllY();

        assertTrue(result.contains(y1) && result.contains(y2) & result.size() == 2);

    }
}
