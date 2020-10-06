using System;
using System.Collections;
using System.Text;
using System.Diagnostics;

using RelationshipManager.Interfaces;
using RelationshipManager.Turbo;

namespace Speed_Trials_01
{
    class Program
    {

        static void Main(string[] args)
        {
            SpeedTest01 test = new SpeedTest01();
            test.Run();
        }
    }

    class SpeedTest01
    {
        private IRelationshipManager rm;
        DateTime start;

        public SpeedTest01()
        {
            rm = new RelationshipMgrTurbo();

            PrintPercentFaster(1,2);
            PrintPercentFaster(2, 1);
        }
        public void Run()
        {
            ((RelationshipMgrTurbo)rm).optimiseOneToOne = false;
            TimeSpan duration1 = SimpleLoop01();
            Console.WriteLine(duration1);

            ((RelationshipMgrTurbo)rm).optimiseOneToOne = true;
            TimeSpan duration2 = SimpleLoop01();
            Console.WriteLine(duration2);

            PrintPercentFaster(duration1.Ticks, duration2.Ticks);

            Console.ReadLine();
        }

        private TimeSpan SimpleLoop01()
        {
            start = DateTime.Now;
            rm.EnforceRelationship("rel1", Cardinality.OneToOne);
            for (int i = 1; i < 300900; i++)
            {
                if (i % 500 == 0)
                    Console.Write(".");
                rm.AddRelationship("a", "b", "rel1");
                IList list = rm.FindObjectsPointedToByMe("a", "rel1");
                Debug.Assert((string)list[0] == "b");
            }
            Console.WriteLine("!");
            return DateTime.Now - start;
        }

        public double PrintPercentFaster(double old, double newtime)
        {
	        // The jist of the logic is (C2-C1)/C1*100

	        double result, times, diff;
            string diffmsg1 = "{0:0.0} to {1:0.0} = no change";
            string diffmsg2 = "{0:0.0} to {1:0.0} diff is {2:0.0}% or {3:0.0}x {4}.";
	
	        if (newtime == old)
            {
		        result = 0;
                Console.WriteLine(diffmsg1, old, newtime);
            }
	        else if (newtime < old)
            {
		        diff = (old-newtime);
                times = old / newtime;
                result = diff / newtime * 100;
                Console.WriteLine(diffmsg2, old, newtime, result, times, "faster");
	        }
            else
            {
                diff = (newtime - old);
                times =  newtime / old;
                result =  diff / old * 100;
                Console.WriteLine(diffmsg2, old, newtime, result, times, "slower");

	        }
            return result;
        }

    }
}
