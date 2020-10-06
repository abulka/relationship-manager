package relationshipmanager.turbo;

/**
 *
 * @author Tarik
 */
public class CallCache {

    public static boolean cacheEnabled = true;
    protected boolean cachedDataIsRealData = false;

    public void Invalidate() {
        cachedDataIsRealData = false;
    }
}

