package relationshipmanager.turbo;

/**
 *
 * @author Tarik
 */
public class RelIds extends HashColl<String, IToObjs> {

    IToObjs result;

    public IToObjs FindToObjs(String relId) {
        result = (IToObjs) Value.get(relId);
        return result;
    }

    public void SetEntry(String relId, IToObjs toObj) {
        Value.put(relId, toObj);
    }
}
