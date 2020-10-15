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
public class UnitTestBackLinks {

    public UnitTestBackLinks() {
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
    public void SetUp() {
        rm = new RelationshipMgrTurbo();
    }

    @Test
    public void BackSingleBackLink() {
        rm.AddRelationship('a', 'b', "rel1");

        List list = rm.FindObjectsPointingToMe('b', "rel1");
        assertEquals(list.get(0), 'a');
    }

    @Test
    public void BackMultipleLinks() {

        rm.AddRelationship('a', 'b', "rel1");
        rm.AddRelationship('a', 'c', "rel1");
        rm.AddRelationship('x', 'c', "rel1");
        rm.AddRelationship('a', 'c', "rel2");

        List list = rm.FindObjectsPointingToMe('c', "rel1");
        char[] expected = {'a', 'x'};
        assertTrue(list.contains('a') && list.contains('x') && list.size() == 2);
    }

    @Test
    public void BackLinksSingleObject() {
        rm.AddRelationship('a', 'b', "rel1");
        rm.AddRelationship('a', 'c', "rel1");
        rm.AddRelationship('x', 'c', "rel1");
        rm.AddRelationship('q', 'c', "rel2");

        assertEquals('q', rm.FindObjectPointingToMe('c', "rel2"));
    }

    @Test
    public void BackFindSingularWhenNonExistent() {
        rm.AddRelationship("andy", 'b', "rel1");

        assertEquals(null, rm.FindObjectPointingToMe('b', "rel2"));
    }
}
