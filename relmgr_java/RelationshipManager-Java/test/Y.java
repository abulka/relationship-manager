/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 *
 * @author Tarik
 */
class Y extends BO {

    public void setX(X x) {
        RM.R(x, this, "xtoy");  // though bi, there is still a direction!
    }

    public Object getX() {
        return RM.P(this, "xtoy");
    }

    public void clearX() {
        RM.NR(this, this.getX(), "xtoy");
    }
}

