import flask
from flask import request, jsonify

from NewsModules import NewsDataFeed
from miscModules import sectionDump

# Initialize app
app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Home page
@app.route('/', methods=['GET'])
def home():
    return '''
    <h1>Xander's News RSS API</h1>
    <p>Get the lastest stories here!</p>
    '''

# NYT page
@app.route('/api/nyt', methods=['GET'])
def api_nyt():

    # Initialize available sections and default output
    sections = ["Africa", "Americas", "ArtandDesign", "Arts", "AsiaPacific", "Automobile", "Baseball", "Books", "Business", "Climate", "CollegeBasketball", "CollegeFootball", "Dance", "Dealbook", "DiningandWine", "Economy", "Education", "EnergyEnvironment", "Europe", "FashionandStyle", "Golf", "Health", "Hockey", "HomePage", "Jobs", "Lens", "MediaandAdvertising", "MiddleEast", "MostEmailed", "MostShared", "MostViewed", "Movies", "Music", "NYRegion", "Obituaries", "PersonalTech", "Politics", "ProBasketball", "ProFootball", "RealEstate", "Science", "SmallBusiness", "Soccer", "Space", "Sports", "SundayBookReview", "Sunday-Review", "Technology", "Television", "Tennis", "Theater", "TMagazine", "Travel", "Upshot", "US", "Weddings", "Well", "YourMoney"]
    formatOutput = "json"

    args = request.args

    # Parse arguments
    if "section" in args:
        section = args["section"]

        if "format" in args:
            if args["format"] in ["json", "xml", "csv", "html"]:
                formatOutput = args["format"]

        nytFeed = NewsDataFeed("nyt")

        # Execute request
        try:
            if "search" in args:
                searchterm = args["search"]

                return nytFeed.searchFeed(nytFeed.getFeed(section + ".xml", "pandas"), searchterm, format=formatOutput)

            return nytFeed.getFeed(section + ".xml", formatOutput)
        except:
            # Error statement on request issue
            return f'''
            <h1>Unable to to get NYT feed</h1>
            <p>Try specifing a section in your query. Valid sections are:</p>
            {sectionDump(sections)}
            Additionally you can specify a format in your query ("json", "xml", "csv", "html")
            '''
    else:
        # Error statement for no section
        return f'''
        <h1>No NYT section was specified</h1>
        <p>Try specifing a section in your query. Valid sections are:</p>
        {sectionDump(sections)}
        Additionally you can specify a format in your query ("json", "xml", "csv", "html")
        '''

# WSJ page
@app.route('/api/wsj', methods=['GET'])
def api_wsj():

    # Initialize available sections and default output
    sections = ["RSSOpinion", "RSSWorldNews", "WSJcomUSBusiness", "RSSMarketsMain", "RSSWSJD", "RSSLifestyle"]
    formatOutput = "json"
    
    args = request.args

    # Parse arguments
    if "section" in args:
        section = args["section"]

        if "format" in args:
            if args["format"] in ["json", "xml", "csv", "html"]:
                formatOutput = args["format"]

        wsjFeed = NewsDataFeed("wsj")

        # Execute request
        try:
            if "search" in args:
                searchterm = args["search"]

                return wsjFeed.searchFeed(wsjFeed.getFeed(section + ".xml", "pandas"), searchterm, format=formatOutput)

            
            return wsjFeed.getFeed(section + ".xml", formatOutput)
        except:
            # Error statement on request issue
            return f'''
            <h1>Unable to to get WSJ feed</h1>
            <p>Try specifing a section in your query. Valid sections are:</p>
            {sectionDump(sections)}
            Additionally you can specify a format in your query ("json", "xml", "csv", "html")
            '''
    else:
        # Error statement for no section
        return f'''
        <h1>No WSJ section was specified</h1>
        <p>Try specifing a section in your query. Valid sections are:</p>
        {sectionDump(sections)}
        Additionally you can specify a format in your query ("json", "xml", "csv", "html")
        '''

if __name__ == "__main__":
    app.run()
