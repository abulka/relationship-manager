using System;
using System.Text;
using System.Collections.Generic;
using Microsoft.VisualStudio.TestTools.UnitTesting;

using RelationshipManager56;
using RelationshipManager.Interfaces;
//using System.EnterpriseServices;

namespace Boo56MicrosoftTestProject1
{
    /// <summary>
    /// Summary description for Boo56MicrosoftUnitTest1
    /// </summary>
    [TestClass]
    public class Boo56MicrosoftUnitTest1
    {
        public Boo56MicrosoftUnitTest1()
        {
            //
            // TODO: Add constructor logic here
            //
        }

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

        [TestMethod]
        public void TestMethod1()
        {
            //
            // TODO: Add test logic	here
            //
        }

        [TestMethod]
        public void TestMethod2()
        {
            //
            // TODO: Add test logic	here
            //
            Assert.AreEqual(2, 1 + 1);
        }

        [TestMethod]
        public void TestMethod3()
        {
            //
            // TODO: Add test logic	here
            //
            RM1 RM;
            RM = new RM1();
            RM.ER("p->o", Cardinality.OneToMany, Directionality.DoubleDirectional);

            RM.R(this, "ug", "p->o");

            System.Collections.IList list = RM.PS(this, "p->o");
            Assert.IsTrue((string)list[0] == "ug");

        }


    }
}
