import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36", 
}

oneDay = timedelta(days=1)
lastCall = dict()


def memoize(func):
    # Build a version of a function which stores the return value
    # Only rerun func if the last run of the function is more than a day ago
    lastCall = None
    ret = None
    def memoized(*args, **kwargs):
        nonlocal lastCall
        nonlocal ret
        now = datetime.now()
        if lastCall == None or now - lastCall > oneDay:
            # Only call function if it hasnt been run or it was run more than a day ago
            lastCall = now
            ret = func(*args, **kwargs)
        return ret
    return memoized

@memoize
def restaurant_list():
    # Return a list of disney restaurants (name and link to it)
    ret = []
    RESTAURANTS_URL = "https://allears.net/dining/menu/"
    restaurants_page = BeautifulSoup(requests.get(RESTAURANTS_URL, headers=headers).content, "html.parser")
    restaurants = restaurants_page.find_all(class_="dining-card-slide")

    for restaurant in restaurants:
        a = restaurant.find("a")
        link = a.get("href")
        name = a.decode_contents()
        ret.append((name, link))
    return ret

@memoize
def get_menu(link):
    # Get the menu of a restaurant given its link
    ret = []
    menu_page = BeautifulSoup(requests.get(link, headers=headers).content, "html.parser")
    items = menu_page.find_all(class_="menuItems__item")

    for item in items:
        span = item.find("span")
        ret.append(span.decode_contents())
    return ret