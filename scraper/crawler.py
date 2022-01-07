"""
Crawls through the Twitter API responses for PS5 alerts and stores it in a PostGres/SQLite DB 
with body, created_at, tweet_id, link_to_store, bundle_binary, notified, notified_time, link_hash 
"""
import requests
import sqlite3
import json
import hashlib
import re

database = r"C:\Users\tarun\OneDrive\Documents\Projects\grabem\scraper\db\data.db"  # replace it with relative path, once done debuging
relevant_tweets = []


class tweets:
    """
    Initialized a class to store the info returned from the APIs
    """

    def __init__(
        self,
        body,
        created_at,
        tweet_id,
        link_to_store,
        bundle_binary,
        tweet_hash,
    ):
        self.body = body
        self.created_at = created_at
        self.tweet_id = tweet_id
        self.link_to_store = link_to_store
        self.bundle_binary = bundle_binary
        self.tweet_hash = tweet_hash


def create_connection(db_file):
    """create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)


def token_read(conn, app):
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute("SELECT * FROM tokens")
    rows = cur.fetchall()
    for row in rows:
        if row["app_id"] == app:
            return row["bearer_token"]


def create_sql():
    sql_create_responses_table = """ CREATE TABLE IF NOT EXISTS tweets (
                                        tweet_id integer PRIMARY KEY,
                                        created_at text NOT NULL,
                                        body text,
                                        link_to_store text NOT NULL,
                                        bundle_binary text NOT NULL,
                                        tweet_hash text NOT NULL
                                    ); """
    sql_create_token_table = """ CREATE TABLE IF NOT EXISTS tokens (
                                    platform text PRIMARY KEY,
                                    app_id text NOT NULL,
                                    bearer_token text NOT NULL
                                ); """

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create tasks table
        create_table(conn, sql_create_responses_table)
        create_table(conn, sql_create_token_table)
    else:
        print("Error! cannot create the database connection.")


def bundle_parse(tweet_text):
    if "Bundle" in tweet_text:
        return "1"
    else:
        return "0"


def link_parser(tweet_text):
    """findall() has been used with valid conditions for urls in string"""
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, tweet_text)
    # print([x[0] for x in url])
    return [x[0] for x in url]


def tweet_grab():
    """Makes a call to twitter APIs and gets the all the relevant tweets"""
    conn = create_connection(database)
    if conn is not None:
        token = token_read(conn, app="sredreamsv1")
    headers = {"Authorization": "Bearer " + token}
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/recent?query=from:PS5StockAlerts&tweet.fields=created_at&expansions=author_id&user.fields=created_at&max_results=100",
        headers=headers,
    )
    json_out = json.loads(response.text)
    dup_tweet = []
    for tweet in json_out["data"]:
        tweet_text = (tweet["text"]).replace("/n", " ")
        # print(tweet_text)
        links = link_parser(tweet_text)
        is_bundle = bundle_parse(tweet_text)
        tweet_text_enc = tweet_text.encode("utf-8")
        tweet_hash = hashlib.sha1(tweet_text_enc)
        if tweet_hash not in dup_tweet:
            dup_tweet.append(tweet_hash)
            ent = tweets(
                tweet_text,
                tweet["created_at"],
                tweet["id"],
                str(links),
                is_bundle,
                tweet_hash.hexdigest(),
            )
            relevant_tweets.append(ent)


def write_sql(conn, collection):
    sql = """ INSERT OR IGNORE INTO tweets(tweet_id, created_at, body, link_to_store, bundle_binary, tweet_hash)
            VALUES(?,?,?,?,?,?) """
    cur = conn.cursor()
    cur.execute(sql, collection)
    conn.commit()
    return cur.lastrowid


def main():
    conn = create_connection(database)
    create_sql()
    tweet_grab()
    for tweet in relevant_tweets:
        tweet_id = tweet.tweet_id
        created_at = tweet.created_at
        body = tweet.body
        link_to_store = tweet.link_to_store
        bundle_binary = tweet.bundle_binary
        tweet_hash = tweet.tweet_hash
        tweet_entry = (
            tweet_id,
            created_at,
            body,
            link_to_store,
            bundle_binary,
            tweet_hash,
        )
        if conn is not None:
            write_sql(conn, tweet_entry)
        else:
            print("Error! cannot create the database connection.")


if __name__ == "__main__":
    main()
