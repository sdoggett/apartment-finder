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

def get_pharmacy(overpass,areaId):
    query = overpassQueryBuilder(area=areaId, 
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



x = get_pharmacy(overpass, areaId)
print(x)



import geopandas as gpd
import osmnx as ox
import networkx as nx
ox.config(log_console=True, use_cache=True)
ox.__version__


location_point = (37.829617, -122.278865)

dest = (37.829405, -122.280013)

# same point again, but create network only of nodes within 500m along the network from point
G3 = ox.graph_from_point(location_point, distance=500, distance_type='network',network_type='walk')
fig, ax = ox.plot_graph(G3)

origin_node = ox.get_nearest_node(G3, location_point)
dest_node = ox.get_nearest_node(G3, dest)

G_projected = ox.project_graph(G3)
nc = ['r' if (node==origin_node or node==dest_node) else '#336699' for node in G_projected.nodes()]
ns = [50 if (node==origin_node or node==dest_node) else 8 for node in G_projected.nodes()]
fig, ax = ox.plot_graph(G_projected, node_size=ns, node_color=nc, node_zorder=2)

route = nx.shortest_path(G_projected, origin_node, dest_node, weight='length')
fig, ax = ox.plot_graph_route(G_projected, route, node_size=0)
l =nx.shortest_path_length(G_projected, origin_node, dest_node, weight='length')





import pandas as pd
import numpy as np
import pandana as pdna
from pandana.loaders import osm


import warnings
warnings.filterwarnings('ignore')



tmp = [-122.8662, 37.1373, -121.4798, 38.2158]

# Reordered for Pandana functions
bbox = [tmp[1], tmp[0], tmp[3], tmp[2]]

poi_df = osm.node_query(*bbox, tags='shop=supermarket')
x, y = poi_df['lon'], poi_df['lat']


store = pd.HDFStore('osm_bayarea.h5')

nodes = store.nodes
edges = store.edges
print(nodes.head(3))
print(edges.head(3))


net=pdna.Network(nodes.x, 
                 nodes.y, 
                 edges["from"], 
                 edges["to"],
                 edges[["weight"]])
net.precompute(3000)


net.set_pois("supermarkets", 2000, 10, x, y)

a = net.nearest_pois(2000, "supermarkets", num_pois=10)
print(a.head(1))