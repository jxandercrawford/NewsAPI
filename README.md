*Note: This was a short learning project done in October of 2021 to get a handle on using flask as an interface of a RSS feed*

# NewsAPI
A short and sweet news fetching script

#### Documentation

Paths:
- /api/nyt
- /api/wsj


Queries:
- section : section of news source to yeild (route to specific path for more info)
- format : format to return results (json, xml, csv, html)
- search : term to search headlines for


example url:

http://127.0.0.1:5000/api/nyt?section=CollegeBasketball&format=html&search=tournament

explaination:

Will query New York Times news rss feed in the College Basketball section for the term "tournament"

#### Requirements:

- Flask
- Pandas
- Fuzzywuzzy
- LXML
- Requests
