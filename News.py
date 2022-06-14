import pandas as pd
from RSS import RSS


class NewsParser(RSS):
    """
    News RSS Object Parent Class

    Keyword Arguments:
    parentLink -- A link to the RSS feed
    RSSxpath -- A path to use as the root of the RSS feed
    childLinks -- list of URL paths to RSS feeds
    """


    def __init__(self, parentLink, RSSxpath, childLinks):

        self.__childLinks = childLinks
        super().__init__(parentLink, RSSxpath)


    def parseAll(self, format="pandas"):
        """
        Returns the content of all childLinks in the RSS object in a pandas dataframe.

        Keyword Arguments
        format -- format to return the results in
        Valid formats: ["json", "xml", "csv", "html", "pandas"]
        """
        
        news = []
        for child in self.__childLinks:
            try:
                df = self.readRSS(child + ".xml")
                df["section"] = child
                news.append(df)
            except:
                pass

        return pd.concat(news, axis=0).reindex()


class NYT(NewsParser):
    """
    New York Times RSS parser

    Keyword Arguments
    parentLink -- A link to the RSS feed
    RSSxpath -- A path to use as the root of the RSS feed
    childLinks -- list of URL paths to RSS feeds
    """


    def __init__(self):

        self.__parentLink = "https://rss.nytimes.com/services/xml/rss/nyt/"
        self.__xpath = "/rss/channel//item"
        self.sections = ["Africa", "Americas", "ArtandDesign", "Arts", "AsiaPacific", "Automobile", "Baseball", "Books", "Business", "Climate", "CollegeBasketball", "CollegeFootball", "Dance", "Dealbook", "DiningandWine", "Economy", "Education", "EnergyEnvironment", "Europe", "FashionandStyle", "Golf", "Health", "Hockey", "HomePage", "Jobs", "Lens", "MediaandAdvertising", "MiddleEast", "MostEmailed", "MostShared", "MostViewed", "Movies", "Music", "NYRegion", "Obituaries", "PersonalTech", "Politics", "ProBasketball", "ProFootball", "RealEstate", "Science", "SmallBusiness", "Soccer", "Space", "Sports", "SundayBookReview", "Sunday-Review", "Technology", "Television", "Tennis", "Theater", "TMagazine", "Travel", "Upshot", "US", "Weddings", "Well", "YourMoney"]
        
        super().__init__(self.__parentLink, self.__xpath, self.sections)


    def __str__(self):
        return "New York Times RSS Object"


    def newsDump(self):
        """
        Returns the content of all sections in the RSS object in a pandas dataframe.

        """
        return self.parseAll(format)


class WSJ(NewsParser):
    """
    Wall Street Journal RSS parser

    Keyword Arguments
    parentLink -- A link to the RSS feed
    RSSxpath -- A path to use as the root of the RSS feed
    childLinks -- list of URL paths to RSS feeds
    """


    def __init__(self):

        self.__parentLink = "https://feeds.a.dj.com/rss/"
        self.__xpath = "/rss/channel//item"
        self.sections = ["RSSOpinion", "RSSWorldNews", "WSJcomUSBusiness", "RSSMarketsMain", "RSSWSJD", "RSSLifestyle"]
        
        super().__init__(self.__parentLink, self.__xpath, self.sections)


    def __str__(self):
        return "Wall Street Journal RSS Object"


    def newsDump(self):
        """
        Returns the content of all sections in the RSS object in a pandas dataframe.
        """
        return self.parseAll()
