import json
import time
from bs4 import BeautifulSoup
from constants import TARGET_URL
from selenium import webdriver
driver = webdriver.Chrome()


def get_max_page(driver) -> str:
    """
      Returns:
          int: max page of oikotie pagination
    """

    driver.get(TARGET_URL)

    # Wait for the page to load
    driver.implicitly_wait(10)
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    elems = soup.find_all(
        "span", class_="ng-binding")

    last_page = elems[len(elems) - 2].get_text()

    time.sleep(2)

    return last_page


def get_url_dict(arr_of_listing):
    # generates two dicts for diff after looping through every oikotie page

    ret = {}

    for item in arr_of_listing:
        url = str(item.url)
        ret[url] = False

    return ret


def get_url(page):
    return TARGET_URL.format(page)


def is_integer(str):
    try:
        int(str)
        return True
    except ValueError:
        return False


def fmt_square_meters(sqm):

    sqm = sqm.replace(u"\xa0", "")
    return sqm


def fmt_price(price):

    if price == "Kysy hintaa":
        return None

    price = price.replace("€", "")
    price = price.replace(u"\xa0", "")
    return int(price)


def parse_apartment_feature_text(text):
    # YEAR BUILT
    if is_integer(text):
        return ("year", float(text))

    # SQUARE METERS
    if "m²" in text:
        return ("square_meters", text.replace(" m²", ""))

    # ROOMS
    if " h" in text:
        return ("rooms", float(text.replace(" h", "").strip()))

    # TYPE OF APARTMENT
    return ("apartment_type", text)


def get_data_from_card(card):

    ret_dict = {}

    price = card.find("h2", "ot-card-v2__title margined margined--v5")
    info_div = card.find("div", "ot-card-v2__info")

    if info_div == None:
        return None

    # BOOSTED CARD
    if price == None:
        price = card.find(
            "h2", "ot-card-v2__title margined margined--v5 ot-card-v2__title--extra-visibility")

    address_text = info_div.find("div", "ot-card-v2__text")
    splitted_address = address_text.get_text().split(", ")
    city = splitted_address[len(splitted_address) - 1]
    neighborhood = splitted_address[len(splitted_address) - 2]
    features_text = info_div.find_all(
        "div", "card-features__value")

    ret_dict["price"] = fmt_price(price.get_text())
    ret_dict["address"] = address_text.get_text()
    ret_dict["city"] = city
    ret_dict["neighborhood"] = neighborhood

    for item in features_text:
        tuple_item = parse_apartment_feature_text(item.get_text())
        ret_dict[tuple_item[0]] = tuple_item[1]

    a_tag = card.a
    href = a_tag.get("href")

    ret_dict["url"] = href
    ret_dict['sale_active'] = True

    if "price" in ret_dict and "square_meters" in ret_dict:

        ret_dict["square_meters"] = fmt_square_meters(
            ret_dict["square_meters"])

        if ret_dict["price"] != None and ret_dict["square_meters"] != None:
            square_meters = ret_dict["square_meters"]

            if "," in square_meters:
                square_meters = float(square_meters.replace(",", "."))

            ret_dict["square_meters"] = float(square_meters)

            ret_dict["price_to_sqm"] = float(
                ret_dict["price"] / float(square_meters))

    return ret_dict

    # driver.get(href)
    # time.sleep(1)
    ##soup = BeautifulSoup(driver.page_source, "html.parser")
##
    # listing_details_container = soup.find_all(
    # "div", "listing-details-container")
    # for container in listing_details_container:
    # listing_details_elems = container.find_all(
    # "div", "info-table__row")
##
    # for item in listing_details_elems:
    ##        title = item.find("dt", "info-table__title")
    ##        value = item.find("dd", "info-table__value")
##
    # if title != None:
    ##            ret_dict[title.get_text().lower()] = value.get_text()
