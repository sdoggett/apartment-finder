# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 12:49:57 2020

@author: sdoggett
"""

##Use Open Street Maps to find grocery stores and transit stops

import getpass
import sys
user = getpass.getuser()
sys.path.insert(0, '/Users/{}/Documents/GitHub/apartment-finder'.format(user))

from OSMPythonTools.overpass import Overpass, overpassQueryBuilder
from OSMPythonTools.nominatim import Nominatim

from geolocation import GeoLocation




def generate_bbox_around_point(point, distance):
    #distance in km
    point_lat = point[0]
    point_lon = point[1]
    loc = GeoLocation.from_degrees(point_lat, point_lon)
    SW_loc, NE_loc = loc.bounding_locations(distance)
    return [SW_loc.deg_lat, SW_loc.deg_lon, NE_loc.deg_lat, NE_loc.deg_lon]




def get_supermarkets(overpass,bbox):
    query = overpassQueryBuilder(bbox=bbox, 
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



def get_convenience_store(overpass,bbox):
    query = overpassQueryBuilder(bbox=bbox, 
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

def get_pharmacy(overpass,bbox):
    query = overpassQueryBuilder(bbox=bbox, 
                                 elementType='node', 
                                 selector='"amenity"="pharmacy"', 
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

def get_bus_stops(overpass,bbox):
    query = overpassQueryBuilder(bbox=bbox, 
                                 elementType='node', 
                                 selector='"highway"="bus_stop"', 
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

def get_BART(overpass,bbox):
    query = overpassQueryBuilder(bbox=bbox, 
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

if __name__ == "__main__":
    
    
    nominatim = Nominatim()
    overpass = Overpass()

    bbox=[37.835727,-122.368679,37.90669,-122.234196]
    
    
    
    #bbox = generate_bbox_around_point([38.069908,-121.908297],1)
    print(bbox)
    x = get_supermarkets(overpass, bbox)
    
    for node, info in x.items():
        print(node)
        print(info[0])
        print(info[1][0])
        print(info[1][1])

    dict_of_nearby_bus_stops = get_bus_stops(overpass,bbox)
    num_of_bus_stops_in_area = len(dict_of_nearby_bus_stops)
    for node, info in dict_of_nearby_bus_stops.items():
        name = info[0]
        routes = info[1]
        if routes != None:
            list_of_routes = routes.split(';')
            for route in list_of_routes:
                print(route)

        
        lat = info[2][0]
        long = info[2][1]
