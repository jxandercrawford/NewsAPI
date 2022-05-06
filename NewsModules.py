import lxml.html
import requests
import pandas as pd
from fuzzywuzzy import fuzz


class NewsDataFeed():


    def __init__(self, NewsOrg="nyt", RSSxpath=""):

        NewsOrg = NewsOrg.lower()

        # Set variables for RSS source
        if NewsOrg == "nyt":
            self.__baseLink = "https://rss.nytimes.com/services/xml/rss/nyt/"
            self.__xpath = "/rss/channel//item"
            self.__sections = ["Africa", "Americas", "ArtandDesign", "Arts", "AsiaPacific", "Automobile", "Baseball", "Books", "Business", "Climate", "CollegeBasketball", "CollegeFootball", "Dance", "Dealbook", "DiningandWine", "Economy", "Education", "EnergyEnvironment", "Europe", "FashionandStyle", "Golf", "Health", "Hockey", "HomePage", "Jobs", "Lens", "MediaandAdvertising", "MiddleEast", "MostEmailed", "MostShared", "MostViewed", "Movies", "Music", "NYRegion", "Obituaries", "PersonalTech", "Politics", "ProBasketball", "ProFootball", "RealEstate", "Science", "SmallBusiness", "Soccer", "Space", "Sports", "SundayBookReview", "Sunday-Review", "Technology", "Television", "Tennis", "Theater", "TMagazine", "Travel", "Upshot", "US", "Weddings", "Well", "YourMoney"]
        elif NewsOrg == "wsj":
            self.__baseLink = "https://feeds.a.dj.com/rss/"
            self.__xpath = "/rss/channel//item"
            self.__sections = ["RSSOpinion", "RSSWorldNews", "WSJcomUSBusiness", "RSSMarketsMain", "RSSWSJD", "RSSLifestyle"]
        else:
            self.__baseLink = NewsOrg
            self.__xpath = RSSxpath
            self.__sections = []


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


    def readRSS(self, categoryLink):
        """Takes categoryLink and requests RSS news feed then returns a pandas dataframe containing the data.

        Keyword arguments:
        categoryLink -- A string of last segment of a RSS feed (i.e. HomePage.xml)
        """

        # Make request
        response = requests.get(self.__baseLink + categoryLink.strip())
        if response.status_code != 200:
            raise Exception("Unable to access " + self.__baseLink + categoryLink.strip())

        content = response.content

        # Read content
        try:
            return pd.read_xml(content, self.__xpath)
        except:
            raise Exception("Unable to parse specified link's xml")


    def getFeed(self, categoryLink="HomePage.xml", format="json"):
        """Takes categoryLink and format and returns specified  news feed in specified format
        Valid formats: ["json", "xml", "csv", "html", "pandas"]

        Keyword arguments:
        categoryLink -- A string of last segment of a RSS feed (i.e. HomePage.xml)
        format -- A string of the format type of the dataframe to be returned in
        """

        df = self.readRSS(categoryLink)

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
