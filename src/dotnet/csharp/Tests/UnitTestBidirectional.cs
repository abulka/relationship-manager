using System;
using System.Text;
using System.Collections;
using Microsoft.VisualStudio.TestTools.UnitTesting;

using RelationshipManager.Interfaces;
using RelationshipManager.Turbo;

namespace Tests
{
    /// <summary>
    /// Summary description for UnitTestBidirectional
    /// </summary>
    [TestClass]
    public class UnitTestBidirectional
    {
        //private IRelationshipManager rm;
        private IRM RM;

        
        [TestInitialize()]
        public void SetUp()
        {
            //rm = new RelationshipMgrTurbo();
            RM = new RM();
        }


        [TestMethod]
        public void BidirectionalBug1()
        {
            RM.ER("xtoy", Cardinality.OneToMany, Directionality.DoubleDirectional);
            RM.R("x1", "y1", "xtoy");   // x1.addY(y1)
            RM.R("x1", "y2", "xtoy");   // x1.addY(y2)
            IList result = RM.PS("x1", "xtoy");  // getAllY()

            string[] expected1 = { "y1", "y2" };
            string[] expected2 = { "y2", "y1" };
            Assert.IsTrue(result.ToString() == new ArrayList(expected1).ToString() || 
                          result.ToString() == new ArrayList(expected2).ToString());
        }
    }


    [TestClass]
    public class UnitTestBidirectional2
    {
        public IRM RM;

        [TestInitialize()]
        public void SetUp()
        {
            RM = new RM();
            BO.SetRm(RM);
        }

        [TestMethod]
        public void BidirectionalBug1a()
        {
            RelationshipMgrTurbo rm = RM as RelationshipMgrTurbo;

            X x1, x2;
            Y y1, y2;
            x1 = new X();
            x2 = new X();
            y1 = new Y();
            y2 = new Y();
            x1.addY(y1);
            Assert.AreEqual(2, RM.Count());
            Assert.AreEqual(2, RM.CountRelationships("xtoy"));

            x1.addY(y2);
            Assert.AreEqual(4, RM.Count());
            Assert.AreEqual(4, RM.CountRelationships("xtoy"));

            IList result = x1.getAllY();

            string[] expected1 = { "y1", "y2" };
            string[] expected2 = { "y2", "y1" };
            Assert.IsTrue(result.ToString() == new ArrayList(expected1).ToString() ||
                          result.ToString() == new ArrayList(expected2).ToString());

        }

    }

    class BO 
    {
        static protected IRM RM;
        static public void SetRm(IRM rm)
        {
            RM = rm;
        }
    }
        
    class X : BO 
    {
        public X() {
            RM.ER("xtoy", Cardinality.OneToMany, Directionality.DoubleDirectional);
        }
        public void addY(Y y) {
            RM.R(this, y, "xtoy");
        }
        public IList getAllY() {
            return RM.PS(this, "xtoy");
        }
        public void removeY(Y y) {
            RM.NR(this, y, "xtoy");
        }
    }       
    class Y : BO
    {
        public void setX(X x) {
            RM.R(x, this, "xtoy");  // though bi, there is still a direction!
        }
        public object getX() {
            return RM.P(this, "xtoy");
        }
        public void clearX() {
            RM.NR(this, this.getX(), "xtoy");
        }
    }
 
}
