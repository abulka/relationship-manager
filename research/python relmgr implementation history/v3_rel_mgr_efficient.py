import copy


class EfficientRelationshipManager(object):
    """
    Good core implementation, maps forward and reverse pointers
    for efficiency e.g.

        relations {
            from1 : {to1:[rel1]}
            from2 : {to5:[rel1,rel2], to6:[rel1]}
        }
        inverseRelations {
            same as above except meaning is reversed.
        }

    Adds Relationships property for setting and getting the relationships
    which helps if persisting.
    """

    def __init__(self):     # Constructor
        self.Relations = {}
        self.InverseOfRelations = {}

    def GetRelations(self):
        result = []
        for fromobj in self.Relations:
            todict = self.Relations[fromobj]
            for toobj in todict:
                for relId in todict[toobj]:
                    result.append((fromobj, toobj, relId))
        return result

    def SetRelations(self, listofrelationshiptuples):
        for r in listofrelationshiptuples:
            self.AddRelationship(From=r[0], To=r[1], RelId=r[2])
    Relationships = property(GetRelations, SetRelations)  # ANDY

    def AddRelationship(self, From, To, RelId=1):
        def AddEntry(relationsDict, From, To, RelId):
            if From not in relationsDict:
                relationsDict[From] = {}
            if To not in relationsDict[From]:
                relationsDict[From][To] = []
            if RelId not in relationsDict[From][To]:
                relationsDict[From][To].append(RelId)
        AddEntry(self.Relations, From, To, RelId)
        AddEntry(self.InverseOfRelations, To, From, RelId)

    def RemoveRelationships(self, From, To, RelId=1):
        """
        Specifying None as a parameter means 'any'
        """
        def havespecifiedallParams(): return (
            From != None and To != None and RelId != None)

        def NumberOfNonWildcardParamsSupplied():
            numberOfNoneParams = 0
            if From == None:
                numberOfNoneParams += 1
            if To == None:
                numberOfNoneParams += 1
            if RelId == None:
                numberOfNoneParams += 1
            return numberOfNoneParams

        if NumberOfNonWildcardParamsSupplied() > 1:
            raise RuntimeError(
                'Only one parameter can be left as None, (indicating a match with anything).')

        def ZapRelId(From, To, RelId):
            def _ZapRelationId(rdict, From, To, RelId):
                assert (From != None and To != None and RelId != None)
                relList = rdict[From][To]
                if RelId in relList:
                    relList.remove(RelId)
                if relList == []:     # no more relationships, so remove the entire mapping
                    del rdict[From][To]
            _ZapRelationId(self.Relations,          From, To,   RelId)
            _ZapRelationId(self.InverseOfRelations, To,   From, RelId)

        if havespecifiedallParams():
            if self.FindObjects(From, To, RelId):  # returns T/F
                ZapRelId(From, To, RelId)
        else:
            # this list will be either From or To or RelIds depending on which param was set as None (meaning match anything)
            lzt = self.FindObjects(From, To, RelId)
            if lzt:
                for objOrRelid in lzt:
                    if From == None:
                        # lzt contains all the things that point to 'To' with relid 'RelId'
                        # objOrRelid is the specific thing during this iteration that point to 'To', so delete it
                        ZapRelId(objOrRelid, To, RelId)
                    elif To == None:
                        ZapRelId(From, objOrRelid, RelId)
                    elif RelId == None:
                        ZapRelId(From, To, objOrRelid)

    def FindObjects(self, From=None, To=None, RelId=1):
        """
        Specifying None as a parameter means 'any'
        Can specify
          # 'From' is None - use normal relations dictionary
          From=None To=blah RelId=blah  anyone pointing to 'To' of specific RelId
          From=None To=blah RelId=None  anyone pointing to 'To'

          # 'To' is None - use inverse relations dictionary
          From=blah To=None RelId=blah  anyone 'From' points to, of specific RelId
          From=blah To=None RelId=None  anyone 'From' points to

          # Both 'To' & 'From' specified, use any e.g. use normal relations dictionary
          From=blah To=blah RelId=None  all RelId's between blah and blah
          From=blah To=blah RelId=blah  T/F does this specific relationship exist

          From=None To=None RelId=blah  error (though you could implement returning a list of From,To pairs using the R blah e.g. [('a','b'),('a','c')]
          From=None To=None RelId=None  error
        """
        if From == None and To == None:
            raise RuntimeError("Either 'From' or 'To' has to be specified")

        def havespecifiedallParams(): return (
            From != None and To != None and RelId != None)
        resultlist = []

        if From == None:
            subdict = self.InverseOfRelations.get(To, {})
            resultlist = [k for k, v in subdict.items() if (
                RelId in v or RelId == None)]

        elif To == None:
            # returns a list of all the matching tos
            subdict = self.Relations.get(From, {})
            resultlist = [k for k, v in subdict.items() if (
                RelId in v or RelId == None)]

        else:
            """
            # Both 'To' & 'From' specified, use any e.g. use normal relations dictionary
            From=blah To=blah RelId=None  all RelId's between blah and blah
            From=blah To=blah RelId=blah  T/F does this specific relationship exist
            """
            subdict = self.Relations.get(From, {})
            relationIdsList = subdict.get(To, [])
            if RelId == None:
                # return the entire list of relationship ids between these two.
                resultlist = relationIdsList
            else:
                return RelId in relationIdsList  # return T/F
        return copy.copy(resultlist)

    def Clear(self):
        self.Relations.clear()
        self.InverseOfRelations.clear()

    def FindObject(self, From=None, To=None, RelId=1):    # ANDY
        lzt = self.FindObjects(From, To, RelId)
        if lzt:
            return lzt[0]
        else:
            return None


if __name__ == "__main__":
    import pprint

    rm = EfficientRelationshipManager()
    rm.AddRelationship('a', 'b', 1)  # {'a': {'b': 1}}
    pprint.pprint(rm.Relations)
    rm.AddRelationship('a', 'b', 2)  # this clobbers the previous relationship: {'a': {'b': 2}}
    pprint.pprint(rm.Relations)

    rm.AddRelationship('a', 'x', 1)
    rm.AddRelationship('fred', 'mary', 1)
    pprint.pprint(rm.Relations)
    pprint.pprint(rm.InverseOfRelations)

    print(rm.Relationships)  # the official property returns a flat list
