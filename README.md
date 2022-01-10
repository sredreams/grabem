# grabem
A project to crawl internet for items that are scarce and help users buy them
Please note this is a work in progress with only few scrappers working such as the bb_scraper.py for BestBuy, which can search for any products availability and ps5_twitter_alert.py for tweet alerts indicative of PS5 being available on PS5StockAlerts account.

The project has the following structure:
- scraper/bb_scrapper.py: Hold the modules for crawling BestBuy and looking for search_product keyword. All the products that are available are returned and store in best_buy_products table of SQLlite DB
    - bb_scrapper.py requirements:
        - Download chrome webdriver for the version of chrome you are running on the machine and add it to your path
-scrapper/models.py: Contains the db models
- scrapper/ps5_twitter_alert.py: This is currently scoped to scrape for tweets from PS5Alerts and looks for patterns that are indicative of a PS5 being available. All the returned tweets that have the urls of sites where ps5 is available is stored in tweets table of SQLlite DB
    - ps5_twitter.py requirements:
        - you will need a token created from twitter developer console. Please store this token in a row against DBs tokens table with columns platform="twitter", app_id="test", bearer_token=<your_token_here>
- scrapper/db_parser.py: This will contain the code to go through all the entries in the DB and look for trigger word (product name) and return the website or source indicative of it's availability
- notifier.py: In version1, we intend to send out sms based notification with plans to soon move to a push based notification using a mobile app
- webserver/app.py: Still in progress, this will be used to run the app that can continuously monitor the availability of products and serve the page for the mobile app (version2)

Virtual Environment:
One can use conda environement and build the vir env by running 'conda env create -f environment.yml' using the environment.yml in this repository