from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pymongo
# import pymongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Create a root route `/` that will query your Mongo database and pass the mars data into an HTML template to display the data.
@app.route("/")
def home():
    # Find one record of data from the mongo database
    destination_data = mongo.db.collection.find_one()
    # Return template and data
    return render_template("index.html", mars=destination_data)

# create a route called `/scrape` that will import your `scrape_mars.py` script and call your `scrape` function.
@app.route("/scrape")
def scrape():

    mars_data = scrape_mars.scrape()

    #Store the return value in Mongo as a Python dictionary
    mongo.db.collection.update({}, mars_data, upsert=True)

    print(mars_data)

    # Redirect back to home page

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
