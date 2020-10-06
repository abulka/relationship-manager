/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package relationshipmanager.turbo;

/**
 *
 * @author Tarik
 */
public class ToObjs extends HashColl<Object, Boolean> implements IToObjs {
        public void Add(Object obj) {
            this.Add(obj, true);
        }

}
