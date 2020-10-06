package relationshipmanager.turbo;

/**
 *
 * @author Tarik
 */
public class CallCacheStrInt extends CallCache {

    private String paramStr;
    private int resultInt;

    public int getResult() {
        return resultInt;
    }

    public void SetData(String paramStr, int resultInt) {
        this.paramStr = paramStr;
        this.resultInt = resultInt;
        cachedDataIsRealData = true;
    }

    public boolean CallMatches(String paramStr) {
        return (cacheEnabled &&
                cachedDataIsRealData &&
                this.paramStr.equals(paramStr));
    }
}
