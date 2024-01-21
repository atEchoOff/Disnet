from flask import Flask, session, request, render_template
import Scraper, Utils
import secrets
import json
from urllib.parse import unquote_plus

app = Flask(__name__, template_folder="../Client", static_folder="../Client")
app.secret_key = secrets.token_urlsafe(16)

def set_new_restaurant(restaurant):
    # Set the user's restaurant as the given restaurant and initialize game variables
    # Return the menu size
    session["name"] = restaurant[0]
    session["link"] = restaurant[1]
    session["menu_count"] = 0
    session["guess_count"] = 0

    # Find a number which is relatively prime to the menu length
    # This will allow element menu items to be unique
    menu_len = len(Scraper.get_menu(restaurant[1]))
    session["menu_key"] = Utils.get_relprime(menu_len)
    return str(menu_len)

@app.route('/restaurant/list')
def get_restaurant_list():
    # Get a full list of all restaurant names, no duplicates
    return json.dumps(Scraper.restaurant_name_list())

@app.route('/restaurant/random')
def get_restaurant():
    # Set a random restaurant along with a link to the session
    # Return the menu size
    restaurant = secrets.choice(Scraper.restaurant_list())
    return str(set_new_restaurant(restaurant))

@app.route('/guess', methods=["GET"])
def guess():
    # Make a guess for the restaurant, return Y or N
    if not "name" in session:
        # This should not happen, as this should not be called until a restaurant is already chosen
        return "ERROR, user restaurant is not selected"
    
    session["guess_count"] += 1
    user_guess = unquote_plus(request.args.get("guess")).lower()
    return "Y" if user_guess == session["name"].lower() else "N"

@app.route('/menu/random')
def get_menu_item():
    # Obtain a random menu item given the current user's restaurant
    if not "link" in session:
        # This should not happen, as this should not be called until a restaurant is already chosen
        return "ERROR, user restaurant is not selected"
    
    # Return menu item at multiple of nonfactor of menu length
    # This ensures no duplicates and good memory usage
    menu = Scraper.get_menu(session["link"])
    menu_item = menu[session["menu_count"] * session["menu_key"] % len(menu)]

    session["menu_count"] += 1
    return menu_item

@app.route('/')
def home():
    return render_template("home.html")

    
if __name__ == '__main__':
   app.run(host='localhost', port=9999, debug=True)