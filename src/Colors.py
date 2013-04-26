from Multivector import *
import math

Color = Multivector
#class Color(Multivector):
#	def __init__(self, r, g, b):
		#Multivector.__init__(self, {})

#    def __add__(self, other):
#        sumResult = Multivector.__add__(self, other)
#        return Color(sumResult.coeficients)
#
#    def __repr__(self):
#        components = [0, 0, 0]
#        componentsKeys = (0b0010000, 0b0100000, 0b1000000)
#
#        for i in range(3):
#            key = componentsKeys[i]
#            if self.coeficients.has_key(key):
#                components[i] = self.coeficients[key]
#            components[i] = math.floor(components[i] * 127) + 128
#            
#        return "color(%d, %d, %d)" % (components[0], components[1], components[2])

def toByteRGB(color):
    components = [0, 0, 0]
    componentsKeys = (0b0010000, 0b0100000, 0b1000000)

    for i in range(3):
        key = componentsKeys[i]
        if color.coeficients.has_key(key):
            components[i] = color.coeficients[key]
        components[i] = math.floor(components[i] * 127) + 128
    
    return components
    
def toFloatRGB(color):
    byteColors = toByteRGB(color)
    return [c / 255.0 for c in byteColors]

r = Color({0b0010000 : 1})
g = Color({0b0100000 : 1})
b = Color({0b1000000 : 1})

d = r + g
print toByteRGB(d)
print toFloatRGB(d)


print r, g, b
print r + g