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
import relationshipmanager.turbo.IRM;
import relationshipmanager.turbo.RM;
import static org.junit.Assert.*;

/**
 *
 * @author Tarik
 */
public class UnitTestRMShortHand {

    public UnitTestRMShortHand() {
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
    private IRM rm;

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
        rm = new RM();
    }

    @Test
    public void TestRM_01() {
        Object a = 'a', b = 'b'; // use boxed 
        rm.ER("rel1", Cardinality.OneToOne);
        rm.R(a, b, "rel1");
        assertTrue(rm.QR(a, b, "rel1"));
    }

    @Test
    public void TestRM_02() {

        Object one = 1, two = 2, three = 3; // use boxed 
        rm.ER("rel2", Cardinality.OneToOne);
        rm.R(one, two, "rel2");
        rm.R(one, three, "rel2");
        assertFalse(rm.QR(one, two, "rel2"));
        assertTrue(rm.QR(one, three, "rel2"));
    }
}
    
