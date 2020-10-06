# Generate Relationship API's

"""
When are backpointers used?
===========================
When building an official API (or even privately wanting a reference via a back pointer)
 from the receiving end of a directional relationship (the "to" side), then we use the
 deductive backpointer technology.  Look at uses of the B() relationship in the Y classes.
"""

NOTE1 = '  [must first clearX(), though..see note 1A]'
NOTE2 = '  [must first clearY(), though..see note 1A]'
AVOID_RM_WHERE_POSSIBLE = 0

class API:
    def __init__(self, fromclassname, toclassname, cardinality):
        self.fromclassname = fromclassname
        self.toclassname = toclassname
        assert cardinality in ('onetoone', 'onetomany', 'manytoone', 'manytomany')
        self.cardinality = cardinality
        self.result = ''
        self.theoneclass = ''
        self._InitWhoIsTheOne()

    def _InitWhoIsTheOne(self):
        if self.cardinality in ('onetoone', 'onetomany'):
            self.theoneclass = self.fromclassname
        elif self.cardinality == 'manytoone':
            self.theoneclass = self.toclassname
        
    def _Init(self, lhs, rhs):
        self.result = ''
        return self._ConvertLhsRhsToTuplesIfManyToMany(lhs, rhs)

    def _CarriageReturnBetweenDoubleApis(self, rhsOrlhs):
        assert self.cardinality == 'manytomany'
        if len(rhsOrlhs) == 2:
            self.result += '\n'

    def _ConvertLhsRhsToTuplesIfManyToMany(self, lhs, rhs):
        """
        Whilst all cardinalities take a single value for lhs and rhs either
         'singularapi'
         'pluralapi'
         ''
        where an empty string (meaning no api is wanted).  However in the case
        of manytomany cardinality, you can have double values e.g.
         'pluralapi,singularapi'
        since the class is wanting both api's.
        """
        if self.cardinality == 'manytomany':
            lhs = lhs.split(',')
            rhs = rhs.split(',')
        return lhs, rhs
            
    def _YmethodsMessage(self):
        self.result += '\n---- %s methods ----\n'%self.toclassname

    def _XmethodsMessage(self):
        self.result += '\n---- %s methods ----\n'%self.fromclassname
        
    def _LhsRhsMsg(self, lhs, rhs):
        if lhs and not rhs:
            self.result += 'X has %s   -  Y has no API\n'%(lhs,)
        elif rhs and not lhs:
            self.result += 'X has no API  -  Y has %s\n'%(rhs,)
        elif lhs and rhs:
            self.result += 'X has %s  -  Y has %s\n'%(lhs, rhs)
        return self.result
    
    def _CardinalityHeaderMsg(self):
        self.result += '\n' + '='*10 + '   ' + self.cardinality + '   ' + '='*20 + '\n'

    def _PureLine(self):
        self.result += '*'*45 + '\n'

    def _NeedPluralApi(self):
        self.result += "\nN/A - %s requires a plural api on the 'one' class %s.\n"%(self.cardinality,self.theoneclass)
        return self.result


    def _apiLhsSingular(self):
        self.result += 'void  setY(y)    RM.R(this, y, "xtoy")%s\n'%NOTE2
        self.result += 'Y     getY()     RM.P(this, "xtoy")\n'
        self.result += 'void  clearY()   RM.NR(this, getY(), "xtoy")\n'

    def _apiLhsSingular2(self, rhs, rhsCardinality='pluralapi'):
        assert rhsCardinality == 'pluralapi'  # we have no other calls than this. yet.
        # Could potentially split this off into common and then routines which use RM and those that
        # use the rhs 'pluralapi'.  Just like the other case.
        self.result += 'Y     getY()     RM.B(this, "ytox")\n'
        self.result += 'void  setY(y)    RM.R(y, this, "ytox")%s\n'%NOTE2
        self.result += 'void  clearY()   RM.NR(getY(), this, "ytox")\n'

    def _apiLhsPlural(self):
        self.result += 'void  addY(y)    RM.R(this, y, "xtoy")\n'
        self.result += 'list  getAllY()  RM.PS(this, "xtoy")\n'
        self.result += 'void  removeY(y) RM.NR(this, y, "xtoy")\n'

    def _apiRhsPlural(self):
        self.result += 'void  addX(x)    RM.R(x, this, "xtoy")\n'
        self.result += 'list  getAllX()  RM.BS(this, "xtoy")\n'
        self.result += 'void  removeX(x) RM.NR(x, this, "xtoy")\n'

    def _apiRhsPlural2(self):
        self.result += 'void  addX(x)    RM.R(this, x, "ytox")\n'
        self.result += 'list  getAllX()  RM.PS(this, "ytox")\n'
        self.result += 'void  removeX(x) RM.NR(this, x, "ytox")\n'

    def _apiRhsSingularCommon(self):
        self.result += 'X     getX()     RM.B(this, "xtoy")\n'

    def _apiRhsSingular_UseLhsAssistanceRatherThanRm(self, lhsCardinality):
        assert lhsCardinality in ('pluralapi', 'singularapi')
        if lhsCardinality == 'pluralapi':
            yClassSetCallsXmethod, yClassRemoveCallsXmethod = 'addY', 'removeY'
        else:
            yClassSetCallsXmethod, yClassRemoveCallsXmethod = 'setY', 'clearY'
        
        self.result += 'void  setX(x)    x.%s(this)%s\n'%(yClassSetCallsXmethod, NOTE1)
        self.result += 'void  clearX()   getX().%s()\n'%yClassRemoveCallsXmethod

    def _apiRhsSingular_PureRm(self):
        # self.result += '  (no lhs, so have to call RM methods directly)\n'
        self.result += 'void  setX(x)    RM.R(x, this, "xtoy")%s\n'%NOTE1
        self.result += 'void  clearX()   RM.NR( RM.B(this, "xtoy"), this, "xtoy")\n'

    def _apiRhsSingular(self, lhs, lhsCardinality):
        """
        Note:  one-to-many is the same as one-to-one with backpointer Y methods, except due
        to the fact that X holds 'many' Y's, the setX implementation calls
        addy instead of setY.
        """
        self._apiRhsSingularCommon()
        if lhs and AVOID_RM_WHERE_POSSIBLE:
            self._apiRhsSingular_UseLhsAssistanceRatherThanRm(lhsCardinality)
        else:
            self._apiRhsSingular_PureRm()

    def gen(self, lhs, rhs):
        lhs, rhs = self._Init(lhs, rhs)

        self._CardinalityHeaderMsg()
        self._LhsRhsMsg(lhs, rhs)
        self._PureLine()
        
        if self.cardinality == 'onetoone':
            assert lhs <> 'pluralapi'
            assert lhs <> 'pluralapi'

            self._XmethodsMessage()
            
            if lhs == 'singularapi':
                self._apiLhsSingular()
            else:
                self.result += 'None\n'
                
            self._YmethodsMessage()
            
            if rhs == 'singularapi':
                self._apiRhsSingular(lhs, lhsCardinality='singularapi')
            else:
                self.result += 'None\n'

        elif self.cardinality == 'onetomany':
            assert lhs == 'pluralapi' or lhs == ''
            assert rhs == 'singularapi' or rhs == ''
            
            if rhs == 'singularapi' and lhs <> 'pluralapi':
                return self._NeedPluralApi()

            self._XmethodsMessage()
            
            if lhs == 'pluralapi':
                self._apiLhsPlural()
            else:
                self.result += 'None\n'
            
            self._YmethodsMessage()
            
            if rhs == 'singularapi':
                self._apiRhsSingular(lhs, lhsCardinality='singularapi')
            else:
                self.result += 'None\n'

           
        elif self.cardinality == 'manytoone':
            assert lhs == 'singularapi' or lhs == ''
            assert rhs == 'pluralapi' or rhs == ''

            if lhs == 'singularapi' and rhs <> 'pluralapi':
                return self._NeedPluralApi()
            
            self._XmethodsMessage()
            
            if lhs == 'singularapi' and rhs:
                self._apiLhsSingular()
            else:
                self.result += 'None\n'
            
            self._YmethodsMessage()
            
            if rhs == 'pluralapi':
                self._apiRhsPlural()
            else:
                self.result += 'None\n'

        elif self.cardinality == 'manytomany':
            assert 'pluralapi' in lhs
            assert 'pluralapi' in rhs

            self._XmethodsMessage()

            if 'pluralapi' in lhs:
                self._apiLhsPlural()
            self._CarriageReturnBetweenDoubleApis(lhs)
            if 'singularapi' in lhs:
                self._apiLhsSingular2(rhs, rhsCardinality='pluralapi')
            
            self._YmethodsMessage()
            
            if 'pluralapi' in rhs:
                self._apiRhsPlural2()
            self._CarriageReturnBetweenDoubleApis(rhs)
            if 'singularapi' in rhs:
                self._apiRhsSingular(lhs, lhsCardinality='pluralapi')

        else:
            self.result += 'NOT IMPLEMENTED\n'

        return self.result

print '\n'*50

"""
One-to-one there are three possibilites.
 Singluar API on one, other or both.
"""
api = API('X', 'Y', 'onetoone')
print api.gen(lhs='singularapi', rhs='')
print api.gen(lhs='',            rhs='singularapi')
print api.gen(lhs='singularapi', rhs='singularapi')

"""
One-to-many there are two possibilites.
 Always requires a plural API on the 'from' class (otherwise it wouldn't be a 'many' relationship).
 Plural API on one, with or without a singular API on the other.
"""
api = API('X', 'Y', 'onetomany')
print api.gen(lhs='pluralapi', rhs='')
#print api.gen(lhs='',          rhs='singularapi')  # N/A - onetomany requires a plural api on the 'one' class X.
print api.gen(lhs='pluralapi', rhs='singularapi')

"""
Many-to-one there are two possibilites.
 Always requires a plural API on the 'to' class (otherwise it wouldn't be a 'many' relationship).
 Plural API on the other, with or without a singular API on the one.
"""
api = API('X', 'Y', 'manytoone')
#print api.gen(lhs='singularapi', rhs='')   # N/A - manytoone requires a plural api on the 'one' class Y.
print api.gen(lhs='',            rhs='pluralapi')
print api.gen(lhs='singularapi', rhs='pluralapi')

"""
Many-to-many there are four possibilites.
 Plural API must be on both sides (otherwise it wouldn't be many to many :-).
 Then singular API on none, the one, the other or both.
"""
api = API('X', 'Y', 'manytomany')
print api.gen(lhs='pluralapi',             rhs='pluralapi')
print api.gen(lhs='pluralapi',             rhs='pluralapi,singularapi')
print api.gen(lhs='pluralapi,singularapi', rhs='pluralapi')
print api.gen(lhs='pluralapi,singularapi', rhs='pluralapi,singularapi')



"""
Sample run: 10 June 2003


==========   onetoone   ====================
X has singularapi   -  Y has no API
*********************************************

---- X methods ----
void  setY(y)    RM.R(this, y, "xtoy")  [must first clearY(), though..see note 1A]
Y     getY()     RM.P(this, "xtoy")
void  clearY()   RM.NR(this, getY(), "xtoy")  

---- Y methods ----
None


==========   onetoone   ====================
X has no API  -  Y has singularapi
*********************************************

---- X methods ----
None

---- Y methods ----
X     getX()     RM.B(this, "xtoy")
void  setX(x)    RM.R(x, this, "xtoy")  [must first clearX(), though..see note 1A]
void  clearX()   RM.NR( RM.B(this, "xtoy"), this, "xtoy")


==========   onetoone   ====================
X has singularapi  -  Y has singularapi
*********************************************

---- X methods ----
void  setY(y)    RM.R(this, y, "xtoy")
Y     getY()     RM.P(this, "xtoy")
void  clearY()   RM.NR(this, getY(), "xtoy")

---- Y methods ----
X     getX()     RM.B(this, "xtoy")
void  setX(x)    RM.R(x, this, "xtoy")  [must first clearX(), though..see note 1A]
void  clearX()   RM.NR( RM.B(this, "xtoy"), this, "xtoy")


==========   onetomany   ====================
X has pluralapi   -  Y has no API
*********************************************

---- X methods ----
void  addY(y)    RM.R(this, y, "xtoy")
list  getAllY()  RM.PS(this, "xtoy")
void  removeY(y) RM.NR(this, y, "xtoy")

---- Y methods ----
None


==========   onetomany   ====================
X has pluralapi  -  Y has singularapi
*********************************************

---- X methods ----
void  addY(y)    RM.R(this, y, "xtoy")
list  getAllY()  RM.PS(this, "xtoy")
void  removeY(y) RM.NR(this, y, "xtoy")

---- Y methods ----
X     getX()     RM.B(this, "xtoy")
void  setX(x)    RM.R(x, this, "xtoy")  [must first clearX(), though..see note 1A]
void  clearX()   RM.NR( RM.B(this, "xtoy"), this, "xtoy")


==========   manytoone   ====================
X has no API  -  Y has pluralapi
*********************************************

---- X methods ----
None

---- Y methods ----
void  addX(x)    RM.R(x, this, "xtoy")
list  getAllX()  RM.BS(this, "xtoy")
void  removeX(x) RM.NR(x, this, "xtoy")


==========   manytoone   ====================
X has singularapi  -  Y has pluralapi
*********************************************

---- X methods ----
void  setY(y)    RM.R(this, y, "xtoy")
Y     getY()     RM.P(this, "xtoy")
void  clearY()   RM.NR(this, getY(), "xtoy")

---- Y methods ----
void  addX(x)    RM.R(x, this, "xtoy")
list  getAllX()  RM.BS(this, "xtoy")
void  removeX(x) RM.NR(x, this, "xtoy")


==========   manytomany   ====================
X has ['pluralapi']  -  Y has ['pluralapi']
*********************************************

---- X methods ----
void  addY(y)    RM.R(this, y, "xtoy")
list  getAllY()  RM.PS(this, "xtoy")
void  removeY(y) RM.NR(this, y, "xtoy")

---- Y methods ----
void  addX(x)    RM.R(this, x, "ytox")
list  getAllX()  RM.PS(this, "ytox")
void  removeX(x) RM.NR(this, x, "ytox")


==========   manytomany   ====================
X has ['pluralapi']  -  Y has ['pluralapi', 'singularapi']
*********************************************

---- X methods ----
void  addY(y)    RM.R(this, y, "xtoy")
list  getAllY()  RM.PS(this, "xtoy")
void  removeY(y) RM.NR(this, y, "xtoy")

---- Y methods ----
void  addX(x)    RM.R(this, x, "ytox")
list  getAllX()  RM.PS(this, "ytox")
void  removeX(x) RM.NR(this, x, "ytox")

X     getX()     RM.B(this, "xtoy")
void  setX(x)    RM.R(x, this, "xtoy")  [must first clearX(), though..see note 1A]
void  clearX()   RM.NR( RM.B(this, "xtoy"), this, "xtoy")


==========   manytomany   ====================
X has ['pluralapi', 'singularapi']  -  Y has ['pluralapi']
*********************************************

---- X methods ----
void  addY(y)    RM.R(this, y, "xtoy")
list  getAllY()  RM.PS(this, "xtoy")
void  removeY(y) RM.NR(this, y, "xtoy")

Y     getY()     RM.B(this, "ytox")
void  setY(y)    RM.R(y, this, "ytox")  [must first clearY(), though..see note 1A]
void  clearY()   RM.NR(getY(), this, "ytox")

---- Y methods ----
void  addX(x)    RM.R(this, x, "ytox")
list  getAllX()  RM.PS(this, "ytox")
void  removeX(x) RM.NR(this, x, "ytox")


==========   manytomany   ====================
X has ['pluralapi', 'singularapi']  -  Y has ['pluralapi', 'singularapi']
*********************************************

---- X methods ----
void  addY(y)    RM.R(this, y, "xtoy")
list  getAllY()  RM.PS(this, "xtoy")
void  removeY(y) RM.NR(this, y, "xtoy")

Y     getY()     RM.B(this, "ytox")
void  setY(y)    RM.R(y, this, "ytox")  [must first clearY(), though..see note 1A]
void  clearY()   RM.NR(getY(), this, "ytox")

---- Y methods ----
void  addX(x)    RM.R(this, x, "ytox")
list  getAllX()  RM.PS(this, "ytox")
void  removeX(x) RM.NR(this, x, "ytox")

X     getX()     RM.B(this, "xtoy")
void  setX(x)    RM.R(x, this, "xtoy")  [must first clearX(), though..see note 1A]
void  clearX()   RM.NR( RM.B(this, "xtoy"), this, "xtoy")

"""
