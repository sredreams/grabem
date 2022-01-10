from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.sqltypes import Boolean, Integer, String, Text, Boolean
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine(
    "sqlite:///database.db"
)  # Please replace it with a db connection suitable for your environment, read https://docs.sqlalchemy.org/en/14/core/engines.html for more info
db_session = sessionmaker(bind=engine)
db_session = db_session()


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

    product_id = Column(Integer, primary_key=True)
    product_name = Column(String(200), nullable=False)
    product_status = Column(String(200), nullable=False)
    product_url = Column(String(200), nullable=False)
    product_price = Column(String(20), nullable=False)

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
    app_id = Column(String(50), nullable=False)
    bearer_token = Column(String(200), nullable=False)
