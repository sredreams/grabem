# grabem
A project to crawl internet for items that are scarce and help users buy them
Currently only scopped/targeted towards PS5 but plans are to expand it beyond PS5

The project has the following structure:
- scraper/bbscrapper.py: Hold the modules for crawling different online shopping websites. Currently under bbscrapper.py we have functions that are intended to crawl BestBuy and Walmart.
- scrapper/crawler.py: This is currently scoped to scrape for tweets from PS5Alerts and looks for patterns that are indicative of a PS5 being available. This will be expanded to other products as well
- scrapper/db_parser.py: This will contain the code to go through all the entries in the DB and look for trigger word (product name) and return the website or source indicative of it's availability
- notifier.py: In version1, we intend to send out sms based notification with plans to soon move to a push based notification using a mobile app
- webserver/app.py: Still in progress, this will be used to run the app that can continuously monitor the db an serve the page for the mobile app (version2)

