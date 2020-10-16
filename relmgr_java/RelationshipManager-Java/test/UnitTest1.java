/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

import java.util.ArrayList;
import java.util.List;
import org.junit.After;
import org.junit.AfterClass;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;
import relationshipmanager.turbo.IRelationshipManager;
import relationshipmanager.turbo.RelationshipMgrTurbo;
import static org.junit.Assert.*;

/**
 *
 * @author Tarik
 */
public class UnitTest1 {

    public UnitTest1() {
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

    // TODO add test methods here.
    // The methods must be annotated with annotation @Test. For example:
    //
    // @Test
    // public void hello() {}

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
        public void TestMethod1()
        {
            //
            // TODO: Add test logic	here
            //
            assertEquals (2, 1 + 1);
            ArrayList a = new ArrayList();
            a.add('a');
            assertEquals ('a', a.get(0));
        }

        @Test
        public void BasicSingleAdd()
        {
            rm.AddRelationship('a', 'b', "rel1");
            List list = rm.FindObjectsPointedToByMe('a', "rel1");
            assertEquals(list.get(0), 'b');
        }

        @Test
        public void AddAFew()
        {
            rm.AddRelationship('a', 'b', "rel1");
            rm.AddRelationship('a', 'c', "rel1");
            rm.AddRelationship('a', 'z', "rel2");

            List list;
            list = rm.FindObjectsPointedToByMe('a', "rel1");
            assertTrue(list.contains('b') && list.contains('c') && list.size() == 2);

            list = rm.FindObjectsPointedToByMe('a', "rel2");
            assertEquals(list.get(0), 'z');
        }

        @Test
        public void FingSingular()
        {
            rm.AddRelationship("andy", 'b', "rel1");
            rm.AddRelationship("andy", 'c', "rel2");

            assertEquals(rm.FindObjectPointedToByMe("andy", "rel2"), 'c');
        }

        @Test
        public void FindSingularWhenNonExistent()
        {
            rm.AddRelationship("andy", 'b', "rel1");

            assertEquals (null, rm.FindObjectPointedToByMe("andy", "rel2"));
        }

        @Test
        public void RemoveRelationship()
        {

            rm.AddRelationship("andy", 'b', "rel1");
            rm.AddRelationship("andy", 'c', "rel1");
            rm.RemoveRelationship("andy", 'b', "rel1");

            assertEquals (rm.FindObjectPointedToByMe("andy", "rel1"), 'c');
        }

        @Test
        public void RemoveNonExistantRelationship()
        {
            assertEquals (null, rm.FindObjectPointedToByMe("andy", "rel1"));
            rm.AddRelationship("andy", 'b', "rel1");
            rm.RemoveRelationship("andy", 'b', "rel1");

            assertEquals (null, rm.FindObjectPointedToByMe("andy", "rel1"));
            assertEquals (null, rm.FindObjectPointedToByMe("andy", "rel2"));
        }

        @Test
        public void RemoveAllRelationshipsFrom()
        {
            rm.AddRelationship("andy", 'b', "rel1");
            rm.AddRelationship("andy", 'c', "rel1");
            rm.AddRelationship("andy", 'z', "rel2");

            rm.RemoveAllRelationshipsInvolving("andy", "rel1");
            assertEquals (null, rm.FindObjectPointedToByMe("andy", "rel1"));
            assertEquals (rm.FindObjectPointedToByMe("andy", "rel2"), 'z');
        }

        @Test
        public void RemoveAllRelationshipsTo()
        {
            rm.AddRelationship("andy", 'b', "rel1");
            rm.AddRelationship("andy", 'c', "rel1");
            rm.AddRelationship("andy", 'b', "rel2");

            rm.RemoveAllRelationshipsInvolving('b', "rel1");
            assertEquals (rm.FindObjectPointedToByMe("andy", "rel1"), 'c');
            assertEquals (rm.FindObjectPointedToByMe("andy", "rel2"), 'b');
        }
    
    
    
}