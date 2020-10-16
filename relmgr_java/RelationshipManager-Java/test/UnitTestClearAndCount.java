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
import relationshipmanager.turbo.IRelationshipManager;
import relationshipmanager.turbo.RelationshipMgrTurbo;
import static org.junit.Assert.*;

/**
 *
 * @author Tarik
 */
public class UnitTestClearAndCount {

    public UnitTestClearAndCount() {
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
        public void ClearSingle()
        {
            rm.AddRelationship('a', 'b', "rel1");
            rm.Clear();
            List list = rm.FindObjectsPointingToMe('b', "rel1");
            assertEquals(0, list.size());
        }

        @Test
        public void ClearMany()
        {
            rm.AddRelationship('a', 'b', "rel1");
            rm.AddRelationship("andy", 'b', "rel1");
            rm.AddRelationship("andy", 'c', "rel1");
            rm.AddRelationship("andy2", 'z', "rel2");
            rm.Clear();

            assertEquals(null, rm.FindObjectPointedToByMe('a', "rel1"));
            assertEquals(null, rm.FindObjectPointedToByMe("andy", "rel2"));
            assertEquals(null, rm.FindObjectPointedToByMe("andy", "rel2"));

            assertEquals(0, rm.FindObjectsPointingToMe('b', "rel1").size());
            assertEquals(null, rm.FindObjectPointingToMe('b', "rel1"));
            assertEquals(null, rm.FindObjectPointingToMe('c', "rel1"));
            assertEquals(null, rm.FindObjectPointingToMe('z', "rel2"));
        }

        @Test
        public void CountZero()
        {
            assertEquals(0, rm.Count());
        }

        @Test
        public void CountZeroAfterClear()
        {
            rm.AddRelationship('a', 'b', "rel1");
            rm.AddRelationship("andy", 'b', "rel1");
            rm.Clear();
            assertEquals(0, rm.Count());
        }

        @Test
        public void CountOne()
        {
            rm.AddRelationship('a', 'b', "rel1");
            assertEquals(1, rm.Count());
        }

        @Test
        public void CountMany()
        {
            rm.AddRelationship('a', 'b', "rel1");
            rm.AddRelationship("andy", 'b', "rel2");
            assertEquals(2, rm.Count());
        }

        @Test
        public void CountManyAfterRemove()
        {
            rm.AddRelationship('a', 'b', "rel1");
            rm.AddRelationship("andy", 'b', "rel2"); 
            assertEquals(2, rm.Count());

            rm.RemoveAllRelationshipsInvolving("andy", "rel2");
            assertEquals(1, rm.Count());

            rm.RemoveAllRelationshipsInvolving('b', "rel2");  // does not affect anything
            assertEquals(1, rm.Count());
            rm.RemoveAllRelationshipsInvolving('b', "rel1");
            assertEquals(0, rm.Count());
        }

        @Test
        public void CountRelationshipsSimple()
        {
            rm.AddRelationship('a', 'b', "rel1");
            rm.AddRelationship('a', 'c', "rel1");
            rm.AddRelationship("andy", 'b', "rel2"); 
            assertEquals(2, rm.CountRelationships("rel1"));
            assertEquals(1, rm.CountRelationships("rel2"));

            rm.RemoveAllRelationshipsInvolving("andy", "rel2");
            assertEquals(2, rm.CountRelationships("rel1"));
            assertEquals(0, rm.CountRelationships("rel2"));

            rm.RemoveAllRelationshipsInvolving('a', "rel1");
            assertEquals(0, rm.CountRelationships("rel1"));
            assertEquals(0, rm.CountRelationships("rel2"));

        }
    

}