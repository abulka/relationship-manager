using System;
using System.Text;
using System.Collections;
using Microsoft.VisualStudio.TestTools.UnitTesting;

using RelationshipManager.Interfaces;
using RelationshipManager.Turbo;

namespace Tests
{
    /// <summary>
    /// Summary description for UnitTestRMShortHand
    /// </summary>
    [TestClass]
    public class UnitTestRMShortHand
    {
        private IRM rm;

        #region Additional test attributes
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
        #endregion

        [TestInitialize()]
        public void SetUp()
        {
            rm = new RM();
        }

        [TestMethod]
        public void TestRM_01()
        {
            object a = 'a', b = 'b'; // use boxed 
            rm.ER("rel1", Cardinality.OneToOne);
            rm.R(a, b, "rel1");
            Assert.IsTrue(rm.QR(a, b, "rel1"));
        }

        [TestMethod]
        public void TestRM_02()
        {

            object one = 1, two = 2, three = 3; // use boxed 
            rm.ER("rel2", Cardinality.OneToOne);
            rm.R(one, two, "rel2");
            rm.R(one, three, "rel2");
            Assert.IsFalse(rm.QR(one, two, "rel2"));
            Assert.IsTrue(rm.QR(one, three, "rel2"));
        }
    }
}
