"""
 An example from an old project of using relationship manager in a real project. This file wil compile
 but not run due to missing dependencies. It does show how to do persistence of objects and relationships.
 It is probably of limited value.

 Oob, MetoOobMappings, Oobtree
"""
# from src.relationship_manager import RelationshipManager
from src.core import EfficientRelationshipManager1 as RelationshipManager

import copy
#from loglevels import Log
import sys, os
import random, time
import pprint
from pprint import pformat
#from mountedness import MountedCalculator
#import utilcc
#import motionconstants

#show=utilcc.show

oobattributelogging = 0
metoobmappingattributelogging = 0

includeclassinitial = 0

stdoutlogging = 0

if stdoutlogging:
    _Log=Log
    def Log(s,f):
        print(f())
        _Log(s,f)

class gettabs(str):
    tbroot = []
    def __new__(cls, flag):
        tbroot = cls.tbroot
        import traceback
        tb = traceback.extract_stack()
        for i in range(len(tb)):
            if i < len(tbroot) and tb[i] == tbroot[i]:
                continue
            if tb[i][0].endswith("oobtree.py"):
                break

            fileinfo = 'File "%s", line %s'%(tb[i][0], tb[i][1])
            tbstr = "%s\t\t\t%s"%(tb[i][2], fileinfo)
            Log('OOB    ', lambda: (' '*i)+' '+tbstr)
        cls.tbroot = tb
        count = len(tb)

        return str.__new__(cls, (' '*count)+flag+" ")

class CallWrapper(object):
    def __init__(self, f, name, c, dontlog):
        self.f = f
        self.name = name
        self.c = c # initial char of the class name
        self.dontlog = dontlog

    def __call__(self, *args, **kw):
        import traceback
        tb = traceback.extract_stack()

        fileinfo = 'File "%s", line %s'%(tb[-2][0], tb[-2][1])

        if includeclassinitial:
            flag = self.c
        elif self.name in self.dontlog:
            flag = '*'
        else:
            flag = ' '

        Log('OOBCALL', lambda: '%s%s%s\t\t\t%s'%(gettabs(flag), self.name, repr(args)[:80], fileinfo))
        return self.f(*args, **kw)

def X_getattribute__(self, name):
    attr = object.__getattribute__(self, name)
    c= object.__getattribute__(self, '__class__').__name__[0]


# This stuff checks for undeclared methods

##    if name[0] != '_' and hasattr(attr, '__call__'):
##        # __mro__[-1] is object of course
##        base = self.__class__.__mro__[-2]
##        if not hasattr(base, name):
##            print ("WARNING: %s does not have %s declared"%(base.__name__, name))


    dontlog = ['GetInfoForMgmClientDisplay']
    import traceback
    tb = traceback.extract_stack()

    for frame in tb:
        if frame[2] in dontlog:
            return attr

    if name == '__class__':
        return attr

    if hasattr(attr, '__call__'):
        return CallWrapper(attr, name, c, dontlog)

    if includeclassinitial:
        flag = self.c
    else:
        flag = ' '

    Log('OOB GET', lambda: '%sgetattr(%s)'%(gettabs(flag), name))
    return attr

def X_setattr__(self, name, value):
    c=object.__getattribute__(self, '__class__').__name__[0]

    if includeclassinitial:
        flag = self.c
    else:
        flag = ' '

    Log('OOB SET', lambda: '%ssetattr(%s, %s)'%(gettabs(flag),name, object.__repr__(value)))
    object.__setattr__(self, name, value)


class OobBase(object):

    if oobattributelogging:
        __getattribute__ = X_getattribute__
        __setattr__ = X_setattr__

    # Theoretically should have entire oob API defined here.
    def LoadFromModule(self, module): raise RuntimeError('Not implemented in decendent class?')
    def LoadFromDict(self, dict): raise RuntimeError('Not implemented in decendent class?')
    def GetParent(self, oobid): raise RuntimeError('Not implemented in decendent class?')
    def FindChildren(self, oobid): raise RuntimeError('Not implemented in decendent class?')
    def FindAllRoles(self): raise RuntimeError('Not implemented in decendent class?')
    def FindAllHqs(self): raise RuntimeError('Not implemented in decendent class?')
    def FindHqsUnderCommandOfRole(self, roleoobid): raise RuntimeError('Not implemented in decendent class?')
    def FindAncestors(self, oobid): raise RuntimeError('Not implemented in decendent class?')
    def GetAllMePiecesUnderCommandOfRole(self, role): raise RuntimeError('Not implemented in decendent class?')
    def GetStartingCoord(self, oobid): raise RuntimeError('Not implemented in decendent class?')
    def CumulativeDelay(self, fromoobid, tooobid): raise RuntimeError('Not implemented in decendent class?')

    def DetermineWhichTreeFromSide(self, side): raise RuntimeError('Not implemented in decendent class?')
    def DetermineWhichTreeFromOobNodeId(self, oobid): raise RuntimeError('Not implemented in decendent class?')
    def GetSideOfPiece(self, meid): raise RuntimeError('Not implemented in decendent class?')
    def GetNationPrefixOfPiece(self, meid): raise RuntimeError('Not implemented in decendent class?')
    def GetNationality(self, oobid): raise RuntimeError('Not implemented in decendent class?')
    def GetNationalityPrefix(self, oobid): raise RuntimeError('Not implemented in decendent class?')
    def DetermineSideFromOobNodeId(self, oobid): raise RuntimeError('Not implemented in decendent class?')

    def RankingHqAboveMe(self, meid): raise RuntimeError('Not implemented in decendent class?')
    def RankingHqInMe(self, meid): raise RuntimeError('Not implemented in decendent class?')
    def IsRole(self, oobid): raise RuntimeError('Not implemented in decendent class?')
    def IsHq(self, oobid): raise RuntimeError('Not implemented in decendent class?')
    def IsMe(self, oobid): raise RuntimeError('Not implemented in decendent class?')
    def IsMounted(self, meid): raise RuntimeError('Not implemented in decendent class?')
    def GetDelay(self, oobid): raise RuntimeError('Not implemented in decendent class?')
    def SetDelay(self, oobid): raise RuntimeError('Not implemented in decendent class?')
    def GetOobName(self, oobid): raise RuntimeError('Not implemented in decendent class?')
    def GetOfficerName(self, oobid): raise RuntimeError('Not implemented in decendent class?')
    def GetOfficerRankAndName(self, oobid): raise RuntimeError('Not implemented in decendent class?')
    def GetOfficerRank(self, oobid): raise RuntimeError('Not implemented in decendent class?')
    def GetOfficerAggressiveness(self, oobid): raise RuntimeError('Not implemented in decendent class?')
    def GetOfficerEfficiency(self, oobid): raise RuntimeError('Not implemented in decendent class?')
    def GetOfficerLeadership(self, oobid): raise RuntimeError('Not implemented in decendent class?')
    def GetRootNodeId(self, side): raise RuntimeError('Not implemented in decendent class?')
    def SetTroopType(self, oobid, trooptype='Infantry'): raise RuntimeError('Not implemented in decendent class?')
    def GetTroopType(self, oobid): raise RuntimeError('Not implemented in decendent class?')
    def SetTransportType(self, oobid, transporttype='Foot'): raise RuntimeError('Not implemented in decendent class?')
    def GetTransportType(self, oobid): raise RuntimeError('Not implemented in decendent class?')
    def SetPoints(self, oobid, points): raise RuntimeError('Not implemented in decendent class?')
    def GetPoints(self, oobid): raise RuntimeError('Not implemented in decendent class?')
    def SetExperience(self, oobid, experience=0): raise RuntimeError('Not implemented in decendent class?')
    def GetExperience(self, oobid): raise RuntimeError('Not implemented in decendent class?')
    def GetOffRoadAbility(self, oobid): raise RuntimeError('Not implemented in decendent class?')
    def GetNumberOfMen(self, oobid): raise RuntimeError('Not implemented in decendent class?')
##    def GetCanHoldNumberOfMen(self, oobid): raise RuntimeError('Not implemented in decendent class?')
    def GetCarryingCapacity(self, oobid): raise RuntimeError('Not implemented in decendent class?') # depreciated
##    def GetSquadSize(self, oobid): raise RuntimeError('Not implemented in decendent class?')
##    def GetSquadCapacity(self, oobid): raise RuntimeError('Not implemented in decendent class?')
##    def GetHowMuchCanTow(self, oobid): raise RuntimeError('Not implemented in decendent class?')
##    def GetHowHardToTow(self, oobid): raise RuntimeError('Not implemented in decendent class?')
    def GetFitness(self, oobid): raise RuntimeError('Not implemented in decendent class?')
    def GetFitnessTime(self, oobid): raise RuntimeError('Not implemented in decendent class?')
    def SetFitness(self, oobid, fitness=0): raise RuntimeError('Not implemented in decendent class?')
    def GetSupplyAmmo(self, oobid): raise RuntimeError('Not implemented in decendent class?')
    def GetInitialDirection(self, oobid): raise RuntimeError('Not implemented in decendent class?')
    def GetSupplyBasics(self, oobid): raise RuntimeError('Not implemented in decendent class?')
    def GetSupplyFuel(self, oobid): raise RuntimeError('Not implemented in decendent class?')
    def GetMeAppearsAfterTurn(self, oobid): raise RuntimeError('Not implemented in decendent class?')
    def ClearMeAppearsAfterTurn(self, oobid): raise RuntimeError('Not implemented in decendent class?')
    def GetInitialMeReadiness(self, oobid): raise RuntimeError('Not implemented in decendent class?')
    def SetInitialMeReadiness(self, oobid, value): raise RuntimeError('Not implemented in decendent class?')
    def GetInitialMeName(self, oobid): raise RuntimeError('Not implemented in decendent class?')
    def GetSignals(self, oobid): raise RuntimeError('Not implemented in decendent class?')
    def SetSignals(self, oobid, signalsdict): raise RuntimeError('Not implemented in decendent class?')
    def __str__(self, oobid): raise RuntimeError('Not implemented in decendent class?')
    def __repr__(self, oobid): raise RuntimeError('Not implemented in decendent class?')
    def CreateTemporaryOobidUnderRole(self, parentroleoobid, trooptype, transporttype):  raise RuntimeError('Not implemented in decendent class?')
    def DestroyTemporaryOobid(self, signaloobid):  raise RuntimeError('Not implemented in decendent class?')
    def Exists(self, oobid): raise RuntimeError('Not implemented in decendent class?')

    def SetDamagePointsLastBattle(self, oobid, points): raise RuntimeError('Not implemented in decendent class?')
    def GetDamagePointsLastBattle(self, oobid): raise RuntimeError('Not implemented in decendent class?')

    def SetStrength(self, oobid, mtgvlist): raise RuntimeError('Not implemented in decendent class?')
    def GetStrength(self, oobid): raise RuntimeError('Not implemented in decendent class?')
    def GetStrengthTime(self, oobid): raise RuntimeError('Not implemented in decendent class?')
    def SetCasualtiesIncurredTotal(self, oobid, mtgvlist): raise RuntimeError('Not implemented in decendent class?')
    def GetCasualtiesIncurredTotal(self, oobid): raise RuntimeError('Not implemented in decendent class?')
    def SetCasualtiesIncurredLastBattle(self, oobid, mtgvlist): raise RuntimeError('Not implemented in decendent class?')
    def GetCasualtiesIncurredLastBattle(self, oobid): raise RuntimeError('Not implemented in decendent class?')
    def SetCasualtiesCausedTotal(self, oobid, mtgvlist): raise RuntimeError('Not implemented in decendent class?')
    def GetCasualtiesCausedTotal(self, oobid): raise RuntimeError('Not implemented in decendent class?')
    def SetCasualtiesCausedLastBattle(self, oobid, mtgvlist): raise RuntimeError('Not implemented in decendent class?')
    def GetCasualtiesCausedLastBattle(self, oobid): raise RuntimeError('Not implemented in decendent class?')
    def PostProcessOOBTree(self, oobid): raise RuntimeError('Not implemented in decendent class?')
    def InitStrengthsAndCasualties(self, oobid): raise RuntimeError('Not implemented in decendent class?')
    def AllocateNewOobNode(self, meid): raise RuntimeError('Not implemented in decendent class?')
    def AllocateNewOobNodeId(self, meid): raise RuntimeError('Not implemented in decendent class?')
    def LoadFromReprStr(self, meid): raise RuntimeError('Not implemented in decendent class?')
    def myrepr(self, meid): raise RuntimeError('Not implemented in decendent class?')

    def IsDead(self, oobid): raise RuntimeError('Not implemented in decendent class?')
    def SetOOBGameState(self, oobgamestate): raise RuntimeError('Not implemented in decendent class?')

    def GetRankingDepth(self, oobid): raise RuntimeError('Not implemented in decendent class?')
    def GetTOEDepth(self, oobid): raise RuntimeError('Not implemented in decendent class?')

    def GetOrderSkill(self, oobid): raise RuntimeError('Not implemented in decendent class?')
    def GetCombatSkill(self, oobid): raise RuntimeError('Not implemented in decendent class?')
    def GetRallySkill(self, oobid): raise RuntimeError('Not implemented in decendent class?')
    def GetStealthSkill(self, oobid): raise RuntimeError('Not implemented in decendent class?')

    def SetOrderSkill(self, oobid, level): raise RuntimeError('Not implemented in decendent class?')
    def SetCombatSkill(self, oobid, level): raise RuntimeError('Not implemented in decendent class?')
    def SetRallySkill(self, oobid, level): raise RuntimeError('Not implemented in decendent class?')
    def SetStealthSkill(self, oobid, level): raise RuntimeError('Not implemented in decendent class?')

    def GetImmobilized(self, oobid): raise RuntimeError('Not implemented in decendent class?')
    def SetImmobilized(self, oobid, immobilized): raise RuntimeError('Not implemented in decendent class?')

    def GetBogged(self, oobid): raise RuntimeError('Not implemented in decendent class?')
    def SetBogged(self, oobid, bogged): raise RuntimeError('Not implemented in decendent class?')

    def GetGunDestroyed(self, oobid): raise RuntimeError('Not implemented in decendent class?')
    def SetGunDestroyed(self, oobid, gundestroyed): raise RuntimeError('Not implemented in decendent class?')

    def GetDugIn(self, oobid): raise RuntimeError('Not implemented in decendent class?')
    def SetDugIn(self, oobid, dugin): raise RuntimeError('Not implemented in decendent class?')

class MeToOobMappingsBase(object):
    if metoobmappingattributelogging: # do you want attribute logging?
        __getattribute__ = X_getattribute__
        __setattr__ = X_setattr__
    def LoadFromStr(self): raise RuntimeError('Not implemented in decendent class?')
    def GetAllMeIds(self): raise RuntimeError('Not implemented in decendent class?')
    def MeIdToOobIds(self, meid): raise RuntimeError('MeIdToOobIds not implemented in subclass yet!')
    def MeIdToListOfOobIds(self, meid): raise RuntimeError('MeIdToListOfOobIds not implemented in subclass yet!')
    def Build(self): raise RuntimeError('Not implemented in decendent class?')
    def BuildMeForHqMeOobNode(self, oobid): raise RuntimeError('BuildMeForHqMeOobNode not implemented yet in derived class.')
    def BuildTemporaryMeForOob(self, oobid): raise RuntimeError('Not implemented in decendent class?')
    def DestroyTemporaryMeid(self, meid):  raise RuntimeError('Not implemented in decendent class?')
##    def MeIdToTroopTypes(self, meid, fastmove=1): raise 'MeIdToTroopType not implemented yet in derived class.'
##    def MeIdToPredominantTroopType(self, meid, fastmove=1):  raise RuntimeError('Not implemented in decendent class?')
##    def MeIdToTroopTypesAndOffroadAbilities(self, meid, fastmove=1): raise 'MeIdToTroopTypesAndOffroadAbilities not implemented yet in derived class.'
##    def MeIdToTroopTypesAndHQness(self, meid, fastmove=0): raise 'MeIdToTroopTypesAndHQness not implemented yet in derived class.'
    def GetMeCommanderName(self, meid): raise RuntimeError('Not implemented in decendent class?')
    def GetMeCommanderRank(self, meid): raise RuntimeError('Not implemented in decendent class?')
    def GetMeCommanderLeadership(self, meid): raise RuntimeError('Not implemented in decendent class?')
    def GetMeCommanderEfficiency(self, meid): raise RuntimeError('Not implemented in decendent class?')
    def GetMeCommanderAggressiveness(self, meid): raise RuntimeError('Not implemented in decendent class?')
    def GetMeNameForMe(self, meid): raise RuntimeError('Not implemented in decendent class?')
    def GetMeIdForName(self, mename): raise RuntimeError('Not implemented in decendent class?')
    def GetMeInitialReadiness(self, meid): raise RuntimeError('Not implemented in decendent class?')
    def GetMeInitialAmmo(self, meid): raise RuntimeError('Not implemented in decendent class?')
    def GetMeInitialDirection(self, meid): raise RuntimeError('Not implemented in decendent class?')
    def GetMeInitialBasics(self, meid): raise RuntimeError('Not implemented in decendent class?')
    def GetMeInitialFuel(self, meid): raise RuntimeError('Not implemented in decendent class?')
    def GetMeSignals(self, meid): raise RuntimeError('Not implemented in decendent class?')
    def _GetMeCompositePointsValue(self, meid): raise RuntimeError('Not implemented in decendent class?')
    def GetMeCompositeSize(self, meid): raise RuntimeError('Not implemented in decendent class?')
    def GetMeCompositeExperience(self, meid): raise RuntimeError('Not implemented in decendent class?')
    def GetMeCompositeFitness(self, meid): raise RuntimeError('Not implemented in decendent class?')
    def Exists(self, meid): raise RuntimeError('Not implemented in decendent class?')
    def ExistsMappingToOobid(self, oobid): raise RuntimeError('Not implemented in decendent class?')
    def GetSideOfMe(self, meid): raise RuntimeError('Not implemented in decendent class?')
    def OobIdToMeId(self, role): raise RuntimeError('Not implemented in decendent class?')
    def OobIdToMeIdAnywhere(self, oobid): raise RuntimeError('Not implemented in decendent class?')

    def GetRecursiveListOfOobidsExcludingMes(self, oobid): raise RuntimeError('Not implemented in decendent class?')
    def GetMeRecursiveListOfOobidsExcludingMesAndDead(self, meid): raise RuntimeError('Not implemented in decendent class?')
    def GetMeRecursiveListOfOobidsExcludingMes(self, meid): raise RuntimeError('Not implemented in decendent class?')
    def GetRecursiveListOfOobidsIncludingMes(self, meid): raise RuntimeError('Not implemented in decendent class?')
    def GetMeRecursiveListOfOobidsIncludingMesAndAlive(self, meid): raise RuntimeError('Not implemented in decendent class?')

    def GetMeCompositeNumberofmen(self, meid): raise RuntimeError('Not implemented in decendent class?')
    def GetNumberOfMenInMe(self, meid): raise RuntimeError('Not implemented in decendent class?')
    def GetNumberOfAliveMenInMeIncludingMe(self, meid): raise RuntimeError('Not implemented in decendent class?')
    def GetMeCompositeNumberofVEHICLES(self, meid): raise RuntimeError('Not implemented in decendent class?')
    def GetMeCompositeNumberofARMOR(self, meid): raise RuntimeError('Not implemented in decendent class?')
    def GetMeCompositeNumberofGUNS(self, meid): raise RuntimeError('Not implemented in decendent class?')
    def GetMeMetatypeSizes(self, oobidlist): raise RuntimeError('Not implemented in decendent class?')
    def RolesRelevantToPiece(self, meid): raise RuntimeError('Not implemented in decendent class?')
    def LoadFromLists(self, meid): raise RuntimeError('Not implemented in decendent class?')
    def GetInfoForMgmClientDisplay(self, meid): raise RuntimeError('Not implemented in decendent class?')

    def IsDead(self, meid): raise RuntimeError('Not implemented in decendent class?')



####################################### MeToOobMappings ###########


class MeToOobMappingsCommon_ImplementationUsingTwoTreesAndDicts(MeToOobMappingsBase):

    def __init__(self, oob):
        self.oob = oob
        self.melist = []
        self.Build()

    def RolesRelevantToPiece(self, meid):
        allroles = self.oob.FindAllRoles()
        oldstylepiece = lambda piecename: len(piecename) == 2
        if oldstylepiece(meid):   # it seems that old style pieces are relevant to all roles - even enemy ones!!!
            return allroles

        # Could move this next few lines into an oob function called RolesRelevantToOobid(oobid)
        hqoobid = self.oob.RankingHqInMe(meid)
        ancestoroobids = self.oob.FindAncestors(hqoobid)
        assert 'default' not in ancestoroobids
        return [ oobid for oobid in ancestoroobids+[hqoobid] if oobid in allroles ]

    def GetAllMeIds(self):
        return self.melist

    def Exists(self, meid):
        return meid in self.GetAllMeIds()
    def ExistsMappingToOobid(self, oobid):
        raise RuntimeError('Not implemented in decendent class?')

    def Build(self):
        del self.melist[0:]
        self._PreBuildInit()

        for oobtree in (self.oob.oobtreeAxis, self.oob.oobtreeAllies):
            for oobid in list(oobtree.nodes.keys()):
                if 'ME' in oobtree.nodes[oobid] and oobtree.nodes[oobid]['ME']:
                    self.melist.append(self.BuildMeForHqMeOobNode(oobid))
    def BuildMeForHqMeOobNode(self, oobid):
        raise RuntimeError('BuildMeForHqMeOobNode not implemented yet in derived class.')

    def BuildTemporaryMeForOob(self, oobid):
        raise RuntimeError('Not implemented in decendent class?')
    def DestroyTemporaryMeid(self, meid):
        raise RuntimeError('Not implemented in decendent class?')


    def GetSideOfMe(self, meid):
        # TODO: Change battle and gamestatus to use side in HAS.
        #       Only hasmanager will then need this function.
        rankingoobid = self.oob.RankingHqInMe(meid)
        side = self.oob.DetermineSideFromOobNodeId(rankingoobid)
        return side

    def GetNationPrefixOfPiece(self, meid):
        """
        Only used for version2.0 scenarios with new trooptype system.
        For the moment get the side and assume G or R
        Later look up 'nationlity field' of the ranking oobid
        """
        assert 0, "Deprecated. - see MeImageNamer.py"
        side = self.GetSideOfMe(meid)
        if side == 'axis':
            return 'G'
        else:
            return 'R'

    def _GetSingleOobNodeAttribute(self, oobid, key, default):
        oobtree = self.oob.DetermineWhichTreeFromOobNodeId(oobid)
        nodedict = oobtree.nodes[oobid]
        if key not in nodedict:
            return default
        return nodedict[key]

    def GetMeCommanderName(self, meid):
        rankingoobid = self.oob.RankingHqInMe(meid)
        return self.oob.GetOfficerName(rankingoobid)
    def GetMeCommanderRank(self, meid):
        rankingoobid = self.oob.RankingHqInMe(meid)
        return self.oob.GetOfficerRank(rankingoobid)

    def GetMeCommanderLeadership(self, meid):
        rankingoobid = self.oob.RankingHqInMe(meid)
        print("BattleGen: rankingoobid for leadership = ", rankingoobid)
        return self.oob.GetOfficerLeadership(rankingoobid)
    def GetMeCommanderEfficiency(self, meid):
        rankingoobid = self.oob.RankingHqInMe(meid)
        return self.oob.GetOfficerEfficiency(rankingoobid)
    def GetMeCommanderAggressiveness(self, meid):
        rankingoobid = self.oob.RankingHqInMe(meid)
        return self.oob.GetOfficerAggressiveness(rankingoobid)

    def GetInfoForMgmClientDisplay(self, meid):
        rankingoobid = self.oob.RankingHqInMe(meid)
        return {
            'MeCommanderName': self.oob.GetOfficerName(rankingoobid),
            'MeCommanderRank': self.oob.GetOfficerRank(rankingoobid),
            'MeCommanderLeadership': self.oob.GetOfficerLeadership(rankingoobid),
            'MeCommanderEfficiency': self.oob.GetOfficerEfficiency(rankingoobid),
            'MeCommanderAggressiveness': self.oob.GetOfficerAggressiveness(rankingoobid),
            'MeSignals': self.oob.GetSignals(rankingoobid)
            }

    def GetMeNameForMe(self, meid):
        rankingoobid = self.oob.RankingHqInMe(meid)
        return self.oob.GetInitialMeName(rankingoobid)
    def GetMeIdForName(self, mename):
        for meid in self.melist:
            if self.GetMeNameForMe(meid) == mename:
                return meid
        return None


    def GetMeInitialReadiness(self, meid):
        rankingoobid = self.oob.RankingHqInMe(meid)
        return self.oob.GetInitialMeReadiness(rankingoobid)
    def GetMeInitialAmmo(self, meid):
        rankingoobid = self.oob.RankingHqInMe(meid)
        return self.oob.GetSupplyAmmo(rankingoobid)
    def GetMeInitialDirection(self, meid):
        rankingoobid = self.oob.RankingHqInMe(meid)
        return self.oob.GetInitialDirection(rankingoobid)
    def GetMeInitialBasics(self, meid):
        rankingoobid = self.oob.RankingHqInMe(meid)
        return self.oob.GetSupplyBasics(rankingoobid)
    def GetMeInitialFuel(self, meid):
        rankingoobid = self.oob.RankingHqInMe(meid)
        return self.oob.GetSupplyFuel(rankingoobid)


    def GetMeSignals(self, meid):
        rankingoobid = self.oob.RankingHqInMe(meid)
        return self.oob.GetSignals(rankingoobid)

    def GetRecursiveListOfOobidsExcludingMes(self, oobid):
        result = []
        if not self.oob.IsMe(oobid):
            result.append(oobid)
        children = self.oob.FindChildren(oobid)
        for childoobid in children:
            if not self.oob.IsMe(oobid):
                result += self.GetRecursiveListOfOobidsExcludingMes(childoobid)
        return result
    def GetMeRecursiveListOfOobidsExcludingMesAndDead(self, meid):
        oobidsexcludingmes = self.GetMeRecursiveListOfOobidsExcludingMes(meid)
        return [ oobid for oobid in oobidsexcludingmes if not self.oob.IsDead(oobid) ]

    def GetMeRecursiveListOfOobidsExcludingMes(self, meid):
        result = []
        for oobid in self.MeIdToListOfOobIds(meid):

            if oobid == self.oob.RankingHqInMe(meid):
                assert self.oob.IsMe(oobid)
                result.append(oobid)
                continue # don't look at its children cos already have 1st level children returned to us by RankingHqInMe function.
            elif not self.oob.IsMe(oobid):
                result.append(oobid)
            else:
                raise RuntimeError('Do not know how to recurse into me %s at oobid %s' % (meid, oobid))

            children = self.oob.FindChildren(oobid)
            if children:
                for childoobid in children:
                    result += self.GetRecursiveListOfOobidsExcludingMes(childoobid)
        return result

##    def GetMeRecursiveListOfOobidsExcludingMes(self, meid):
##        result = []
##        for oobid in self.MeIdToListOfOobIds(meid):
##            children = self.oob.FindChildren(oobid)
##            if oobid == self.oob.RankingHqInMe(meid):
##                assert self.oob.IsMe(oobid)
##                result.append(oobid)
##            elif not children and not self.oob.IsMe(oobid):
##                result.append(oobid)
##            elif children:
##                for childoobid in children:
##                    result += self.GetRecursiveListOfOobidsExcludingMes(childoobid)
##            else:
##                raise RuntimeError, 'Do not know how to recurse into me %s at oobid %s' % (meid, oobid)
##        return result


    def GetMeRecursiveListOfOobidsIncludingMes(self, meid):
        result = []
        for oobid in self.MeIdToListOfOobIds(meid):

            if oobid == self.oob.RankingHqInMe(meid):
                assert self.oob.IsMe(oobid)
                result.append(oobid)
                continue # don't look at its children cos already have 1st level children returned to us by RankingHqInMe function.
            elif not self.oob.IsMe(oobid):
                result.append(oobid)
            else:
                raise RuntimeError('Do not know how to recurse into me %s at oobid %s' % (meid, oobid))

            children = self.oob.FindChildren(oobid)
            if children:
                for childoobid in children:
                    result += self.GetRecursiveListOfOobidsIncludingMes(childoobid)
        return result

    def GetRecursiveListOfOobidsIncludingMes(self, oobid):
        result = []
        result.append(oobid)
        children = self.oob.FindChildren(oobid)
        for childoobid in children:
            if not self.oob.IsMe(oobid):
                result += self.GetRecursiveListOfOobidsIncludingMes(childoobid)
        return result

    def GetMeRecursiveListOfOobidsIncludingMesAndAlive(self, meid):
        oobidsincludingmes = self.GetMeRecursiveListOfOobidsIncludingMes(meid)
        return [ oobid for oobid in oobidsincludingmes if not self.oob.IsDead(oobid) ]

    def GetNumberOfMenInMe(self, meid):
        result = 0
        # seems to take into account the dead as strength is 0 for dead oobs
        for oobid in self.GetMeRecursiveListOfOobidsExcludingMes(meid):
            men = self.oob.GetStrength(oobid)[0]
            result += men
        return result

    def GetNumberOfAliveMenInMeIncludingMe(self, meid):
        result = 0
        for oobid in self.GetMeRecursiveListOfOobidsIncludingMesAndAlive(meid):
            men = self.oob.GetStrength(oobid)[0]
            result += men
        return result


    def _GetMeCompositePointsValue(self, meid):
        oobidlist = self.GetMeRecursiveListOfOobidsExcludingMesAndDead(meid)
        return self._AddUpPointsForOobids(oobidlist)

    def _GetMeCompositePointsValue_ORI(self, meid):
        oobidlist = self.MeIdToListOfOobIds(meid)
        return self._AddUpPointsForOobids(oobidlist)

    def _AddUpPointsForOobids(self, oobidlist):
        result = 0
        for oobid in oobidlist:
            val = self._GetSingleOobNodeAttribute(oobid, 'points', 0)
            result += val
        return result

    def GetMeMetatypeSizes(self, oobidlist):
        # RETURNS a dict of metatypes with size of each as value.
        info = {'ARMOR':0,'ARTILLERY':0,'INFANTRY':0,'VEHICLE':0,'HQ':0}

        # Prepare totals
        for oobid in oobidlist:
            fulltrooptype = self.oob.GetTroopType(oobid)
            maintrooptype, subtrooptype = self.oob.trooptypesmgr.ExtractTroopAndSubTroopTypes(fulltrooptype)

            metatrooptype = self.oob.trooptypesmgr.MetaTroopTypeFromMainTroopType(maintrooptype)
            if metatrooptype == 'INFANTRY' or metatrooptype == 'HQ':
                nummen = self.oob.GetNumberOfMen(oobid)
                info[metatrooptype] += nummen
            else:
                info[metatrooptype] += 1

        # Final pass convert entries which convert total into entries storing sizes
        meta = 'ARMOR'
        # (1-5)=1 (6-20)=2 (21+)=3
        if info[meta] <= 5:
            info[meta] = 1
        elif info[meta] <= 20:
            info[meta] = 2
        else:
            info[meta] = 3

        meta = 'ARTILLERY'
        # (1-9)=1, (10-18) =2, (19+)=3
##        info[meta] = self.GetMeCompositeNumberofGUNS(meid)
        if info[meta] <= 9:
            info[meta] = 1
        elif info[meta] <= 18:
            info[meta] = 2
        else:
            info[meta] = 3

        meta = 'INFANTRY'
        # (1-50)=1  (51-200)=2  (201+)=3
##        total = self.GetMeCompositeNumberofmen(meid)
        if info[meta] <= 50:
            info[meta] = 1
        elif info[meta] <= 200:
            info[meta] = 2
        else:
            info[meta] = 3

        meta = 'VEHICLE'
        # (1-7)=1, (8,30)=2 (31+)=3
##        total = self.GetMeCompositeNumberofVEHICLES(meid)
        if info[meta] <= 7:
            info[meta] = 1
        elif info[meta] <= 30:
            info[meta] = 2
        else:
            info[meta] = 3

        meta = 'HQ'
        # (1-50)=1, (51+)=2
##        total = self.GetMeCompositeNumberofmen(meid)
        if info[meta] <= 50:
            info[meta] = 1
        else:
            info[meta] = 2

        return info

    def GetMeCompositeSize(self, meid):
        """
        We don't use pointValue or pointsSize for this anymore.
        """
        predominantmetatrooptype = self.oob.trooptypesmgr.MeidToPredominantMetaTroopType(meid)

## DEBUG
##        oobidlist = self.GetMeRecursiveListOfOobidsExcludingMes(meid)
##        print '-'*20, 'DEAD FOR', meid
##        for oobid in oobidlist:
##            print self.oob.IsDead(oobid), oobid
##        print '-'*20
##        dead = [ oobid for oobid in oobidlist if self.oob.IsDead(oobid) ]
##        if dead:
##            print 'there are some dead?', dead
## DEBUG #######

        # INCLUDE THE DEAD
        #oobidlist = self.GetMeRecursiveListOfOobidsExcludingMes(meid)

        # SKIP THE DEAD
        oobidlist = self.GetMeRecursiveListOfOobidsExcludingMesAndDead(meid)
        if not oobidlist: # Everyone is dead
            return 0

        scoresdict = self.GetMeMetatypeSizes(oobidlist)
        return scoresdict[predominantmetatrooptype]

##    def GetMeCompositeSize(self, meid):
##        """
##        We don't use pointValue or pointsSize for this anymore.
##        """
##        trooptype_subtype = self.oob.trooptypesmgr.MeIdToPredominantTroopType(meid)
##        trooptype, troopsubtype = self.oob.trooptypesmgr.ExtractTroopAndSubTroopTypes(trooptype_subtype)
##        predominantmetatrooptype = self.oob.trooptypesmgr.MetaTroopTypeFromMainTroopType(trooptype)
##
##        if predominantmetatrooptype == 'ARMOR':
##            # (1-5)=1 (6-20)=2 (21+)=3
##            total = self.GetMeCompositeNumberofARMOR(meid)
##            if total <= 5:
##                return 1
##            elif total <= 20:
##                return 2
##            else:
##                return 3
##        elif predominantmetatrooptype == 'ARTILLERY':
##            # (1-9)=1, (10-18) =2, (19+)=3
##            total = self.GetMeCompositeNumberofGUNS(meid)
##            if total <= 9:
##                return 1
##            elif total <= 18:
##                return 2
##            else:
##                return 3
##        elif predominantmetatrooptype == 'INFANTRY':
##            # (1-50)=1  (51-200)=2  (201+)=3
##            total = self.GetMeCompositeNumberofmen(meid)
##            if total <= 50:
##                return 1
##            elif total <= 200:
##                return 2
##            else:
##                return 3
##        elif predominantmetatrooptype == 'VEHICLE':
##            # (1-7)=1, (8,30)=2 (31+)=3
##            total = self.GetMeCompositeNumberofVEHICLES(meid)
##            if total <= 7:
##                return 1
##            elif total <= 30:
##                return 2
##            else:
##                return 3
##        elif predominantmetatrooptype == 'HQ':
##            # (1-50)=1, (51+)=2
##            total = self.GetMeCompositeNumberofmen(meid)
##            if total <= 50:
##                return 1
##            else:
##                return 2
##        else:
##            raise RuntimeError, 'Unknown predominant trooptype "%s" for meid %s.' % (predominanttrooptype, meid)

##    def GetMeCompositeSize(self, meid):
##        # Maps composite value onto a number 0-4
##        value = self._GetMeCompositePointsValue(meid)
##        if value < 100:
##            return 1
##        elif value < 300:
##            return 2
##        elif value < 500:
##            return 3
##        elif value < 1000:
##            return 4
##        else:
##            return 5
##            #raise 'No ME should be greater than 1000 points'
##    def GetMeCompositeSizeAsString(self, meid):
##        size = self.GetMeCompositeSize(meid)
##        if size == 1:
##            return 'Platoon'
##        elif size == 2:
##            return 'Company'
##        elif size == 3:
##            return 'Battalion'
##        elif size == 4:
##            return 'Regiment'
##        else:
##            raise 'No ME should have size greater than 4'


##    def _GetMeCompositeFitness(self, meid):
##        oobidlist = self.MeIdToListOfOobIds(meid)
##        result = 0
##        for oobid in oobidlist:
##            val = self.oob.GetFitness(oobid)
##            result += val
##        return result
##    def GetMeCompositeFitness(self, meid):
##        # Maps composite value onto a number 0-4
##        value = self._GetMeCompositeFitness(meid)
##        if value < 100:
##            return 1
##        elif value < 300:
##            return 2
##        elif value < 500:
##            return 3
##        elif value < 1000:
##            return 4
##        else:
##            raise 'No ME should be greater than 1000 points'
##    def GetMeCompositeFitnessAsString(self, meid):
##        size = self.GetMeCompositeFitness(meid)
##        if size == 1:
##            return 'Platoon'
##        elif size == 2:
##            return 'Company'
##        elif size == 3:
##            return 'Battalion'
##        elif size == 4:
##            return 'Regiment'
##        else:
##            raise 'No ME should have size greater than 4'

    def _GetMeCompositeExperienceRawTotal(self, meid):
        # this is used by some unit tests so we keep it around...
        oobidlist = self.GetMeRecursiveListOfOobidsExcludingMesAndDead(meid)
        result = 0
        for oobid in oobidlist:
            oobexperience = self.oob.GetExperience(oobid)
            result += oobexperience
        return result

    def GetMeCompositeExperience(self, meid):
        return self._AddUpAndAverageCompositeInfo(meid, self.oob.GetExperience)

    def _AddUpAndAverageCompositeInfo(self, meid, lambdafunction):
        # this is the preferred way of adding up composite values.
        oobidlist = self.GetMeRecursiveListOfOobidsExcludingMesAndDead(meid)
        if len(oobidlist) == 0:
            return 0

        result = 0
        for oobid in oobidlist:
##            if meid == 'me_1' and lambdafunction.__name__=='GetExperience':
##                print '%s experience is %s'%(oobid, lambdafunction(oobid))
            result += lambdafunction(oobid)
##        if meid == 'me_1' and lambdafunction.__name__=='GetExperience':
##            print "result", result, "oobidlist", oobidlist
        return result/len(oobidlist)

    def GetMeCompositeFitness(self, meid):
        return self._AddUpAndAverageCompositeInfo(meid, self.oob.GetFitness)

##    def GetMeCompositeNumberofmen(self, meid):
##        #print 'GetMeCompositeNumberofmen--------------------------'
##        total = 0
##        oobidlist = self.GetMeRecursiveListOfOobidsExcludingMes(meid)
##        for oobid in oobidlist:
##            #print total, self.oob.GetOobName(oobid), self.oob.GetNumberOfMen(oobid), oobid
##            total += self.oob.GetNumberOfMen(oobid)
##        #print total, 'DONE GetMeCompositeNumberofmen--------------------------'
##        return total

##    def _GetMeCompositeNumberofMetaTroopType(self, meid, metatrooptype):
##        """
##        Counts the number of 'metatrooptype' oob's of the type
##                 'ARTILLERY' VEHICLE' or 'ARMOR'
##        in the meid.
##        Assumes you are never wanting to count the # of hq's in the meid.
##        Assumes that if there is only 1 hq in an me then there is 0 count of the
##         metatype you are searching for. viz.
##                 'ARTILLERY' VEHICLE' or 'ARMOR'
##        """
##        assert metatrooptype <> 'HQ'
##
##        total = 0
##        oobidlist = self.GetMeRecursiveListOfOobidsExcludingMes(meid)
##
##        if len(oobidlist) == 1:
##            """
##            The metatrooptype priority list (in descending priority) of
##              'ARMOR', 'ARTILLERY', 'INFANTRY', 'VEHICLE', 'HQ'
##            puts HQ's at the bottom.
##            However if an ME contains only one unit, then that
##            unit must be a HQ and so even if it is armor trooptype,
##            its metatrooptype for image display purposes is actually HQ.
##            """
##            assert self.oob.IsHq(oobidlist[0]), 'Any lone me with one unit in it must be a HQ'
##            return 0
##
##        for oobid in oobidlist:
##            trooptype_subtype = self.oob.GetTroopType(oobid)
##            trooptype, troopsubtype = self.oob.trooptypesmgr.ExtractTroopAndSubTroopTypes(trooptype_subtype)
##
##            if metatrooptype == self.oob.trooptypesmgr.MetaTroopTypeFromMainTroopType(trooptype):
##                total += 1
##        return total
##
##    def GetMeCompositeNumberofGUNS(self, meid):
##        return self._GetMeCompositeNumberofMetaTroopType(meid, 'ARTILLERY')
##    def GetMeCompositeNumberofVEHICLES(self, meid):
##        return self._GetMeCompositeNumberofMetaTroopType(meid, 'VEHICLE')
##    def GetMeCompositeNumberofARMOR(self, meid):
##        return self._GetMeCompositeNumberofMetaTroopType(meid, 'ARMOR')

    def OobIdToMeIdAnywhere(self, oobid):
        meid = self.OobIdToMeId(oobid)
        while not meid:
            oobid = self.oob.GetParent(oobid)
            meid = self.OobIdToMeId(oobid)
        if meid:
            return meid
        else:
            return None
            #raise RuntimeError, 'Cannot find an ME containing role ' + role

    def IsDead(self, meid):
        """
        If all oobids in it are dead, then the ME is dead.
        It there are some oobids that we don't know the strength of
        """
        notsure = ''
        oobidlist = self.GetMeRecursiveListOfOobidsExcludingMes(meid)
        for oobid in oobidlist:
            if self.oob.GetStrength(oobid) is None:
                notsure = '??'
            # if anyone is alive return straight away
            elif not self.oob.IsDead(oobid):
                return 0

        return notsure or 1



class RelationshipManagerPersistent(RelationshipManager):
    def __init__(self):
        RelationshipManager.__init__(self)

    def __repr__(self):
        return pprint.pformat(self.Relationships)

    def LoadFromStr(self, str):
        self.Relationships = eval(str)

    def LoadFromList(self, L):
        self.Relationships = L



class MeToOobMappings_NEWSTYLE(MeToOobMappingsCommon_ImplementationUsingTwoTreesAndDicts):

    def __init__(self, oob):
        self.relations = RelationshipManagerPersistent()
        self.nextid = 0
        MeToOobMappingsCommon_ImplementationUsingTwoTreesAndDicts.__init__(self, oob)

        self.pp = pprint.PrettyPrinter(indent = 4,width=10)
        #self.myrepr = repr
        self.myrepr = self.pp.pformat

    def _PreBuildInit(self):
        self.nextid = 0
        self.relations.Clear()

    def LoadFromStr(self, str):
        self.relations.LoadFromStr(str)

    def LoadFromLists(self, melist, relations):
        self.relations.LoadFromList(relations)
        self.melist = melist

    def __repr__(self):
        return repr(self.relations)


    def _AllocateMeId(self):
        self.nextid += 1
        return 'me_' + repr(self.nextid)
    def BuildMeForHqMeOobNode(self, oobid):   # overriden
        meid = self._AllocateMeId()
        firstlevelchildrenoobids = self.oob.FindChildren(oobid)
        def AllChildrenAreNotMes():
            for childoobid in firstlevelchildrenoobids:
                if self.oob.IsMe(childoobid):
                    return 0
            return 1
        if AllChildrenAreNotMes():
            self.relations.AddRelationship(meid, oobid, 'G') # Group
        else:
            self.relations.AddRelationship(meid, oobid, 'S') # Single
            for childoobid in firstlevelchildrenoobids:
                if self.oob.IsMe(childoobid):
                    continue     # ignore me children
                if self.oob.IsHq(childoobid):
                    """
                    WARNING: we are assuming that the G will point to an oob which doesn't have any ME's in it.
                    This may not be the case. Should write a unit test.  Perhaps solution is to recursively call
                     the above code somehow so that we are checking for AllChildrenAreNotMes()
                    """
                    self.relations.AddRelationship(meid, childoobid, 'G') # Group
                else:
                    self.relations.AddRelationship(meid, childoobid, 'S') # Single
        return meid

    def _DumpMeRelations(self):
        print('------- _DumpMeRelations ---------')
        for r in self.relations.Relationships:
            oobname = self.oob.GetOobName(r[1])
            print(r, oobname)
        print('----------------------------------')
        print('ALL MEIDs', self.GetAllMeIds())
        for meid in self.GetAllMeIds():
            print('%s %s' % (meid, self.GetMeNameForMe(meid)), '    MeIdToListOfOobIds')
            oobids = self.MeIdToListOfOobIds(meid)
            for oobid in oobids:
                print('   oobid %s %s HQ=%d ME=%d' % (oobid, self.oob.GetOobName(oobid), self.oob.IsHq(oobid), self.oob.IsMe(oobid)))
        print('++++++++++++++++++++++++++++++++++')

        print('ALL MEIDs again, as MeIdToOobIds')
        for meid in self.GetAllMeIds():
            print('%s %s' % (meid, self.GetMeNameForMe(meid)))
            oobids = self.MeIdToOobIds(meid)
            for oobid in oobids:
                print('   oobid %s %s HQ=%d ME=%d' % (oobid, self.oob.GetOobName(oobid), self.oob.IsHq(oobid), self.oob.IsMe(oobid)))
        print('==================================')

    def ExistsMappingToOobid(self, oobid):
        objs = self.relations.FindObjects(From=None, To=oobid, RelId='S')
        if objs:
            return 1
        return 0

    def BuildTemporaryMeForOob(self, oobid):
        meid = 'signalmeid'
        self.melist.append(meid)
        self.relations.AddRelationship(meid, oobid, 'S')
        return meid
    def DestroyTemporaryMeid(self, meid):
        # remove the meid
        self.melist.remove(meid)
        # remove the relationship
        tempoobidobjs = self.relations.FindObjects(From=meid, To=None, RelId='S')
        assert len(tempoobidobjs) == 1, 'should only be one temp oobid to clean up'
        oobid = tempoobidobjs[0]
        self.relations.RemoveRelationships(meid, oobid, 'S')


##    def MeIdToTroopTypesAndHQness(self, meid, fastmove=0):  # FASTMOVE not used?
##        oobidlist = self.GetMeRecursiveListOfOobidsExcludingMes(meid)
##        resultlist = []
##        for oobid in oobidlist:
##            trooptype = self.oob.GetTroopType(oobid)
####            trooptype = self._GetSingleOobNodeAttribute(oobid, 'trooptype', 0)
##            ishq = self.oob.IsHq(oobid)
##            resultlist.append( (trooptype, ishq) )
##        return resultlist

    def MeIdToOobIds(self, meid):
        assert meid, 'MeIdToOobIds: Cannot have meid of None'
        g = self.relations.FindObjects(From = meid, To = None, RelId = 'G')
        s = self.relations.FindObjects(From = meid, To = None, RelId = 'S')
        result = g + s
        return result

    def MeIdToListOfOobIds(self, meid):
        assert meid, 'MeIdToListOfOobIds: Cannot have meid of None'
        s = self.relations.FindObjects(From = meid, To = None, RelId = 'S')
        # s are guaranteed to be non me's
        g = self.relations.FindObjects(From = meid, To = None, RelId = 'G')

        if g and not s and len(g) == 1:
            oobid = g[0]
            result = self.oob.FindChildren(oobid)
            result.append(oobid)
            return result
        else:
            return self.MeIdToOobIds(meid)

    def OobIdToMeId(self, role):
        g = self.relations.FindObject(From = None, To = role, RelId = 'G')
        s = self.relations.FindObject(From = None, To = role, RelId = 'S')
        if g:
            return g
        if s:
            return s
        return None


    def MeIdToTroopTypes(self, meid, fastmove=1):      # overridden     # FASTMOVE not used?
        print('WARNING MeIdToTroopTypes (newstyle oob) being called')
##        oobidlist = self.MeIdToOobIds(meid)  # this returns only the HQ for a G relation - and we want more...
##        oobidlist = self.MeIdToListOfOobIds(meid)  # this is non recursive
        oobidlist = self.GetMeRecursiveListOfOobidsExcludingMesAndDead(meid)

        trooptypelist = []
        for oobid in oobidlist:
            trooptype = self._GetSingleOobNodeAttribute(oobid, 'trooptype', 0)
            trooptypelist.append(trooptype)
        return trooptypelist

##    def MeIdToTroopTypesAndOffroadAbilities(self, meid, fastmove=1):  # FASTMOVE not used?
##        # TODO this might be better as a common algorithm
##        #  as long as we don't use _GetSingleOobNodeAttribute but instead use
##        #  calls to oob.Get..... which have new & old style sub flavors.
####        oobidlist = self.MeIdToListOfOobIds(meid)
##        oobidlist = self.GetMeRecursiveListOfOobidsExcludingMes(meid)
##        resultlist = []
##        for oobid in oobidlist:
##            trooptype = self._GetSingleOobNodeAttribute(oobid, 'trooptype', 0)
##            offroadability = self._GetSingleOobNodeAttribute(oobid, 'offroadability', 1)
##            resultlist.append( (trooptype, offroadability) )
##        return resultlist

    # def MeIdToTroopTypesAndHQness(self, meid, fastmove=0):  # FASTMOVE not used?
    #  implemented in common.


class MeToOobMappings_OLDSTYLE(MeToOobMappingsCommon_ImplementationUsingTwoTreesAndDicts):
    def __init__(self, oob):
        MeToOobMappingsCommon_ImplementationUsingTwoTreesAndDicts.__init__(self, oob)
        self.PieceTypeToTroopTypes = {
            'AD': [ 'Infantry' ],
            'AR': [ 'Infantry' ],
            'AT': [ 'Armor_Churchhill' ],
            'AB': [ 'Infantry' ],
            'AC': [ 'Infantry' ],
            'AP': [ 'Infantry' ],
            'GD': [ 'Infantry' ],
            'GR': [ 'Infantry' ],
            'GT': [ 'Armor_Panzer' ],
            'GB': [ 'Infantry' ],
            'GC': [ 'Infantry' ],
            'GP': [ 'Infantry' ]
        }

    def _DumpMeRelations(self):
        print('------- _DumpMeRelations ---------')
        print("we do not dump me relations in old style oob's")

##    def _OldStyleMeidtotrooptypefunction(self, meid):
##        oldtype = meid[0:2]
##        if oldtype == 'AR':
##            return 'Ski'
##        elif  oldtype == 'AD':
##            return 'Infantry'
##        elif  oldtype == 'AT':
##            return 'Armor_Panzer'
##        elif  oldtype == 'AB':
##            return 'Cavalry'
##        else:
##            return 'Infantry'

    def _PreBuildInit(self):
        pass

    def BuildMeForHqMeOobNode(self, oobid):             # overridden
        return oobid    # the oobid IS the meid

    def ExistsMappingToOobid(self, oobid):
        return 0
    def BuildTemporaryMeForOob(self, oobid):
        return ''
    def DestroyTemporaryMeid(self, meid):
        pass

    def MeIdToOobIds(self, meid):
        oobid = meid
        return (oobid,)
    def MeIdToListOfOobIds(self, meid):
        return self.MeIdToOobIds(meid)
    def OobIdToMeId(self, role):
        meid = role
        return meid

    def __PieceIdToPieceType(self, meid):
        # OLD STYLE - supports MeIdToTroopType()
        oobid = meid
        return oobid[0: 2]

    def __PieceTypeToTroopType(self, piecetype):
        # OLD STYLE - supports MeIdToTroopType()
        """
        The trooplist currently has one item and for the moment we
        take the first troop type...later we find the slowest troop type etc.
        HOWEVER this future solution is flawed since who is in each troop group will be
        totally dependant on scenario oobtrees.
        """
        trooplist = self.PieceTypeToTroopTypes[piecetype]
        return trooplist[0]

    def MeIdToTroopTypes(self, meid, fastmove=1):      # overridden
        print('WARNING MeIdToTroopTypes (oldstyle oob) being called')
        if self.oob.IsMounted(meid) and fastmove:
            trooptype = 'Truck_Basic'
        else:
            piecetype = self.__PieceIdToPieceType(meid)
            trooptype = self.__PieceTypeToTroopType(piecetype)
        return [trooptype]

##    def MeIdToTroopTypesAndOffroadAbilities(self, meid, fastmove=1):
##        resultlist = self.MeIdToTroopTypes(meid, fastmove)       ############?????????????????????
##        fakeoffroadability = 1
##        trooptype = resultlist[0]
##        return [ (trooptype, fakeoffroadability) ]

##    def MeIdToTroopTypesAndHQness(self, meid, fastmove=0):  # FASTMOVE not used?
##        resultlist = self.MeIdToTroopTypes(meid, fastmove)
##        fakeHqness = 1
##        trooptype = resultlist[0]
##        return [ (trooptype, fakeHqness) ]

    def GetMeCompositeSize(self, meid):
        return 1   # size is 1..4  Hard wire to 1 since don't care for old style.



# Comes from current storyline playhead position
##    def GetMeLocation(self, meid):
##        return (0,0)


# Moved to terrain manager?
##    def GetMeCompositeSpeed(self, meid):
##        return ''
##    def GetMeCompositeTroopType(self, meid):
##        return ''
##    def GetMeTransportSpeed(self, meid):
##        return 0
##    def GetMeCompositeTransportType(self, meid):
##        return ''


##    def GetMeReadiness(self, meid):
##        return 0
##    def GetMeCompositeExperience(self, meid):
##        return ''
##    def GetMeCompositeFitness(self, meid):
##        return ''
##    def GetMeRankingHqLeadership(self, meid):
##        return ''
##    def GetMeRankingHqEfficiency(self, meid):
##        return ''
##    def GetMeRankingHqAggressiveness(self, meid):
##        return ''
##    def GetMeRankingHqSignalsOrdersType(self, meid):
##        return ''
##    def GetMeRankingHqSignalsReportsType(self, meid):
##        return ''
##    def GetMeRankingHqSignalsOrdersState(self, meid):
##        return ''
##    def GetMeRankingHqSignalsReportsState(self, meid):
##        return ''
##    def GetMeCompositeSupplyBasics(self, meid):
##        return ''
##    def GetMeCompositeSupplyFuel(self, meid):
##        return ''
##    def GetMeCompositeSupplyAmmo(self, meid):
##        return ''



######################################################  Oob ######

class OobConversions:
    def ConvertMeCompositePointsSizeToString(self, meid, size):
        if size == 1:
            return 'Platoon'
        elif size == 2:
            return 'Company'
        elif size == 3:
            return 'Battalion'
        elif size == 4:
            return 'Regiment'
        else:
            raise RuntimeError('No ME should have size greater than 4')

    def ConvertExperienceToString(self, experience):
        if experience < 0:
            raise RuntimeError('No such experience %d' % (experience,))
        elif experience <= 20:
            return 'Conscript'
        elif experience <= 40:
            return 'Green'
        elif experience <= 60:
            return 'Regular'
        elif experience <= 80:
            return 'Veteran'
        elif experience <= 95:
            return 'Crack'
        elif experience <= 100:
            return 'Elite'
        else:
            raise RuntimeError('No such experience %d' % (experience,))

    def ConvertExperienceStringToExperience(self, experiencestring):
        if experiencestring == 'Conscript':
            return 20
        elif experiencestring == 'Green':
            return 40
        elif experiencestring == 'Regular':
            return 60
        elif experiencestring == 'Veteran':
            return 80
        elif experiencestring == 'Crack':
            return 95
        elif experiencestring == 'Elite':
            return 100
        else:
            raise RuntimeError('No such experience %s' % (experiencestring,))


    def ConvertFitnessToString(self, fitness):
        if fitness < 0:
            raise RuntimeError('No such fitness %d' % (fitness,))
        elif fitness <= 30:
            return 'Unfit'
        elif fitness <= 70:
            return 'Weakened'
        elif fitness <= 100:
            return 'Fit'
        else:
            raise RuntimeError('No such fitness %d' % (fitness,))
    def ConvertFitnessStringToFitness(self, fitnessstring):
        if fitnessstring == 'Unfit':
            return 30
        elif fitnessstring == 'Weakened':
            return 70
        elif fitnessstring == 'Fit':
            return 100
        else:
            raise RuntimeError('No such fitness %s' % (fitnessstring,))

    def ConvertReadinessToString(self, readiness):
        if readiness < 0:
            raise RuntimeError('No such readiness %d' % (readiness,))
        elif readiness <= 20:
            return 'Rabble'
        elif readiness <= 40:
            return 'Exhausted'
        elif readiness <= 60:
            return 'Tired'
        elif readiness <= 75:
            return 'Tiring'
        elif readiness <= 90:
            return 'Ready'
        elif readiness <= 100:
            return 'Rested'
        else:
            raise RuntimeError('No such fitness %d' % (readiness,))
    def ConvertReadinessStringToReadiness(self, readinessstring):
        if readinessstring == 'Rabble':
            return 20
        elif readinessstring == 'Exhausted':
            return 40
        elif readinessstring == 'Tired':
            return 60
        elif readinessstring == 'Tiring':
            return 75
        elif readinessstring == 'Ready':
            return 90
        elif readinessstring == 'Rested':
            return 100
        else:
            raise RuntimeError('No such readiness %s' % (readinessstring,))


    def ConvertOffRoadAbilityToString(self, ability):
        if ability == 0:
            return 'Poor'
        elif ability == 1:
            return 'Fair'
        elif ability == 2:
            return 'Good'
        else:
            raise RuntimeError('No such OffRoadAbility %d' % (ability,))
    def ConvertOffRoadAbilityStringToOffRoadAbility(self, abilitystring):
        if abilitystring == 'Poor':
            return 0
        elif abilitystring == 'Fair':
            return 1
        elif abilitystring == 'Good':
            return 2
        else:
            raise RuntimeError('No such OffRoadAbility %s' % (abilitystring,))


################################ OOB #######################################################

class OobXML(OobBase):
    pass

class OobCommon_ImplementationUsingTwoTreesAndDicts(OobBase):
    def __init__(self):
        self.oobtreeAxis = OOBTree(lamdaIsRole=self.IsRole, lambdaGetDelay=self.GetDelay, lambdaIsHq=self.IsHq)
        self.oobtreeAllies = OOBTree(lamdaIsRole=self.IsRole, lambdaGetDelay=self.GetDelay, lambdaIsHq=self.IsHq)

        self.pp = pprint.PrettyPrinter(indent = 4)
        #self.myrepr = repr
        self.myrepr = self.pp.pformat

        self.conversions = OobConversions()


    def GetNationalityPrefix(self, oobid):
        side = self.GetNationality(oobid)
        if side == 'German':
            return 'G'
        elif side == 'Soviet':
            return 'R'
        else:
            raise RuntimeError('Unkown nationality ' + nationality)

    def GetNationality(self, oobid):
        """
        Nationality should be stored as an attribute of the oob node, or even as a part of the trooptype string
        For the moment we can tell the side and we assume german or russian from that.
        """
        if oobid.find('allied') != -1:
            return 'Soviet'
        else:
            return 'German'

    def Exists(self, oobid):
        tree = self.DetermineWhichTreeFromOobNodeId(oobid)
        result_nodeexists = oobid in tree.nodes
        result_relationexist = tree.relations.FindObjects(From=None, To=oobid, RelId = 'parent') or \
                               tree.relations.FindObjects(From=oobid, To=None, RelId = 'parent')
        return result_nodeexists or result_relationexist

    def AllocateNewOobNodeId(self, side):
        assert side == 'axis'or side == 'allied'
        return side+'_' + '%15.0f%s' % ( random.random()*(10**20), int(time.time()) )
    def AllocateNewOobNode(self, side):
        assert side == 'axis'or side == 'allied'
        id = self.AllocateNewOobNodeId(side)
        tree = self.DetermineWhichTreeFromSide(side)
        assert id not in tree.nodes, 'Key clash - non unique id'
        tree.nodes[id] = {'ME':0,'HQ':0}
        return id, tree.nodes[id]

    def _ConvertRelations(self, rmRelationsList):
        """
         Converts RelationManager Relations (list) To Oob File Format (list)

        RelationManager Relations look like
          [('a', 'b', 'parent'), ('c', 'd', 'parent')]
        Returns:
          [['a', 'b'],['c', 'd']]
        """
##        print '-'*30
##        print rmRelationsList
##        print '='*30

        rez = [ [fromoob, tooob] for fromoob, tooob, relid in rmRelationsList ]
        return rez

##        rezlist = []
##        for atuple in rmRelationsList:
##            relitem = [atuple[0], atuple[1]]
##            rezlist.append(relitem)
##
##        rez= [['a', 'b'],['c', 'd']]
##
##        assert rezlist == rez, 'refactoring didnt work!!!'
##        return rez

    def __str__(self):
        # Used by OobEditor to persist to file
        nodedictstringAllies = 'allies = '+self.myrepr(self.oobtreeAllies.nodes)
        nodedictstringAxis = 'axis = '+    self.myrepr(self.oobtreeAxis.nodes)
        relationsstringAllies = 'alliedparentrelations = '+self.myrepr(self._ConvertRelations(self.oobtreeAllies.relations.Relationships))
        relationsstringAxis = 'axisparentrelations = '+    self.myrepr(self._ConvertRelations(self.oobtreeAxis.relations.Relationships))
        all = [nodedictstringAllies, nodedictstringAxis, relationsstringAllies, relationsstringAxis]
        return '\n'.join(all)

    def __repr__(self):
        # Used by resolver to persist to file or turngo/resolver to transmit entire oob over the wire.
        adict = {}
        adict['allies'] = self.oobtreeAllies.nodes
        adict['axis'] = self.oobtreeAxis.nodes
        adict['alliedparentrelations'] = self._ConvertRelations(self.oobtreeAllies.relations.Relationships)
        adict['axisparentrelations'] = self._ConvertRelations(self.oobtreeAxis.relations.Relationships)
        return self.myrepr(adict)

    def LoadFromReprStr(self, strdict):
        # Used by resolver to persist to file or turngo/resolver to transmit entire oob over the wire.
        dict = eval(strdict)
        self.LoadFromDict(dict)

##    def LoadFromStr(self, strdict):
##        # Unused.  Difference between str and repr version of Oob is that the repr version is a text
##        # pretty print of a single dict containing four important keys, whilst the str version is
##        # four textlines of variable assignments, where the variables are the four important keys, as strings.
##        assert 0, 'Supposed to be unused.'
##        mydict = {}
##        exec(strdict, None, mydict)

##    def LoadFromModule(self, module):
##        self.oobtreeAxis = OOBTree(module.axis, module.axisparentrelations, lamdaIsRole=self.IsRole, lambdaGetDelay=self.GetDelay, lambdaIsHq=self.IsHq)
##        self.oobtreeAllies = OOBTree(module.allies, module.alliedparentrelations, lamdaIsRole=self.IsRole, lambdaGetDelay=self.GetDelay, lambdaIsHq=self.IsHq)
###        self.metooobmappings.Build()
##
##        if 'metooobmappingsparentrelations' in module.__dict__ and 'melist' in module.__dict__:
##            self.metooobmappings.LoadFromLists(module.melist, module.metooobmappingsparentrelations)
##        else:
##            self.metooobmappings.Build()  # failsafe

    def LoadFromDict(self, dict):
        self.oobtreeAxis = OOBTree(dict['axis'], dict['axisparentrelations'], lamdaIsRole=self.IsRole, lambdaGetDelay=self.GetDelay, lambdaIsHq=self.IsHq)
        self.oobtreeAllies = OOBTree(dict['allies'], dict['alliedparentrelations'], lamdaIsRole=self.IsRole, lambdaGetDelay=self.GetDelay, lambdaIsHq=self.IsHq)
##        self.metooobmappings.Build()

        if 'metooobmappingsparentrelations' in dict and 'melist' in dict:
            self.metooobmappings.LoadFromLists(dict['melist'], dict['metooobmappingsparentrelations'])
        else:
            self.metooobmappings.Build()  # failsafe

        self._ClearAnyCachesCosLoad()

        """
        Do not initialise Strengths And Casualties automatically, since want to be able to persists an oob and load it again
        without any changes.
        So whilst a scenario DOES call PostProcessOOBTree()
        the resolver loads its own oob over the top of a scernarios natural (and re-initialised) oob, and in this way, manages
        to persists the state of the changing oob, including any ongoing casualties and strengths.
        """
        # self.PostProcessOOBTree()

    def PostProcessOOBTree(self):
        self.InitStrengthsAndCasualties()
        self._StoreInitialExperienceStrengthEtc()

    def InitStrengthsAndCasualties(self):
        """
        mtvg corresponds to our meta troop types of
         m = men = INFANTRY
         t = tanks = ARMOR
         v - vehicles = VEHICLE
         g = guns = ARTILLERY

        Our HQ's map to 't' if they are armored.
        Everybody gets an 'm' entry.
        """

        if not self.trooptypesmgr:
            #assert 0
##            print '**Warning - could not PostProcessOOBTree cos oob has no trooptypesmgr'
            return
##        print '******************************************************PostProcessOOBTree'
        for meid in self.metooobmappings.GetAllMeIds():  # from both trees
            oobids = self.metooobmappings.GetMeRecursiveListOfOobidsExcludingMes(meid)
            for oobid in oobids:
                strength_mtvg_list = [0,0,0,0]
                strength_mtvg_list[0] = self.GetNumberOfMen(oobid)          # M

                fulltrooptype = self.GetTroopType(oobid)
                maintrooptype, subtrooptype = self.trooptypesmgr.ExtractTroopAndSubTroopTypes(fulltrooptype)
                metatrooptype = self.trooptypesmgr.MetaTroopTypeFromMainTroopType(maintrooptype)
                if metatrooptype == 'ARMOR':
                    strength_mtvg_list[1] = 1                                   # T
                elif metatrooptype == 'HQ' and maintrooptype == 'Armored HQ':
                    strength_mtvg_list[1] = 1                                   # T
                elif metatrooptype == 'VEHICLE':
                    strength_mtvg_list[2] = 1                                   # V
                elif metatrooptype == 'ARTILLERY':
                    strength_mtvg_list[3] = 1                                   # G
                elif metatrooptype in ('INFANTRY', 'HQ'):
                    pass
                else:
                    raise RuntimeError('Unknown metatrooptype '+metatrooptype)

                self.SetStrength(oobid, strength_mtvg_list)
##                print self.GetOobName(oobid), self.GetStrength(oobid)

    def _StoreInitialExperienceStrengthEtc(self):
        pass

    def GetRootNodeId(self, side):
        assert side == 'axis'or side == 'allied'
        tree = self.DetermineWhichTreeFromSide(side)
        rootnodeid = tree.FindRoot()
        return rootnodeid

    def GetParent(self, oobid):
        if oobid == 'default':
            return None
        tree = self.DetermineWhichTreeFromOobNodeId(oobid)
        if not tree:
            raise RuntimeError('Scenario GetParent cannot identify side of oob node '+oobid)
        if oobid == tree.Root():
            return 'default'
        result = tree.FindParent(oobid)
        if not result:
            errmsg = 'Could not find parent for '+oobid+' in oobtree '+str(tree)
            raise errmsg
        return result

    def FindChildren(self, oobid):
        tree = self.DetermineWhichTreeFromOobNodeId(oobid)
        if not tree:
            raise RuntimeError('Scenario GetParent cannot identify side of oob node '+oobid)
        return tree.FindChildren(oobid)

    def FindAllRoles(self):
        axisRoles = self.oobtreeAxis.FindAllRoles()
        alliedRoles = self.oobtreeAllies.FindAllRoles()
        allRoles = axisRoles+alliedRoles
        allRoles.insert(0, 'default')
        return allRoles

    def FindAllHqs(self):
        axisHqs = self.oobtreeAxis.FindAllHqs()
        alliedHqs = self.oobtreeAllies.FindAllHqs()
        allHqs = axisHqs+alliedHqs
        return allHqs

##    def FindHqsUnderCommandOfRole(self, roleoobid):
##        if roleoobid == 'default':
##            return self.FindAllHqs()
##        resultlist = []
##        childrenoobids = self.FindChildren(roleoobid)
##        for childoobid in childrenoobids:
##            if self.IsHq(childoobid):
##                resultlist.append(childoobid)
##        return resultlist

    def FindHqsUnderCommandOfRole(self, roleoobid):
        if roleoobid == 'default':
            return self.FindAllHqs()
        resultlist = []
        childrenoobids = self.FindChildren(roleoobid)
        for childoobid in childrenoobids:
            if self.IsHq(childoobid):
                if not self.IsRole(childoobid):
                    resultlist.append(childoobid)
                    resultlist += self.FindHqsUnderCommandOfRole(childoobid)
        return resultlist

    def FindAncestors(self, oobid):
        if oobid == 'default':
            raise RuntimeError('No Ancestors for default role')

        tree = self.DetermineWhichTreeFromOobNodeId(oobid)
        if not tree:
            raise RuntimeError('Scenario FindAncestors cannot identify side of oob node '+oobid)

        return tree.FindAncestors(oobid)

    def GetAllMePiecesUnderCommandOfRole(self, role):
        # just get the children of role, which are ME's.  Returns a list

        allmeids = self.metooobmappings.GetAllMeIds()
        if role == 'default':
            return allmeids
        else:
            tree = self.DetermineWhichTreeFromOobNodeId(role)
            if not tree:
                return ''
            commandablechildren = tree.FindChildren(role)
            resultlist = []
            for meid in allmeids:
                oobids_ofme = self.metooobmappings.MeIdToOobIds(meid)
                for commandablechildoobid in commandablechildren:
                    if commandablechildoobid in oobids_ofme:
                        resultlist.append(meid)
            return resultlist

    def GetTroopType(self, oobid):
        tree = self.DetermineWhichTreeFromOobNodeId(oobid)
        return self._GetTroopType(oobid, tree)

    def IsRole(self, oobid):
        if oobid == 'default':
            return 1
        if not self.IsHq(oobid):
            return 0
        tree = self.DetermineWhichTreeFromOobNodeId(oobid)
        return self._IsRole(oobid, tree)

    def GetDelay(self, oobid):
        if oobid == 'default':
            return 0    # do we need this?
        tree = self.DetermineWhichTreeFromOobNodeId(oobid)
        return self._GetDelay(oobid, tree)

    def SetDelay(self, oobid, delay):
        tree = self.DetermineWhichTreeFromOobNodeId(oobid)
        self._SetDelay(oobid, tree, delay=delay)

    def IsHq(self, oobid):
        if oobid == 'default':
            return 1
        tree = self.DetermineWhichTreeFromOobNodeId(oobid)
        return self._IsHq(oobid, tree)

    def GetOobName(self, oobid):
        if oobid == 'default':
            return ''
        tree = self.DetermineWhichTreeFromOobNodeId(oobid)
        return self._GetOobName(oobid, tree)

    def GetOfficerName(self, oobid):
        if oobid == 'default':
            return 'God'
        tree = self.DetermineWhichTreeFromOobNodeId(oobid)
        return self._GetOfficerName(oobid, tree)

    def GetOfficerRankAndName(self, oobid):
        if oobid == 'default':
            return 'God'
        tree = self.DetermineWhichTreeFromOobNodeId(oobid)
        return self._GetOfficerRank(oobid, tree) +' '+ self._GetOfficerName(oobid, tree)

    def IsMe(self, oobid):
        tree = self.DetermineWhichTreeFromOobNodeId(oobid)
        if not tree:
            return 0
        if 'ME' in tree.nodes[oobid]:
            return tree.nodes[oobid]['ME']
        else:
            return 0

    def GetStartingCoord(self, oobid):
        tree = self.DetermineWhichTreeFromOobNodeId(oobid)
        if not tree:
            msg = ' GetStartingCoord: No such oob node '+oobid
            raise msg
        return self._GetStartingCoord(oobid, tree)


    def CumulativeDelay(self, fromoobid, tooobid):
        if fromoobid == 'default' or tooobid == 'default' or fromoobid == tooobid:
            return 0

        tree = self.DetermineWhichTreeFromOobNodeId(fromoobid)
        assert tree, ("determining tree for %s to work out delay to %s"%(fromoobid, tooobid))
        return tree.CumulativeDelay(fromoobid, tooobid)

    def DetermineWhichTreeFromSide(self, side):
        # Common
        if side == 'allied':
            return self.oobtreeAllies
        if side == 'axis':
            return self.oobtreeAxis
        return None

    def DetermineWhichTreeFromOobNodeId(self, oobid):
        # Common
        if oobid == 'default':
            return None
        elif oobid[:6] == 'allied':
            return self.oobtreeAllies
        elif oobid[:4] == 'axis':
            return self.oobtreeAxis

        # if all else fails - and it will for oldstyle scenarios
        # do it the proper way

        side = self.DetermineSideFromOobNodeId(oobid)
        tree = self.DetermineWhichTreeFromSide(side)
        if not tree:
            raise RuntimeError('Cannot identify subtree tree of oob node '+oobid)
        return tree

    def CreateTemporaryOobidUnderRole(self, parentroleoobid, trooptype='Infantry', transporttype='Foot'):
        side = self.DetermineSideFromOobNodeId(parentroleoobid)
        tree = self.DetermineWhichTreeFromOobNodeId(parentroleoobid)
        signaloobid, node = self.AllocateNewOobNode(side)
        tree.AddRelationshipFromOobidToParent(signaloobid, parentroleoobid)
        self._SetTroopType(signaloobid, tree, trooptype)
        self._SetTransportType(signaloobid, tree, transporttype)
        self._SetIsHq(signaloobid, tree, 1)
        self._SetIsMe(signaloobid, tree, 1)

        self._SetCarryingCapacity(signaloobid, tree, 0) # depreciated
        self._SetNumberOfMen(signaloobid, tree, 1)      # boring - not used in calculations any more.
        self._SetStrength(signaloobid, tree, [1,0,0,0]) # so that is not dead.

##        self._SetSquadSize(signaloobid, tree, 'team')
##        self._SetSquadCapacity(signaloobid, tree, '')

        assert self.GetTroopType(signaloobid), 'What no transport type for temp signal oobid?'
        return signaloobid

    def DestroyTemporaryOobid(self, signaloobid):
        tree = self.DetermineWhichTreeFromOobNodeId(signaloobid)
        tree.RemoveOobid(signaloobid)

    def GetSideOfPiece(self, meid):
        # Common
        oobid = self.RankingHqInMe(meid)
        side = self.DetermineSideFromOobNodeId(oobid)
        return side

    def GetTransportType(self, oobid):
        return self._GetTransportType(oobid, self.DetermineWhichTreeFromOobNodeId(oobid))

    def SetTroopType(self, oobid, trooptype='Infantry'):
        tree = self.DetermineWhichTreeFromOobNodeId(oobid)
        self._SetTroopType(oobid, tree, trooptype)

    def SetTransportType(self, oobid, transporttype='Foot'):
        tree = self.DetermineWhichTreeFromOobNodeId(oobid)
        self._SetTransportType(oobid, tree, transporttype)

    def SetInitialMeReadiness(self, oobid, value):
        tree = self.DetermineWhichTreeFromOobNodeId(oobid)
        self._SetInitialMeReadiness(oobid, tree, value)

    def SetExperience(self, oobid, experience=0):
        tree = self.DetermineWhichTreeFromOobNodeId(oobid)
        self._SetExperience(oobid, tree, experience=experience)

    def GetExperience(self, oobid):
        tree = self.DetermineWhichTreeFromOobNodeId(oobid)
        return self._GetExperience(oobid, tree)

    def GetExperienceTime(self, oobid):
        tree = self.DetermineWhichTreeFromOobNodeId(oobid)
        return self._GetExperienceTime(oobid, tree)

    def SetPoints(self, oobid, points):
        tree = self.DetermineWhichTreeFromOobNodeId(oobid)
        self._SetPoints(oobid, tree, points)

    def GetPoints(self, oobid):
        return self._GetPoints(oobid, self.DetermineWhichTreeFromOobNodeId(oobid))

    def SetNeedOOBEvent(self, oobid, needoobevent):
        tree = self.DetermineWhichTreeFromOobNodeId(oobid)
        self._SetNeedOOBEvent(oobid, tree, needoobevent)

    def GetNeedOOBEvent(self, oobid):
        tree = self.DetermineWhichTreeFromOobNodeId(oobid)
        return self._GetNeedOOBEvent(oobid, tree)



    def GetOffRoadAbility(self, oobid):
        return self._GetOffRoadAbility(oobid, self.DetermineWhichTreeFromOobNodeId(oobid))
    def GetNumberOfMen(self, oobid):
        return self._GetNumberOfMen(oobid, self.DetermineWhichTreeFromOobNodeId(oobid))
##    def GetCanHoldNumberOfMen(self, oobid):
##        return self._GetCanHoldNumberOfMen(oobid, self.DetermineWhichTreeFromOobNodeId(oobid))
    def SetFitness(self, oobid, fitness=0):
        tree = self.DetermineWhichTreeFromOobNodeId(oobid)
        self._SetFitness(oobid, tree, fitness=fitness)

    def GetFitness(self, oobid):
        return self._GetFitness(oobid, self.DetermineWhichTreeFromOobNodeId(oobid))

    def GetFitnessTime(self, oobid):
        return self._GetFitnessTime(oobid, self.DetermineWhichTreeFromOobNodeId(oobid))

    def GetCarryingCapacity(self, oobid):
        return self._GetCarryingCapacity(oobid, self.DetermineWhichTreeFromOobNodeId(oobid))

##    def GetSquadSize(self, oobid):
##        return self._GetSquadSize(oobid, self.DetermineWhichTreeFromOobNodeId(oobid))
##    def GetSquadCapacity(self, oobid):
##        return self._GetSquadCapacity(oobid, self.DetermineWhichTreeFromOobNodeId(oobid))
##    def GetHowMuchCanTow(self, oobid):
##        return self._GetHowMuchCanTow(oobid, self.DetermineWhichTreeFromOobNodeId(oobid))
##    def GetHowHardToTow(self, oobid):
##        return self._GetHowHardToTow(oobid, self.DetermineWhichTreeFromOobNodeId(oobid))

    def GetSupplyAmmo(self, oobid):
        return self._GetSupplyAmmo(oobid, self.DetermineWhichTreeFromOobNodeId(oobid))
    def GetInitialDirection(self, oobid):
        return self._GetInitialDirection(oobid, self.DetermineWhichTreeFromOobNodeId(oobid))
    def GetSupplyBasics(self, oobid):
        return self._GetSupplyBasics(oobid, self.DetermineWhichTreeFromOobNodeId(oobid))
    def GetSupplyFuel(self, oobid):
        return self._GetSupplyFuel(oobid, self.DetermineWhichTreeFromOobNodeId(oobid))

    def GetMeAppearsAfterTurn(self, oobid):
        return self._GetMeAppearsAfterTurn(oobid, self.DetermineWhichTreeFromOobNodeId(oobid))
    def ClearMeAppearsAfterTurn(self, oobid):
        return self._ClearMeAppearsAfterTurn(oobid, self.DetermineWhichTreeFromOobNodeId(oobid))
    def GetInitialMeReadiness(self, oobid):
        return self._GetInitialMeReadiness(oobid, self.DetermineWhichTreeFromOobNodeId(oobid))
    def GetInitialMeName(self, oobid):
        aname = self._GetInitialMeName(oobid, self.DetermineWhichTreeFromOobNodeId(oobid))
        if aname == '':
            return self.GetOobName(oobid)
        else:
            return aname

    def GetOfficerRank(self, oobid):
        return self._GetOfficerRank(oobid, self.DetermineWhichTreeFromOobNodeId(oobid))
    def GetOfficerAggressiveness(self, oobid):
        return self._GetOfficerAggressiveness(oobid, self.DetermineWhichTreeFromOobNodeId(oobid))
    def GetOfficerEfficiency(self, oobid):
        return self._GetOfficerEfficiency(oobid, self.DetermineWhichTreeFromOobNodeId(oobid)).strip()
    def GetOfficerLeadership(self, oobid):
        return self._GetOfficerLeadership(oobid, self.DetermineWhichTreeFromOobNodeId(oobid))

    def GetSignals(self, oobid):
        return self._GetSignals(oobid, self.DetermineWhichTreeFromOobNodeId(oobid))

    def SetSignals(self, oobid, signalsdict):
        tree = self.DetermineWhichTreeFromOobNodeId(oobid)
        self._SetSignals(oobid, tree, signalsdict=signalsdict)

    def SetDamagePointsLastBattle(self, oobid, points=0):
        tree = self.DetermineWhichTreeFromOobNodeId(oobid)
        self._SetDamagePointsLastBattle(oobid, tree, points=points)
    def GetDamagePointsLastBattle(self, oobid):
        tree = self.DetermineWhichTreeFromOobNodeId(oobid)
        return self._GetDamagePointsLastBattle(oobid, tree)

    def SetStrength(self, oobid, mtgvlist):
        self._SetStrength(oobid, self.DetermineWhichTreeFromOobNodeId(oobid), mtgvlist)
        self._InvalidateMountednessCacheEntry(oobid)
    def GetStrength(self, oobid):
        return self._GetStrength(oobid, self.DetermineWhichTreeFromOobNodeId(oobid))

    def GetStrengthTime(self, oobid):
        return self._GetStrengthTime(oobid, self.DetermineWhichTreeFromOobNodeId(oobid))

    def SetCasualtiesIncurredTotal(self, oobid, mtgvlist):
        self._SetCasualtiesIncurredTotal(oobid, self.DetermineWhichTreeFromOobNodeId(oobid), mtgvlist)
    def GetCasualtiesIncurredTotal(self, oobid):
        return self._GetCasualtiesIncurredTotal(oobid, self.DetermineWhichTreeFromOobNodeId(oobid))
    def SetCasualtiesIncurredLastBattle(self, oobid, mtgvlist):
        self._SetCasualtiesIncurredLastBattle(oobid, self.DetermineWhichTreeFromOobNodeId(oobid), mtgvlist)
    def GetCasualtiesIncurredLastBattle(self, oobid):
        return self._GetCasualtiesIncurredLastBattle(oobid, self.DetermineWhichTreeFromOobNodeId(oobid))
    def SetCasualtiesCausedTotal(self, oobid, mtgvlist):
        self._SetCasualtiesCausedTotal(oobid, self.DetermineWhichTreeFromOobNodeId(oobid), mtgvlist)
    def GetCasualtiesCausedTotal(self, oobid):
        return self._GetCasualtiesCausedTotal(oobid, self.DetermineWhichTreeFromOobNodeId(oobid))
    def SetCasualtiesCausedLastBattle(self, oobid, mtgvlist):
        self._SetCasualtiesCausedLastBattle(oobid, self.DetermineWhichTreeFromOobNodeId(oobid), mtgvlist)
    def GetCasualtiesCausedLastBattle(self, oobid):
        return self._GetCasualtiesCausedLastBattle(oobid, self.DetermineWhichTreeFromOobNodeId(oobid))

    def IsDead(self, oobid):
        strength = self.GetStrength(oobid)
##        print 'IsDead(self, oobid): strength', strength, 'oobid', oobid
        if strength[0] == 0 and strength[1] == 0 and strength[2] == 0 and strength[3] == 0:
            return 1
        else:
            return 0

    def SetOOBGameState(self, oobgamestate):
        pass

    def GetRankingDepth(self, oobid):
        depth = 0
        parentNode = self.GetParent(oobid)
        if parentNode == 'default':
            print('parentNode == default')
            # hit root node
            return depth
        else:
            depth += 1
            depth += self.GetRankingDepth(parentNode)
            return depth


    def GetTOEDepth(self, oobid):
        # Depth limitation of 0-3
        depth = self.GetRankingDepth(oobid)
        if depth > 3:
            return 3
        else:
            return depth



    def GetOrderSkill(self, oobid):
        if self.IsHq(oobid):
             return self._GetOrderSkill(oobid, self.DetermineWhichTreeFromOobNodeId(oobid))
        else:
            # if not a HQ
            return 0

    def GetCombatSkill(self, oobid):
        if self.IsHq(oobid):
            return self._GetCombatSkill(oobid, self.DetermineWhichTreeFromOobNodeId(oobid))
        else:
            return 0


    def GetRallySkill(self, oobid):
        if self.IsHq(oobid):
            return self._GetRallySkill(oobid, self.DetermineWhichTreeFromOobNodeId(oobid))
        else:
            return 0


    def GetStealthSkill(self, oobid):
        if self.IsHq(oobid):
            return self._GetStealthSkill(oobid, self.DetermineWhichTreeFromOobNodeId(oobid))
        else:
            return 0

    def SetOrderSkill(self, oobid, level):
        if self.IsHq(oobid):
            self._SetOrderSkill(oobid, self.DetermineWhichTreeFromOobNodeId(oobid), level)

    def SetCombatSkill(self, oobid, level):
        if self.IsHq(oobid):
            self._SetCombatSkill(oobid, self.DetermineWhichTreeFromOobNodeId(oobid), level)

    def SetRallySkill(self, oobid, level):
        if self.IsHq(oobid):
            self._SetRallySkill(oobid, self.DetermineWhichTreeFromOobNodeId(oobid), level)

    def SetStealthSkill(self, oobid, level):
        if self.IsHq(oobid):
            self._SetStealthSkill(oobid, self.DetermineWhichTreeFromOobNodeId(oobid), level)


    def GetImmobilized(self, oobid):
        return self._GetImmobilized(oobid, self.DetermineWhichTreeFromOobNodeId(oobid))


    def SetImmobilized(self, oobid, immobilized):
        self._SetImmobilized(oobid, self.DetermineWhichTreeFromOobNodeId(oobid), immobilized)

    def GetBogged(self, oobid):
        return self._GetBogged(oobid, self.DetermineWhichTreeFromOobNodeId(oobid))

    def SetBogged(self, oobid, bogged):
        self._SetBogged(oobid, self.DetermineWhichTreeFromOobNodeId(oobid), bogged)

    def GetGunDestroyed(self, oobid):
        return self._GetGunDestroyed(oobid, self.DetermineWhichTreeFromOobNodeId(oobid))

    def SetGunDestroyed(self, oobid, gundestroyed):
        self._SetGunDestroyed(oobid, self.DetermineWhichTreeFromOobNodeId(oobid), gundestroyed)


    def GetDugIn(self, oobid):
        return self._GetDugIn(oobid, self.DetermineWhichTreeFromOobNodeId(oobid))

    def SetDugIn(self, oobid, dugin):
        self._SetDugIn(oobid, self.DetermineWhichTreeFromOobNodeId(oobid), dugin)

class Oob_NEWSTYLE(OobCommon_ImplementationUsingTwoTreesAndDicts):
    def __init__(self, trooptypesmgr=None):
        OobCommon_ImplementationUsingTwoTreesAndDicts.__init__(self)
        self.metooobmappings = MeToOobMappings_NEWSTYLE(self)
        self.trooptypesmgr = trooptypesmgr
        self.cachedmountedness = None
        self._ClearAnyCachesCosLoad()
        self._ooboverlay = None

    def _ClearAnyCachesCosLoad(self):
        self.cachedmountedness = {}

##    def FormatSignalsDictForDisplay(self, sigdict):
##        # Should only be called by post scenario40, V2 trooptype system.  which will be oob newstyle
##        result = ''
##        if sigdict['NonRadio']:
##            result += str(sigdict['NonRadio']) + '\n'
##        if sigdict['Radio']['whilststationary']:
##            result += sigdict['Radio']['whilststationary'] + '   (whilst stationary)\n'
##        if sigdict['Radio']['whilstmoving']:
##            result += sigdict['Radio']['whilstmoving'] + '   (whilst moving)'
##        return result

    def _GetSignals(self, oobid, tree): return tree.nodes[oobid]['HqDict']['Signals']
    def _SetSignals(self, oobid, tree, signalsdict):
        if not 'HqDict' in tree.nodes[oobid]:
            tree.nodes[oobid]['HqDict'] = {}
        tree.nodes[oobid]['HqDict']['Signals'] = copy.copy(signalsdict)

    def _GetOfficerRank(self, oobid, tree): return tree.nodes[oobid]['HqDict']['Officer']['rank']
    def _GetOfficerAggressiveness(self, oobid, tree): return tree.nodes[oobid]['HqDict']['Officer']['aggressiveness']
    def _GetOfficerEfficiency(self, oobid, tree): return tree.nodes[oobid]['HqDict']['Officer']['efficiency']
    def _GetOfficerLeadership(self, oobid, tree): return tree.nodes[oobid]['HqDict']['Officer']['leadership']
    def _GetMeAppearsAfterTurn(self, oobid, tree): return tree.nodes[oobid]['MeDict']['appearsafterturn']
    def _ClearMeAppearsAfterTurn(self, oobid, tree): tree.nodes[oobid]['MeDict']['appearsafterturn']=0
    def _GetInitialMeReadiness(self, oobid, tree): return tree.nodes[oobid]['MeDict']['initialreadiness']
    def _GetInitialMeName(self, oobid, tree): return tree.nodes[oobid]['MeDict']['mename']
    def _GetSupplyAmmo(self, oobid, tree): return tree.nodes[oobid]['MeDict']['Supply']['ammo']
    def _GetInitialDirection(self, oobid, tree): return tree.nodes[oobid]['MeDict'].get('initialdirection','S')
    def _GetSupplyBasics(self, oobid, tree): return tree.nodes[oobid]['MeDict']['Supply']['basics']
    def _GetSupplyFuel(self, oobid, tree): return tree.nodes[oobid]['MeDict']['Supply']['fuel']

    def _SetFitness(self, oobid, tree, fitness):
        tree.nodes[oobid]['fitness'] = fitness
        tree.nodes[oobid]['needoobevent'] = 1

    def _GetFitness(self, oobid, tree):
        if self._ooboverlay is None:
            return tree.nodes[oobid]['fitness']
        if oobid in self._ooboverlay:
            return self._ooboverlay[oobid]['fitness']
        return None
#        return tree.nodes[oobid]['initial_fitness']

    def _GetFitnessTime(self, oobid, tree):
        if self._ooboverlay is None:
            return None
        return self._ooboverlay[oobid]['fitness_time']


    def _GetOrderSkill(self, oobid, tree):
        if self._ooboverlay is None:
            return tree.nodes[oobid]['HqDict']['Extras'].get('order', 0)
        if oobid in self._ooboverlay:
            if self._ooboverlay[oobid]['HqDict']['Extras'] is None:
                return None
            return self._ooboverlay[oobid]['HqDict']['Extras'].get('order', 0)
        return None


    def _GetRallySkill(self, oobid, tree):
        if self._ooboverlay is None:
            return tree.nodes[oobid]['HqDict']['Extras'].get('rally', 0)
        if oobid in self._ooboverlay:
            if self._ooboverlay[oobid]['HqDict']['Extras'] is None:
                return None
            return self._ooboverlay[oobid]['HqDict']['Extras'].get('rally', 0)
        return None


    def _GetCombatSkill(self, oobid, tree):
        if self._ooboverlay is None:
            return tree.nodes[oobid]['HqDict']['Extras'].get('combat', 0)
        if oobid in self._ooboverlay:
            if self._ooboverlay[oobid]['HqDict']['Extras'] is None:
                return None
            return self._ooboverlay[oobid]['HqDict']['Extras'].get('combat', 0)
        return None


    def _GetStealthSkill(self, oobid, tree):
        if self._ooboverlay is None:
            return tree.nodes[oobid]['HqDict']['Extras'].get('stealth', 0)
        if oobid in self._ooboverlay:
            if self._ooboverlay[oobid]['HqDict']['Extras'] is None:
                return None
            return self._ooboverlay[oobid]['HqDict']['Extras'].get('stealth', 0)
        return None


    def _SetOrderSkill(self, oobid, tree, level): tree.nodes[oobid]['HqDict']['Extras']['order'] = level
    def _SetRallySkill(self, oobid, tree, level): tree.nodes[oobid]['HqDict']['Extras']['rally'] = level
    def _SetCombatSkill(self, oobid, tree, level): tree.nodes[oobid]['HqDict']['Extras']['combat'] = level
    def _SetStealthSkill(self, oobid, tree, level): tree.nodes[oobid]['HqDict']['Extras']['stealth'] = level

    def _GetImmobilized(self, oobid, tree):
        self.__EnsureVehicleDictExists(oobid, tree)
        if self._ooboverlay is None:
            return tree.nodes[oobid]['VehicleDict'].get('immobilized', 0)
        if oobid in self._ooboverlay:
            if self._ooboverlay[oobid]['VehicleDict'] is None:
                return None
            return self._ooboverlay[oobid]['VehicleDict'].get('immobilized', 0)
        return None

    def _SetImmobilized(self, oobid, tree, immobilized):
        self.__EnsureVehicleDictExists(oobid, tree)
        tree.nodes[oobid]['immobilized'] = immobilized

    def _GetBogged(self, oobid, tree):
        self.__EnsureVehicleDictExists(oobid, tree)
        if self._ooboverlay is None:
            return tree.nodes[oobid]['VehicleDict'].get('bogged', 0)
        if oobid in self._ooboverlay:
            if self._ooboverlay[oobid]['VehicleDict'] is None:
                return None
            return self._ooboverlay[oobid]['VehicleDict'].get('bogged', 0)
        return None

    def _SetBogged(self, oobid, tree, bogged):
        self.__EnsureVehicleDictExists(oobid, tree)
        tree.nodes[oobid]['bogged'] = bogged

    def _GetGunDestroyed(self, oobid, tree):
        self.__EnsureVehicleDictExists(oobid, tree)
        if self._ooboverlay is None:
            return tree.nodes[oobid]['VehicleDict'].get('gundestroyed', 0)
        if oobid in self._ooboverlay:
            if self._ooboverlay[oobid]['VehicleDict'] is None:
                return None
            return self._ooboverlay[oobid]['VehicleDict'].get('gundestroyed', 0)
        return None

    def _SetGunDestroyed(self, oobid, tree, gundestroyed):
        self.__EnsureVehicleDictExists(oobid, tree)
        tree.nodes[oobid]['gundestroyed'] = gundestroyed



    def _GetDugIn(self, oobid, tree):
        self.__EnsureVehicleDictExists(oobid, tree)
        if self._ooboverlay is None:
            return tree.nodes[oobid]['VehicleDict'].get('dugin', 0)
        if oobid in self._ooboverlay:
            if self._ooboverlay[oobid]['VehicleDict'] is None:
                return None
            return self._ooboverlay[oobid]['VehicleDict'].get('dugin', 0)
        return None

    def _SetDugIn(self, oobid, tree, dugin):
        self.__EnsureVehicleDictExists(oobid, tree)
        tree.nodes[oobid]['dugin'] = dugin



    def _GetNumberOfMen(self, oobid, tree): return tree.nodes[oobid]['numberofmen']
##    def _GetCanHoldNumberOfMen(self, oobid, tree): return tree.nodes[oobid]['canholdnumberofmen']
    def _GetCarryingCapacity(self, oobid, tree): return tree.nodes[oobid]['carryingcapacity']

    def _SetNumberOfMen(self, oobid, tree, num): tree.nodes[oobid]['numberofmen'] = num
    def _SetCarryingCapacity(self, oobid, tree, num): tree.nodes[oobid]['carryingcapacity'] = num

##    def _GetHowMuchCanTow(self, oobid, tree): return tree.nodes[oobid]['howmuchcantow']
##    def _GetHowHardToTow(self, oobid, tree): return tree.nodes[oobid]['howhardtotow']
##
##    def _GetSquadSize(self, oobid, tree): return tree.nodes[oobid]['squadsize']
##    def _GetSquadCapacity(self, oobid, tree): return tree.nodes[oobid]['squadcapacity']
##
##    def _SetSquadSize(self, oobid, tree, strsize): tree.nodes[oobid]['squadsize'] = strsize
##    def _SetSquadCapacity(self, oobid, tree, strsize): tree.nodes[oobid]['squadcapacity'] = strsize

    def _GetOffRoadAbility(self, oobid, tree):
        """
        oldstyle oob => no offroad ability
        newstyle oob, V1 trooptypes (scenario 3x) => oob attribute
        newstyle oob, V2 trooptypes (scenario 4x) => depreciated oob attribute, use r/o troop table instead
        """
        offroadability = ''
        if 'offroadability' in tree.nodes[oobid]:   # may not be there cos may be a temp signal type oob with no offroadability attribute.  (newstyle oob, V1 )
            offroadability = tree.nodes[oobid]['offroadability']
        if offroadability == '':
            offroadability = 'poor' # 'fair'
        return offroadability

    def _GetTransportType(self, oobid, tree): return tree.nodes[oobid]['transporttype']
    def _GetTroopType(self, oobid, tree): return tree.nodes[oobid]['trooptype']

    def _SetTroopType(self, oobid, tree, trooptype):         tree.nodes[oobid]['trooptype'] = trooptype
    def _SetTransportType(self, oobid, tree, transporttype): tree.nodes[oobid]['transporttype'] = transporttype
    def _SetInitialMeReadiness(self, oobid, tree, value):
        if not 'MeDict' in tree.nodes[oobid]:
            tree.nodes[oobid]['MeDict'] = {}
        tree.nodes[oobid]['MeDict']['initialreadiness'] = value

    def _GetOobName(self, oobid, tree):
        if not 'name' in tree.nodes[oobid]:
            return ''
        return tree.nodes[oobid]['name']

    def _GetOfficerName(self, oobid, tree):
        if not 'HQ' in tree.nodes[oobid]:
            return ''
        return tree.nodes[oobid]['HqDict']['Officer']['name']

    def _GetOfficerRank(self, oobid, tree):
        if not 'HQ' in tree.nodes[oobid]:
            return ''
        return tree.nodes[oobid]['HqDict']['Officer']['rank']

    def _IsHq(self, oobid, tree):
        return tree.nodes[oobid]['HQ']  # NEW

    def _SetIsHq(self, oobid, tree, val):
        tree.nodes[oobid]['HQ'] = val
        if val:
            if not 'HqDict' in tree.nodes[oobid]:
                tree.nodes[oobid]['HqDict'] = {}
        else:
            if 'HqDict' in tree.nodes[oobid]:
                del tree.nodes[oobid]['HqDict']

    def _SetIsMe(self, oobid, tree, val):
        tree.nodes[oobid]['ME'] = val
        if val:
            if not 'MeDict' in tree.nodes[oobid]:
                tree.nodes[oobid]['MeDict'] = {}
        else:
            if 'MeDict' in tree.nodes[oobid]:
                del tree.nodes[oobid]['MeDict']

    def _IsRole(self, oobid, tree):
        return tree.nodes[oobid]['HqDict']['role']  # NEW

    def _GetDelay(self, oobid, tree):
        return tree.nodes[oobid]['HqDict']['delay']  # NEW

    def _SetDelay(self, oobid, tree, delay):
        tree.nodes[oobid]['HqDict']['delay'] = delay

    def _GetStartingCoord(self, oobid, tree):
        return tree.nodes[oobid]['coord']  #OLD
##        assert tree.nodes[oobid]['ME'] == 1, 'No coord if not an ME'
##        return tree.nodes[oobid]['MeInfo']['coord']  #NEW

    def _SetPoints(self, oobid, tree, points):
        tree.nodes[oobid]['points'] = points
        tree.nodes[oobid]['needoobevent'] = 1

    def _GetPoints(self, oobid, tree):
        return tree.nodes[oobid]['points']

    def _SetExperience(self, oobid, tree, experience):
        tree.nodes[oobid]['experience'] = experience
        tree.nodes[oobid]['needoobevent'] = 1

    def _GetExperience(self, oobid, tree):
        if self._ooboverlay is None:
##            show("getting experience from real oob")
            return tree.nodes[oobid]['experience']
        if oobid in self._ooboverlay:
##            show("getting experience from overlay")
            return self._ooboverlay[oobid]['experience']
##        show("getting experience from initial oob")
        return None
##        return tree.nodes[oobid]['initial_experience']



    def SetOOBGameState(self, oobgamestate):
##        show(oobgamestate)
        print("Setting oobgamestate for OOBOverlay")
        if oobgamestate is None:
            self._ooboverlay = None
            return
        from event import EventobjList
        self._ooboverlay = {}
##        show(EventobjList().AddChunk(oobgamestate).FindMatching2(cmd='OOB'))
        for e in EventobjList().AddChunk(oobgamestate):#.FindMatching2(cmd='OOB'):
            print(e.oobdict)
            self._ooboverlay.update(e.oobdict)
#            show(e, self._ooboverlay)

        print(self._ooboverlay)

    def _SetNeedOOBEvent(self, oobid, tree, needoobevent):
        tree.nodes[oobid]['needoobevent'] = needoobevent

    def _GetNeedOOBEvent(self, oobid, tree):
        return tree.nodes[oobid].get('needoobevent', 0)

##    def GetOOBEvents(self):
##      return self.oobtreeAxis.GetOOBEvents() + self.oobtreeAllies.GetOOBEvents()

    def RankingHqAboveMe(self, meid):
        """
        Find the RankingHqInMe, return parent of it
        """
        hqoobid = self.RankingHqInMe(meid)
        result = self.GetParent(hqoobid)  # Warning - may return 'default'
        return result

    def _GetRankingHqOrAnySiblingHq(self, hqlist):
        # Is any hq the parent of the others
        assert hqlist, 'Empy Hq list - cannot determine rank.'
        parentlist = []
        for hq in hqlist:
            parent = self.GetParent(hq)
            if not parent or parent == 'default':
                return hq   # found the root hq
            parentlist.append(parent)
        for hq in hqlist:
            if hq in parentlist:
                return hq
        return hqlist[0]

    def RankingHqInMe(self, meid):
        """
        Find the oobs that are in the me
        Determine which is the one that is a HQ, if none raise exception.
         cos cannot split me such that an me has no hq in it
         (me's can have multiple hq's of the same rank)
        If there are more than one HQ then determine which is ranking,
          if none return any of the sibling HQ's
        return oobid of ranking HQ
        """
##        print 'RankingHqInMe(self, meid)', meid
        oobids = self.metooobmappings.MeIdToOobIds(meid)
        hqlist = []
        for oobid in oobids:
            if self.IsHq(oobid):
                hqlist.append(oobid)
        if not hqlist:
            raise RuntimeError('Must always have an Hq in an ME ' + meid)
        if len(hqlist) == 1:
            return hqlist[0]
        rankinghq = self._GetRankingHqOrAnySiblingHq(hqlist)
        if not rankinghq:
            raise RuntimeError('Cannot find a sibling hq nor a ranking hq in ME ' + meid)
        return rankinghq

    def DetermineSideFromOobNodeId(self, oobid):
        list = oobid.split('_')
        assert list > 1, 'Missing side id from oobid'
        side = list[0]
        #print side
        if not (side == 'allied' or side == 'axis'):
            msg = 'Error/Exception: Side %s must be allied or axis for oobid %s' % (side, oobid)
            raise msg
        assert side == 'allied' or side == 'axis', 'Side must be allied or axis'
        return side


    def IsMounted(self, meid):
        """
        Cache this.

        >  QUESTION:  I'm figuring that the mountedness state of an ME won't change
        > unless there is a subsequent split and merge?

        Or casualties or losses for one reason or another. Change of orders from FM
        to M or D or whatever?
        """
##      NON CACHED
##      fullymounted, listoftranportingoobids, listofnonmountedremainingoobids = MountedCalculator(self, meid).IsMounted()

        if meid == 'signalmeid':
            """
            When signals (runners, bikes etc.) are run in the game, the mountedness kicks in and asks the
            temporary signal ME 'are you mounted'.
            I'm building it in so that the answer is always no, since there is only ever one oob unit
            in that signal ME.  This will speed things up, and is, I think, right.
            """
            listofnonmountedremainingoobids = self.metooobmappings.MeIdToListOfOobIds(meid)
            listoftranportingoobids = []
            fullymounted = 0
            #print 'Saved time - mountedness info simplified! :-)', meid
            Log('Oob.IsMounted', lambda : 'Saved time - SIGNAL mountedness info simpler algorithm used! :-) ' + str( (fullymounted, listoftranportingoobids, listofnonmountedremainingoobids) ) + '\n' )
        else:
            CACHE_ON = 1
            if not CACHE_ON or not meid in self.cachedmountedness:
                fullymounted, listoftranportingoobids, listofnonmountedremainingoobids = MountedCalculator(self, meid).IsMounted()
                self.cachedmountedness[meid] = (fullymounted, listoftranportingoobids, listofnonmountedremainingoobids)
                #print 'recalced mountedness...', meid, self.cachedmountedness[meid]
            else:
                #print 'Saved time - mountedness info cached! :-)', meid, self.cachedmountedness[meid]

                import pprint
                pp = pprint.PrettyPrinter(indent = 4)
                Log('Oob.IsMounted', lambda : 'Saved time - mountedness info cached! :-) ' + meid + '\n' + pp.pformat( self.cachedmountedness ) + '\n' )

            fullymounted, listoftranportingoobids, listofnonmountedremainingoobids = self.cachedmountedness[meid]

        return fullymounted, listoftranportingoobids, listofnonmountedremainingoobids

    def _InvalidateMountednessCacheEntry(self, oobid):
        meid = self.metooobmappings.OobIdToMeIdAnywhere(oobid)
        if meid and meid in self.cachedmountedness:
            #print 'ZAP', meid
            del self.cachedmountedness[meid]

    def __EnsureBattleDictExists(self, oobid, tree):
        if not 'BattleDict' in tree.nodes[oobid]:
            tree.nodes[oobid]['BattleDict'] = {}

    def __EnsureVehicleDictExists(self, oobid, tree):
        if not 'VehicleDict' in tree.nodes[oobid]:
            tree.nodes[oobid]['VehicleDict'] = {}

    def _SetDamagePointsLastBattle(self, oobid, tree, points):
        self.__EnsureBattleDictExists(oobid, tree)
        tree.nodes[oobid]['BattleDict']['damagepoints_lastbattle_temponly'] = points
    def _GetDamagePointsLastBattle(self, oobid, tree):
        self.__EnsureBattleDictExists(oobid, tree)
        return tree.nodes[oobid]['BattleDict'].get('damagepoints_lastbattle_temponly', 0)

    def _SetStrength(self, oobid, tree, mtgvlist):
##        if oobid == 'axis_644808740011804750001045191089':
##            print '-'*20
##            '_SetStrength mtgvlist', oobid, mtgvlist
##            __import__("traceback").print_stack(limit=6)
##            print '='*30

        self.__EnsureBattleDictExists(oobid, tree)
        tree.nodes[oobid]['BattleDict']['strength'] = mtgvlist
    def _GetStrength(self, oobid, tree):
        self.__EnsureBattleDictExists(oobid, tree)
        if self._ooboverlay is None:
            return tree.nodes[oobid]['BattleDict'].get('strength', [0,0,0,0])
        if oobid in self._ooboverlay:
            if self._ooboverlay[oobid]['BattleDict'] is None:
                return None
            return self._ooboverlay[oobid]['BattleDict'].get('strength', [0,0,0,0])
#        return tree.nodes[oobid]['BattleDict'].get('initial_strength', [0,0,0,0])
        return None

    def _GetOverlayAttribute(self, oobid, attr):
        try:
            return self._ooboverlay[oobid][attr]
        except:
            return None

    def _GetStrengthTime(self, oobid, tree):
        return self._GetOverlayAttribute(oobid, 'BattleDict_time')

    def _GetExperienceTime(self, oobid, tree):
        return self._GetOverlayAttribute(oobid, 'experience_time')

    def _GetFitnessTime(self, oobid, tree):
        return self._GetOverlayAttribute(oobid, 'fitness_time')

    def _SetCasualtiesIncurredTotal(self, oobid, tree, mtgvlist):
        self.__EnsureBattleDictExists(oobid, tree)
        tree.nodes[oobid]['BattleDict']['casualties_incurred_total'] = mtgvlist

    def _GetCasualtiesIncurredTotal(self, oobid, tree):
        self.__EnsureBattleDictExists(oobid, tree)
        if self._ooboverlay is None:
            return tree.nodes[oobid]['BattleDict'].get('casualties_incurred_total', [0,0,0,0])
        if oobid in self._ooboverlay:
            if self._ooboverlay[oobid]['BattleDict'] is None:
                return None
            return self._ooboverlay[oobid]['BattleDict'].get('casualties_incurred_total', [0,0,0,0])
        return [0,0,0,0]

    def _SetCasualtiesIncurredLastBattle(self, oobid, tree, mtgvlist):
        self.__EnsureBattleDictExists(oobid, tree)
        tree.nodes[oobid]['BattleDict']['casualties_incurred_lastbattle'] = mtgvlist

    def _GetCasualtiesIncurredLastBattle(self, oobid, tree):
        self.__EnsureBattleDictExists(oobid, tree)
        if self._ooboverlay is None:
            return tree.nodes[oobid]['BattleDict'].get('casualties_incurred_lastbattle', [0,0,0,0])
        if oobid in self._ooboverlay:
            if self._ooboverlay[oobid]['BattleDict'] is None:
                return None
            return self._ooboverlay[oobid]['BattleDict'].get('casualties_incurred_lastbattle', [0,0,0,0])
        return [0,0,0,0]

    def _SetCasualtiesCausedTotal(self, oobid, tree, mtgvlist):
        self.__EnsureBattleDictExists(oobid, tree)
        tree.nodes[oobid]['BattleDict']['casualties_caused_total'] = mtgvlist
    def _GetCasualtiesCausedTotal(self, oobid, tree):
        self.__EnsureBattleDictExists(oobid, tree)
        if self._ooboverlay is None:
            return tree.nodes[oobid]['BattleDict'].get('casualties_caused_total', [0,0,0,0])
        if oobid in self._ooboverlay:
            if self._ooboverlay[oobid]['BattleDict'] is None:
                return None
            return self._ooboverlay[oobid]['BattleDict'].get('casualties_caused_total', [0,0,0,0])
        return [0,0,0,0]

    def _SetCasualtiesCausedLastBattle(self, oobid, tree, mtgvlist):
        self.__EnsureBattleDictExists(oobid, tree)
        tree.nodes[oobid]['BattleDict']['casualties_caused_lastbattle'] = mtgvlist
    def _GetCasualtiesCausedLastBattle(self, oobid, tree):
        self.__EnsureBattleDictExists(oobid, tree)
        if self._ooboverlay is None:
            return tree.nodes[oobid]['BattleDict'].get('casualties_caused_lastbattle', [0,0,0,0])
        if oobid in self._ooboverlay:
            if self._ooboverlay[oobid]['BattleDict'] is None:
                return None
            return self._ooboverlay[oobid]['BattleDict'].get('casualties_caused_lastbattle', [0,0,0,0])
        return [0,0,0,0]

    def _StoreInitialExperienceStrengthEtc(self):
##        print "storing InitialExperienceStrengthEtc"
        for tree in (self.oobtreeAllies, self.oobtreeAxis):
            for attrs in tree.nodes.values():
                attrs['initial_experience'] = attrs['experience']
                attrs['initial_fitness'] = attrs['fitness']
                if 'BattleDict' in attrs:
                    attrs['BattleDict']['initial_strength'] = attrs['BattleDict']['strength']
##                print attrs['initial_experience']

class Oob_OLDSTYLE(OobCommon_ImplementationUsingTwoTreesAndDicts):
    def __init__(self, trooptypesmgr=None):
        OobCommon_ImplementationUsingTwoTreesAndDicts.__init__(self)
        self.metooobmappings = MeToOobMappings_OLDSTYLE(self)
        self.trooptypesmgr = trooptypesmgr

    def _ClearAnyCachesCosLoad(self): pass
    def _InvalidateMountednessCacheEntry(self, oobid): pass

    def _SetPoints(self, oobid, tree, points): pass
    def _GetPoints(self, oobid, tree):         return 0

    def _GetSignals(self, oobid, tree): return {'Orders': {}, 'Reports': {}}
    def _SetSignals(self, oobid, tree, signalsdict): pass

    def _GetOfficerRank(self, oobid, tree): return 'Captain'
    def _GetOfficerAggressiveness(self, oobid, tree): return 'Bold'
    def _GetOfficerEfficiency(self, oobid, tree): return 'Average'
    def _GetOfficerLeadership(self, oobid, tree): return 'Good'
    def _GetMeAppearsAfterTurn(self, oobid, tree): return 0
    def _ClearMeAppearsAfterTurn(self, oobid, tree): return
    def _GetInitialMeReadiness(self, oobid, tree): return 0
    def _GetInitialMeName(self, oobid, tree): return ''
    def _GetSupplyAmmo(self, oobid, tree): return 0
    def _GetInitialDirection(self, oobid, tree): return 'W'
    def _GetSupplyBasics(self, oobid, tree): return 0
    def _GetSupplyFuel(self, oobid, tree): return 0

    def _GetFitness(self, oobid, tree): return 0
    def _GetNumberOfMen(self, oobid, tree): return 0
##    def _GetCanHoldNumberOfMen(self, oobid, tree): return 0
    def _GetCarryingCapacity(self, oobid, tree): return 0
##    def _GetHowMuchCanTow(self, oobid, tree): return 0
##    def _GetHowHardToTow(self, oobid, tree): return 0
##
##    def _GetSquadSize(self, oobid, tree):  return 0
##    def _GetSquadCapacity(self, oobid, tree):  return 0

    def _GetOffRoadAbility(self, oobid, tree): return 'fair'

    def _GetTransportType(self, oobid, tree): return '' # ????????????????
    def _SetTransportType(self, oobid, tree, transporttype):  pass
    def _SetInitialMeReadiness(self, oobid, tree, value): pass


    def GetTroopType(self, oobid):
        # 'Old style oob have a totally replaced GetTroopType method cos self.DetermineWhichTreeFromOobNodeId(oobid) won't work'
        # tree = self.DetermineWhichTreeFromOobNodeId(oobid)    # this won't work
        return self._GetTroopType(oobid, tree=None)
    def _GetTroopType(self, oobid, tree):
        # TODO get all code that already calcs me to troop type to call this function instead
        # move functionality into this class.

        OldPieceTypeToTroopType = {
            'AD': 'Infantry',
            'AR': 'Infantry',
            'AT': 'Armor_Churchhill',
            'AB': 'Infantry',
            'AC': 'Infantry',
            'AP': 'Infantry',
            'GD': 'Infantry',
            'GR': 'Infantry',
            'GT': 'Armor_Panzer',
            'GB': 'Infantry',
            'GC': 'Infantry',
            'GP': 'Infantry'
        }
        oobid = oobid[0: 2]
        return OldPieceTypeToTroopType[oobid]

##        def __PieceIdToPieceType(self, meid):
##            # OLD STYLE - supports MeIdToTroopType()
##            oobid = meid
##            return oobid[0: 2]
##
##        def __PieceTypeToTroopType(self, piecetype):
##            # OLD STYLE - supports MeIdToTroopType()
##            """
##            The trooplist currently has one item and for the moment we
##            take the first troop type...later we find the slowest troop type etc.
##            HOWEVER this future solution is flawed since who is in each troop group will be
##            totally dependant on scenario oobtrees.
##            """
##            trooplist = self.PieceTypeToTroopTypes[piecetype]
##            return trooplist[0]
##        def MeIdToTroopTypes(self, meid, fastmove=1):      # overridden
##            if self.oob.IsMounted(meid) and fastmove:
##                trooptype = 'Truck_Basic'
##            else:
##                piecetype = self.__PieceIdToPieceType(meid)
##                trooptype = self.__PieceTypeToTroopType(piecetype)
##            return [trooptype]

        raise RuntimeError("Cannot get troop type of old style scenario")

    def _SetTroopType(self, oobid, tree, trooptype): pass

    def _GetOobName(self, oobid, tree):
        if not 'bigname' in tree.nodes[oobid]:
            return ''
        return tree.nodes[oobid]['bigname']

    def _GetOfficerRank(self, oobid, tree):
        return ''

    def _GetOfficerName(self, oobid, tree):
        return oobid

    def _IsHq(self, oobid, tree):
        return 1   # all nodes are hq nodes in old style scenarios

    def _IsRole(self, oobid, tree):
        return tree.nodes[oobid]['role']  #OLD

    def _GetDelay(self, oobid, tree):
        return tree.nodes[oobid]['delay']  #OLD

    def _SetDelay(self, oobid, tree, delay):
        tree.nodes[oobid]['delay'] = delay

    def _GetStartingCoord(self, oobid, tree):
        return tree.nodes[oobid]['coord']  #OLD

    def _SetExperience(self, oobid, tree, experience):
        pass

    def _GetExperience(self, oobid, tree):
        return 0


    def RankingHqAboveMe(self, meid):
        oobid = meid
        return self.GetParent(oobid)

    def RankingHqInMe(self, meid):
        return meid

    def DetermineSideFromOobNodeId(self, oobid):
        if oobid[0] == 'A':
            side = 'allied'
        elif oobid[0] == 'G':
            side = 'axis'
        else:
            msg = "DetermineSideFromOobNodeId: Couldn't determine side of "+oobid
            raise msg
        return side

##    def IsMounted(self, meid):
##        oobid = meid
##
##        tree = self.DetermineWhichTreeFromOobNodeId(oobid)
##        if not tree:
##            raise 'Scenario IsMounted cannot identify side of oob node '+oobid
##        if 'motorized'in tree.nodes[oobid]:
##            return tree.nodes[oobid]['motorized']
##        else:
##            return 0
    def IsMounted(self, meid):
        oobid = meid

        tree = self.DetermineWhichTreeFromOobNodeId(oobid)
        if not tree:
            raise RuntimeError('Scenario IsMounted cannot identify side of oob node '+oobid)
        if 'motorized'in tree.nodes[oobid]:
            fullymounted = tree.nodes[oobid]['motorized']
            if fullymounted:
                listoftranportingoobids = [oobid]
                listofnonmountedremainingoobids = []
            else:
                listoftranportingoobids = []
                listofnonmountedremainingoobids = [oobid]
        else:
                fullymounted = 0
                listoftranportingoobids = []
                listofnonmountedremainingoobids = [oobid]
        return fullymounted, listoftranportingoobids, listofnonmountedremainingoobids


    def _SetDamagePointsLastBattle(self, oobid, tree, points):
        pass
    def _GetDamagePointsLastBattle(self, oobid, tree):
        return 0

##    def __getattr__(self, attr):
##        print 'get attr', attr
##        return 0
##    def __setattr__(self, attr, val):
##        pass

    def _SetStrength(self, oobid, tree, mtgvlist):                      pass
    def _GetStrength(self, oobid, tree):                                return [1,0,0,0]
    def _SetCasualtiesIncurredTotal(self, oobid, tree, mtgvlist):       pass
    def _GetCasualtiesIncurredTotal(self, oobid, tree):                 return None
    def _SetCasualtiesIncurredLastBattle(self, oobid, tree, mtgvlist):  pass
    def _GetCasualtiesIncurredLastBattle(self, oobid, tree):            return None
    def _SetCasualtiesCausedTotal(self, oobid, tree, mtgvlist):         pass
    def _GetCasualtiesCausedTotal(self, oobid, tree):                   return None
    def _SetCasualtiesCausedLastBattle(self, oobid, tree, mtgvlist):    pass
    def _GetCasualtiesCausedLastBattle(self, oobid, tree):              return None


    def _GetOrderSkill(self, oobid, tree): return 0
    def _GetCombatSkill(self, oobid, tree): return 0
    def _GetRallySkill(self, oobid, tree): return 0
    def _GetStealthSkill(self, oobid, tree): return 0

    def _SetOrderSkill(self, oobid, tree, level): pass
    def _SetCombatSkill(self, oobid, tree, level): pass
    def _SetRallySkill(self, oobid, tree, level): pass
    def _SetStealthSkill(self, oobid, tree, level): pass

    def _GetImmobilized(self, oobid, tree): return 0
    def _SetImmobilized(self, oobid, tree, immobilized): pass

    def _GetBogged(self, oobid, tree): return 0
    def _SetBogged(self, oobid, tree, bogged): pass

    def _GetGunDestroyed(self, oobid, tree): return 0
    def _SetGunDestroyed(self, oobid, tree, gundestroyed): pass

    def _GetDugIn(self, oobid, tree): return 0
    def _SetDugIn(self, oobid, tree, dugin): pass

############################################## OOBTree ####################

class OOBTree:
    def __init__(self, nodes = None, relations = None, lamdaIsRole=None, lambdaGetDelay=None, lambdaIsHq=None):
        if nodes:
            self.nodes = copy.deepcopy(nodes)
        else:
            self.nodes = {}

        self.relations = RelationshipManager()

        if relations:
            for line in relations:
                self.relations.AddRelationship(line[0], line[1], 'parent')
        self._calcRoot()

        if lamdaIsRole:
            self.lamdaIsRole = lamdaIsRole
        else:
            self.lamdaIsRole = self.__IsRoleDefaultLambda

        if lambdaGetDelay:
            self.lambdaGetDelay = lambdaGetDelay
        else:
            self.lambdaGetDelay = self.__GetDelayDefaultLambda

        if lambdaIsHq:
            self.lambdaIsHq = lambdaIsHq
        else:
            self.lambdaIsHq = self.__IsRoleDefaultLambda  # should be ok.

    def AddRelationshipFromOobidToParent(self, oobid, parentoobid):
        self.relations.AddRelationship(parentoobid, oobid, 'parent')
    def RemoveOobid(self, oobid):
        del self.nodes[oobid]
        relations = self.relations.FindObjects(From=None, To=oobid, RelId='parent')
        assert len(relations) > 0, 'No parent relation for oobid'
        parentofoobid = relations[0]
        self.relations.RemoveRelationships(parentofoobid, oobid, 'parent')

    def __IsRoleDefaultLambda(self, oobid):
        return self.nodes[oobid]['role'] == 1
    def __GetDelayDefaultLambda(self, oobid):
        return self.nodes[oobid]['delay']

    def _calcRoot(self):
        if not list(self.nodes.keys()):
            self.root = ''
            return
        randompiece = list(self.nodes.keys())[0]
        ancestors = self.FindAncestors(randompiece)
        if not ancestors:
            self.root = randompiece
        else:
            self.root = ancestors[-1]

    def FindChildren(self, oobid):
        return self.relations.FindObjects(From = oobid, To = None, RelId = 'parent')

    def FindParent(self, oobid):
        return self.relations.FindObject(From = None, To = oobid, RelId = 'parent')

    def FindAncestors(self, oobid):
        ancestors = []
        while 1:
            parent = self.FindParent(oobid)
            if not parent:
                break
            ancestors.append(parent)
            oobid = parent
        return ancestors

    def FindDescendants(self, oobid):
        truelambda = lambda oobid: 1
        allnodes = self.FindFilteredDescendants(oobid, truelambda)
        return allnodes[1:]


    def FindFilteredDescendants(self, oobid, filterlambda):
        if oobid == '':
            descendants = []
        elif filterlambda(oobid):
            descendants = [oobid]
        else:
            descendants = []
        children = self.FindChildren(oobid)
        for child in children:
            rez = self.FindFilteredDescendants(child, filterlambda)
            if rez:
                descendants+=rez
        return descendants

    def Root(self):
        return self.root

    def FindRoot(self):
        self._calcRoot()
        return self.Root()


    def FindAllRoles(self):
        filter = self.lamdaIsRole   # filter = lambda(oobid): self.nodes[oobid]['role'] == 1
        return self.FindFilteredDescendants(self.Root(), filter)

    def FindAllHqs(self):
        filter = self.lambdaIsHq
        return self.FindFilteredDescendants(self.Root(), filter)

    def CumulativeDelay(self, fromoobid, tooobid):
        Log('OOBTree.CumulativeDelay', lambda: 'PARAMETERS fromoobid=%s, tooobid=%s'%(fromoobid, tooobid))
        if fromoobid == tooobid:
            return 0
        ancestorlist = self.FindAncestors(fromoobid)
        if tooobid in ancestorlist:

            # Leave out ancestors including and after 'tooobid'
            pos = ancestorlist.index(tooobid)
            ancestorlist = ancestorlist[: pos]

            delay = self.lambdaGetDelay(fromoobid)  #delay = self.nodes[fromoobid]['delay']
            Log('OOBTree.CumulativeDelay', lambda: ' delay from myself %s is %d'%(fromoobid, delay))
            for oobid in ancestorlist:
                delaycomponent = self.lambdaGetDelay(oobid)
                if delaycomponent in (motionconstants.NO_COMPATIBLE_SIGNAL_PAIRS, motionconstants.INFINITE_DELAY):
                    delay = delaycomponent
                    break
                delay += delaycomponent
                Log('OOBTree.CumulativeDelay', lambda: ' adding delay of ancestor %s delay is now %d'%(oobid, delay))
            Log('OOBTree.CumulativeDelay', lambda: 'ancestors of %s are %s, delay=%d'%(fromoobid, str(ancestorlist), delay))
            return delay
        # Try looking the other way
        descendantslist = self.FindDescendants(fromoobid)
        if tooobid in descendantslist:
            return self.CumulativeDelay(tooobid, fromoobid)

        # Not found - no path between the two oobids
        msg = 'CumulativeDelay no path from %s to %s'%(fromoobid, tooobid)
        #raise msg

        # TODO FUDGE!!!!!!

        # Visibility isue for roles not ancestral to fromoobid
        # Should in fact never get this situation since visibilty stage
        # of resolver should filter these events out
        return 0

##    def GetOOBEvents(self):
##        dbg = []
##        dbg.append('getting oob events...')
##        for oobid, node in self.nodes.iteritems():
##            if 'needoobevent' in node and node['needoobevent'] == 1:
##                continue
##            dbg.append('this node needs an oobevent %s experience = %s'%(oobid, node['experience']))
##        print "\n".join(dbg)
##        return []



import unittest

##def EnsureScenarioPath():
##    scenariofilespath = os.path.join('..', 'Scenarios')
##    if not scenariofilespath in sys.path:
##        sys.path.append(scenariofilespath)

class TestCase00(unittest.TestCase):
    def setUp(self):
        """
        Ok to access ['coord'] directly cos old 1d scenario module.
        """

## IMPORT TECHNIQUE DEPRECIATED
##        EnsureScenarioPath()
##        module = __import__('scenario1')
##        self.t = OOBTree(module.allies, module.alliedparentrelations)

## EVEN OLDER IMPORT TECHNIQUE DEPRECIATED
##        from scenario1 import allies, alliedparentrelations
##        self.t = OOBTree(allies, alliedparentrelations)

        adict = utilcc.ImportScenarioFile('scenario1')
        self.t = OOBTree(adict['allies'], adict['alliedparentrelations'])

    def checkBasicTree(self):
        t = self.t
        assert t.FindChildren('AD1') == ['AR1', 'AR2', 'AT1']
    def checkTreeChildren02(self):
        t = self.t
        kids = self.t.relations.FindObjects(From = 'AD1', To = None, RelId = 'parent')
        #print kids
        assert kids == ['AR1', 'AR2', 'AT1']
        assert t.FindChildren('AD1') == ['AR1', 'AR2', 'AT1']
    def checkTreeParent01(self):
        t = self.t
        parents = self.t.relations.FindObjects(From = None, To = 'AT1', RelId = 'parent')
        #print parents
        assert parents == ['AD1']
        assert t.FindParent('AT1') == 'AD1'
    def checkModifyNodeWithoutAffectingSourceData(self):
        t = self.t
        regiment = t.nodes['AR1']
        #print regiment['coord']
        regiment['coord'] = 6
        #print regiment['coord']
        #print regiment
        #print t.nodes['AR1']

        #t.MoveNodeToCoord('AR1', 7) # replaced method call with actual ref to inner data, since method not being called by anyone else except this unit test.
        t.nodes['AR1']['coord'] = 7

        assert t.nodes['AR1']['coord']
        #print t.nodes['AR1']

        ##        from scenario1 import allies, alliedparentrelations
        ##        t2 = OOBTree(allies, alliedparentrelations)

## IMPORT TECHNIQUE DEPRECIATED
##        module = __import__('scenario1')
##        t2 = OOBTree(module.allies, module.alliedparentrelations)

        adict = utilcc.ImportScenarioFile('scenario1')
        t2 = OOBTree(adict['allies'], adict['alliedparentrelations'])

        assert t2.nodes['AR1']['coord'] == 15

    def checkAncestors(self):
        t = self.t
        ac1ancestors = t.FindAncestors('AC1')
        #print ac1ancestors
        assert ac1ancestors == ['AB1', 'AR1', 'AD1']
        ab1ancestors = t.FindAncestors('AB1')
        assert ab1ancestors == ['AR1', 'AD1']
        ad1descendants = t.FindDescendants('AD1')
        #print 'AD1 descendants: ', ad1descendants
        ab1descendants = t.FindDescendants('AB1')

        #assert ab1descendants == ['AC1', 'AC2', 'AC3', 'AC4', 'AP1']
        assert len(ab1descendants) == 5
        for oobid in ['AC1', 'AC2', 'AC3', 'AC4', 'AP1']:
            assert oobid in ab1descendants

        ab2descendants = t.FindDescendants('AB2')
        #print 'AB2 descendants: ', ab2descendants
        assert ab2descendants == []

    def checkCumulativeDelays01(self):
        t = self.t
        assert t.CumulativeDelay('AR1', 'AD1') == 60
        assert t.CumulativeDelay('AD1', 'AR1') == 60
        assert t.CumulativeDelay('AC1', 'AD1') == 90
        assert t.CumulativeDelay('AD1', 'AC1') == 90
        assert t.Root() == 'AD1'
        assert t.FindAllRoles() == ['AD1', 'AR1', 'AB1', 'AB2', 'AT1']
        #print 'Now for some CumulativeDelays' + '-'*40
        #print 'Delay AR1 to AD1: ', t.CumulativeDelay('AR1', 'AD1')
        #print 'Delay AD1 to AR1: ', t.CumulativeDelay('AD1', 'AR1')
        #print 'Delay AC1 to AD1: ', t.CumulativeDelay('AC1', 'AD1')
        #print 'Delay AD1 to AC1: ', t.CumulativeDelay('AD1', 'AC1')
        #print 'Root is: ', t.Root()
        #print 'All Roles are: ', t.FindAllRoles()



class TestCase03(unittest.TestCase):
    def setUp(self):
        self.oob = Oob_NEWSTYLE()

## IMPORT TECHNIQUE DEPRECIATED
##        EnsureScenarioPath()
##        module = __import__('scenario30')
##        self.oob.LoadFromModule(module)

        adict = utilcc.ImportScenarioFile('scenario30')
        self.oob.LoadFromDict(adict)
        self.oob.PostProcessOOBTree()

    def checkMeMappingsBuild(self):
        result = self.oob.metooobmappings.GetAllMeIds()
        #print result
        assert len(result) == 2
        #print self.oob.metooobmappings.MeIdToOobIds('me_1')
        #print self.oob.metooobmappings.MeIdToOobIds('me_2')

        #assert self.oob.metooobmappings.MeIdToOobIds('me_1') == ['axis_5491036892712.11', 'axis_9971036892669.34', 'axis_6171036892713.66']
        result = self.oob.metooobmappings.MeIdToOobIds('me_1')
        assert len(result) == 3
        for oobid in ['axis_5491036892712.11', 'axis_9971036892669.34', 'axis_6171036892713.66']:
            assert oobid in result

        assert self.oob.metooobmappings.MeIdToOobIds('me_2') == ['axis_1461036892667.5']

        assert self.oob.metooobmappings.GetSideOfMe('me_1') == 'axis'
        assert self.oob.metooobmappings.GetSideOfMe('me_2') == 'axis'

    def checkRankingInHQ_01(self):
        resultoobid = self.oob.RankingHqInMe('me_1')
        #print resultoobid
        assert resultoobid == 'axis_9971036892669.34'

        resultoobid = self.oob.RankingHqInMe('me_2')
        #print resultoobid
        assert resultoobid == 'axis_1461036892667.5'

    def checkRankingAboveHQ_02(self):
        resultoobid = self.oob.RankingHqAboveMe('me_1')
        #print resultoobid
        assert resultoobid == 'default'

        resultoobid = self.oob.RankingHqAboveMe('me_2')
        #print resultoobid
        assert resultoobid == 'axis_9971036892669.34'

class TestCase04(unittest.TestCase):
    def setUp(self):

        from trooptypes import TroopTypeMgr_V1
        trooptypesmgr=TroopTypeMgr_V1()

        self.oob = Oob_NEWSTYLE( trooptypesmgr=trooptypesmgr )
        trooptypesmgr.oob = self.oob   # Hack wire up.


## IMPORT TECHNIQUE DEPRECIATED
##        EnsureScenarioPath()
##        module = __import__('scenario31')
##        self.oob.LoadFromModule(module)

        adict = utilcc.ImportScenarioFile('scenario31')
        self.oob.LoadFromDict(adict)
        self.oob.PostProcessOOBTree()

    def checkMeMappingsBuild(self):
        result = self.oob.metooobmappings.GetAllMeIds()
        #print result
        assert len(result) == 12
##        print self.oob.metooobmappings.MeIdToOobIds('me_1')
##        print self.oob.metooobmappings.MeIdToOobIds('me_2')
##        print self.oob.metooobmappings.MeIdToOobIds('me_3')
        #assert self.oob.metooobmappings.MeIdToOobIds('me_1') == ['axis_5491036892712.11', 'axis_9971036892669.34', 'axis_6171036892713.66']
        #assert self.oob.metooobmappings.MeIdToOobIds('me_2') == ['axis_1461036892667.5']

        assert len(self.oob.metooobmappings.MeIdToOobIds('me_1')) == 3
        assert len(self.oob.metooobmappings.MeIdToOobIds('me_2')) == 1 # G not S relation
        assert len(self.oob.metooobmappings.MeIdToOobIds('me_3')) == 1 # G not S relation

        #print self.oob.metooobmappings.MeIdToListOfOobIds('me_1')
        #print self.oob.metooobmappings.MeIdToListOfOobIds('me_2')
        #print self.oob.metooobmappings.MeIdToListOfOobIds('me_3')
        assert len(self.oob.metooobmappings.MeIdToListOfOobIds('me_1')) == 3
        assert len(self.oob.metooobmappings.MeIdToListOfOobIds('me_2')) == 7
        assert len(self.oob.metooobmappings.MeIdToListOfOobIds('me_3')) == 3

    def checkMePointsValueSize_01(self):
        #print self.oob.metooobmappings._GetMeCompositePointsValue('me_3')
        assert self.oob.metooobmappings._GetMeCompositePointsValue('me_3') == 45
        assert self.oob.metooobmappings.GetMeCompositeSize('me_3') == 1

        #assert self.oob.metooobmappings.GetMeCompositeSizeAsString('me_3') == 'Platoon'
        size = self.oob.metooobmappings.GetMeCompositeSize('me_3')
        assert self.oob.conversions.ConvertMeCompositePointsSizeToString('me_3', size) == 'Platoon'

    def checkIncOobExperienceAndGetCompositeExperience(self):
        assert self.oob.metooobmappings._GetMeCompositeExperienceRawTotal('me_3') == 140
        assert self.oob.metooobmappings.GetMeCompositeExperience('me_3') == 46 # i.e. 140/3  cos 3 troops with 5 experience points between them
        oobids = self.oob.metooobmappings.MeIdToListOfOobIds('me_3')
        assert len(oobids) == 3

        oobid = oobids[0]
        self.oob.SetExperience( oobid, self.oob.GetExperience(oobid) + 10 )
        assert self.oob.metooobmappings._GetMeCompositeExperienceRawTotal('me_3') == 150
        assert self.oob.metooobmappings.GetMeCompositeExperience('me_3') == 50  # average

        oobid = oobids[1]
        self.oob.SetExperience( oobid, self.oob.GetExperience(oobid) + 7 )
        assert self.oob.metooobmappings._GetMeCompositeExperienceRawTotal('me_3') == 157
        assert self.oob.metooobmappings.GetMeCompositeExperience('me_3') == 157/3 # average

    def checkRepr_Basic(self):
        str = repr(self.oob)
        self.oob.LoadFromReprStr(str)

    def checkRepr_Advanced(self):
        oobids = self.oob.metooobmappings.MeIdToListOfOobIds('me_3')
        oobid = oobids[0]

        oldexperience = self.oob.GetExperience(oobid)
        oldcompositeexperience = self.oob.metooobmappings._GetMeCompositeExperienceRawTotal('me_3')

        self.oob.SetExperience( oobid, oldexperience + 10 )
        assert self.oob.metooobmappings._GetMeCompositeExperienceRawTotal('me_3') == oldcompositeexperience+10
        str = repr(self.oob)

        oob2 = Oob_NEWSTYLE()
        oob2.LoadFromReprStr(str)
        assert oob2.metooobmappings._GetMeCompositeExperienceRawTotal('me_3') == oldcompositeexperience+10

    def checkOobUnitAttributes_01(self):
        """
        'axis_181037599056.83': {   'HQ': 1,
        'HqDict': {   'Extras': {   'combat': 2,
                                    'command': 1,
                                    'morale': 1,
                                    'stealth': 2},
                      'Officer': {   'aggressiveness': 'Bold',
                                     'efficiency': 'Average',
                                     'leadership': 'Good',
                                     'name': 'Kurt Vonnegut',
                                     'rank': 'Captain'},
                      'Signals': {   'Orders': {   'Radio (A)': 'good',
                                                   'Radio (C)': 'bad',
                                                   'Runner': 'good'},
                                     'Reports': {   'Runner': 'bad'}},
                      'delay': 1,
                      'role': 1},
        'ME': 1,
        'MeDict': {   'Supply': {   'ammo': 600,
                                    'basics': 500,
                                    'fuel': 400},
                      'appearsafterturn': 0,
                      'initialreadiness': 20,
                      'mename': 'Company B Halftracks'},
        'carryingcapacity': 6,
        'coord': (96, 416),
        'experience': 20,
        'fitness': 70,
        'name': 'Comany B',
        'numberofmen': 34,
        'offroadability': 'Fair',
        'points': 25,
        'transporttype': 'Motorized',                           # OBSOLETE FOR V40 scenarios
        'trooptype': 'Halftrack_Light'},
        """
        oobid = 'axis_181037599056.83'
        assert self.oob.GetExperience(oobid) == 20
        #assert self.oob.metooobmappings.GetMeCompositeExperience('me_3') == 5

        assert self.oob.GetTroopType(oobid) == 'Halftrack_Light'
        assert self.oob.GetTransportType(oobid) == 'Motorized'  # OBSOLETE FOR V40 scenarios
        assert self.oob.GetPoints(oobid) == 25
        assert self.oob.GetOffRoadAbility(oobid) == 'Fair'
        assert self.oob.GetNumberOfMen(oobid) == 34
        assert self.oob.GetOobName(oobid) == 'Comany B'
        assert self.oob.GetFitness(oobid) == 70
        assert self.oob.GetCarryingCapacity(oobid) == 6
        assert self.oob.GetStartingCoord(oobid) == (96, 416)
        assert self.oob.GetSupplyAmmo(oobid) == 600
        assert self.oob.GetSupplyBasics(oobid) == 500
        assert self.oob.GetSupplyFuel(oobid) == 400

        assert self.oob.GetMeAppearsAfterTurn(oobid) == 0
        assert self.oob.GetInitialMeReadiness(oobid) == 20
        assert self.oob.GetInitialMeName(oobid) == 'Company B Halftracks'

        #print self.oob.GetDelay(oobid)
        assert self.oob.GetDelay(oobid) == 0
        assert self.oob.IsRole(oobid) == 1
        assert self.oob.IsHq(oobid) == 1
        assert self.oob.GetOfficerName(oobid) == 'Kurt Vonnegut'
        assert self.oob.GetOfficerRank(oobid) == 'Captain'
        assert self.oob.GetOfficerAggressiveness(oobid) == 'Bold'
        assert self.oob.GetOfficerEfficiency(oobid) == 'Average'
        assert self.oob.GetOfficerLeadership(oobid) == 'Good'

        assert self.oob.GetSignals(oobid) == {   'Orders': {   'Radio (A)': 'good',

                      'Radio (C)': 'bad',
                                                   'Runner': 'good'},
                                     'Reports': {   'Runner': 'bad'}}

    def checkMeDerivedAndDerivedCompositeAttributes(self):
        """
        'experience': 20,
        'fitness': 70,

            'experience': 20,
            'fitness': 30,

            'experience': 100
,
            'fitness': 100,

        Composite of above info for me_3  headed by 'axis_181037599056.83'
            140/3 =  46   experience
            200/3 = 66    fitness
        """
        #print 'Comany B me is', self.oob.metooobmappings.GetMeIdForName('Company B Halftracks')
        assert 'me_3' == self.oob.metooobmappings.GetMeIdForName('Company B Halftracks')

        experience = self.oob.metooobmappings.GetMeCompositeExperience('me_3')
        #print experience
        assert experience == 46

        fitness = self.oob.metooobmappings.GetMeCompositeFitness('me_3')
        #print fitness
        assert fitness == 66

        pointsvalue = self.oob.metooobmappings._GetMeCompositePointsValue('me_3')
        pointssize = self.oob.metooobmappings.GetMeCompositeSize('me_3')
        assert pointssize == 1
        #print 'pointsvalue for me_3 Company B Halftracks', pointsvalue
        assert pointsvalue == 45

# Valid test, but function not used by anyone else.
##        nummen = self.oob.metooobmappings.GetMeCompositeNumberofmen('me_3')
##        #print 'Composite Number of men', nummen
##        assert nummen == 37


        # Check composite attributes of 'Russian 10th Army', scenario 31

        meid10thArmy = self.oob.metooobmappings.GetMeIdForName('Russian 10th Army')
        #print 'Russian 10th Army', meid
        hqoobid = self.oob.RankingHqInMe(meid10thArmy)
        assert hqoobid == 'allied_1771038189604.58'
        # Ensure 4th Troopers in there
        assert 'allied_890626726695036030001041985938' in self.oob.metooobmappings.GetMeRecursiveListOfOobidsExcludingMes(meid10thArmy)

##        nummen = self.oob.metooobmappings.GetMeCompositeNumberofmen(meid10thArmy)
##        #print nummen
##        assert nummen == 106
##
##        numvehicles = self.oob.metooobmappings.GetMeCompositeNumberofVEHICLES(meid10thArmy)
##        #print 'Composite Number of vehicles', numvehicles
##        assert numvehicles == 4
##
##        numarmor = self.oob.metooobmappings.GetMeCompositeNumberofARMOR(meid10thArmy)
##        #print 'Composite Number of armor', numarmor
##        assert numarmor == 7
##
##        numguns = self.oob.metooobmappings.GetMeCompositeNumberofGUNS(meid10thArmy)
##        #print 'Composite Number of guns', numguns
##        assert numguns == 5
##
##        # meidLoneWolf is all alone so troop type is not 1 ARMOR but simply a HQ
##        meidLoneWolf = self.oob.metooobmappings.GetMeIdForName('Lone Wolf')
##        numarmor = self.oob.metooobmappings.GetMeCompositeNumberofARMOR(meidLoneWolf)
##        #print 'Composite Number of armor LoneWolf', numarmor
##        assert numarmor <> 1
##        assert numarmor == 0


        # See terrainmanager test case 05 checkMeCompositeAttributes
        #
        # trooptype       ====> terrainmgr.GetPieceNormalTroopTypeNow('me_3',...
        # speed (normal)  ====> terrainmgr.GetPieceNormalSpeedNow('me_3',...
        # transporttype   ====> terrainmgr.GetPieceTransportTroopTypeNow('me_3',...
        # transport speed ====> terrainmgr.GetPieceTransportSpeedNow('me_3',...
        # offroad ability ====> terrainmgr.GetMeCompositeOffroadAbilityNow('me_3',...

        # Derived ME attribute (but not composite) ##############
        #

        assert self.oob.metooobmappings.GetMeNameForMe('me_3') == 'Company B Halftracks'
        assert self.oob.metooobmappings.GetMeInitialReadiness('me_3') == 20
        assert self.oob.metooobmappings.GetMeInitialAmmo('me_3') == 600
        assert self.oob.metooobmappings.GetMeInitialBasics('me_3') == 500
        assert self.oob.metooobmappings.GetMeInitialFuel('me_3') == 400
        assert self.oob.metooobmappings.GetMeCommanderName('me_3') == 'Kurt Vonnegut'
        assert self.oob.metooobmappings.GetMeCommanderRank('me_3') == 'Captain'
        assert self.oob.metooobmappings.GetMeCommanderLeadership('me_3') == 'Good'
        assert self.oob.metooobmappings.GetMeCommanderEfficiency('me_3') == 'Average'
        assert self.oob.metooobmappings.GetMeCommanderAggressiveness('me_3') == 'Bold'
        assert self.oob.metooobmappings.GetMeSignals('me_3') == {
                                    'Orders': {   'Radio (A)': 'good',
                                                   'Radio (C)': 'bad',
                                                   'Runner': 'good'},
                                     'Reports': {   'Runner': 'bad'}}

    def checkMeIntrinsicAttributes(self):
        # extract all the intrinsic me info from the has dict.

        hasdict = {'mename':'Company A', 'readiness':50,
                   'ammo':50, 'basics':10, 'fuel':20 }

        assert hasdict['mename'] == 'Company A'
        assert hasdict['readiness'] == 50
        assert hasdict['ammo'] == 50
        assert hasdict['basics'] == 10
        assert hasdict['fuel'] == 20


##    def checkCalcCompatibleSignalsDict_01(self):
##        """
##            Telephone
##            Radio (A)
##            Radio (B)
##            Radio (C)
##            Vehicle
##            Motorcycle
##            Halftrack
##            Ski
##            Rider
##            Runner
##        """
##        hqoobid1 = 'allied_1771038189604.58'  # 'Russian 10th Army'
##        hqoobid2 = 'allied_4541038189652.26'  # '1st Motorized Company'
##        resultsignalsdict = self.oob.CalcCompatibleSignalsDict(fromhqoobid=hqoobid1,tohqoobid=hqoobid2)
##        #print 'Compatible signals', resultsignalsdict
##        assert resultsignalsdict == { 'Radio (B)': 'bad',
##                                      'Motorcycle': 'bad' }
##
##    def checkCalcCompatibleSignalsDict_02(self):
##        hqoobid1 = 'allied_1771038189604.58'  # 'Russian 10th Army'
##        hqoobid2 = 'allied_3121038189769.33'  # '2nd Motorized'
##        resultsignalsdict = self.oob.CalcCompatibleSignalsDict(fromhqoobid=hqoobid1,tohqoobid=hqoobid2)
##        #print 'Compatible signals', resultsignalsdict
##        assert resultsignalsdict == { 'Radio (C)': 'good',
##                                      'Motorcycle': 'bad' }
##
##    def checkCalcCompatibleSignalsDict_03(self):
##        hqoobid1 = 'axis_1461036892667.5'  # 'Company A Motorized Co.'
##        hqoobid2 = 'axis_9931036892680.99'  # 'Platoon1'
##        resultsignalsdict = self.oob.CalcCompatibleSignalsDict(fromhqoobid=hqoobid1,tohqoobid=hqoobid2)
##        #print 'Compatible signals', resultsignalsdict
##        assert resultsignalsdict == { 'Telephone': 'bad',
##                                      'Ski': 'bad',
##                                      'Rider':'good' }

class TestCase05(unittest.TestCase):
    def setUp(self):
        from trooptypes import TroopTypeMgr_V2

        trooptypesmgr = TroopTypeMgr_V2()

        self.oob = Oob_NEWSTYLE(trooptypesmgr)
        trooptypesmgr.oob = self.oob   # Hack wire up.

## IMPORT TECHNIQUE DEPRECIATED
##        EnsureScenarioPath()
##        module = __import__('scenario30points01')
##        self.oob.LoadFromModule(module)

        adict = utilcc.ImportScenarioFile('scenario30points01')
        self.oob.LoadFromDict(adict)
        self.oob.PostProcessOOBTree()

    def GetMeInfo(self, meid):
        mename = self.oob.metooobmappings.GetMeNameForMe(meid)
        pointvalue = self.oob.metooobmappings._GetMeCompositePointsValue(meid)
        return '%s %s pointsvalue %d' % (meid, mename, pointvalue)

    def checkMeNamesAllocatedAsRequired(self):
        assert self.oob.metooobmappings.GetMeIdForName('3rd Army') == 'me_3'
        assert self.oob.metooobmappings.GetMeIdForName('Brutalis') == 'me_6'
        assert self.oob.metooobmappings.GetMeIdForName('Big Sub2') == None
        assert self.oob.metooobmappings.GetMeIdForName('Big Sub') == None

    def checkRecursion01(self):
        rankingoobid = self.oob.RankingHqInMe('me_3')
        numoobids = len(self.oob.metooobmappings.GetRecursiveListOfOobidsExcludingMes(rankingoobid))
        #print numoobids
        assert numoobids == 0

    def checkRecursion02(self):
        ooblist = self.oob.metooobmappings.GetRecursiveListOfOobidsExcludingMes('axis_122555889341296580001040964619')
        pointsvalue = self.oob.metooobmappings._AddUpPointsForOobids(ooblist)
        #print 'BigSub', pointsvalue
        assert 61 == pointsvalue

        ooblist = self.oob.metooobmappings.GetRecursiveListOfOobidsExcludingMes('axis_101361108144105040001040965051')
        pointsvalue = self.oob.metooobmappings._AddUpPointsForOobids(ooblist)
        #print 'BigSub2', pointsvalue
        assert 6 == pointsvalue

    def checkMePointsValueSize_01(self):
        # 3rd Army should add up to something quite complex.
        meid = self.oob.metooobmappings.GetMeIdForName('3rd Army')
        #print '3rd Army', self.GetMeInfo(meid)
        #self.oob.metooobmappings._DumpMeRelations()
        #print 'self.oob.metooobmappings._GetMeCompositePointsValue(3rd Army)', self.oob.metooobmappings._GetMeCompositePointsValue(meid)
        self.assertEqual(self.oob.metooobmappings._GetMeCompositePointsValue(meid), 80)

    def checkMePointsValueSize_02(self):
        meid = self.oob.metooobmappings.GetMeIdForName('Brutalis')
        #print 'Brutalis:', self.GetMeInfo(meid)
        self.assertEqual(self.oob.metooobmappings._GetMeCompositePointsValue(meid), 50)


##
##    PUT TOGETHER WITH BRUCE, BUT THEN WE CHANGED OUR MINDS
##
##    class TestCase06(unittest.TestCase):
##        def setUp(self):
##            self.oob = Oob_NEWSTYLE()
##
##            EnsureScenarioPath()
##
##            module = __import__('Alpha2')
##            self.oob.LoadFromModule(module)
##
##        def checkMePointsValueSize_01(self):
##            #meid = self.oob.metooobmappings.GetMeIdForName('SS-Panzer-Aufklarungsabteilung 1 LSSAH')
##            meid = self.oob.metooobmappings.OobIdToMeId('axis_721240718578272580001040614537')
##            size = self.oob.metooobmappings.GetMeCompositeSize(meid)
##            print meid, size
##            assert size == 1
##
##        def checkMePointsValueSize_02(self):
##            meid = self.oob.metooobmappings.GetMeIdForName('Staff Kompanie')
##            meid2 = self.oob.metooobmappings.OobIdToMeId('axis_902496560790971680001040615173')
##            size = self.oob.metooobmappings.GetMeCompositeSize(meid)
##            #print meid, meid2
##            assert meid == meid2
##            print meid, size
##            assert size == 1
##
##        def checkMePointsValueSize_03(self):
##            # 1 Kompanie VW
##            meid = self.oob.metooobmappings.OobIdToMeId('axis_687175295975411790001040616024')
##            size = self.oob.metooobmappings.GetMeCompositeSize(meid)
##            print meid, size
##            assert size == 2
##
##        def checkMePointsValueSize_04(self):
##            # 2 Kompanie VW
##            meid = self.oob.metooobmappings.OobIdToMeId('axis_31498754249648988001040634179')
##            size = self.oob.metooobmappings.GetMeCompositeSize(meid)
##            print meid, size
##            assert size == 2
##
##        def checkMePointsValueSize_05(self):
##            # 3 Kompanie le SPW
##            meid = self.oob.metooobmappings.OobIdToMeId('axis_842937697270703880001040634750')
##            size = self.oob.metooobmappings.GetMeCompositeSize(meid)
##            print meid, size
##            assert size == 2
##
##        def checkMePointsValueSize_06(self):
##            # 1. Kompanie PanzerJagerAbteilung 1
##            meid = self.oob.metooobmappings.OobIdToMeId('axis_210550682602259250001040637276')
##            size = self.oob.metooobmappings.GetMeCompositeSize(meid)
##            print meid, size
##            assert size == 1
##
##        def checkMePointsValueSize_07(self):
##            # 1. Kompanie Sturmgeschutz Abteilung 1
##            meid = self.oob.metooobmappings.OobIdToMeId('axis_233261810541569600001040637943')
##            size = self.oob.metooobmappings.GetMeCompositeSize(meid)
##            print meid, size
##            assert size == 1
##
##        # Allied
##
##        def checkMePointsValueSize_08(self):
##            # 399 Rifle Regiment
##            meid = self.oob.metooobmappings.OobIdToMeId('allied_788482920959136400001040641346')
##            size = self.oob.metooobmappings.GetMeCompositeSize(meid)
##            print meid, size
##            assert size == 1
##
##        def checkMePointsValueSize_09(self):
##            # Artillery Battery
##            meid = self.oob.metooobmappings.OobIdToMeId('allied_35521738934794824001040642287')
##            size = self.oob.metooobmappings.GetMeCompositeSize(meid)
##            print meid, size
##            assert size == 1
##
##        def checkMePointsValueSize_10(self):
##            # Mortar Battery
##            meid = self.oob.metooobmappings.OobIdToMeId('allied_863969491314396530001040642465')
##            size = self.oob.metooobmappings.GetMeCompositeSize(meid)
##            print meid, size
##            assert size == 1
##
##        def checkMePointsValueSize_11(self):
##            # 1 Rifle Battalion   - just the HQ has been split off
##            meid = self.oob.metooobmappings.OobIdToMeId('allied_939725441537684770001040642631')
##            size = self.oob.metooobmappings.GetMeCompositeSize(meid)
##            print meid, size
##            assert size == 1
##
##        def checkMePointsValueSize_12(self):
##            # A Company
##            meid = self.oob.metooobmappings.OobIdToMeId('allied_949879911518473910001040642800')
##            size = self.oob.metooobmappings.GetMeCompositeSize(meid)
##            print meid, size
##            assert size == 2
##
##        def checkMePointsValueSize_13(self):
##            # 2 Rifle Battalion
##            meid = self.oob.metooobmappings.OobIdToMeId('allied_949879911518473910001040642800')
##            size = self.oob.metooobmappings.GetMeCompositeSize(meid)
##            print meid, size
##            assert size == 2
##
##        def checkMePointsValueSize_14(self):
##            # A Company
##            meid = self.oob.metooobmappings.OobIdToMeId('allied_181714359917704910001040647899')
##            size = self.oob.metooobmappings.GetMeCompositeSize(meid)
##            print meid, size
##            assert size == 2
##        def checkMePointsValueSize_15(self):
##            # B Company
##            meid = self.oob.metooobmappings.OobIdToMeId('allied_540531731051140140001040647912')
##            size = self.oob.metooobmappings.GetMeCompositeSize(meid)
##            print meid, size
##            assert size == 2
##
##
##        def checkMePointsValueSize_16(self):
##            # 3 Rifle Battalion
##            meid = self.oob.metooobmappings.OobIdToMeId('allied_126365597515497370001040647868')
##            size = self.oob.metooobmappings.GetMeCompositeSize(meid)
##            print meid, size
##            assert size == 3
##
##        def checkMetaSizes_01(self):
##            oobidlist = [ 'allied_126365597515497370001040647868',
##                          'allied_540531731051140140001040647912',
##                          'allied_181714359917704910001040647899' ]
##            metainfodict = self.oob.metooobmappings.GetMeMetatypeSizes(self, oobidlist)
##            print metainfodict

class TestCase07(unittest.TestCase):

    def checkGetTroopType_new(self):
        self.oob = Oob_NEWSTYLE()

## IMPORT TECHNIQUE DEPRECIATED
##        EnsureScenarioPath()
##        module = __import__('scenario30')
##        self.oob.LoadFromModule(module)

        adict = utilcc.ImportScenarioFile('scenario30')
        self.oob.LoadFromDict(adict)

        result = self.oob.GetTroopType('axis_9971036892669.34')
        assert result == 'Armor_Panzer'

    def checkGetTroopType_newest(self):
        self.oob = Oob_NEWSTYLE()

## IMPORT TECHNIQUE DEPRECIATED
##        EnsureScenarioPath()
##        module = __import__('scenario40')
##        self.oob.LoadFromModule(module)

        adict = utilcc.ImportScenarioFile('scenario40')
        self.oob.LoadFromDict(adict)
        self.oob.PostProcessOOBTree()

        result = self.oob.GetTroopType('axis_9971036892669.34')
        assert result == 'Senior HQ_Army HQ'


    def checkGetTroopType_oldest(self):
        self.oob = Oob_OLDSTYLE()

## IMPORT TECHNIQUE DEPRECIATED
##        EnsureScenarioPath()
##        module = __import__('scenario1')
##        self.oob.LoadFromModule(module)

        adict = utilcc.ImportScenarioFile('scenario1')
        self.oob.LoadFromDict(adict)

        result = self.oob.GetTroopType('AD1')
        assert result == 'Infantry'
        result = self.oob.GetTroopType('AT1')
        assert result == 'Armor_Churchhill'


class TestCase08(unittest.TestCase):

    def checkMappingsPersistence01(self):
        self.oob = Oob_NEWSTYLE()

## IMPORT TECHNIQUE DEPRECIATED
##        EnsureScenarioPath()
##
##        #module = __import__('scenario40')
##        import scenario40 as module
##        self.oob.LoadFromModule(module)

        adict = utilcc.ImportScenarioFile('scenario40')
        self.oob.LoadFromDict(adict)

        #print # start a new line
        astr = repr(self.oob.metooobmappings)
        #print astr

        self.oob.metooobmappings.LoadFromStr(astr)
        self.oob.PostProcessOOBTree()
        assert astr == repr(self.oob.metooobmappings)

    def checkMeCompositeExperience(self):
        from trooptypes import TroopTypeMgr_V2
        trooptypesmgr=TroopTypeMgr_V2()

        self.oob = Oob_NEWSTYLE( trooptypesmgr=trooptypesmgr )
        trooptypesmgr.oob = self.oob   # Hack wire up.

        adict = utilcc.ImportScenarioFile('scenario46')
        self.oob.LoadFromDict(adict)
        self.oob.PostProcessOOBTree()  # this relies on having a trooptypesmgr, so wire up the above!

        assert self.oob.metooobmappings.GetMeCompositeExperience('me_3') == 20

        self.oob = Oob_OLDSTYLE()
        adict = utilcc.ImportScenarioFile('scenario22')
        self.oob.LoadFromDict(adict)
        self.oob.PostProcessOOBTree()
        assert self.oob.metooobmappings.GetMeCompositeExperience('AR1') == 0

    def checkDamagePoints01(self):
        self.oob = Oob_NEWSTYLE()
        adict = utilcc.ImportScenarioFile('scenario44')
        self.oob.LoadFromDict(adict)
        oobids = self.oob.metooobmappings.GetMeRecursiveListOfOobidsExcludingMes('me_1')
        assert len(oobids) > 1

        for oobid in oobids:
            assert self.oob.GetDamagePointsLastBattle(oobid) == 0

        for oobid in oobids:
            self.oob.SetDamagePointsLastBattle(oobid, 100)

        for oobid in oobids:
            assert self.oob.GetDamagePointsLastBattle(oobid) == 100

    def checkCasualtyDamageAndVictoryPoints01(self):
        self.oob = Oob_NEWSTYLE()
        adict = utilcc.ImportScenarioFile('scenario47')
        self.oob.LoadFromDict(adict)
        oobids = self.oob.metooobmappings.GetMeRecursiveListOfOobidsExcludingMes('me_1')

        oobid = oobids[0]  # pick a random oobid unit

        """
            def SetStrength(self, oobid, mtgvlist): raise 'Not implemented in decendent class?'
            def GetStrength(self, oobid): raise 'Not implemented in decendent class?'
            def SetCasualtiesIncurredTotal(self, oobid, mtgvlist): raise 'Not implemented in decendent class?'
            def GetCasualtiesIncurredTotal(self, oobid): raise 'Not implemented in decendent class?'
            def SetCasualtiesIncurredLastBattle(self, oobid, mtgvlist): raise 'Not implemented in decendent class?'
            def GetCasualtiesIncurredLastBattle(self, oobid): raise 'Not implemented in decendent class?'
            def SetCasualtiesCausedTotal(self, oobid, mtgvlist): raise 'Not implemented in decendent class?'
            def GetCasualtiesCausedTotal(self, oobid): raise 'Not implemented in decendent class?'
            def SetCasualtiesCausedLastBattle(self, oobid, mtgvlist): raise 'Not implemented in decendent class?'
            def GetCasualtiesCausedLastBattle(self, oobid): raise 'Not implemented in decendent class?'
        """
        self.oob.SetStrength(oobid, [4,1,0,0])
        assert self.oob.GetStrength(oobid) == [4,1,0,0]

        self.oob.SetCasualtiesIncurredTotal(oobid, [3,1,0,0])
        assert self.oob.GetCasualtiesIncurredTotal(oobid) == [3,1,0,0]
        self.oob.SetCasualtiesIncurredLastBattle(oobid, [2,1,0,0])
        assert self.oob.GetCasualtiesIncurredLastBattle(oobid) == [2,1,0,0]

        self.oob.SetCasualtiesCausedTotal(oobid, [1,1,0,0])
        assert self.oob.GetCasualtiesCausedTotal(oobid) == [1,1,0,0]
        self.oob.SetCasualtiesCausedLastBattle(oobid, [5,1,0,0])
        assert self.oob.GetCasualtiesCausedLastBattle(oobid) == [5,1,0,0]

        self.oob.SetStrength(oobid, [0,1,0,0])
        assert self.oob.IsDead(oobid) == 0
        self.oob.SetStrength(oobid, [1,0,0,0])
        assert self.oob.IsDead(oobid) == 0
        self.oob.SetStrength(oobid, [0,0,0,0])
        assert self.oob.IsDead(oobid) == 1

        oldpoints = self.oob.GetPoints(oobid)
        newpoints = oldpoints+200
        self.oob.SetPoints(oobid, newpoints)
        assert self.oob.GetPoints(oobid) == newpoints

    def checkWhoCanCommandWho01(self):
        self.oob = Oob_NEWSTYLE()
        adict = utilcc.ImportScenarioFile('Alpha3_badrussians01')
        self.oob.LoadFromDict(adict)

        # Oobids
        Oob_3rdTank = 'allied_424853673433386520001040638864'
        Oob_111thRifle = 'allied_443906865603334230001040640877'
        Oob_399Rifle = 'allied_788482920959136400001040641346'
        Oob_1Rifle = 'allied_939725441537684770001040642631'
        Oob_ACompany = 'allied_949879911518473910001040642800'
        # Meids
        Level1_3rdTank =          self.oob.metooobmappings.GetMeIdForName('3rd Tank Army')
        Level2_111thRifle =       self.oob.metooobmappings.GetMeIdForName('111th Rifle Division')
        Level3_399Rifle_ME_ROLE = self.oob.metooobmappings.GetMeIdForName('399 Rifle Regiment')
        Level4_1Rifle_ME =        self.oob.metooobmappings.GetMeIdForName('1 Rifle Battalion')
        Level5_ACompany_ME =      self.oob.metooobmappings.OobIdToMeId(Oob_ACompany)


        # Not Me's
        assert Level1_3rdTank == None
        assert Level2_111thRifle == None

        hqs = self.oob.FindHqsUnderCommandOfRole(Oob_399Rifle)
        #assert Oob_399Rifle in hqs
        assert Oob_1Rifle in hqs
        assert Oob_ACompany in hqs # Can command your multi-lower-level-down subordinate


        hqs = self.oob.FindHqsUnderCommandOfRole(Oob_111thRifle)
        #print hqs
        #assert Oob_111thRifle in hqs
        assert Oob_399Rifle not in hqs # cannot command another role
        assert Oob_1Rifle not in hqs   # Cannot command your multi-lower-level-down subordinate, cos intervening role in the way
        assert Oob_ACompany not in hqs # Cannot command your multi-lower-level-down subordinate, cos intervening role in the way



def suite():
    suite1 = unittest.makeSuite(TestCase00, 'check')
    #suite2 = unittest.makeSuite(TestCase02, 'check')   # was the editor test case
    suite3 = unittest.makeSuite(TestCase03, 'check')
    suite4 = unittest.makeSuite(TestCase04, 'check')
    suite5 = unittest.makeSuite(TestCase05, 'check')
    #suite6 = unittest.makeSuite(TestCase06, 'check') # BRUCE tests - changed our minds - OFFLINE
    suite7 = unittest.makeSuite(TestCase07, 'check')
    suite8 = unittest.makeSuite(TestCase08, 'check')

    alltests = unittest.TestSuite((suite1, suite3, suite4, suite5, suite7, suite8))
##    alltests = unittest.TestSuite((suite1,))  # TestCase00
##    alltests = unittest.TestSuite((suite3,))
##    alltests = unittest.TestSuite((suite5,))
##    alltests = unittest.TestSuite((suite6,))
##    alltests = unittest.TestSuite((suite7,))
##    alltests = unittest.TestSuite((suite8,))
    return alltests

def main():
    """ Run all the suites.  To run via a gui, then
            python unittestgui.py NestedDictionaryTest.suite
        Note that I run with VERBOSITY on HIGH  :-) just like in the old days
        with pyUnit for python 2.0
        Simply call
          runner = unittest.TextTestRunner(descriptions=0, verbosity=2)
        The default arguments are descriptions=1, verbosity=1
    """
    runner = unittest.TextTestRunner(descriptions = 0, verbosity = 2) # default is descriptions=1, verbosity=1
    #runner = unittest.TextTestRunner(descriptions=0, verbosity=1) # default is descriptions=1, verbosity=1
    runner.run(suite())

if __name__ == '__main__':
    main()

