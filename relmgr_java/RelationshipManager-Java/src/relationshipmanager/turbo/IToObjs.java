package relationshipmanager.turbo;

import java.util.ArrayList;

/**
 *
 * @author Tarik
 */
public interface IToObjs {
    int getCount();
    void Add(Object obj);
    void Remove(Object obj);
    boolean Contains(Object obj);
    Object GetFirstHashKey();
    ArrayList ToArray();
}

