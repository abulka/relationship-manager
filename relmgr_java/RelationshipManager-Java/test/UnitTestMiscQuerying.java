/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

import java.util.ArrayList;
import org.junit.After;
import org.junit.AfterClass;
import org.junit.Assert;
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
public class UnitTestMiscQuerying {

    public UnitTestMiscQuerying() {
    }

    @BeforeClass
    public static void setUpClass() throws Exception {
    }

    @AfterClass
    public static void tearDownClass() throws Exception {
    }

    @Before
    public void setUp() {
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
    public void DoesRelIdExistBetween() {
        rm.EnforceRelationship("rel1", Cardinality.OneToOne);
        rm.AddRelationship("a", "b", "rel1");

        assertTrue(rm.DoesRelIdExistBetween("a", "b", "rel1"));
    }

    @Test
    public void FindRelIdsBetween() {
        rm.EnforceRelationship("rel1", Cardinality.OneToMany);
        rm.AddRelationship('a', 'b', "rel1");
        rm.AddRelationship('a', 'b', "rel1");
        rm.AddRelationship('a', 'b', "rel2");

        ArrayList expected = new ArrayList();
        expected.add("rel1");
        expected.add("rel2");
        assertTrue(expected.containsAll(rm.FindRelIdsBetween('a', 'b')));
        assertTrue(rm.FindRelIdsBetween('a', 'b').containsAll(expected));
    }
}
