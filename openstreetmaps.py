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


def get_supermarkets(overpass,areaId):
    query = overpassQueryBuilder(area=areaId, 
                                 elementType='node', 
                                 selector='"shop"="supermarket"', 
                                 includeGeometry=True,
                                 out='body')
    result = overpass.query(query)
    output = {}
    for x in result.elements():
        nodeID = x.id()
        shopName = x.tag('name')
        coord = [x.lat(),x.lon()]
        output[nodeID] = [shopName, coord]
        
    return output

def get_convenience_store(overpass,areaId):
    query = overpassQueryBuilder(area=areaId, 
                                 elementType='node', 
                                 selector='"shop"="convenience"', 
                                 includeGeometry=True,
                                 out='body')
    result = overpass.query(query)
    output = {}
    for x in result.elements():
        nodeID = x.id()
        shopName = x.tag('name')
        coord = [x.lat(),x.lon()]
        output[nodeID] = [shopName, coord]
        
    return output

def get_bus_stops(overpass,areaId):
    query = overpassQueryBuilder(area=areaId, 
                                 elementType='node', 
                                 selector='"highway"="bus stop"', 
                                 includeGeometry=True,
                                 out='body')
    result = overpass.query(query)
    output = {}
    for x in result.elements():
        nodeID = x.id()
        stopName = x.tag('name')
        routes = x.tag('route_ref')
        coord = [x.lat(),x.lon()]
        output[nodeID] = [stopName,routes, coord]
        
    return output

def get_BART(overpass,areaId):
    query = overpassQueryBuilder(area=areaId, 
                                 elementType='node', 
                                 selector=['"network" = "BART"','"railway"="station"'], 
                                 includeGeometry=True,
                                 out='body')
    result = overpass.query(query)
    output = {}
    for x in result.elements():
        nodeID = x.id()
        stopName = x.tag('name')
        coord = [x.lat(),x.lon()]
        output[nodeID] = [stopName, coord]
        
    return output





