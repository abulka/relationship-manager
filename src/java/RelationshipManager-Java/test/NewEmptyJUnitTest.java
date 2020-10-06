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
public class NewEmptyJUnitTest {

    public NewEmptyJUnitTest() {
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
        public void BackRemoveSimpleSingle()
        {
            rm.AddRelationship('a', 'b', "rel1");
            rm.RemoveRelationship('a', 'b', "rel1");
            List list = rm.FindObjectsPointingToMe('b', "rel1");
            assertEquals(0, list.size());
        }

        @Test
        public void BackRemoveAllRelationshipsFrom()
        {
            rm.AddRelationship("andy", 'b', "rel1");
            rm.AddRelationship("andy", 'c', "rel1");
            rm.AddRelationship("andy2", 'z', "rel2");
            rm.RemoveAllRelationshipsInvolving("andy", "rel1");
            assertEquals(null, rm.FindObjectPointingToMe('b', "rel1"));
            assertEquals(null, rm.FindObjectPointingToMe('c', "rel1"));
            assertEquals("andy2", rm.FindObjectPointingToMe('z', "rel2"));
        }

        @Test
        public void BackRemoveAllRelationshipsTo()
        {
            rm.AddRelationship("andy", 'b', "rel1");
            rm.AddRelationship("andy2", 'c', "rel1");
            rm.AddRelationship("andy", 'b', "rel2");
            rm.RemoveAllRelationshipsInvolving('b', "rel1");
            assertEquals(null, rm.FindObjectPointingToMe('b', "rel1"));
            assertEquals("andy", rm.FindObjectPointingToMe('b', "rel2"));

            rm.RemoveAllRelationshipsInvolving('b', "rel2");
            assertEquals(null, rm.FindObjectPointingToMe('b', "rel2"));

            assertEquals("andy2", rm.FindObjectPointingToMe('c', "rel1"));
        }

}