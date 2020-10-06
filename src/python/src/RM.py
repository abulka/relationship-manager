"""
Relationship manager revisited.
Version 1.2
June 2003. 
(c) Andy Bulka
http://www.atug.com/andypatterns

  ____      _       _   _                 _     _
 |  _ \ ___| | __ _| |_(_) ___  _ __  ___| |__ (_)_ __
 | |_) / _ \ |/ _` | __| |/ _ \| '_ \/ __| '_ \| | '_ \
 |  _ <  __/ | (_| | |_| | (_) | | | \__ \ | | | | |_) |
 |_| \_\___|_|\__,_|\__|_|\___/|_| |_|___/_| |_|_| .__/
                                                 |_|
  __  __
 |  \/  | __ _ _ __   __ _  __ _  ___ _ __
 | |\/| |/ _` | '_ \ / _` |/ _` |/ _ \ '__|
 | |  | | (_| | | | | (_| | (_| |  __/ |
 |_|  |_|\__,_|_| |_|\__,_|\__, |\___|_|
                           |___/
"""


class RM1:
    def __init__(self):
        from src.relationshipmanager import RelationshipManager
        self.rm = RelationshipManager()
        self.enforcer = {}
        
    def ER(self, relId, cardinality, directionality="directional"):
        # enforceRelationship(id, cardinality, directionality)
        self.enforcer[relId] = (cardinality, directionality)
        
    def _RemoveExistingRelationships(self, fromObj, toObj, relId):
        def ExtinguishOldFrom():
            oldFrom = self.B(toObj, relId)
            self.NR(oldFrom, toObj, relId)
        def ExtinguishOldTo():
            oldTo = self.P(fromObj, relId)
            self.NR(fromObj, oldTo, relId)
        if relId in self.enforcer.keys():
            cardinality, directionality = self.enforcer[relId]
            if cardinality == "onetoone":
                ExtinguishOldFrom()
                ExtinguishOldTo()
            elif cardinality == "onetomany": # and directionality == "directional":
                ExtinguishOldFrom()

    def R(self, fromObj, toObj, relId):
        # addRelationship(f, t, id)
        self._RemoveExistingRelationships(fromObj, toObj, relId)
        self.rm.AddRelationship(fromObj, toObj, relId)

        if relId in self.enforcer.keys():
            cardinality, directionality = self.enforcer[relId]
            if directionality == "bidirectional":
                self.rm.AddRelationship(toObj, fromObj, relId)
        
    def P(self, fromObj, relId):
        # findObjectPointedToByMe(fromMe, id, cast)
        return self.rm.FindObject(fromObj, None, relId)
        
    def B(self, toObj, relId):
        # findObjectPointingToMe(toMe, id cast)
        return self.rm.FindObject(None, toObj, relId)

    def PS(self, fromObj, relId):
        # findObjectsPointedToByMe(fromMe, id, cast)
        return self.rm.FindObjects(fromObj, None, relId)

    def NR(self, fromObj, toObj, relId):
        # removeRelationship(f, t, id)
        self.rm.RemoveRelationships(fromObj, toObj, relId)
        
        if relId in self.enforcer.keys():
            cardinality, directionality = self.enforcer[relId]
            if directionality == "bidirectional":
                self.rm.RemoveRelationships(toObj, fromObj, relId)

