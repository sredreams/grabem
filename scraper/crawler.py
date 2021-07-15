"""
Crawls through the API response and stores it in a PostGres/SQLite DB
Attributes would be text, created_at, tweet_id, link_to_store, bundle_binary, notified, notified_time, link_hash 
"""
import requests
import sqlite3
from sqlite3 import Error

database= (r"C:\Users\tarun\OneDrive\Documents\Projects\grabem\scraper\db\data.db")

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
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
        if row['app_id'] == app:
            return row['bearer_token']
            
    

def create_sql():
    sql_create_responses_table = """ CREATE TABLE IF NOT EXISTS tweets (
                                        tweet_id integer PRIMARY KEY,
                                        created_at text NOT NULL,
                                        body text,
                                        link_to_store text NOT NULL,
                                        bundle_binary text NOT NULL,
                                        notified integer NOT NULL,
                                        notified_time text NOT NULL,
                                        link_hash text NOT NULL
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

def tweet_grab():
    conn = create_connection(database)
    if conn is not None:
        token= token_read(conn, app='sredreamsv1')
    headers = {'Authorization': 'Bearer ' + token}
    response = requests.get('https://api.twitter.com/2/tweets/search/recent?query=from:PS5StockAlerts&tweet.fields=created_at&expansions=author_id&user.fields=created_at', headers=headers)
    print(response.text)
    
    




def main():
    create_sql()
    tweet_grab()



if __name__ == '__main__':
    main()





