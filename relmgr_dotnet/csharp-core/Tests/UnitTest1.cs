using System;
using System.Text;
using System.Collections;
using Microsoft.VisualStudio.TestTools.UnitTesting;

using RelationshipManager.Interfaces;
using RelationshipManager.Turbo;

namespace Tests
{
    /// <summary>
    /// Summary description for UnitTest1
    /// </summary>
    [TestClass]
	public class UnitTest1
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
        public void TestMethod1()
        {
            //
            // TODO: Add test logic	here
            //
            Assert.AreEqual(2, 1 + 1);
        }

        [TestMethod]
        public void BasicSingleAdd()
        {
            rm.AddRelationship('a', 'b', "rel1");
            IList list = rm.FindObjectsPointedToByMe('a', "rel1");
            Assert.AreEqual(list[0], 'b');
        }

        [TestMethod]
        public void AddAFew()
        {
            rm.AddRelationship('a', 'b', "rel1");
            rm.AddRelationship('a', 'c', "rel1");
            rm.AddRelationship('a', 'z', "rel2");

            IList list;

            list = rm.FindObjectsPointedToByMe('a', "rel1");
            char[] expected = {'b', 'c'};
            Assert.AreEqual(list.ToString(), new ArrayList(expected).ToString());

            list = rm.FindObjectsPointedToByMe('a', "rel2");
            Assert.AreEqual(list[0], 'z');
        }

        [TestMethod]
        public void FingSingular()
        {
            rm.AddRelationship("andy", 'b', "rel1");
            rm.AddRelationship("andy", 'c', "rel2");
            Assert.AreEqual('c', (char) rm.FindObjectPointedToByMe("andy", "rel2"));
        }

        [TestMethod]
        public void FindSingularWhenNonExistent()
        {
            rm.AddRelationship("andy", 'b', "rel1");
            Assert.AreEqual(null, rm.FindObjectPointedToByMe("andy", "rel2"));
        }

        [TestMethod]
        public void RemoveRelationship()
        {
            rm.AddRelationship("andy", 'b', "rel1");
            rm.AddRelationship("andy", 'c', "rel1");
            rm.RemoveRelationship("andy", 'b', "rel1");
            Assert.AreEqual('c', (char) rm.FindObjectPointedToByMe("andy", "rel1"));
        }

        [TestMethod]
        public void RemoveNonExistantRelationship()
        {
            Assert.AreEqual(null, rm.FindObjectPointedToByMe("andy", "rel1"));

            rm.AddRelationship("andy", 'b', "rel1");
            rm.RemoveRelationship("andy", 'b', "rel1");
            Assert.AreEqual(null, rm.FindObjectPointedToByMe("andy", "rel1"));
            Assert.AreEqual(null, rm.FindObjectPointedToByMe("andy", "rel2"));
        }

        [TestMethod]
        public void RemoveAllRelationshipsFrom()
        {
            rm.AddRelationship("andy", 'b', "rel1");
            rm.AddRelationship("andy", 'c', "rel1");
            rm.AddRelationship("andy", 'z', "rel2");
            rm.RemoveAllRelationshipsInvolving("andy", "rel1");
            Assert.AreEqual(null, rm.FindObjectPointedToByMe("andy", "rel1"));
            Assert.AreEqual('z', (char)rm.FindObjectPointedToByMe("andy", "rel2"));
        }

        [TestMethod]
        public void RemoveAllRelationshipsTo()
        {
            rm.AddRelationship("andy", 'b', "rel1");
            rm.AddRelationship("andy", 'c', "rel1");
            rm.AddRelationship("andy", 'b', "rel2");
            rm.RemoveAllRelationshipsInvolving('b', "rel1");
            Assert.AreEqual('c', (char)rm.FindObjectPointedToByMe("andy", "rel1"));
            Assert.AreEqual('b', (char)rm.FindObjectPointedToByMe("andy", "rel2"));
        }

    }
}
