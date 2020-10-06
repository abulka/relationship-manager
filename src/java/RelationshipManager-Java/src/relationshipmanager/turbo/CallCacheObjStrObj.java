package relationshipmanager.turbo;

/**
 *
 * @author Tarik
 */
public class CallCacheObjStrObj extends CallCache {

    private Object paramObj = null;
    private String paramStr = null;
    private Object resultObj = null;

    public Object getResult() {
        return resultObj;
    }

    public void SetData(Object paramObj, String paramStr, Object resultObj) {
        this.paramObj = paramObj;
        this.paramStr = paramStr;
        this.resultObj = resultObj;
        cachedDataIsRealData = true;
    }

    public boolean CallMatches(Object fromObj, String relId) {
        return (cacheEnabled &&
                cachedDataIsRealData &&
                this.paramObj.equals(fromObj) &&
                this.paramStr.equals(relId));
    }
}


