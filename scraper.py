from craigslist import CraigslistHousing
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.orm import sessionmaker
from dateutil.parser import parse
from util import find_points_of_interest
import time
import settings
import pandas as pd

engine = create_engine('sqlite:///listings.db', echo=False)

Base = declarative_base()

class Listing(Base):
    """
    A table to store data on craigslist listings.
    """

    __tablename__ = 'listings'

    id = Column(Integer, primary_key=True)
    link = Column(String, unique=True)
    created = Column(DateTime)
    #geotag = Column(String)
    lat = Column(Float)
    lon = Column(Float)
    name = Column(String)
    price = Column(Float)
    location = Column(String)
    cl_id = Column(Integer, unique=True)
    area = Column(String)
    bart_stop = Column(String)

class Good_Listing(Base):
    """
    A table to store data on craigslist listings that match my criteria.
    """

    __tablename__ = 'good_listings'

    id = Column(Integer, primary_key=True)
    link = Column(String, unique=True)
    created = Column(DateTime)
    #geotag = Column(String)
    lat = Column(Float)
    lon = Column(Float)
    name = Column(String)
    price = Column(Float)
    location = Column(String)
    cl_id = Column(Integer, unique=True)
    area = Column(String)
    bart_stop = Column(String)

    #to do - add more fields to this


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


## To do: find way to drop listing and good listing tables so i can restart analysis with new parameters


def scrape_area(area):
    """
    Scrapes craigslist for a certain geographic area, and finds the latest listings.
    :param area:
    :return: A list of results.
    """
    cl_h = CraigslistHousing(site=settings.CRAIGSLIST_SITE, area=area, category=settings.CRAIGSLIST_HOUSING_SECTION,
                             filters={'max_price': settings.MAX_PRICE, "min_price": settings.MIN_PRICE})

    results = []
    gen = cl_h.get_results(sort_by='newest', geotagged=True, limit=20)
    while True:
        try:
            result = next(gen)
        except StopIteration:
            break
        except Exception:
            continue
        listing = session.query(Listing).filter_by(cl_id=result["id"]).first()

        # Don't store the listing if it already exists.
        if listing is None:
            if result["where"] is None:
                # If there is no string identifying which neighborhood the result is from, skip it.
                continue

            lat = 0
            lon = 0
            if result["geotag"] is not None:
                # Assign the coordinates.
                lat = result["geotag"][0]
                lon = result["geotag"][1]

                # Annotate the result with information about the area it's in and points of interest near it.
                geo_data = find_points_of_interest(result["geotag"], result["where"])
                result.update(geo_data)
            else:
                result["area"] = ""
                result["bart"] = ""
                result['closest_supermarket'] = ""

            # Try parsing the price.
            price = 0
            try:
                price = float(result["price"].replace("$", ""))
            except Exception:
                pass

            # Create the listing object.
            listing = Listing(
                link=result["url"],
                created=parse(result["datetime"]),
                lat=lat,
                lon=lon,
                name=result["name"],
                price=price,
                location=result["where"],
                cl_id=result["id"],
                area=result["area"],
                bart_stop=result["bart"]
            )

            # Save the listing so we don't grab it again.
            session.add(listing)
            session.commit()

            # Return the result if meets conditions

            if (result['near_supermarket']==True and
                result['near_pharmacy']==True and
                result['near_bart']==True): 
                
                good_listing = Good_Listing(
                    link=result["url"],
                    created=parse(result["datetime"]),
                    lat=lat,
                    lon=lon,
                    name=result["name"],
                    price=price,
                    location=result["where"],
                    cl_id=result["id"],
                    area=result["area"],
                    bart_stop=result["bart"]
                    )
                
                
                print('')
                print('Match found:')
                print(result)
                results.append(result)
                
                session.add(good_listing)
                session.commit()

    return results

def do_scrape():
    """
    Runs the craigslist scraper, and prints result.
    """


    # Get all the results from craigslist.
    all_results = []
    for area in settings.AREAS:
        all_results += scrape_area(area)

    print("{}: Got {} results".format(time.ctime(), len(all_results)))

    
    for result in all_results:
       print(result)
    
def get_df():
    y = pd.read_sql(session.query(Good_Listing).statement,session.bind)
    return y

if __name__ == "__main__":
    ##test
    cl_h = CraigslistHousing(site=settings.CRAIGSLIST_SITE, area='eby', category=settings.CRAIGSLIST_HOUSING_SECTION,
                             filters={'max_price': settings.MAX_PRICE, "min_price": settings.MIN_PRICE,'laundry':settings.LAUNDRY})      
    results = []
    
    
    
    
    gen = cl_h.get_results(sort_by='newest', geotagged=True,include_details=True, limit=20)
    while True:
        try:
            result = next(gen)
        except StopIteration:
            break
        except Exception:
            continue
        listing = session.query(Listing).filter_by(cl_id=result["id"]).first()
        
        # Don't store the listing if it already exists.
        if listing is None:
            if result["where"] is None:
                # If there is no string identifying which neighborhood the result is from, skip it.
                continue

            lat = 0
            lon = 0
            if result["geotag"] is not None:
                # Assign the coordinates.
                lat = result["geotag"][0]
                lon = result["geotag"][1]

                # Annotate the result with information about the area it's in and points of interest near it.
                geo_data = find_points_of_interest(result["geotag"], result["where"])
                result.update(geo_data)
            else:
                result["area"] = ""
                result["bart"] = ""
                result['closest_supermarket'] = ""

            # Try parsing the price.
            price = 0
            try:
                price = float(result["price"].replace("$", ""))
            except Exception:
                pass

            # Create the listing object.
            listing = Listing(
                link=result["url"],
                created=parse(result["datetime"]),
                lat=lat,
                lon=lon,
                name=result["name"],
                price=price,
                location=result["where"],
                cl_id=result["id"],
                area=result["area"],
                bart_stop=result["bart"]
            )

            # Save the listing so we don't grab it again.
            session.add(listing)
            session.commit()

            # Return the result if meets conditions

            #if (result['near_supermarket']==True and
            #    result['near_pharmacy']==True and
            #    result['near_bart']==True): 
            
            if (result['near_supermarket']==True): 
                
                good_listing = Good_Listing(
                    link=result["url"],
                    created=parse(result["datetime"]),
                    lat=lat,
                    lon=lon,
                    name=result["name"],
                    price=price,
                    location=result["where"],
                    cl_id=result["id"],
                    area=result["area"],
                    bart_stop=result["bart"]
                    )
                
                print('')
                print('Match found:')
                print(result)
                results.append(result)
                
                session.add(good_listing)
                session.commit()
        
    df = get_df()
    df.to_excel(r'C:\Users\sdoggett\Documents\GitHub\apartment-finder\Test\results.xlsx')
    
