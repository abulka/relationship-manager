
import java.util.List;
import relationshipmanager.turbo.Cardinality;
import relationshipmanager.turbo.Directionality;

/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 *
 * @author Tarik
 */
class X extends BO {

    public X() {
        RM.ER("xtoy", Cardinality.OneToMany, Directionality.DoubleDirectional);
    }

    public void addY(Y y) {
        RM.R(this, y, "xtoy");
    }

    public List getAllY() {
        return RM.PS(this, "xtoy");
    }

    public void removeY(Y y) {
        RM.NR(this, y, "xtoy");
    }
}
