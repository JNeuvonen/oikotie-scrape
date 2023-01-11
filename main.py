import time
from selenium import webdriver
from bs4 import BeautifulSoup
import utils
import asyncio
from prisma import Prisma
from prisma.models import Listing


driver = webdriver.Chrome()
last_page = int(utils.get_max_page(driver))


async def main() -> None:
    db = Prisma(auto_register=True)
    await db.connect()

    for i in range(1, last_page + 1):
        print(i)
        URL = utils.get_url(i)
        driver.get(URL)
        time.sleep(0.5)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        elems = soup.find_all("div", "cards-v2__card")
        for item in elems:

            sale_listing_object = utils.get_data_from_card(item)

            if sale_listing_object != None:
                try:
                    await Listing.prisma().create(
                        data=sale_listing_object
                    )
                except Exception:
                    pass

    driver.quit()


if __name__ == '__main__':
    asyncio.run(main())
