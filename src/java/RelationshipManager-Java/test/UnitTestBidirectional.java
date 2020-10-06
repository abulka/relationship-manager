/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

import java.util.List;
import org.junit.Before;
import org.junit.Test;
import relationshipmanager.turbo.Cardinality;
import relationshipmanager.turbo.Directionality;
import relationshipmanager.turbo.IRM;
import relationshipmanager.turbo.RM;
import static org.junit.Assert.*;

/**
 *
 * @author Tarik
 */
public class UnitTestBidirectional {
    //private IRelationshipManager rm;
    private IRM RM;

    @Before
    public void SetUp() {
        //rm = new RelationshipMgrTurbo();
        RM = new RM();
    }

    @Test
    public void BidirectionalBug1() {
        RM.ER("xtoy", Cardinality.OneToMany, Directionality.DoubleDirectional);
        RM.R("x1", "y1", "xtoy");   // x1.addY(y1)
        RM.R("x1", "y2", "xtoy");   // x1.addY(y2)

        List result = RM.PS("x1", "xtoy");  // getAllY()

        assertTrue(result.contains("y1") && result.contains("y2") && result.size() == 2);
    }
}

