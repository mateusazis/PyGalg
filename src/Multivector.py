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
        
        for bitmap, coef in other.coeficients.items():
            if respDict.has_key(bitmap):
                respDict[bitmap] += coef
            else:
                respDict[bitmap] = coef
        return Multivector(respDict)
        
            
    def getCoeficient(self, bitmap):
        """
        Returns the coeficient of a given bitmap representing a base
        """
        return self.coeficients[bitmap]
        
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
            resp += "%.1f%s%s" % (coef, spacing, productRepr)
            
        return resp or "0"
        
    def __eq__(self, other):
        return self.coeficients == other.coeficients
        
if __name__ == '__main__':        

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
    d = Multivector({0b11101:0})
    print Multivector()
    #import random
    #a = Multivector([0 for i in range(10)])
    #print a
    #for i in range(30):
    #    print "%s: %s" % (bin(i), vectorRerp(i))