/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

import java.util.List;
import org.junit.After;
import org.junit.AfterClass;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;
import relationshipmanager.turbo.Cardinality;
import relationshipmanager.turbo.IRelationshipManager;
import relationshipmanager.turbo.RelationshipMgrTurbo;
import static org.junit.Assert.*;

/**
 *
 * @author Tarik
 */
public class UnitTestEnforcement {

    public UnitTestEnforcement() {
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

            private IRelationshipManager rm;

        // region Additional test attributes
        //
        // You can use the following additional attributes as you write your tests:
        //
        // Use ClassInitialize to run code before running the first test in the class
        // [ClassInitialize()]
        // public static void MyClassInitialize(TestContext testContext) { }
        //
        // Use ClassCleanup to run code after all tests in a class have run
        // [ClassCleanup()]
        // public static void MyClassCleanup() { }
        //
        // Use TestInitialize to run code before running each test 
        // [TestInitialize()]
        // public void MyTestInitialize() { }
        //
        // Use TestCleanup to run code after each test has run
        // [TestCleanup()]
        // public void MyTestCleanup() { }
        //
        // endregion

        @Before
        public void SetUp()
        {
            rm = new RelationshipMgrTurbo();
        }

        @Test
        public void EnforceOneToOneSimple()
        {
            //rm.EnforceRelationship("rel1", Cardinality.OneToOne);
            //rm.AddRelationship('a', 'b', "rel1");
            //rm.AddRelationship('a', 'c', "rel1");
            //List list = rm.FindObjectsPointedToByMe('a', "rel1");
            //assertEquals(1, list.size());
            //assertEquals(list.get(0), 'c');

            Object a = 'a', b = 'b', c = 'c';
            rm.EnforceRelationship("rel1", Cardinality.OneToOne);
            rm.AddRelationship(a, b, "rel1");
            rm.AddRelationship(a, c, "rel1");
            List list = rm.FindObjectsPointedToByMe(a, "rel1");
            assertEquals(1, list.size());
            assertEquals(list.get(0), c);

            list = rm.FindObjectsPointingToMe(c, "rel1");
            assertEquals(1, list.size());
            assertEquals(list.get(0), a);

            list = rm.FindObjectsPointingToMe(b, "rel1");
            assertEquals(0, list.size());
        }



}