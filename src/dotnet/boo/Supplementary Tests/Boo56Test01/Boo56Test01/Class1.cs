using System;
using System.Collections.Generic;
using System.Text;

using NUnit.Framework;
using RelationshipManager56;
using RelationshipManager.Interfaces;

namespace Boo56Test01
{
    [TestFixture]
    public class Class1
    {
        RM1 RM;

        [SetUp]
        public void Setup()
        {
		    this.RM = new RM1();
            RM.ER("p->o", Cardinality.OneToMany, Directionality.DoubleDirectional);
        }

        [Test]
        public void CheckRM01()
        {
            RM.R(this, "ug", "p->o"); 

			System.Collections.IList list = RM.PS(this, "p->o");
            Assert.IsTrue((string) list[0] == "ug");
        }    
    
    }

    [TestFixture]
    public class TestNewBiggerNames
    {
        RelationshipManagerConstrained RM;

        [SetUp]
        public void Setup()
        {
            this.RM = new RelationshipManagerConstrained();
        }

        [Test]
        public void CheckLongNames()
        {
            RM.EnforceRelationship("p->o", Cardinality.OneToMany, Directionality.DoubleDirectional);
            RM.AddRelationship(this, "ug", "p->o");

            // FindObjectsPointedToByMe

            System.Collections.IList list = RM.FindObjectsPointedToByMe(this, "p->o");
            Assert.IsTrue((string)list[0] == "ug");

            string s = (string) RM.FindObjectPointedToByMe(this, "p->o");
            Assert.AreEqual("ug", s);

            // FindObjectsPointingToMe

            list = RM.FindObjectsPointingToMe("ug", "p->o");
            Assert.AreSame(list[0], this);

            object o = RM.FindObjectPointingToMe("ug", "p->o");
            Assert.AreSame(this, o);

            // Removal

            RM.RemoveRelationship(this, "ug", "p->o");
            list = RM.FindObjectsPointedToByMe(this, "p->o");
            Assert.AreEqual(0, list.Count);
        }

    }

    [TestFixture]
    public class TestMultiRemove
    {
        RelationshipManagerConstrained RM;

        [TestFixtureSetUp]
        public void Setup0()
        {
            // run once per class
        }

        [SetUp]
        public void Setup()
        {
            this.RM = new RelationshipManagerConstrained();

            RM.AddRelationship(this, "ug", "p->o");
            RM.AddRelationship(this, "ug2", "p->o");
            RM.AddRelationship("zz", "ug2", "p->o");

        }

        private void CheckOriginalPosition()
        {
            Assert.AreEqual(2, RM.FindObjectsPointedToByMe(this, "p->o").Count);
            Assert.AreEqual(2, RM.FindObjectsPointingToMe("ug2", "p->o").Count);
        }

        [Test]
        public void CheckRemovalMulti01()
        {
            // Removal (multi)

            this.CheckOriginalPosition();

            RM.RemoveAllRelationshipsInvolving("ug", "p->o");
            Assert.AreEqual(1, RM.FindObjectsPointedToByMe(this, "p->o").Count);
            Assert.AreEqual(2, RM.FindObjectsPointingToMe("ug2", "p->o").Count);
        }

        [Test]
        public void CheckSetupIsWorking()
        {
            this.CheckOriginalPosition();
        }

        [Test]
        public void CheckRemovalMulti02()
        {
            this.CheckOriginalPosition();

            
            RM.RemoveAllRelationshipsInvolving(this, "p->o");
            Assert.AreEqual(0, RM.FindObjectsPointedToByMe(this, "p->o").Count);
            Assert.AreEqual(1, RM.FindObjectsPointingToMe("ug2", "p->o").Count);
            
        }
    }

}
