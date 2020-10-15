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
    public class UnitTestCacheBug
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
        public void Bug00111()
        {
            RM.ER("xtoy", Cardinality.OneToOne, Directionality.DirectionalWithBackPointer);

            // # After clearing pointers
            RM.NR("x1", RM.P("x1", "xtoy"), "xtoy"); // x1.clearY()
            RM.NR("x2", RM.P("x2", "xtoy"), "xtoy"); // x2.clearY()
            RM.NR(RM.B("y1", "xtoy"), "y1", "xtoy"); // y1.clearX()
            RM.NR(RM.B("y2", "xtoy"), "y2", "xtoy"); // y2.clearX()

            //assertallclear(x1, x2, y1, y2)

            // # After setting one pointer, x1 <-> y1
            RM.R("x1", "y1", "xtoy"); // x1.setY(y1)
            Assert.AreEqual("y1", RM.P("x1", "xtoy")); // assert x1.getY() == y1
            Assert.AreEqual(null, RM.P("x2", "xtoy")); // assert x2.getY() == null
        }
    }


    [TestClass]
    public class FindCacheFullTest1
    {
        public IRM RM;

        [TestInitialize()]
        public void SetUp()
        {
            RM = new RM();
            BO.SetRm(RM);
        }

        [TestMethod]
        public void CacheBug1a()
        {
            RelationshipMgrTurbo rm = RM as RelationshipMgrTurbo;

            X x1, x2;
            Y y1, y2;
            x1 = new X();
            x2 = new X();
            y1 = new Y();
            y2 = new Y();

            // onetooneasserts(x1,x2,y1,y2)

            //# Initial situation
            //assertallclear(x1, x2, y1, y2)

            //# After clearing pointers
            /*
            x1.clearY();
            x2.clearY();
            y1.clearX();
            y2.clearX();
            */ 
            //assertallclear(x1, x2, y1, y2)

            //# After setting one pointer, x1 <-> y1
            x1.setY(y1);
            Assert.AreEqual(y1, x1.getY());  // usual point of failure
            Assert.AreEqual(null, x2.getY());

            //Assert.AreEqual(1, 0); // force fail
        }

        class X : BO
        {
            public X()
            {
                RM.ER("xtoy", Cardinality.OneToOne, Directionality.DirectionalWithBackPointer);
            }

            public void setY(Y y)
            {
		        RM.R(this, y, "xtoy");
            }
	        public Y getY()
            {
 		        return (Y) RM.P(this, "xtoy");
            }
            public void clearY()
            {
                RM.NR(this, this.getY(), "xtoy");
            }
        }
        class Y : BO
        {
            public Y() 
            {
		        RM.ER("xtoy", Cardinality.OneToOne, Directionality.DirectionalWithBackPointer);
            }
            public void setX(X x)
            {
		        RM.R(x, this, "xtoy");
            }
	        public X getX()
            {
		        return (X) RM.B(this, "xtoy");
            }
            public void clearX()
            {
                RM.NR(this.getX(), this, "xtoy");
            }
        }
    }
}
