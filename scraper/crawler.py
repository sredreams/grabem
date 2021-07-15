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

def main():
    sql_create_responses_table = """ CREATE TABLE IF NOT EXISTS projects (
                                        tweet_id integer PRIMARY KEY,
                                        created_at text NOT NULL,
                                        body text,
                                        link_to_store text NOT NULL,
                                        bundle_binary text NOT NULL,
                                        notified integer NOT NULL,
                                        notified_time text NOT NULL,
                                        link_hash text NOT NULL
                                    ); """

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create tasks table
        create_table(conn, sql_create_responses_table)
    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()





