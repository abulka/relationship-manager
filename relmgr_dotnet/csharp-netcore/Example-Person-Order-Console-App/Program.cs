using System;
using System.Collections;
using System.Collections.Generic;
using RelationshipManager.Interfaces;
using RelationshipManager.Turbo;

namespace Example_Person_Order_Console_App
{
    class Program
    {
        static void Main(string[] args)
        {
            var jane = new Person("Jane");
            var order1 = new Order("Boots");
            var order2 = new Order("Clothes");
            jane.AddOrder(order1);
            jane.AddOrder(order2);

            // test forward pointer wiring
            Console.WriteLine(jane + " has " + jane.GetOrders().Count + " orders");

            // test the backpointer wiring
            foreach (var order in jane.GetOrders())
            {
                Console.WriteLine("The person who ordered " + order + " is " + order.GetPerson());
            }

            Console.WriteLine("Done!");

        }

        ///   
        /// BO is the base Business Object class which holds a single static reference  
        /// to a relationship manager. This one relationship manager is  
        /// used for managing all the relationships between Business Objects
        /// like Person and Order.  
        ///   
        public class BO // Base business object  
        {
            static protected RelationshipMgrTurbo rm = new RelationshipMgrTurbo();
        }


        ///   
        /// Person class points to one or more orders.  
        /// Implemented using a relationship manager rather   
        /// than via pointers and arraylists etc.  
        ///   
        public class Person : BO
        {
            public string name;

            static Person()
            {
                rm.EnforceRelationship("p->o", Cardinality.OneToMany, Directionality.DirectionalWithBackPointer);
            }

            public Person(string name)
            {
                this.name = name;
            }

            public override string ToString()
            {
                return "Person: " + this.name;
            }

            public void AddOrder(Order o)
            {
                rm.AddRelationship(this, o, "p->o");
            }

            public void RemoveOrder(Order o)
            {
                rm.RemoveRelationship(this, o, "p->o");
            }

            public List<Order> GetOrders()
            {
                IList list = rm.FindObjectsPointedToByMe(this, "p->o");

                // cast from list of 'object' to list of 'Person'
                var result = new List<Order>();
                foreach (var order in list)
                    result.Add((Order)order);

                // attempts at other simpler ways to cast a whole list
                //result = list as List<Order>;  // crash
                //result = new List<Order>(list); // syntax error?

                return result;
            }
        }

        ///   
        /// Order class points back to the person holding the order.  
        /// Implemented using a relationship manager rather
        /// than via pointers and arraylists etc.  
        ///  
        public class Order : BO
        {
            public string description;

            public Order(string description)
            {
                this.description = description;
            }

            public override string ToString()
            {
                return "Order Description: " + this.description;
            }

            public void SetPerson(Person p)
            {
                // though mapping is bidirectional, there is still a primary relationship direction!
                rm.AddRelationship(p, this, "p->o");

            }

            public Person GetPerson()
            {
                // cast from 'object' to 'Person'
                return (Person)rm.FindObjectPointingToMe(this, "p->o");
            }

            public void ClearPerson()
            {
                rm.RemoveRelationship(this, this.GetPerson(), "p->o");
            }
        }

    }

}
