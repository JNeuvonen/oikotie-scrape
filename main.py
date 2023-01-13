import time
from selenium import webdriver
from bs4 import BeautifulSoup
import utils
import asyncio
from prisma import Prisma
from prisma.models import Listing


driver = webdriver.Chrome()

# GET MAX PAGE FROM PAGINATION
last_page = int(utils.get_max_page(driver))


async def main() -> None:

    db = Prisma(auto_register=True)
    await db.connect()

    listing_urls = await Listing.prisma().find_many()

    # LIST OF URLS, USED TO DELETE LISTINGS FROM DB THAT WAS MISSED ON A LOOP
    active_listing_dict = utils.get_url_dict(listing_urls)

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
                # FLAG URL FOUND TO NOT BE DELETED
                if listing_url in active_listing_dict:
                    active_listing_dict[listing_url] = True
                try:
                    await Listing.prisma().create(
                        data=sale_listing_object
                    )
                except Exception:
                    pass

    total_row_dels = 0

    # DEL LISTINGS IN DB THAT WASNT FOUND ON A PASS
    for (key, value) in active_listing_dict.items():
        if value == False:
            await Listing.prisma().delete(where={
                "url": value
            })
            total_row_dels += 1

    print("-----------------------------------")
    print("total row dels: " + str(total_row_dels))
    print("-----------------------------------")


if __name__ == "__main__":
    while True:
        asyncio.run(main())
