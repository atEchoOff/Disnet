from flask import Flask, session, request, render_template
import Scraper
import secrets
import json
from urllib.parse import unquote_plus

app = Flask(__name__, template_folder="../Client", static_folder="../Client")
app.secret_key = secrets.token_urlsafe(16)

def set_new_restaurant(restaurant):
    # Set the user's restaurant as the given restaurant
    session["name"] = restaurant[0]
    session["link"] = restaurant[1]

@app.route('/restaurant/list')
def get_restaurant_list():
    # Get a full list of all restaurant names, no duplicates
    return json.dumps(Scraper.restaurant_name_list())

@app.route('/restaurant/random')
def get_restaurant():
    # Set a random restaurant along with a link to the session
    restaurant = secrets.choice(Scraper.restaurant_list())
    set_new_restaurant(restaurant)
    return "Done"

@app.route('/guess', methods=["GET"])
def guess():
    print(session["name"])
    print(unquote_plus(request.args.get("guess")))
    # Make a guess for the restaurant, return Y or N
    if not session["name"]:
        # This should not happen, as this should not be called until a restaurant is already chosen
        return "ERROR, user restaurant is not selected"
    
    user_guess = unquote_plus(request.args.get("guess")).lower()
    return "Y" if user_guess == session["name"].lower() else "N"

@app.route('/menu/random')
def get_menu_item():
    # Obtain a random menu item given the current user's restaurant
    if not session["link"]:
        # This should not happen, as this should not be called until a restaurant is already chosen
        return "ERROR, user restaurant is not selected"
    menu = Scraper.get_menu(session["link"])
    
    return secrets.choice(menu)

@app.route('/')
def home():
    # Set the restaurant, and serve the home page
    restaurant = secrets.choice(Scraper.restaurant_list())
    set_new_restaurant(restaurant)

    return render_template("home.html")

    
if __name__ == '__main__':
   app.run(host='localhost', port=9999, debug=True)