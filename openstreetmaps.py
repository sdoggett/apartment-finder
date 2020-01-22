# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 12:49:57 2020

@author: sdoggett
"""

##Use Open Street Maps to find grocery stores and transit stops


from OSMPythonTools.overpass import Overpass, overpassQueryBuilder
from OSMPythonTools.nominatim import Nominatim


nominatim = Nominatim()
overpass = Overpass()
areaId = nominatim.query('Oakland, California').areaId()



query = overpassQueryBuilder(area=areaId, 
                             elementType='node', 
                             selector='"shop"="supermarket"', 
                             includeGeometry=True,
                             out='body')
result = overpass.query(query)
print('number of supermarkets (nodes):  %s' % result.countElements())

output = {}
for x in result.elements():
    nodeID = x.id()
    shopName = x.tag('name')
    coord = [x.lat(),x.lon()]
    
    output[nodeID] = [shopName, coord]
    
for y in output:
    print(output[y][0])
    print("")
    
#node
#"shop"="convenience"
#"shop"="supermarket"
#amenity

#"highway"="bus_stop"
#route_ref

