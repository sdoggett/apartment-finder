import settings
import math
import openstreetmaps as osm
from OSMPythonTools.overpass import Overpass

def coord_distance(lat1, lon1, lat2, lon2):
    """
    Finds the distance between two pairs of latitude and longitude.
    :param lat1: Point 1 latitude.
    :param lon1: Point 1 longitude.
    :param lat2: Point two latitude.
    :param lon2: Point two longitude.
    :return: Kilometer distance.
    """
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    km = 6367 * c
    return km

def in_box(coords, box):
    """
    Find if a coordinate tuple is inside a bounding box.
    :param coords: Tuple containing latitude and longitude.
    :param box: Two tuples, where first is the bottom left, and the second is the top right of the box.
    :return: Boolean indicating if the coordinates are in the box.
    """
    if box[0][0] < coords[0] < box[1][0] and box[1][1] < coords[1] < box[0][1]:
        return True
    return False


def find_points_of_interest(geotag, location):
    """
    Find points of interest, like transit, near a result.
    :param geotag: The geotag field of a Craigslist result.
    :param location: The where field of a Craigslist result.  Is a string containing a description of where
    the listing was posted.
    :return: A dictionary containing annotations.
    """
    area_found = False
    area = ""
    min_dist = None

    num_supermarkets_in_area = 0
    closest_supermarket = "N/A"
    near_supermarket = False
    closest_supermarket_dist = 'N/A'
    
    num_convenience_stores_in_area = 0
    closest_convenience_store = "N/A"
    near_convenience_store = False
    closest_convenience_store_dist = 'N/A'

    num_pharmacys_in_area = 0
    closest_pharmacy = "N/A"
    near_pharmacy = False
    closest_pharmacy_dist = 'N/A'
    
    num_BART_in_area = 0
    closest_BART = "N/A"
    near_BART = False
    closest_BART_dist = 'N/A'
    
    num_of_bus_stops_in_area = 0
    near_Transbay_stop = False
    nearby_routes = []
    
    # Look to see if the listing is in any of the neighborhood boxes we defined.
    for a, coords in settings.BOXES.items():
        if in_box(geotag, coords):
            area = a
            area_found = True

    #Create a bbox around the listing
    distance = 1 #km
    bbox = osm.generate_bbox_around_point(geotag, distance)
    overpass = Overpass()
    dict_of_nearby_supermarkets = osm.get_supermarkets(overpass,bbox)
    num_supermarkets_in_area = len(dict_of_nearby_supermarkets) 
    for node, info in dict_of_nearby_supermarkets.items():
        name = info[0]
        lat = info[1][0]
        long = info[1][1]
        dist = coord_distance(lat, long, geotag[0], geotag[1])
        if (min_dist is None or dist < min_dist):
            min_dist = dist
            closest_supermarket = name
            near_supermarket = True
            closest_supermarket_dist = dist
        

    dict_of_nearby_convenience_stores = osm.get_convenience_store(overpass,bbox)
    num_convenience_stores_in_area = len(dict_of_nearby_convenience_stores) 
    for node, info in dict_of_nearby_convenience_stores.items():
        name = info[0]
        lat = info[1][0]
        long = info[1][1]
        dist = coord_distance(lat, long, geotag[0], geotag[1])
        if (min_dist is None or dist < min_dist):
            min_dist = dist
            closest_convenience_store = name
            near_convenience_store = True
            closest_convenience_store_dist = dist    
    
    dict_of_nearby_pharmacys = osm.get_pharmacy(overpass,bbox)
    num_pharmacys_in_area = len(dict_of_nearby_pharmacys) 
    for node, info in dict_of_nearby_pharmacys.items():
        name = info[0]
        lat = info[1][0]
        long = info[1][1]
        dist = coord_distance(lat, long, geotag[0], geotag[1])
        if (min_dist is None or dist < min_dist):
            min_dist = dist
            closest_pharmacy = name
            near_pharmacy = True
            closest_pharmacy_dist = dist    
        
    
    
    dict_of_nearby_BART = osm.get_BART(overpass,bbox)
    num_BART_in_area = len(dict_of_nearby_BART) 
    for node, info in dict_of_nearby_BART.items():
        name = info[0]
        lat = info[1][0]
        long = info[1][1]
        dist = coord_distance(lat, long, geotag[0], geotag[1])
        if (min_dist is None or dist < min_dist):
            min_dist = dist
            closest_BART = name
            near_BART = True
            closest_BART_dist = dist   
    
    #Is it close to bus stops?
    Transbay_route_list = ['B','C','CB','E','F','G','H','J','L',
                           'LA','NL','NX','NX1','NX2','NX3','NX4',
                           'O','P','S','SB','V','W','Z']
            
    dict_of_nearby_bus_stops = osm.get_bus_stops(overpass,bbox)
    num_of_bus_stops_in_area = len(dict_of_nearby_bus_stops)
    for node, info in dict_of_nearby_bus_stops.items():
        name = info[0]
        routes = info[1]
        lat = info[2][0]
        long = info[2][1]
        if routes != None:
            list_of_routes_at_stop = routes.split(';')
            for route in list_of_routes_at_stop:
                if route in Transbay_route_list:
                    near_Transbay_stop = True
                #add to list of nearby routes if not there already
                if route not in nearby_routes:
                    nearby_routes.append(route)
        
        

    

    # If the listing isn't in any of the boxes we defined, check to see if the string description of the neighborhood
    # matches anything in our list of neighborhoods.
    if len(area) == 0:
        for hood in settings.NEIGHBORHOODS:
            if hood in location.lower():
                area = hood

    return {
        "area_found": area_found,
        "area": area,
        "num_BART_in_area": num_BART_in_area,
        "near_bart": near_BART,
        "bart_dist": closest_BART_dist,
        "bart": closest_BART,
        "num_supermarkets_in_area":num_supermarkets_in_area,
        'closest_supermarket':closest_supermarket,
        "near_supermarket":near_supermarket,
        'closest_supermarket_dist':closest_supermarket_dist,
        "num_convenience_stores_in_area":num_convenience_stores_in_area,
        'closest_convenience_store':closest_convenience_store,
        "near_convenience_store":near_convenience_store,
        'closest_convenience_store_dist':closest_convenience_store_dist,
        "num_pharmacys_in_area":num_pharmacys_in_area,
        'closest_pharmacy':closest_pharmacy,
        "near_pharmacy":near_pharmacy,
        'closest_pharmacy_dist':closest_pharmacy_dist,
        'nearby_bus_routes':nearby_routes,
        'near_Transbay_stop':near_Transbay_stop,
        'num_of_bus_stops_in_area':num_of_bus_stops_in_area
        
    }
