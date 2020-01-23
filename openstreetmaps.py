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



import geopandas as gpd
import osmnx as ox
ox.config(log_console=True, use_cache=True)
ox.__version__

# define a point at the corner of California St and Mason St in SF
location_point = (37.791427, -122.410018)

# same point again, but create network only of nodes within 500m along the network from point
G3 = ox.graph_from_point(location_point, distance=500, distance_type='network',network_type='walk')
fig, ax = ox.plot_graph(G3)




