using System;
using System.Text;
using System.Collections;
using Microsoft.VisualStudio.TestTools.UnitTesting;

using RelationshipManager.Interfaces;
using RelationshipManager.Turbo;

namespace Tests
{
    [TestClass]
    public class UnitTestBackLinks
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
        public void BackSingleBackLink()
        {
            rm.AddRelationship('a', 'b', "rel1");
            IList list = rm.FindObjectsPointingToMe('b', "rel1");
            Assert.AreEqual(list[0], 'a');
        }

        [TestMethod]
        public void BackMultipleLinks()
        {
            rm.AddRelationship('a', 'b', "rel1");
            rm.AddRelationship('a', 'c', "rel1");
            rm.AddRelationship('x', 'c', "rel1");
            rm.AddRelationship('a', 'c', "rel2");
            IList list = rm.FindObjectsPointingToMe('c', "rel1");
            char[] expected = { 'a', 'x' };
            Assert.AreEqual(list.ToString(), new ArrayList(expected).ToString());
        }

        [TestMethod]
        public void BackLinksSingleObject()
        {
            rm.AddRelationship('a', 'b', "rel1");
            rm.AddRelationship('a', 'c', "rel1");
            rm.AddRelationship('x', 'c', "rel1");
            rm.AddRelationship('q', 'c', "rel2");

            Assert.AreEqual('q', (char)rm.FindObjectPointingToMe('c', "rel2"));
        }

        [TestMethod]
        public void BackFindSingularWhenNonExistent()
        {
            rm.AddRelationship("andy", 'b', "rel1");
            Assert.AreEqual(null, rm.FindObjectPointingToMe('b', "rel2"));
        }

    }
}
