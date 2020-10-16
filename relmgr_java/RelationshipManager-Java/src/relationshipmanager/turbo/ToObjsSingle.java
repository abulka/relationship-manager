/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package relationshipmanager.turbo;

import java.util.ArrayList;

/**
 *
 * @author Tarik
 */
public class ToObjsSingle implements IToObjs {

    private Object ToObj;
    private boolean IsEmpty = true;

    public int getCount() {

        if (IsEmpty) {
            return 0;
        } else {
            return 1;
        }

    }

    public void Add(Object obj) {
        ToObj = obj;
        IsEmpty = false;
    }

    public void Remove(Object obj) {
        ToObj = null;
        IsEmpty = true;
    }

    /// <summary>
    /// See if obj matches the toobj
    /// </summary>
    /// <param name="obj"></param>
    /// <returns></returns>
    /// Be careful when using relationship manager to
    /// maintain relationships between value types
    /// i.e. ints and strings and chars etc. since these
    /// will be auto converted to unique boxed object 
    /// instances and you may not be able to ever 
    /// match that generated value!!
    /// 
    /// The solution is to always store object instances
    /// which is always the case with class instances. 
    /// Strings work out ok since they always get mapped
    /// to the same immutable address anyway, so using
    /// value types in this case is safe.  
    /// Value type of char and int are a problem, so please
    /// convert these to boxed version before storing.
    /// 
    /// (Note the one to many implementation which 
    /// uses a hashtable doesn't suffer this
    /// implementation nuance because of the way hashtable
    /// keys seems work. e.g. storing a value type char
    /// as a key in a hashtable will always match with 
    /// a totally different value type char, as long as 
    /// it is the same 'value'.).
    
    public boolean Contains(Object obj) {
        boolean match = (obj.equals(ToObj));
        return (!IsEmpty && match);
    }

    public Object GetFirstHashKey() {
        if (!IsEmpty) {
            return ToObj;
        } else //throw new Exception("No value in ToObjs object");
        {
            return null;
        }
    }

    public ArrayList ToArray() {
        ArrayList result = new ArrayList();
        if (!IsEmpty) {
            result.add(ToObj);
        }
        return result;
    }
}
