package relationshipmanager.turbo;

/**
 *
 * @author Tarik
 */
public class CallCacheInt extends CallCache {

    private int resultInt;

    public int getResult() {
        return resultInt;
    }

    public void SetData(int resultInt) {
        this.resultInt = resultInt;
        cachedDataIsRealData = true;
    }

    public boolean CallMatches() {
        return (cacheEnabled &&
                cachedDataIsRealData);
    }
}

