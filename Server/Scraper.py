import requests
from datetime import timedelta
from Utils import memoize_for_time
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36", 
}

one_day = timedelta(days=1)

@memoize_for_time(one_day)
def restaurant_list():
    # Return a list of disney restaurants (name and link to it)
    ret = []
    RESTAURANTS_URL = "https://allears.net/dining/menu/search/all/all/breakfast,brunch,dessert,dinner,lunch/all/"
    restaurants_page = BeautifulSoup(requests.get(RESTAURANTS_URL, headers=headers).content, "html.parser")
    restaurants = restaurants_page.find_all(class_="dining-card-slide")

    for restaurant in restaurants:
        a = restaurant.find("a")
        link = a.get("href")
        name = a.text
        if "<" not in name and ">" not in name:
            data = name.split("-")
            if len(data) > 1:
                # There is info about the restaurant. Exclude children's menus (theyre too hard)
                if "Child" in data[1]:
                    continue
            # Get rid of everything after -
            name = data[0].strip()
            ret.append((name, link))
    return ret

@memoize_for_time(one_day)
def restaurant_name_list():
    # Return only a list of restaurant names, no duplicates
    return list(set(restaurant[0] for restaurant in restaurant_list()))

@memoize_for_time(one_day)
def get_menu(link):
    # Get the menu of a restaurant given its link
    ret = []
    menu_page = BeautifulSoup(requests.get(link, headers=headers).content, "html.parser")
    items = menu_page.find_all(class_="menuItems__item")

    for item in items:
        item_name = item.find(class_="item-title")
        item_description = item.find(class_="item-description")
        item_price = item.find(class_="item-price")
        ret.append((item_name.text, item_description.text, item_price.text))
    return ret