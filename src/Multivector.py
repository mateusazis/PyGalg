import math
import copy

def _bitCount(n):
    """
    Counts the amount of bits '1' in a binary integer.
    """
    resp = 0
    while n:
        if n & 1:
            resp += 1
        n = n >> 1
    return resp

def _vectorRepr(bitmap):
    bitLength = bitmap.bit_length()
    resp = ""
    firstVector = True
    for i in range(bitLength):
        if bitmap & (1 << i):
            if not firstVector:
                resp += "^"
            resp += "e%d" % (i + 1)
            
            firstVector = False
    return resp
    
def _canonical_reordering(bitmap1, bitmap2):
    sum = 0
    bitmap1 = bitmap1 >> 1
    while bitmap1:
        sum += _bitCount(bitmap1 & bitmap2)
        bitmap1 = bitmap1 >> 1
    
    #negative if odd number of swaps, positive otherwise
    return -1.0 if (sum & 1) else 1.0      

def _baseOuterProduct(bitmap1, coef1, bitmap2, coef2):
    #check if the basis blades are dependent
    if bitmap1 & bitmap2:
        return Multivector([])
        
    newBitmap = bitmap1 | bitmap2
    sign = _canonical_reordering(bitmap1, bitmap2)
    newCoef = sign * coef1 * coef2
    
    return Multivector({newBitmap : newCoef})
    
def _baseRegressiveProduct(bitmap1, coef1, bitmap2, coef2, dimension):
    """
    Regressive product between two multivectors
    """
    newBitmap = bitmap1 & bitmap2
    
    if _bitCount(bitmap1) + _bitCount(bitmap2) - _bitCount(newBitmap) != dimension:
        return Multivector([])
    
    sign = _canonical_reordering(bitmap1 ^ newBitmap, bitmap2 ^ newBitmap)
    newCoef = sign * coef1 * coef2
    return Multivector({newBitmap : newCoef})
    
def _baseGeometricProduct(bitmap1, coef1, bitmap2, coef2):
    newBitmap = bitmap1 ^ bitmap2
    sign = _canonical_reordering(bitmap1, bitmap2)
    newCoef = sign * coef1 * coef2
    
    return Multivector({newBitmap : newCoef})

class Multivector(object):    
    """
    Class for Multivector representation and manipulation
    """
    def __init__(self, coeficients = None):
        """
        Initializes a multivector with a given arguments
        
        Possible arguments:
            coeficient list: [10, 4, 0, 2, 5] is (10+e1+2e1^e2+5e3)
            
            coeficient dict: {0:10, 1:4, 3:2, 4:5} is (10+e1+2e1^e2+5e3)
        """
        if coeficients == None:
            self.coeficients = {}
        else:
            argType = type(coeficients)
            
            if argType is dict:
                self.coeficients = coeficients.copy()

            #scalar-only constructor
            elif argType is int or argType is float:
                self.coeficients = {0b0 : coeficients}

            elif argType is list or argType is tuple:
                size = len(coeficients)
                sequence = ((i, coeficients[i]) for i in range(size))
                self.coeficients = {bitmap: coef for (bitmap, coef) in sequence}
                
            #remove bitmaps whose keys are zero
            for bitmap, coef in self.coeficients.items():
                if coef == 0:
                    del self.coeficients[bitmap]
    
    def __xor__(self, other):
        """
        Shortcut for outer product between two multivectors
        """
        return self.op(other)
        

        
    def op(self, other):
        """
        Outer product between two multivectors
        """
        resp = Multivector([])
        
        for bitmap1 , coef1 in self.coeficients.items():            
            for bitmap2 , coef2 in other.coeficients.items():
                resp += _baseOuterProduct(bitmap1, coef1, bitmap2, coef2)
                
        return resp
    
    def __add__(self, other):
        """
        Calculates the sum of two multivectores, returning another one
        """
        respDict = self.coeficients.copy()
        
        #convert number to multivector
        if isinstance(other, (float, int)):
            other = Multivector([other])
        
        for bitmap, coef in other.coeficients.items():
            if respDict.has_key(bitmap):
                respDict[bitmap] += coef
            else:
                respDict[bitmap] = coef
        return Multivector(respDict)
        
    def __sub__(self, other):
        return self + (other * -1)
        
    def __mul__(self, value):
        """
        Multiplies all weights of the basis blades by value.
        """
        if isinstance(value, int) or isinstance(value, float):
            respDict = {}
            if value != 0:
                for bitmap in self.coeficients.keys():
                    respDict[bitmap] = self.coeficients[bitmap] * value
            return Multivector(respDict)
        elif isinstance(value, Multivector):
            return self.sp(value)
            
    def __div__(self, value):
        return self * (1.0 / value)
            
    def getCoeficient(self, bitmap):
        """
        Returns the coeficient of a given bitmap representing a base
        """
        if self.coeficients.has_key(bitmap):
            return self.coeficients[bitmap]
        return 0
        
        
    def getStoredBitmaps(self):
        """
        Returns a tuple all stored bitmaps (that is, the ones with non-zero coeficients)
        """
        return self.coeficients.keys()
     
    def rp(self, other, dimension):
        """
        Regressive product between two multivectors
        """
        resp = Multivector([])
        for bitmap1 , coef1 in self.coeficients.items():
            for bitmap2 , coef2 in other.coeficients.items():
                resp += _baseRegressiveProduct(bitmap1, coef1, bitmap2, coef2, dimension)
        return resp
        
    def __repr__(self):
        resp = ""
        keys = self.getStoredBitmaps()
        sortedKeys = sorted(keys)
        for i in range(len(sortedKeys)):
            key = sortedKeys[i]
            coef = self.getCoeficient(key)
            if coef > 0 and i:
                resp += (" " if resp else "") + "+ "
            productRepr = _vectorRepr(key)
            spacing = " " if productRepr else ""
            resp += "%.2f%s%s" % (coef, spacing, productRepr)
            
        return resp or "0"
        
    def __eq__(self, other):
        return self.coeficients == other.coeficients
        
    def gp(self, other):
        """
        Geometric product between two multivectors using Euclidean metrics.
        """
        resp = Multivector([])
        
        for bitmap1 , coef1 in self.coeficients.items():            
            for bitmap2 , coef2 in other.coeficients.items():
                resp += _baseGeometricProduct(bitmap1, coef1, bitmap2, coef2)
                
        return resp
        
    def gradeExtract(self, grade):
        """
        Extract from this multivector the blades that match the specified grade.
        """
        resp = Multivector()
        for bitmap, coef in self.coeficients.items():
            bits1Count = _bitCount(bitmap)
            if bits1Count == grade:
                resp += Multivector({bitmap:coef})
        return resp
        
    @property
    def grade(self):
        """
        Returns the grade of this multivector if it represents a blade. Otherwise, raises an error.
        """
        items = self.coeficients.items()
        if not items:
            return 0
        bitmap, coef = items[0]
        candidateGrade = _bitCount(bitmap)
        for bitmap, coef in items:
            if _bitCount(bitmap) != candidateGrade:
                raise Exception("Requesting grade from a non-blade multivector")
        return candidateGrade
        
    def lcont(self, other):
        """
        Left contraction between 2 multivectors.
        """
        gradeR = self.grade
        gradeS = other.grade
        gp = self.gp(other)
        return gp.gradeExtract(gradeS - gradeR)
        
    def rcont(self, other):
        """
        Right contraction between 2 multivectors.
        """
        gradeR = self.grade
        gradeS = other.grade
        gp = self.gp(other)
        return gp.gradeExtract(gradeR - gradeS)
        
    def sp(self, other):
        """
        Scalar product between 2 multivectors.
        """
        gp = self.gp(other)
        return gp.gradeExtract(0)
        
    @property
    def reverse(self):
        """
        Returns the reverse of this multivector.
        """
        respDict = {}
        for bitmap, coef in self.coeficients.items():
            grade = _bitCount(bitmap)
            respDict[bitmap] = coef * (-1)**(grade * (grade -1) / 2)
        return Multivector(respDict)
#        grade = self.grade
#        multiplier = (-1)**(grade * (grade -1) / 2)
#        return self * multiplier
        
    @property
    def squaredNorm(self):
        """
        Returns the squared norm of this multivector.
        """
        scalarProduct =  self.sp(self.reverse)
        return scalarProduct.coeficients[0]
        
    @property
    def inverse(self):
        """
        Returns the inverse of this multivector.
        """
        return self.reverse * (1.0 / self.squaredNorm)       
    
    def dual(self, spaceDimension):
        """
        Given an integer for the space dimensionality, returns the dual of this multivector.
        """
        pseudoScalarBitmap = 0
        for i in range(spaceDimension):
            pseudoScalarBitmap = (pseudoScalarBitmap << 1) | 1
        pseudoScalar = Multivector({pseudoScalarBitmap : 1})
        return self.lcont(pseudoScalar.inverse)
        
    def versorProduct(self, v):
        gradeR = self.grade
        gradeK = v.grade
        print "grade r", gradeR, "gradeK", gradeK
        return v.gp(self.gp(v.inverse))# * (-1 ** (gradeR * gradeK))
        
    @staticmethod
    def makeRotor(plane, angle):
        norm = math.sqrt(plane.squaredNorm)
        unitPlane = copy.copy(plane) / norm
        
        halfAngle = angle / 2.0        
        
        unitPlane = unitPlane * (-math.sin(halfAngle))
        R = unitPlane + math.cos(halfAngle)
        return R
        
    def rotate(self, rotor, angle):
        invertedRotor = rotor.inverse
        return (rotor.gp(self)).gp(invertedRotor)
        
    def rotateOnPlane(self, plane, angle):
        R = Multivector.makeRotor(plane, angle)
        return self.rotate(R, angle)
    
e1 = Multivector({0b001: 1})
e2 = Multivector({0b010: 1})
e3 = Multivector({0b100: 1})
    
if __name__ == '__main__':        

#    a = Multivector({0:3})
#    print a
#    b = Multivector({0b0:-1, 0b111:49.8})
#    print b
#    c = a + b + Multivector([0, 37.8])
#    print c
#    
#    d = Multivector([0, 1])
#    e = Multivector([0, 0, 3])
#    f = Multivector([0, 1])
#    
#    #print d ^ e ^ f
#    g = d ^ e
#    print g
#    print g.rp(d, 2)
#    d = Multivector({0b11101:0})
#    print Multivector()
    #import random
    #a = Multivector([0 for i in range(10)])
    #print a
    #for i in range(30):
    #    print "%s: %s" % (bin(i), vectorRerp(i))
#    e1 = Multivector.e1
#    e2 = Multivector.e2
#    e3 = Multivector.e3
    def printAll(v):
        print "v:", v
        print "reverse:", v.reverse
        print "inverse:", v.inverse
        print "squared norm:", v.squaredNorm
        
#    printAll(e1*2 ^ e2)

#    a = e1 + e2
#    b = e2 - e1
#    c = e1 + e3
#    plane = a ^ b
#    other = c.lcont(plane)
#    print a
#    print b
#    print c
#    print plane
#    print other
#    
#    print "testing duals"
#    a = e1 ^ e2
#    print a.dual(3)
#    
#    a = e1 + e2
#    v = e2
#    print a.versorProduct(v)
#    
#    a = e1 + e2
#    plane = e1 ^ e3
#    print a.rotateOnPlane(plane, math.pi / 4)