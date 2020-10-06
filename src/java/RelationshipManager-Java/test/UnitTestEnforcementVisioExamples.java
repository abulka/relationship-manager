/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

import java.util.List;
import org.junit.After;
import org.junit.AfterClass;
import org.junit.Assert;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;
import relationshipmanager.turbo.Cardinality;
import relationshipmanager.turbo.IRelationshipManager;
import relationshipmanager.turbo.RelationshipMgrTurbo;
import static org.junit.Assert.*;

/**
 *
 * @author Tarik
 */
public class UnitTestEnforcementVisioExamples {

    public UnitTestEnforcementVisioExamples() {
    }

    @BeforeClass
    public static void setUpClass() throws Exception {
    }

    @AfterClass
    public static void tearDownClass() throws Exception {
    }

    @After
    public void tearDown() {
    }

            private IRelationshipManager rm;
        Object a = 'a', b = 'b', c = 'c', d = 'd';

        @Before
        public void SetUp()
        {
            rm = new RelationshipMgrTurbo();
        }

        private void WireInitialSituation()
        {
            rm.AddRelationship(a, b, "rel1");
            rm.AddRelationship(d, c, "rel1");

            assertEquals(b, rm.FindObjectPointedToByMe(a, "rel1"));
            assertEquals(c, rm.FindObjectPointedToByMe(d, "rel1"));
            assertEquals(a, rm.FindObjectPointingToMe(b, "rel1"));
            assertEquals(d, rm.FindObjectPointingToMe(c, "rel1"));

            assertEquals(null, rm.FindObjectPointedToByMe(b, "rel1"));
            assertEquals(null, rm.FindObjectPointedToByMe(c, "rel1"));
            assertEquals(null, rm.FindObjectPointingToMe(a, "rel1"));
            assertEquals(null, rm.FindObjectPointingToMe(d, "rel1"));

            List list = rm.FindObjectsPointedToByMe(a, "rel1");
            assertEquals(1, list.size());
            assertEquals(list.get(0), b);

            list = rm.FindObjectsPointedToByMe(d, "rel1");
            assertEquals(1, list.size());
            assertEquals(list.get(0), c);

            list = rm.FindObjectsPointingToMe(b, "rel1");
            assertEquals(1, list.size());
            assertEquals(list.get(0), a);

            list = rm.FindObjectsPointingToMe(c, "rel1");
            assertEquals(1, list.size());
            assertEquals(list.get(0), d);

            // null situations
            assertEquals(0, (rm.FindObjectsPointedToByMe(b, "rel1")).size());
            assertEquals(0, (rm.FindObjectsPointedToByMe(c, "rel1")).size());
            assertEquals(0, (rm.FindObjectsPointingToMe(a, "rel1")).size());
            assertEquals(0, (rm.FindObjectsPointingToMe(d, "rel1")).size());

            assertTrue(rm.DoesRelIdExistBetween(a, b, "rel1"));
            assertTrue(rm.DoesRelIdExistBetween(d, c, "rel1"));

            assertFalse(rm.DoesRelIdExistBetween(a, a, "rel1"));
            assertFalse(rm.DoesRelIdExistBetween(a, c, "rel1"));
            assertFalse(rm.DoesRelIdExistBetween(a, d, "rel1"));

            assertFalse(rm.DoesRelIdExistBetween(b, a, "rel1"));
            assertFalse(rm.DoesRelIdExistBetween(b, b, "rel1"));
            assertFalse(rm.DoesRelIdExistBetween(b, c, "rel1"));
            assertFalse(rm.DoesRelIdExistBetween(b, d, "rel1"));

            assertFalse(rm.DoesRelIdExistBetween(d, a, "rel1"));
            assertFalse(rm.DoesRelIdExistBetween(d, b, "rel1"));
            assertFalse(rm.DoesRelIdExistBetween(d, d, "rel1"));

            assertFalse(rm.DoesRelIdExistBetween(c, a, "rel1"));
            assertFalse(rm.DoesRelIdExistBetween(c, b, "rel1"));
            assertFalse(rm.DoesRelIdExistBetween(c, c, "rel1"));
            assertFalse(rm.DoesRelIdExistBetween(c, d, "rel1"));

            assertEquals(2, rm.CountRelationships("rel1"));
            assertEquals(2, rm.Count());

        }

        @Test
        public void ClassicOneToOne()
        {
            rm.EnforceRelationship("rel1", Cardinality.OneToOne);
            WireInitialSituation();

            // proposed move
            rm.AddRelationship(a, c, "rel1");

            assertEquals(c, rm.FindObjectPointedToByMe(a, "rel1"));
            assertEquals(null, rm.FindObjectPointedToByMe(d, "rel1"));
            assertEquals(1, (rm.FindObjectsPointedToByMe(a, "rel1")).size());

            assertEquals(null, rm.FindObjectPointingToMe(b, "rel1"));
            assertEquals(a, rm.FindObjectPointingToMe(c, "rel1"));
            assertEquals(1, (rm.FindObjectsPointingToMe(c, "rel1")).size());

            assertEquals(1, rm.CountRelationships("rel1"));
            assertEquals(1, rm.Count());

            // More laborious checks...
            assertFalse(rm.DoesRelIdExistBetween(a, a, "rel1"));
            assertFalse(rm.DoesRelIdExistBetween(a, b, "rel1"));
            assertTrue(rm.DoesRelIdExistBetween(a, c, "rel1"));
            assertFalse(rm.DoesRelIdExistBetween(a, d, "rel1"));

            assertFalse(rm.DoesRelIdExistBetween(b, a, "rel1"));
            assertFalse(rm.DoesRelIdExistBetween(b, b, "rel1"));
            assertFalse(rm.DoesRelIdExistBetween(b, c, "rel1"));
            assertFalse(rm.DoesRelIdExistBetween(b, d, "rel1"));

            assertFalse(rm.DoesRelIdExistBetween(d, a, "rel1"));
            assertFalse(rm.DoesRelIdExistBetween(d, b, "rel1"));
            assertFalse(rm.DoesRelIdExistBetween(d, c, "rel1"));
            assertFalse(rm.DoesRelIdExistBetween(d, d, "rel1"));

            assertFalse(rm.DoesRelIdExistBetween(c, a, "rel1"));
            assertFalse(rm.DoesRelIdExistBetween(c, b, "rel1"));
            assertFalse(rm.DoesRelIdExistBetween(c, c, "rel1"));
            assertFalse(rm.DoesRelIdExistBetween(c, d, "rel1"));

        }


        @Test
        public void ClassicOneToMany()
        {
            rm.EnforceRelationship("rel1", Cardinality.OneToMany);
            WireInitialSituation();

            // proposed move
            rm.AddRelationship(a, c, "rel1");

            assertEquals(2, (rm.FindObjectsPointedToByMe(a, "rel1")).size());
            List list = rm.FindObjectsPointedToByMe(a, "rel1");
            assertTrue(list.contains(b));
            assertTrue(list.contains(c));

            Object res = rm.FindObjectPointedToByMe(a, "rel1");
            assertTrue(res == b || res == c);

            assertEquals(null, rm.FindObjectPointedToByMe(d, "rel1"));  // strict

            assertEquals(a, rm.FindObjectPointingToMe(b, "rel1"));
            assertEquals(a, rm.FindObjectPointingToMe(c, "rel1"));
            assertEquals(1, (rm.FindObjectsPointingToMe(c, "rel1")).size());

            assertEquals(2, rm.CountRelationships("rel1"));
            assertEquals(2, rm.Count());

            // More laborious checks...
            assertFalse(rm.DoesRelIdExistBetween(a, a, "rel1"));
            assertTrue(rm.DoesRelIdExistBetween(a, b, "rel1"));
            assertTrue(rm.DoesRelIdExistBetween(a, c, "rel1"));
            assertFalse(rm.DoesRelIdExistBetween(a, d, "rel1"));

            assertFalse(rm.DoesRelIdExistBetween(b, a, "rel1"));
            assertFalse(rm.DoesRelIdExistBetween(b, b, "rel1"));
            assertFalse(rm.DoesRelIdExistBetween(b, c, "rel1"));
            assertFalse(rm.DoesRelIdExistBetween(b, d, "rel1"));

            assertFalse(rm.DoesRelIdExistBetween(d, a, "rel1"));
            assertFalse(rm.DoesRelIdExistBetween(d, b, "rel1"));
            assertFalse(rm.DoesRelIdExistBetween(d, c, "rel1"));
            assertFalse(rm.DoesRelIdExistBetween(d, d, "rel1"));

            assertFalse(rm.DoesRelIdExistBetween(c, a, "rel1"));
            assertFalse(rm.DoesRelIdExistBetween(c, b, "rel1"));
            assertFalse(rm.DoesRelIdExistBetween(c, c, "rel1"));
            assertFalse(rm.DoesRelIdExistBetween(c, d, "rel1"));
        }


        @Test
        public void ClassicManyToOne()
        {
            rm.EnforceRelationship("rel1", Cardinality.ManyToOne);
            WireInitialSituation();

            // proposed move
            rm.AddRelationship(a, c, "rel1");

            assertEquals(1, (rm.FindObjectsPointedToByMe(a, "rel1")).size());
            assertEquals(c, rm.FindObjectPointedToByMe(a, "rel1"));  // strict
            assertEquals(c, rm.FindObjectPointedToByMe(d, "rel1"));

            List list = rm.FindObjectsPointingToMe(c, "rel1");
            assertEquals(2, list.size());
            assertTrue(list.contains(a));
            assertTrue(list.contains(d));
            Object res = rm.FindObjectPointingToMe(c, "rel1");
            assertTrue(res == a || res == d);

            assertEquals(null, rm.FindObjectPointingToMe(b, "rel1"));

            assertEquals(2, rm.CountRelationships("rel1"));
            assertEquals(2, rm.Count());

            // More laborious checks...
            assertFalse(rm.DoesRelIdExistBetween(a, a, "rel1"));
            assertFalse(rm.DoesRelIdExistBetween(a, b, "rel1"));
            assertTrue(rm.DoesRelIdExistBetween(a, c, "rel1"));
            assertFalse(rm.DoesRelIdExistBetween(a, d, "rel1"));

            assertFalse(rm.DoesRelIdExistBetween(b, a, "rel1"));
            assertFalse(rm.DoesRelIdExistBetween(b, b, "rel1"));
            assertFalse(rm.DoesRelIdExistBetween(b, c, "rel1"));
            assertFalse(rm.DoesRelIdExistBetween(b, d, "rel1"));

            assertFalse(rm.DoesRelIdExistBetween(d, a, "rel1"));
            assertFalse(rm.DoesRelIdExistBetween(d, b, "rel1"));
            assertTrue(rm.DoesRelIdExistBetween(d, c, "rel1"));
            assertFalse(rm.DoesRelIdExistBetween(d, d, "rel1"));

            assertFalse(rm.DoesRelIdExistBetween(c, a, "rel1"));
            assertFalse(rm.DoesRelIdExistBetween(c, b, "rel1"));
            assertFalse(rm.DoesRelIdExistBetween(c, c, "rel1"));
            assertFalse(rm.DoesRelIdExistBetween(c, d, "rel1"));
        }



        @Test
        public void ClassicManyToMany()
        {
            rm.EnforceRelationship("rel1", Cardinality.ManyToMany);
            CheckManyToMany();
        }

        @Test
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
            List list;
            Object res;
            list = rm.FindObjectsPointedToByMe(a, "rel1");
            assertEquals(2, list.size());
            assertTrue(list.contains(b));
            assertTrue(list.contains(c));
            res = rm.FindObjectPointedToByMe(a, "rel1");
            assertTrue(res == b || res == c);

            list = rm.FindObjectsPointedToByMe(d, "rel1");
            assertEquals(1, list.size());
            assertTrue(list.contains(c));
            res = rm.FindObjectPointedToByMe(d, "rel1");
            assertTrue(res == c);

            // back links

            list = rm.FindObjectsPointingToMe(c, "rel1");
            assertEquals(2, list.size());
            assertTrue(list.contains(a));
            assertTrue(list.contains(d));
            res = rm.FindObjectPointingToMe(c, "rel1");
            assertTrue(res == a || res == d);

            list = rm.FindObjectsPointingToMe(b, "rel1");
            assertEquals(1, list.size());
            assertTrue(list.contains(a));
            res = rm.FindObjectPointingToMe(b, "rel1");
            assertTrue(res == a);


            assertEquals(3, rm.CountRelationships("rel1"));
            assertEquals(3, rm.Count());

            // More laborious checks...
            assertFalse(rm.DoesRelIdExistBetween(a, a, "rel1"));
            assertTrue(rm.DoesRelIdExistBetween(a, b, "rel1"));
            assertTrue(rm.DoesRelIdExistBetween(a, c, "rel1"));
            assertFalse(rm.DoesRelIdExistBetween(a, d, "rel1"));

            assertFalse(rm.DoesRelIdExistBetween(b, a, "rel1"));
            assertFalse(rm.DoesRelIdExistBetween(b, b, "rel1"));
            assertFalse(rm.DoesRelIdExistBetween(b, c, "rel1"));
            assertFalse(rm.DoesRelIdExistBetween(b, d, "rel1"));

            assertFalse(rm.DoesRelIdExistBetween(d, a, "rel1"));
            assertFalse(rm.DoesRelIdExistBetween(d, b, "rel1"));
            assertTrue(rm.DoesRelIdExistBetween(d, c, "rel1"));
            assertFalse(rm.DoesRelIdExistBetween(d, d, "rel1"));

            assertFalse(rm.DoesRelIdExistBetween(c, a, "rel1"));
            assertFalse(rm.DoesRelIdExistBetween(c, b, "rel1"));
            assertFalse(rm.DoesRelIdExistBetween(c, c, "rel1"));
            assertFalse(rm.DoesRelIdExistBetween(c, d, "rel1"));
        }

        private void ManyManyStage2Result()
        {
            ManyManyStage1Result();
        }

        private void ManyManyStage3Result()
        {
            List list;
            Object res;
            list = rm.FindObjectsPointedToByMe(a, "rel1");
            assertEquals(2, list.size());
            assertTrue(list.contains(b));
            assertTrue(list.contains(c));
            res = rm.FindObjectPointedToByMe(a, "rel1");
            assertTrue(res == b || res == c);

            list = rm.FindObjectsPointedToByMe(d, "rel1");
            assertEquals(2, list.size());
            assertTrue(list.contains(b));
            assertTrue(list.contains(c));
            res = rm.FindObjectPointedToByMe(d, "rel1");
            assertTrue(res == b || res == c);

            list = rm.FindObjectsPointedToByMe(c, "rel1");
            assertEquals(2, list.size());
            assertTrue(list.contains(b));
            assertTrue(list.contains(d));
            res = rm.FindObjectPointedToByMe(a, "rel1");
            assertTrue(res == b || res == d);

            // back links

            list = rm.FindObjectsPointingToMe(b, "rel1");
            assertEquals(3, list.size());
            assertTrue(list.contains(a));
            assertTrue(list.contains(c));
            assertTrue(list.contains(d));
            res = rm.FindObjectPointingToMe(b, "rel1");
            assertTrue(res == a || res == c || res == d);

            list = rm.FindObjectsPointingToMe(c, "rel1");
            assertEquals(2, list.size());
            assertTrue(list.contains(a));
            assertTrue(list.contains(d));
            res = rm.FindObjectPointingToMe(c, "rel1");
            assertTrue(res == a || res == d);

            list = rm.FindObjectsPointingToMe(d, "rel1");
            assertEquals(1, list.size());
            assertTrue(list.contains(c));
            res = rm.FindObjectPointingToMe(d, "rel1");
            assertTrue(res == c);


            assertEquals(6, rm.CountRelationships("rel1"));
            assertEquals(6, rm.Count());

            // More laborious checks...
            assertFalse(rm.DoesRelIdExistBetween(a, a, "rel1"));
            assertTrue(rm.DoesRelIdExistBetween(a, b, "rel1"));
            assertTrue(rm.DoesRelIdExistBetween(a, c, "rel1"));
            assertFalse(rm.DoesRelIdExistBetween(a, d, "rel1"));

            assertFalse(rm.DoesRelIdExistBetween(b, a, "rel1"));
            assertFalse(rm.DoesRelIdExistBetween(b, b, "rel1"));
            assertFalse(rm.DoesRelIdExistBetween(b, c, "rel1"));
            assertFalse(rm.DoesRelIdExistBetween(b, d, "rel1"));

            assertFalse(rm.DoesRelIdExistBetween(d, a, "rel1"));
            assertTrue(rm.DoesRelIdExistBetween(d, b, "rel1"));
            assertTrue(rm.DoesRelIdExistBetween(d, c, "rel1"));
            assertFalse(rm.DoesRelIdExistBetween(d, d, "rel1"));

            assertFalse(rm.DoesRelIdExistBetween(c, a, "rel1"));
            assertTrue(rm.DoesRelIdExistBetween(c, b, "rel1"));
            assertFalse(rm.DoesRelIdExistBetween(c, c, "rel1"));
            assertTrue(rm.DoesRelIdExistBetween(c, d, "rel1"));
        }


}