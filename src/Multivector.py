def _bitCount(n):
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
        sum += _bitCount(bitmap1)
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
        return Multivector(coef=0)
    
    sign = _canonical_reordering(bitmap1 ^ newBitmap, bitmap2 ^ newBitmap)
    newCoef = sign * coef1 * coef2
    return Multivector({newBitmap : newCoef})

class Multivector(object):    
    """
    Class for Multivector representation and manipulation
    """
    def __init__(self, coeficients):
        """
        Initializes a multivector with a given arguments
        
        Possible arguments:
            coeficient list: [10, 4, 0, 2, 5] is (10+e1+2e1^e2+5e3)
            
            coeficient dict: {0:10, 1:4, 3:2, 4:5} is (10+e1+2e1^e2+5e3)
        """
        argType = type(coeficients)
        if argType is dict:
            self.coeficients = coeficients
        elif argType is list or argType is tuple:
            self.coeficients = {}
            for i in range(len(coeficients)):
                if coeficients[i]:
                    self.coeficients[i] = coeficients[i]
                    
    
    
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
        for firstItems in self.coeficients.items():
            bitmap1 , coef1 = firstItems[0], firstItems[1]
            
            for secondItems in other.coeficients.items():
                bitmap2 , coef2 = secondItems[0], secondItems[1]
                resp += _baseOuterProduct(bitmap1, coef1, bitmap2, coef2)
        return resp
    
    def __add__(self, other):
        respDict = {}
        for bitmap in self.getStoredBitmaps():
            respDict[bitmap] = self.getCoeficient(bitmap)
        
        for bitmap in other.getStoredBitmaps():
            coef = other.getCoeficient(bitmap)
            if respDict.has_key(bitmap):
                respDict[bitmap] += coef
            else:
                respDict[bitmap] = coef
        return Multivector(respDict)
        
            
    def getCoeficient(self, bitmap):
        return self.coeficients[bitmap]
        
    def getStoredBitmaps(self):
        return self.coeficients.keys()
     
    def rp(self, other, dimension):
        """
        Regressive product between two multivectors
        """
        resp = Multivector([])
        for firstItems in self.coeficients.items():
            bitmap1 , coef1 = firstItems[0], firstItems[1]
            
            for secondItems in other.coeficients.items():
                bitmap2 , coef2 = secondItems[0], secondItems[1]
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
            resp += "%.1f%s%s" % (coef, spacing, productRepr)
            
        return resp or "0"
        
    def __eq__(self, other):
        return self.coeficients == other.coeficients
        
a = Multivector({0:3})
print a
b = Multivector({0b0:-1, 0b111:49.8})
print b
c = a + b + Multivector([0, 37.8])
print c

d = Multivector([0, 1])
e = Multivector([0, 0, 3])
f = Multivector([0, 1])

#print d ^ e ^ f
g = d ^ e
print g
print g.rp(d, 2)
#import random
#a = Multivector([0 for i in range(10)])
#print a
#for i in range(30):
#    print "%s: %s" % (bin(i), vectorRerp(i))