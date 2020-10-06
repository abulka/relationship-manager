package customerordersjava;

import java.util.List;
import relationshipmanager.turbo.Cardinality;
import relationshipmanager.turbo.Directionality;
import relationshipmanager.turbo.IRM;
import relationshipmanager.turbo.RM;

/**
 *
 * @author Andy
 */
public class Main {

    public static void main(String[] args) {
        Test01();
        Test02_Person();
    }

    static private void Test01() {
        System.out.println();

        IRM rm = new RM();
        System.out.println(rm.toString());
        System.out.println();

        rm.ER("xtoy", Cardinality.OneToOne, Directionality.DirectionalWithBackPointer);
        rm.R("andy", "boo", "xtoy");
    }

    static private void Test02_Person() {
        System.out.println("--------- Person ->* Order --------------");
        System.out.println();
        Customer c1 = new Customer("Andy");
        Customer c2 = new Customer("Jim");
        System.out.println(c1.toString());
        System.out.println(c2.toString());

        Order o1 = new Order("widget A");
        Order o2 = new Order("widget B");
        Order o3 = new Order("widget C");
        System.out.println(o1.toString());
        System.out.println(o2.toString());
        System.out.println(o3.toString());
        System.out.println();

        System.out.println(c1.RM.D());
        
        c1.addOrder(o1);
        System.out.println(c1.RM.D());

        c1.addOrder(o2);
        System.out.println(c1.RM.D());

        System.out.println("Orders for " + c1.toString() + " are:");
        for (Order o : (List<Order>) c1.getOrders()) {
            System.out.println(o.toString());
        }

        System.out.println();
        System.out.println("Who ordered widget " + o1.toString() + " ?  Answer is");
        
        Customer whoordered = o1.getCustomer();
        if (whoordered == null)
            System.out.println("That's strange - nobody ordered this?  Something is wrong with RM...please debug me");
        else
            System.out.println(o1.getCustomer().toString());
    }
}
