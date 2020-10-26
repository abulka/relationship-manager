using System;
using System.Text;
using System.Collections;
using Microsoft.VisualStudio.TestTools.UnitTesting;

using RelationshipManager.Interfaces;
using RelationshipManager.Turbo;

namespace Tests
{
    [TestClass]
    public class UnitTestBackLinkRemoval
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
        public void BackRemoveSimpleSingle()
        {
            rm.AddRelationship('a', 'b', "rel1");
            rm.RemoveRelationship('a', 'b', "rel1");
            IList list = rm.FindObjectsPointingToMe('b', "rel1");
            Assert.AreEqual(0, list.Count);
        }

        [TestMethod]
        public void BackRemoveAllRelationshipsFrom()
        {
            rm.AddRelationship("andy", 'b', "rel1");
            rm.AddRelationship("andy", 'c', "rel1");
            rm.AddRelationship("andy2", 'z', "rel2");
            rm.RemoveAllRelationshipsInvolving("andy", "rel1");
            Assert.AreEqual(null, rm.FindObjectPointingToMe('b', "rel1"));
            Assert.AreEqual(null, rm.FindObjectPointingToMe('c', "rel1"));
            Assert.AreEqual("andy2", (string)rm.FindObjectPointingToMe('z', "rel2"));
        }

        [TestMethod]
        public void BackRemoveAllRelationshipsTo()
        {
            rm.AddRelationship("andy", 'b', "rel1");
            rm.AddRelationship("andy2", 'c', "rel1");
            rm.AddRelationship("andy", 'b', "rel2");
            rm.RemoveAllRelationshipsInvolving('b', "rel1");
            Assert.AreEqual(null, rm.FindObjectPointingToMe('b', "rel1"));
            Assert.AreEqual("andy", (string)rm.FindObjectPointingToMe('b', "rel2"));

            rm.RemoveAllRelationshipsInvolving('b', "rel2");
            Assert.AreEqual(null, rm.FindObjectPointingToMe('b', "rel2"));

            Assert.AreEqual("andy2", (string)rm.FindObjectPointingToMe('c', "rel1"));
        }
    }
}
