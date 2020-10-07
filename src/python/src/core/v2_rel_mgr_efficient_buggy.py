class EfficientRelationshipManagerBuggy(object):
    """
     Efficient RM using hash
     
     The faster RM does not support relationship Id's properly, so causes errors
     in saving me mappings, which require 'S' and 'G' relationships.

     Note the reason it doesn't support relationship Id's is that when adding an entry
     any subsequent relationship Id clobbers the previous relationship Id, since dictionaries
     cannot have duplicate keys.
    """
    def __init__(self):     # Constructor
        self.Relations = {}
        self.InverseOfRelations = {}

    def GetRelations(self):
        result = []
        for fromobj in self.Relations:
            todict = self.Relations[fromobj]
            for toobj in todict:
                result.append((fromobj, toobj, '1')) # since BigRelationshipManager1 doesn't support relId properly, fake it.
        return result
    def SetRelations(self, listofrelationshiptuples):
        for r in listofrelationshiptuples:
            self.AddRelationship(From=r[0], To=r[1], RelId=r[2])
    Relationships = property(GetRelations, SetRelations) # ANDY

    def AddRelationship(self, From, To, RelId=1):
        if From not in self.Relations:
            self.Relations[From] = {}
        self.Relations[From][To] = RelId

        if To not in self.InverseOfRelations:
            self.InverseOfRelations[To] = {}
        self.InverseOfRelations[To][From] = RelId
    def RemoveRelationships(self, From, To, RelId=1):
        del self.Relations[From][To]
        if not self.Relations[From]:
            del self.Relations[From]

        del self.InverseOfRelations[To][From]
        if not self.InverseOfRelations[To]:
            del self.InverseOfRelations[To]
    def FindObjects(self, From=None, To=None, RelId=1):
        resultlist = []

        if From==None:
            subdict = self.InverseOfRelations.get(To, {})
            resultlist = [ k for k, v in subdict.items() if v == RelId]
        elif To==None:
            # returns a list of all the matching tos
            subdict = self.Relations.get(From, {})
            resultlist = [ k for k, v in subdict.items() if v == RelId]
        else:
            # returns a list of all the matching (from, to, relid)
            subdict = self.Relations.get(From, {})
            relid = subdict.get(To, None)
            if relid == None:
                resultlist = []
            else:
                resultlist = [(From, To, RelId)]
        return resultlist
    def Clear(self):
        self.Relations.clear()
        self.InverseOfRelations.clear()
    def FindObject(self, From=None, To=None, RelId=1):    # ANDY
        lzt = self.FindObjects(From, To, RelId)
        if lzt:
            return lzt[0]
        else:
            return None
