using System;
using System.Text;
using System.Collections;
using Microsoft.VisualStudio.TestTools.UnitTesting;

using RelationshipManager.Interfaces;
using RelationshipManager.Turbo;

namespace Tests
{
    /// <summary>
    /// Summary description for UnitTestNullSituations
    /// </summary>
    [TestClass]
    public class UnitTestNullSituations
    {
        private IRelationshipManager rm;
        private IRM RM;

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
            rm = new RelationshipMgrTurbo();
            RM = new RM();
        }

        [TestMethod]
        public void TestNoRelationshipsYet()
        {
            Assert.IsFalse(rm.DoesRelIdExistBetween('a', 'b', "rel1"));
        }

        [TestMethod]
        public void FindObjectsPointedToByMe1()
        {
            Assert.AreEqual(0, rm.FindObjectsPointedToByMe('a', "rel1").Count);
            Assert.AreEqual(0, RM.PS('a', "rel1").Count);
        }

    }
}
