from flask import Flask, session
from flask_cors import CORS, cross_origin
import Scraper
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/restaurant/list')
@cross_origin()
def get_restaurant_list():
    # Get a full list of all restaurants
    restaurants = Scraper.restaurant_list()
    return str([restaurant[0] for restaurant in restaurants])

@app.route('/restaurant/random')
@cross_origin()
def get_restaurant():
    # Set a random restaurant along with a link to the session
    restaurant = secrets.choice(Scraper.restaurant_list())
    session["name"] = restaurant[0]
    session["link"] = restaurant[1]
    return str(restaurant)

@app.route('/menu/random')
@cross_origin()
def get_menu_item():
    # Obtain a random menu item given the current user's restaurant
    if not session["link"]:
        # This should not happen, as this should not be called until a restaurant is already chosen
        return "ERROR, user restaurant is not selected"
    menu = Scraper.get_menu(session["link"])
    
    return secrets.choice(menu)
    
if __name__ == '__main__':
   app.run(host='localhost', port=9999, debug=True)