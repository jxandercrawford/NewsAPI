import lxml.html
import requests
import pandas as pd
from fuzzywuzzy import fuzz


class RSS():
    """
    RSS reader and parser.

    Keyword arguments:
    parentLink -- A link to the RSS feed
    RSSxpath -- A path to use as the root of the RSS feed
    """


    def __init__(self, parentLink, RSSxpath):

        self.__parentLink = parentLink
        self.__xpath = RSSxpath


    def dataExport(self, dataset, format):
        """Takes a pandas dataframe and returns the dataframe in the specified format
        Valid formats: ["json", "xml", "csv", "html", "pandas"]

        Keyword arguments:
        dataset -- A pandas dataframe to be formatted
        format -- A string of the format type of the dataframe to be returned in
        """

        format = format.lower()

        # Return in specified format
        if format == "json":
            return dataset.to_json(orient="records")
        elif format == "xml":
            return dataset.to_xml()
        elif format == "csv":
            return dataset.to_csv()
        elif format == "html":
            return dataset.to_html()
        elif format == "pandas":
            return dataset
        else:
            raise Exception("format argument incorrect. Must be 'json', 'xml', 'csv', 'html', or 'pandas.")


    def readRSS(self, childLink):
        """Takes childLink and requests RSS news feed then returns a pandas dataframe containing the data.

        Keyword arguments:
        childLink -- A string of last segment of a RSS feed (i.e. HomePage.xml)
        """

        # Make request
        response = requests.get(self.__parentLink + childLink.strip())
        if response.status_code != 200:
            raise Exception("Unable to access " + self.__parentLink + childLink.strip())

        content = response.content

        # Read content
        try:
            return pd.read_xml(content, xpath=self.__xpath)
        except:
            raise Exception("Unable to parse specified link's xml")


    def getFeed(self, childLink="HomePage.xml", format="json"):
        """Takes childLink and format and returns specified  news feed in specified format
        Valid formats: ["json", "xml", "csv", "html", "pandas"]

        Keyword arguments:
        childLink -- A string of last segment of a RSS feed (i.e. HomePage.xml)
        format -- A string of the format type of the dataframe to be returned in
        """

        df = self.readRSS(childLink)

        return self.dataExport(df, format)


    def searchFeed(self, dataset, term="", column="title", format="json"):
        """Takes a dataset and a term to search in a specified column and outputs the results of the search in the specified format
        Valid formats: ["json", "xml", "csv", "html"]

        Keyword arguments:
        dataset -- A pandas dataframe to be searched
        term -- A string to search the dataset for
        column -- The specified column to search for the term in
        format -- A string of the format type of the dataframe to be returned in
        """

        # Search for one word search terms
        if len(term.split(" ")) == 1:
            dataset = dataset[dataset[column].apply(lambda x: fuzz.partial_ratio(term.lower(), x.lower())) > 75]
        # Search for multi-word search terms
        else:
            dataset = dataset[dataset[column].apply(lambda x: fuzz.token_sort_ratio(term, x)) > 75]

        return self.dataExport(dataset, format)
