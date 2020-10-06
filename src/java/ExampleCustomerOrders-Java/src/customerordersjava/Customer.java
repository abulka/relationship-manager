package customerordersjava;

import java.util.List;
import relationshipmanager.turbo.Cardinality;
import relationshipmanager.turbo.Directionality;

/**
 * Person class points to one or more orders.
 * Implemented using a relationship manager rather 
 * than via pointers and arraylists etc.
 *
 * @author Andy
 */
public class Customer extends BaseBusinessObject {

    private String name;

    public Customer() {
        BaseBusinessObject.RM.ER("c->o", Cardinality.OneToMany, Directionality.DoubleDirectional);
    }

    public Customer(String name) {
        this.name = name;
    }

    @Override
    public String toString() {
        return "Person: " + this.name;
    }

    public void addOrder(Order o) {
        RM.R(this, o, "c->o");
    }

    public void removeOrder(Order o) {
        RM.NR(this, o, "c->o");
    }

    public List getOrders() {
        return RM.PS(this, "c->o");
    }
}
