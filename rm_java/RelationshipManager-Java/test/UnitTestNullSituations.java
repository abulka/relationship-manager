/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

import org.junit.After;
import org.junit.AfterClass;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;
import relationshipmanager.turbo.IRM;
import relationshipmanager.turbo.IRelationshipManager;
import relationshipmanager.turbo.RM;
import relationshipmanager.turbo.RelationshipMgrTurbo;
import static org.junit.Assert.*;

/**
 *
 * @author Tarik
 */
public class UnitTestNullSituations {

    public UnitTestNullSituations() {
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
    private IRM RM;

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
    public void SetUp() {
        rm = new RelationshipMgrTurbo();
        RM = new RM();
    }

    @Test
    public void TestNoRelationshipsYet() {
        assertFalse(rm.DoesRelIdExistBetween('a', 'b', "rel1"));
    }

    @Test
    public void FindObjectsPointedToByMe1() {
        assertEquals(0, rm.FindObjectsPointedToByMe('a', "rel1").size());
        assertEquals(0, RM.PS('a', "rel1").size());
    }
}
