from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use flask_PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Create route that renders index.html template and finds data from mongo
@app.route("/")
def home():

    # Find data
    # news_content = mongo.db.news_content.find()

    mars_db = mongo.db.mars_db.find()

    # return template and data
    return render_template("index.html", mars_db=mars_db)


# Route that will trigger scrape functions
@app.route("/scrape")
def scrape():


    # Run scraping function
    news = scrape_mars.scrape()
    
    # Store results into a dictionary
    content = {
        "news_title": news["news_title"],
        "news_blurb": news["news_blurb"],
        "featured_image_url": news["featured_image_url"],
        "mars_facts": news["mars_facts_html"],
        "mars_hemisphere_urls": news["mars_hemisphere_urls"]
    }

    # Delete previous news content, if it exists
    mongo.db.mars_db.drop()

    # Insert new content into database
    mongo.db.mars_db.insert_one(content)

    # Redirect back to home page
    return redirect("http://localhost:5050/", code=302)

    # Redirect back to home page
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5050)