package relationshipmanager.turbo;

import java.util.ArrayList;
import java.util.Enumeration;
import java.util.Hashtable;

/**
 *
 * @author Tarik
 */
public class HashColl<KeyType, ValueType> {

    public Hashtable<KeyType, ValueType> Value = new Hashtable<KeyType, ValueType>();

    public void Clear() {
        Value.clear();
    }

    public void Add(KeyType obj,ValueType v) {
        Value.put(obj, v);
    }

    public void Remove(KeyType obj) {
        Value.remove(obj);
    }

    public KeyType GetFirstHashKey() {
        Enumeration<KeyType> e = Value.keys();
        if (e.hasMoreElements()) {
            return e.nextElement();
        } else {
            return null;
        }
    }

    public ArrayList<KeyType> ToArray() {
        return new ArrayList<KeyType>(Value.keySet());
    }

    public boolean Contains(KeyType obj) {
        return Value.containsKey(obj);
    }

    public int getCount() {
        return Value.size();
    }
}
