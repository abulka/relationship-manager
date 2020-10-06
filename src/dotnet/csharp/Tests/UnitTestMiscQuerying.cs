using System;
using System.Text;
using System.Collections;
using Microsoft.VisualStudio.TestTools.UnitTesting;

using RelationshipManager.Interfaces;
using RelationshipManager.Turbo;

namespace Tests
{
    /// <summary>
    /// Summary description for UnitTestEnforcement
    /// </summary>
    [TestClass]
    public class UnitTestMiscQuerying
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
        public void DoesRelIdExistBetween()
        {
            rm.EnforceRelationship("rel1", Cardinality.OneToOne);
            rm.AddRelationship("a", "b", "rel1");

            Assert.IsTrue(rm.DoesRelIdExistBetween("a", "b", "rel1"));
        }

        [TestMethod]
        public void FindRelIdsBetween()
        {
            rm.EnforceRelationship("rel1", Cardinality.OneToMany);
            rm.AddRelationship('a', 'b', "rel1");
            rm.AddRelationship('a', 'b', "rel1");
            rm.AddRelationship('a', 'b', "rel2");

            string[] expected = {"rel1", "rel2"};
            Assert.AreEqual(rm.FindRelIdsBetween('a', 'b').ToString(), new ArrayList(expected).ToString());
        }
    }
}
