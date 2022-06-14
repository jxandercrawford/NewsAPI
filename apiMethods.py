from flask import request

def sectionDump(sectionList):
    # Returns all sections in an html list
    sectionHTML = "<ul>"

    for section in sectionList:
        sectionHTML += f"<li>{section}</li>"

    sectionHTML += "</ul>"

    return sectionHTML


def api_news(newsObj, outputFormat="json"):
    # Takes news object and output default and will run a flask api function

    args = request.args

    # Parse arguments
    if "section" in args:
        section = args["section"]

        if section.lower() in map(lambda x: x.lower(), newsObj.sections):
            feed = newsObj.getFeed(section + ".xml", "pandas")
        else:
            # Error statement for no section
            return f'''
            <h1>Incorrect section was specified</h1>
            <p>Try specifying a section in your query. Valid sections are:</p>
            {sectionDump(newsObj.sections)}
            Additionally you can specify a format in your query ("json", "xml", "csv", "html")
            '''
    else:
        feed = newsObj.newsDump()

    # Search feed
    if "search" in args:
        # Execute request
        try:
            searchTerm = args["search"]

            feed = newsObj.searchFeed(feed, searchTerm, format="pandas")

        except:
            # Error statement on request issue
            return f'''
            <h1>Unable to to get NYT feed</h1>
            <p>Try specifying a section in your query. Valid sections are:</p>
            {sectionDump(newsObj.sections)}
            Additionally you can specify a format in your query ("json", "xml", "csv", "html")
            '''

    # Format and return
    if "format" in args:
        if args["format"] in ["json", "xml", "csv", "html"]:
            outputFormat = args["format"]
    return newsObj.dataExport(feed, outputFormat)
