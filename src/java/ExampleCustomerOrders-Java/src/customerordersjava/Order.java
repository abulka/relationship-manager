package customerordersjava;

/**
 * Order class points back to the person holding the order.
 * Implemented using a relationship manager rather 
 * than via pointers and arraylists etc.
 * 
 * @author Andy
 */
public class Order extends BaseBusinessObject {

    public String description;

    public Order(String description) {
        this.description = description;
    }

    @Override
    public String toString() {
        return "Order Description: " + this.description;
    }

    public void setCustomer(Customer c) {
        RM.R(c, this, "c->o");  // though mapping is implemented bidirectionally,
                                //there is still a primary relationship direction!
    }

    public Customer getCustomer() {
        return (Customer) RM.P(this, "c->o");
    }

    public void clearCustomer() {
        RM.NR(this, this.getCustomer(), "c->o");
    }
}