/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

import org.junit.After;
import org.junit.AfterClass;
import org.junit.Assert;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;
import relationshipmanager.turbo.Cardinality;
import relationshipmanager.turbo.Directionality;
import relationshipmanager.turbo.IRM;
import relationshipmanager.turbo.RM;
import relationshipmanager.turbo.RelationshipMgrTurbo;
import static org.junit.Assert.*;

/**
 *
 * @author Tarik
 */
public class FindCacheFullTest1 {

    public FindCacheFullTest1() {
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
    public IRM RM;

    @Before
    public void SetUp() {
        RM = new RM();
        BO.SetRm(RM);
    }

    @Test
    public void CacheBug1a() {
        RelationshipMgrTurbo rm = (RelationshipMgrTurbo) RM;

        X x1, x2;
        Y y1, y2;
        x1 = new X();
        x2 = new X();
        y1 = new Y();
        y2 = new Y();

        // onetooneasserts(x1,x2,y1,y2)

        //# Initial situation
        //assertallclear(x1, x2, y1, y2)

        //# After clearing pointers
            /*
        x1.clearY();
        x2.clearY();
        y1.clearX();
        y2.clearX();
         */
        //assertallclear(x1, x2, y1, y2)

        //# After setting one pointer, x1 <-> y1
        x1.setY(y1);
        assertEquals(y1, x1.getY());  // usual point of failure
        assertEquals(null, x2.getY());

    //Assert.AreEqual(1, 0); // force fail
    }

    class X extends BO {

        public X() {
            RM.ER("xtoy", Cardinality.OneToOne, Directionality.DirectionalWithBackPointer);
        }

        public void setY(Y y) {
            RM.R(this, y, "xtoy");
        }

        public Y getY() {
            return (Y) RM.P(this, "xtoy");
        }

        public void clearY() {
            RM.NR(this, this.getY(), "xtoy");
        }
    }

    class Y extends BO {

        public Y() {
            RM.ER("xtoy", Cardinality.OneToOne, Directionality.DirectionalWithBackPointer);
        }

        public void setX(X x) {
            RM.R(x, this, "xtoy");
        }

        public X getX() {
            return (X) RM.B(this, "xtoy");
        }

        public void clearX() {
            RM.NR(this.getX(), this, "xtoy");
        }
    }
}
