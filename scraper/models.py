from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import Boolean, Integer, String, Text, Boolean
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Tweet(Base):
    __tablename__ = "tweets"

    tweet_id = Column(Integer, primary_key=True)
    created_at = Column(String(20), nullable=False)
    body = Column(Text)
    link_to_store = Column(String(200), nullable=False)
    bundle_binary = Column(Boolean, nullable=False)
    tweet_hash = Column(String(70), nullable=False)

    def __init__(
        self, tweet_id, created_at, body, link_to_store, bundle_binary, tweet_hash
    ):
        self.tweet_id = tweet_id
        self.created_at = created_at
        self.body = body
        self.link_to_store = link_to_store
        self.bundle_binary = bundle_binary
        self.tweet_hash = tweet_hash


class Bestbuy(Base):
    __tablename__ = "best_buy_products"

    # product_name = Column(String(200), primary_key=True)
    # product_status = Column(String(200), nullable=False)
    # product_url = Column(Text, nullable=False)
    # product_price = Column(String(500), nullable=False)
    product_id = Column(Text, primary_key=True)
    product_name = Column(Text)
    product_status = Column(Text)
    product_url = Column(Text)
    product_price = Column(Text)

    def __init__(
        self, product_id, product_name, product_status, product_url, product_price
    ):
        self.product_id = product_id
        self.product_name = product_name
        self.product_status = product_status
        self.product_url = product_url
        self.product_price = product_price


class Token(Base):
    __tablename__ = "tokens"

    platform = Column(String(50), primary_key=True)
    app_id = Column(String(50))
    bearer_token = Column(String(200))
