class RelationshipManagerOriginal:
    def __init__(self):
        self.Relationships = []

    def AddRelationship(self, From, To, RelId=1):
        if not self.FindObjects(From, To, RelId):
            self.Relationships.append((From, To, RelId))  # assoc obj

    def RemoveRelationships(self, From, To, RelId=1):
        if not From or not To:
            return
        lzt = self.FindObjects(From, To, RelId)
        if lzt:
            for association in lzt:
                self.Relationships.remove(association)

    def FindObjects(self, From=None, To=None, RelId=1):
        resultlist = []
        def match(obj, list, index): return obj == list[index] or obj == None
        for association in self.Relationships:
            if match(From, association, 0) and match(To, association, 1) and RelId == association[2]:
                if From == None:
                    resultlist.append(association[0])
                elif To == None:
                    resultlist.append(association[1])
                else:
                    resultlist.append(association)
        return resultlist

    def FindObject(self, From=None, To=None, RelId=1):
        lzt = self.FindObjects(From, To, RelId)
        if lzt:
            return lzt[0]
        else:
            return None

    def Clear(self):
        del self.Relationships[0:]
