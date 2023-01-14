import time
from selenium import webdriver
from bs4 import BeautifulSoup
import utils
import asyncio
from prisma import Prisma
from prisma.models import Listing
from prisma.models import PriceChange
from datetime import datetime
import json


driver = webdriver.Chrome()

# GET MAX PAGE FROM PAGINATION
last_page = int(utils.get_max_page(driver))


async def main() -> None:

    # DB
    db = Prisma(auto_register=True)
    await db.connect()

    # LIST OF URLS, USED TO DELETE LISTINGS FROM DB THAT WAS MISSED ON A LOOP
    listing_urls = await Listing.prisma().find_many()
    active_listing_dict = utils.get_url_dict(listing_urls)

    # UTIL
    added_listings = 0
    t_start = time.time()

    # LOOP OIKOTIE LISTING PAGES
    for i in range(1, last_page + 1):
        print("page: " + str(i))
        URL = utils.get_url(i)
        driver.get(URL)
        time.sleep(1.5)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        elems = soup.find_all("div", "cards-v2__card")
        for item in elems:
            # SCRAPE RELEVANT DATA
            sale_listing_object = utils.get_data_from_card(item)

            if sale_listing_object != None:
                listing_url = sale_listing_object["url"]
                # FLAG URL FOUND, HELPS LATER WITH REMOVAL PASS
                if listing_url in active_listing_dict:
                    active_listing_dict[listing_url] = True

                fetched_listing = await Listing.prisma().find_first(where={'url': listing_url})

                # CREATE LISTING IF DOESNT EXIST IN DB
                if fetched_listing == None:
                    try:
                        await Listing.prisma().create(
                            data=sale_listing_object
                        )
                        added_listings += 1
                    except Exception:
                        pass
                # ELSE CHECK IF PRICE UPDATED
                else:
                    fetched_listing_price = float(fetched_listing.price)
                    scraped_listing_price = sale_listing_object['price']

                    # UPDATE PRICE CHANGE HISTORY
                    if fetched_listing_price != scraped_listing_price:

                        await PriceChange.prisma().create(
                            {
                                "price_change": float((scraped_listing_price - fetched_listing_price)),
                                "Listing": {
                                    "connect": {
                                        "ID": fetched_listing.ID
                                    }
                                }
                            }
                        )
                        await Listing.prisma().update(where={'url': listing_url},
                                                      data={"price": float(scraped_listing_price)})

    # DEL LISTINGS IN DB THAT WASNT FOUND ON A PASS
    deleted_listings = 0
    for (key, value) in active_listing_dict.items():
        if value == False:
            deleted_listings += 1

            await Listing.prisma().update(where={
                "sale_active": False
            })

    t_end = time.time()
    print("-----------------------------------")
    print("total row dels: " + str(deleted_listings))
    print("total row adds: " + str(added_listings))
    print("Time for pass measured: {}".format(str(t_end-t_start)))
    print("-----------------------------------")
    await db.disconnect()


if __name__ == "__main__":

    pass_count = 0
    while True:
        print(pass_count)
        asyncio.run(main())
        pass_count += 1
