using System;
using System.Text;
using System.Collections;
using Microsoft.VisualStudio.TestTools.UnitTesting;

using RelationshipManager.Interfaces;
using RelationshipManager.Turbo;

namespace Tests
{
    [TestClass]
    public class UnitTestClearAndCount
    {

        private IRelationshipManager rm;

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
        }

        [TestMethod]
        public void ClearSingle()
        {
            rm.AddRelationship('a', 'b', "rel1");
            rm.Clear();
            IList list = rm.FindObjectsPointingToMe('b', "rel1");
            Assert.AreEqual(0, list.Count);
        }

        [TestMethod]
        public void ClearMany()
        {
            rm.AddRelationship('a', 'b', "rel1");
            rm.AddRelationship("andy", 'b', "rel1");
            rm.AddRelationship("andy", 'c', "rel1");
            rm.AddRelationship("andy2", 'z', "rel2");
            rm.Clear();

            Assert.AreEqual(null, rm.FindObjectPointedToByMe('a', "rel1"));
            Assert.AreEqual(null, rm.FindObjectPointedToByMe("andy", "rel2"));
            Assert.AreEqual(null, rm.FindObjectPointedToByMe("andy", "rel2"));

            Assert.AreEqual(0, rm.FindObjectsPointingToMe('b', "rel1").Count);
            Assert.AreEqual(null, rm.FindObjectPointingToMe('b', "rel1"));
            Assert.AreEqual(null, rm.FindObjectPointingToMe('c', "rel1"));
            Assert.AreEqual(null, rm.FindObjectPointingToMe('z', "rel2"));
        }

        [TestMethod]
        public void CountZero()
        {
            Assert.AreEqual(0, rm.Count());
        }

        [TestMethod]
        public void CountZeroAfterClear()
        {
            rm.AddRelationship('a', 'b', "rel1");
            rm.AddRelationship("andy", 'b', "rel1");
            rm.Clear();
            Assert.AreEqual(0, rm.Count());
        }

        [TestMethod]
        public void CountOne()
        {
            rm.AddRelationship('a', 'b', "rel1");
            Assert.AreEqual(1, rm.Count());
        }

        [TestMethod]
        public void CountMany()
        {
            rm.AddRelationship('a', 'b', "rel1");
            rm.AddRelationship("andy", 'b', "rel2");
            Assert.AreEqual(2, rm.Count());
        }

        [TestMethod]
        public void CountManyAfterRemove()
        {
            rm.AddRelationship('a', 'b', "rel1");
            rm.AddRelationship("andy", 'b', "rel2"); 
            Assert.AreEqual(2, rm.Count());

            rm.RemoveAllRelationshipsInvolving("andy", "rel2");
            Assert.AreEqual(1, rm.Count());

            rm.RemoveAllRelationshipsInvolving('b', "rel2");  // does not affect anything
            Assert.AreEqual(1, rm.Count());
            rm.RemoveAllRelationshipsInvolving('b', "rel1");
            Assert.AreEqual(0, rm.Count());
        }

        [TestMethod]
        public void CountRelationshipsSimple()
        {
            rm.AddRelationship('a', 'b', "rel1");
            rm.AddRelationship('a', 'c', "rel1");
            rm.AddRelationship("andy", 'b', "rel2"); 
            Assert.AreEqual(2, rm.CountRelationships("rel1"));
            Assert.AreEqual(1, rm.CountRelationships("rel2"));

            rm.RemoveAllRelationshipsInvolving("andy", "rel2");
            Assert.AreEqual(2, rm.CountRelationships("rel1"));
            Assert.AreEqual(0, rm.CountRelationships("rel2"));

            rm.RemoveAllRelationshipsInvolving('a', "rel1");
            Assert.AreEqual(0, rm.CountRelationships("rel1"));
            Assert.AreEqual(0, rm.CountRelationships("rel2"));

        }
    }
}
