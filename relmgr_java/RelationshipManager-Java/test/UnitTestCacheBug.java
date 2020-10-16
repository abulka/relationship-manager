/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

import org.junit.After;
import org.junit.AfterClass;
import org.junit.Before;
import org.junit.BeforeClass;
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
public class UnitTestCacheBug {

    public UnitTestCacheBug() {
    }

    @BeforeClass
    public static void setUpClass() throws Exception {
    }

    @AfterClass
    public static void tearDownClass() throws Exception {
    }

    @After
    public void tearDown() {
    }

    //private IRelationshipManager rm;
    private IRM RM;

    @Before
    public void SetUp() {
        //rm = new RelationshipMgrTurbo();
        RM = new RM();
    }

    @Test
    public void Bug00111() {
        RM.ER("xtoy", Cardinality.OneToOne, Directionality.DirectionalWithBackPointer);

        // # After clearing pointers
        RM.NR("x1", RM.P("x1", "xtoy"), "xtoy"); // x1.clearY()
        RM.NR("x2", RM.P("x2", "xtoy"), "xtoy"); // x2.clearY()
        RM.NR(RM.B("y1", "xtoy"), "y1", "xtoy"); // y1.clearX()
        RM.NR(RM.B("y2", "xtoy"), "y2", "xtoy"); // y2.clearX()

        //assertallclear(x1, x2, y1, y2)

        // # After setting one pointer, x1 <-> y1
        RM.R("x1", "y1", "xtoy"); // x1.setY(y1)

        assertEquals("y1", RM.P("x1", "xtoy")); // assert x1.getY() == y1
        assertEquals(null, RM.P("x2", "xtoy")); // assert x2.getY() == null
    }
}
