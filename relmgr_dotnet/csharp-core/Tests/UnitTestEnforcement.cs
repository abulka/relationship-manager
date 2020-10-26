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
    public class UnitTestEnforcement
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
        public void EnforceOneToOneSimple()
        {
            //rm.EnforceRelationship("rel1", Cardinality.OneToOne);
            //rm.AddRelationship('a', 'b', "rel1");
            //rm.AddRelationship('a', 'c', "rel1");
            //IList list = rm.FindObjectsPointedToByMe('a', "rel1");
            //Assert.AreEqual(1, list.Count);
            //Assert.AreEqual(list[0], 'c');

            object a = 'a', b = 'b', c = 'c';
            rm.EnforceRelationship("rel1", Cardinality.OneToOne);
            rm.AddRelationship(a, b, "rel1");
            rm.AddRelationship(a, c, "rel1");
            IList list = rm.FindObjectsPointedToByMe(a, "rel1");
            Assert.AreEqual(1, list.Count);
            Assert.AreEqual(list[0], c);

            list = rm.FindObjectsPointingToMe(c, "rel1");
            Assert.AreEqual(1, list.Count);
            Assert.AreEqual(list[0], a);

            list = rm.FindObjectsPointingToMe(b, "rel1");
            Assert.AreEqual(0, list.Count);
        }

    }



    [TestClass]
    public class UnitTestEnforcementVisioExamples
    {
        private IRelationshipManager rm;
        object a = 'a', b = 'b', c = 'c', d = 'd';

        [TestInitialize()]
        public void SetUp()
        {
            rm = new RelationshipMgrTurbo();
        }

        private void WireInitialSituation()
        {
            rm.AddRelationship(a, b, "rel1");
            rm.AddRelationship(d, c, "rel1");

            Assert.AreEqual(b, rm.FindObjectPointedToByMe(a, "rel1"));
            Assert.AreEqual(c, rm.FindObjectPointedToByMe(d, "rel1"));
            Assert.AreEqual(a, rm.FindObjectPointingToMe(b, "rel1"));
            Assert.AreEqual(d, rm.FindObjectPointingToMe(c, "rel1"));

            Assert.AreEqual(null, rm.FindObjectPointedToByMe(b, "rel1"));
            Assert.AreEqual(null, rm.FindObjectPointedToByMe(c, "rel1"));
            Assert.AreEqual(null, rm.FindObjectPointingToMe(a, "rel1"));
            Assert.AreEqual(null, rm.FindObjectPointingToMe(d, "rel1"));

            IList list = rm.FindObjectsPointedToByMe(a, "rel1");
            Assert.AreEqual(1, list.Count);
            Assert.AreEqual(list[0], b);

            list = rm.FindObjectsPointedToByMe(d, "rel1");
            Assert.AreEqual(1, list.Count);
            Assert.AreEqual(list[0], c);

            list = rm.FindObjectsPointingToMe(b, "rel1");
            Assert.AreEqual(1, list.Count);
            Assert.AreEqual(list[0], a);

            list = rm.FindObjectsPointingToMe(c, "rel1");
            Assert.AreEqual(1, list.Count);
            Assert.AreEqual(list[0], d);

            // null situations
            Assert.AreEqual(0, (rm.FindObjectsPointedToByMe(b, "rel1")).Count);
            Assert.AreEqual(0, (rm.FindObjectsPointedToByMe(c, "rel1")).Count);
            Assert.AreEqual(0, (rm.FindObjectsPointingToMe(a, "rel1")).Count);
            Assert.AreEqual(0, (rm.FindObjectsPointingToMe(d, "rel1")).Count);

            Assert.IsTrue(rm.DoesRelIdExistBetween(a, b, "rel1"));
            Assert.IsTrue(rm.DoesRelIdExistBetween(d, c, "rel1"));

            Assert.IsFalse(rm.DoesRelIdExistBetween(a, a, "rel1"));
            Assert.IsFalse(rm.DoesRelIdExistBetween(a, c, "rel1"));
            Assert.IsFalse(rm.DoesRelIdExistBetween(a, d, "rel1"));

            Assert.IsFalse(rm.DoesRelIdExistBetween(b, a, "rel1"));
            Assert.IsFalse(rm.DoesRelIdExistBetween(b, b, "rel1"));
            Assert.IsFalse(rm.DoesRelIdExistBetween(b, c, "rel1"));
            Assert.IsFalse(rm.DoesRelIdExistBetween(b, d, "rel1"));

            Assert.IsFalse(rm.DoesRelIdExistBetween(d, a, "rel1"));
            Assert.IsFalse(rm.DoesRelIdExistBetween(d, b, "rel1"));
            Assert.IsFalse(rm.DoesRelIdExistBetween(d, d, "rel1"));

            Assert.IsFalse(rm.DoesRelIdExistBetween(c, a, "rel1"));
            Assert.IsFalse(rm.DoesRelIdExistBetween(c, b, "rel1"));
            Assert.IsFalse(rm.DoesRelIdExistBetween(c, c, "rel1"));
            Assert.IsFalse(rm.DoesRelIdExistBetween(c, d, "rel1"));

            Assert.AreEqual(2, rm.CountRelationships("rel1"));
            Assert.AreEqual(2, rm.Count());

        }

        [TestMethod]
        public void ClassicOneToOne()
        {
            rm.EnforceRelationship("rel1", Cardinality.OneToOne);
            WireInitialSituation();

            // proposed move
            rm.AddRelationship(a, c, "rel1");

            Assert.AreEqual(c, rm.FindObjectPointedToByMe(a, "rel1"));
            Assert.AreEqual(null, rm.FindObjectPointedToByMe(d, "rel1"));
            Assert.AreEqual(1, (rm.FindObjectsPointedToByMe(a, "rel1")).Count);

            Assert.AreEqual(null, rm.FindObjectPointingToMe(b, "rel1"));
            Assert.AreEqual(a, rm.FindObjectPointingToMe(c, "rel1"));
            Assert.AreEqual(1, (rm.FindObjectsPointingToMe(c, "rel1")).Count);

            Assert.AreEqual(1, rm.CountRelationships("rel1"));
            Assert.AreEqual(1, rm.Count());

            // More laborious checks...
            Assert.IsFalse(rm.DoesRelIdExistBetween(a, a, "rel1"));
            Assert.IsFalse(rm.DoesRelIdExistBetween(a, b, "rel1"));
            Assert.IsTrue(rm.DoesRelIdExistBetween(a, c, "rel1"));
            Assert.IsFalse(rm.DoesRelIdExistBetween(a, d, "rel1"));

            Assert.IsFalse(rm.DoesRelIdExistBetween(b, a, "rel1"));
            Assert.IsFalse(rm.DoesRelIdExistBetween(b, b, "rel1"));
            Assert.IsFalse(rm.DoesRelIdExistBetween(b, c, "rel1"));
            Assert.IsFalse(rm.DoesRelIdExistBetween(b, d, "rel1"));

            Assert.IsFalse(rm.DoesRelIdExistBetween(d, a, "rel1"));
            Assert.IsFalse(rm.DoesRelIdExistBetween(d, b, "rel1"));
            Assert.IsFalse(rm.DoesRelIdExistBetween(d, c, "rel1"));
            Assert.IsFalse(rm.DoesRelIdExistBetween(d, d, "rel1"));

            Assert.IsFalse(rm.DoesRelIdExistBetween(c, a, "rel1"));
            Assert.IsFalse(rm.DoesRelIdExistBetween(c, b, "rel1"));
            Assert.IsFalse(rm.DoesRelIdExistBetween(c, c, "rel1"));
            Assert.IsFalse(rm.DoesRelIdExistBetween(c, d, "rel1"));

        }


        [TestMethod]
        public void ClassicOneToMany()
        {
            rm.EnforceRelationship("rel1", Cardinality.OneToMany);
            WireInitialSituation();

            // proposed move
            rm.AddRelationship(a, c, "rel1");

            Assert.AreEqual(2, (rm.FindObjectsPointedToByMe(a, "rel1")).Count);
            IList list = rm.FindObjectsPointedToByMe(a, "rel1");
            Assert.IsTrue(list.Contains(b));
            Assert.IsTrue(list.Contains(c));

            object res = rm.FindObjectPointedToByMe(a, "rel1");
            Assert.IsTrue(res == b || res == c);

            Assert.AreEqual(null, rm.FindObjectPointedToByMe(d, "rel1"));  // strict

            Assert.AreEqual(a, rm.FindObjectPointingToMe(b, "rel1"));
            Assert.AreEqual(a, rm.FindObjectPointingToMe(c, "rel1"));
            Assert.AreEqual(1, (rm.FindObjectsPointingToMe(c, "rel1")).Count);

            Assert.AreEqual(2, rm.CountRelationships("rel1"));
            Assert.AreEqual(2, rm.Count());

            // More laborious checks...
            Assert.IsFalse(rm.DoesRelIdExistBetween(a, a, "rel1"));
            Assert.IsTrue(rm.DoesRelIdExistBetween(a, b, "rel1"));
            Assert.IsTrue(rm.DoesRelIdExistBetween(a, c, "rel1"));
            Assert.IsFalse(rm.DoesRelIdExistBetween(a, d, "rel1"));

            Assert.IsFalse(rm.DoesRelIdExistBetween(b, a, "rel1"));
            Assert.IsFalse(rm.DoesRelIdExistBetween(b, b, "rel1"));
            Assert.IsFalse(rm.DoesRelIdExistBetween(b, c, "rel1"));
            Assert.IsFalse(rm.DoesRelIdExistBetween(b, d, "rel1"));

            Assert.IsFalse(rm.DoesRelIdExistBetween(d, a, "rel1"));
            Assert.IsFalse(rm.DoesRelIdExistBetween(d, b, "rel1"));
            Assert.IsFalse(rm.DoesRelIdExistBetween(d, c, "rel1"));
            Assert.IsFalse(rm.DoesRelIdExistBetween(d, d, "rel1"));

            Assert.IsFalse(rm.DoesRelIdExistBetween(c, a, "rel1"));
            Assert.IsFalse(rm.DoesRelIdExistBetween(c, b, "rel1"));
            Assert.IsFalse(rm.DoesRelIdExistBetween(c, c, "rel1"));
            Assert.IsFalse(rm.DoesRelIdExistBetween(c, d, "rel1"));
        }


        [TestMethod]
        public void ClassicManyToOne()
        {
            rm.EnforceRelationship("rel1", Cardinality.ManyToOne);
            WireInitialSituation();

            // proposed move
            rm.AddRelationship(a, c, "rel1");

            Assert.AreEqual(1, (rm.FindObjectsPointedToByMe(a, "rel1")).Count);
            Assert.AreEqual(c, rm.FindObjectPointedToByMe(a, "rel1"));  // strict
            Assert.AreEqual(c, rm.FindObjectPointedToByMe(d, "rel1"));

            IList list = rm.FindObjectsPointingToMe(c, "rel1");
            Assert.AreEqual(2, list.Count);
            Assert.IsTrue(list.Contains(a));
            Assert.IsTrue(list.Contains(d));
            object res = rm.FindObjectPointingToMe(c, "rel1");
            Assert.IsTrue(res == a || res == d);

            Assert.AreEqual(null, rm.FindObjectPointingToMe(b, "rel1"));

            Assert.AreEqual(2, rm.CountRelationships("rel1"));
            Assert.AreEqual(2, rm.Count());

            // More laborious checks...
            Assert.IsFalse(rm.DoesRelIdExistBetween(a, a, "rel1"));
            Assert.IsFalse(rm.DoesRelIdExistBetween(a, b, "rel1"));
            Assert.IsTrue(rm.DoesRelIdExistBetween(a, c, "rel1"));
            Assert.IsFalse(rm.DoesRelIdExistBetween(a, d, "rel1"));

            Assert.IsFalse(rm.DoesRelIdExistBetween(b, a, "rel1"));
            Assert.IsFalse(rm.DoesRelIdExistBetween(b, b, "rel1"));
            Assert.IsFalse(rm.DoesRelIdExistBetween(b, c, "rel1"));
            Assert.IsFalse(rm.DoesRelIdExistBetween(b, d, "rel1"));

            Assert.IsFalse(rm.DoesRelIdExistBetween(d, a, "rel1"));
            Assert.IsFalse(rm.DoesRelIdExistBetween(d, b, "rel1"));
            Assert.IsTrue(rm.DoesRelIdExistBetween(d, c, "rel1"));
            Assert.IsFalse(rm.DoesRelIdExistBetween(d, d, "rel1"));

            Assert.IsFalse(rm.DoesRelIdExistBetween(c, a, "rel1"));
            Assert.IsFalse(rm.DoesRelIdExistBetween(c, b, "rel1"));
            Assert.IsFalse(rm.DoesRelIdExistBetween(c, c, "rel1"));
            Assert.IsFalse(rm.DoesRelIdExistBetween(c, d, "rel1"));
        }



        [TestMethod]
        public void ClassicManyToMany()
        {
            rm.EnforceRelationship("rel1", Cardinality.ManyToMany);
            CheckManyToMany();
        }

        [TestMethod]
        public void ClassicNoEnforcement()
        {
            CheckManyToMany();
        }

        private void CheckManyToMany()
        {
            WireInitialSituation();

            // proposed move
            rm.AddRelationship(a, c, "rel1");
            ManyManyStage1Result();

            // proposed move (again)
            rm.AddRelationship(a, c, "rel1");
            ManyManyStage2Result();

            // 3 moves
            rm.AddRelationship(d, b, "rel1");
            rm.AddRelationship(c, d, "rel1");
            rm.AddRelationship(c, b, "rel1");
            ManyManyStage3Result();
        }

        private void ManyManyStage1Result()
        {
            IList list;
            object res;
            list = rm.FindObjectsPointedToByMe(a, "rel1");
            Assert.AreEqual(2, list.Count);
            Assert.IsTrue(list.Contains(b));
            Assert.IsTrue(list.Contains(c));
            res = rm.FindObjectPointedToByMe(a, "rel1");
            Assert.IsTrue(res == b || res == c);

            list = rm.FindObjectsPointedToByMe(d, "rel1");
            Assert.AreEqual(1, list.Count);
            Assert.IsTrue(list.Contains(c));
            res = rm.FindObjectPointedToByMe(d, "rel1");
            Assert.IsTrue(res == c);

            // back links

            list = rm.FindObjectsPointingToMe(c, "rel1");
            Assert.AreEqual(2, list.Count);
            Assert.IsTrue(list.Contains(a));
            Assert.IsTrue(list.Contains(d));
            res = rm.FindObjectPointingToMe(c, "rel1");
            Assert.IsTrue(res == a || res == d);

            list = rm.FindObjectsPointingToMe(b, "rel1");
            Assert.AreEqual(1, list.Count);
            Assert.IsTrue(list.Contains(a));
            res = rm.FindObjectPointingToMe(b, "rel1");
            Assert.IsTrue(res == a);


            Assert.AreEqual(3, rm.CountRelationships("rel1"));
            Assert.AreEqual(3, rm.Count());

            // More laborious checks...
            Assert.IsFalse(rm.DoesRelIdExistBetween(a, a, "rel1"));
            Assert.IsTrue(rm.DoesRelIdExistBetween(a, b, "rel1"));
            Assert.IsTrue(rm.DoesRelIdExistBetween(a, c, "rel1"));
            Assert.IsFalse(rm.DoesRelIdExistBetween(a, d, "rel1"));

            Assert.IsFalse(rm.DoesRelIdExistBetween(b, a, "rel1"));
            Assert.IsFalse(rm.DoesRelIdExistBetween(b, b, "rel1"));
            Assert.IsFalse(rm.DoesRelIdExistBetween(b, c, "rel1"));
            Assert.IsFalse(rm.DoesRelIdExistBetween(b, d, "rel1"));

            Assert.IsFalse(rm.DoesRelIdExistBetween(d, a, "rel1"));
            Assert.IsFalse(rm.DoesRelIdExistBetween(d, b, "rel1"));
            Assert.IsTrue(rm.DoesRelIdExistBetween(d, c, "rel1"));
            Assert.IsFalse(rm.DoesRelIdExistBetween(d, d, "rel1"));

            Assert.IsFalse(rm.DoesRelIdExistBetween(c, a, "rel1"));
            Assert.IsFalse(rm.DoesRelIdExistBetween(c, b, "rel1"));
            Assert.IsFalse(rm.DoesRelIdExistBetween(c, c, "rel1"));
            Assert.IsFalse(rm.DoesRelIdExistBetween(c, d, "rel1"));
        }

        private void ManyManyStage2Result()
        {
            ManyManyStage1Result();
        }

        private void ManyManyStage3Result()
        {
            IList list;
            object res;
            list = rm.FindObjectsPointedToByMe(a, "rel1");
            Assert.AreEqual(2, list.Count);
            Assert.IsTrue(list.Contains(b));
            Assert.IsTrue(list.Contains(c));
            res = rm.FindObjectPointedToByMe(a, "rel1");
            Assert.IsTrue(res == b || res == c);

            list = rm.FindObjectsPointedToByMe(d, "rel1");
            Assert.AreEqual(2, list.Count);
            Assert.IsTrue(list.Contains(b));
            Assert.IsTrue(list.Contains(c));
            res = rm.FindObjectPointedToByMe(d, "rel1");
            Assert.IsTrue(res == b || res == c);

            list = rm.FindObjectsPointedToByMe(c, "rel1");
            Assert.AreEqual(2, list.Count);
            Assert.IsTrue(list.Contains(b));
            Assert.IsTrue(list.Contains(d));
            res = rm.FindObjectPointedToByMe(a, "rel1");
            Assert.IsTrue(res == b || res == d);

            // back links

            list = rm.FindObjectsPointingToMe(b, "rel1");
            Assert.AreEqual(3, list.Count);
            Assert.IsTrue(list.Contains(a));
            Assert.IsTrue(list.Contains(c));
            Assert.IsTrue(list.Contains(d));
            res = rm.FindObjectPointingToMe(b, "rel1");
            Assert.IsTrue(res == a || res == c || res == d);

            list = rm.FindObjectsPointingToMe(c, "rel1");
            Assert.AreEqual(2, list.Count);
            Assert.IsTrue(list.Contains(a));
            Assert.IsTrue(list.Contains(d));
            res = rm.FindObjectPointingToMe(c, "rel1");
            Assert.IsTrue(res == a || res == d);

            list = rm.FindObjectsPointingToMe(d, "rel1");
            Assert.AreEqual(1, list.Count);
            Assert.IsTrue(list.Contains(c));
            res = rm.FindObjectPointingToMe(d, "rel1");
            Assert.IsTrue(res == c);


            Assert.AreEqual(6, rm.CountRelationships("rel1"));
            Assert.AreEqual(6, rm.Count());

            // More laborious checks...
            Assert.IsFalse(rm.DoesRelIdExistBetween(a, a, "rel1"));
            Assert.IsTrue(rm.DoesRelIdExistBetween(a, b, "rel1"));
            Assert.IsTrue(rm.DoesRelIdExistBetween(a, c, "rel1"));
            Assert.IsFalse(rm.DoesRelIdExistBetween(a, d, "rel1"));

            Assert.IsFalse(rm.DoesRelIdExistBetween(b, a, "rel1"));
            Assert.IsFalse(rm.DoesRelIdExistBetween(b, b, "rel1"));
            Assert.IsFalse(rm.DoesRelIdExistBetween(b, c, "rel1"));
            Assert.IsFalse(rm.DoesRelIdExistBetween(b, d, "rel1"));

            Assert.IsFalse(rm.DoesRelIdExistBetween(d, a, "rel1"));
            Assert.IsTrue(rm.DoesRelIdExistBetween(d, b, "rel1"));
            Assert.IsTrue(rm.DoesRelIdExistBetween(d, c, "rel1"));
            Assert.IsFalse(rm.DoesRelIdExistBetween(d, d, "rel1"));

            Assert.IsFalse(rm.DoesRelIdExistBetween(c, a, "rel1"));
            Assert.IsTrue(rm.DoesRelIdExistBetween(c, b, "rel1"));
            Assert.IsFalse(rm.DoesRelIdExistBetween(c, c, "rel1"));
            Assert.IsTrue(rm.DoesRelIdExistBetween(c, d, "rel1"));
        }

    }


}
