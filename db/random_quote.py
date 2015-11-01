from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text

Base = declarative_base()


class RandomQuote(Base):
    __tablename__ = 'random_quote'

    id = Column(Integer, primary_key=True, nullable=False)
    quote = Column(Text, nullable=False)
