import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36", 
}

oneDay = timedelta(days=1)

def memoize(func):
    # Build a version of a function which stores the return value
    # Only rerun func if the last run of the function is more than a day ago
    lastCall = dict()
    ret = None
    def memoized(*args):
        nonlocal lastCall
        nonlocal ret
        now = datetime.now()
        if args not in lastCall or now - lastCall[args] > oneDay:
            # Only call function if it hasnt been run or it was run more than a day ago
            print("Calling", func)
            lastCall[args] = now
            ret = func(*args)
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
        name = a.text
        if "<" not in name and ">" not in name:
            # Some restaurants have stupid names, like End Zone Food Court - Lunch/Dinner Updated. Get rid of everything after -
            name = name.split("-")[0].strip()
            ret.append((name, link))
    return ret

@memoize
def restaurant_name_list():
    # Return only a list of restaurant names, no duplicates
    return list(set(restaurant[0] for restaurant in restaurant_list()))

@memoize
def get_menu(link):
    # Get the menu of a restaurant given its link
    ret = []
    menu_page = BeautifulSoup(requests.get(link, headers=headers).content, "html.parser")
    items = menu_page.find_all(class_="menuItems__item")

    for item in items:
        span = item.find("span")
        name = span.text
        if "<" not in name and ">" not in name:
            ret.append(name)
    return ret