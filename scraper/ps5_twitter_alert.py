"""
Makes a Twitter search API call and stores responses for PS5 alerts in a SQLite DB 
using Tweet db model in models.py
"""
from logger import setup_custom_logger
import requests, json, hashlib, re, os
from models import Tweet, Token, Base, engine, db_session


script_path = os.path.dirname(__file__)
log = setup_custom_logger(__file__)
relevant_tweets = []
Base.metadata.create_all(bind=engine)


def token_read(app):
    for token in db_session.query(Token):
        try:
            if token.platform == app:
                return token.bearer_token
            else:
                log.info(f"No macthing token found for {app} in database tokens table")
        except Exception as err:
            log.error(
                f"{err} please store a auth token in the database for {app} API access"
            )
            raise


def bundle_parse(tweet_text):
    if "Bundle" in tweet_text:
        return True
    else:
        return False


def link_parser(tweet_text):
    """
    Looks for urls in the tweet body to find the websites shared where ps5 is available
    """
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, tweet_text)
    return [x[0] for x in url]


def tweet_grab():
    """
    Makes a call to twitter APIs and gets the all the relevant tweets and stores the relevant info in DB
    Please make sure the tokens table in DB has been populated with app twitter and the token for twitter APIs auth
    """
    if db_session is not None:
        token = token_read(app="twitter")
    try:
        headers = {"Authorization": "Bearer " + token}
    except Exception as err:
        log.error(f"No token found for Twitter: error: {err}")
        raise
    try:
        response = requests.get(
            "https://api.twitter.com/2/tweets/search/recent?query=from:PS5StockAlerts&tweet.fields=created_at&expansions=author_id&user.fields=created_at&max_results=100",
            headers=headers,
        )
    except Exception as err:
        log.error(f"Failed to make a request to twitter APIs: {err}")
        raise
    json_out = json.loads(response.text)
    dup_tweet = []
    for tweet in json_out["data"]:
        tweet_text = (tweet["text"]).replace("/n", " ")
        links = link_parser(tweet_text)
        is_bundle = bundle_parse(tweet_text)
        tweet_text_enc = tweet_text.encode("utf-8")
        tweet_hash = hashlib.sha1(tweet_text_enc)
        if tweet_hash not in dup_tweet:
            dup_tweet.append(tweet_hash)
            tweet_data = [
                tweet["id"],
                tweet["created_at"],
                tweet_text,
                str(links),
                is_bundle,
                tweet_hash.hexdigest(),
            ]
            tweet_coll = Tweet(*tweet_data)
            relevant_tweets.append(tweet_coll)
    try:
        db_session.bulk_save_objects(relevant_tweets)
        db_session.commit()
    except Exception as err:
        log.error(f"Couldn't commit bestbuy result to DB: {err}")
        db_session.rollback()
        raise


def main():
    tweet_grab()


if __name__ == "__main__":
    main()
