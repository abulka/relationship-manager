using System;
using System.Collections;
using RelationshipManager55;

namespace WindowsApplicationUsing\_RelationshipManagerDllTest001 {
  ///   
  /// BO is the base Business Object class which holds a single static reference  
  /// to a relationship manager. This one relationship manager is  
  /// used for managing all the relationships between Business Objects.  
  ///   
  public class BO // Base business object  
  {
    static protected RM1 RM = new RM1();
  }

  ///   
  /// Person class points to one or more orders.  
  /// Implemented using a relationship manager rather   
  /// than via pointers and arraylists etc.  
  ///   
  public class Person: BO {
    public string name;

    static Person() {
      RM.ER("p->o", "onetomany", "bidirectional");
    }

    public Person(string name) {
      this.name = name;
    }
    public override string ToString() {
      return "Person: " + this.name;
    }

    public void AddOrder(Order o) {
      RM.R(this, o, "p->o");
    }
    public void RemoveOrder(Order o) {
      RM.NR(this, o, "p->o");
    }
    public IList GetOrders() {
      return RM.PS(this, "p->o");
    }
  }

  ///   
  /// Order class points back to the person holding the order.  
  /// Implemented using a relationship manager rather             /// than via pointers and arraylists etc.  
  ///   
  public class Order: BO {
    public string description;

    public Order(string description) {
      this.description = description;
    }
    public override string ToString() {
      return "Order Description: " + this.description;
    }

    public void SetPerson(Person p) {
      RM.R(p, this, "p->o"); // though mapping is bidirectional,  
      there is still a primary relationship direction !

    }
    public Person GetPerson() {
      return (Person) RM.P(this, "p->o");
    }
    public void ClearPerson() {
      RM.NR(this, this.GetPerson(), "p->o");
    }
  }

}
