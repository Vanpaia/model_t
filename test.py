from sqlalchemy import create_engine, String, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import urllib.parse

url = "test"
url_correct = urllib.parse.quote_plus(url)

engine = create_engine(url_correct)
