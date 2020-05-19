from scraper import do_scrape, get_df
import settings
import time
import sys
import traceback

if __name__ == "__main__":
    while True:
        print("{}: Starting scrape cycle".format(time.ctime()))
        try:
            x = do_scrape()
        except KeyboardInterrupt:
            print("Exiting....")
            
            df = get_df()
            df.to_excel(r'C:\Users\sdoggett\Documents\GitHub\apartment-finder\Test\results.xlsx')
            sys.exit(1)
        except Exception:
            print("Error with the scraping:", sys.exc_info()[0])
            traceback.print_exc()
            sys.exit(1)
        else:
            print("{}: Successfully finished scraping".format(time.ctime()))
            df = get_df()
            df.to_excel(r'C:\Users\sdoggett\Documents\GitHub\apartment-finder\Test\results.xlsx')
            break

        
        #time.sleep(settings.SLEEP_INTERVAL)

