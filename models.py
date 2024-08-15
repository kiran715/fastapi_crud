from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String(255), index = True)

    books = relationship("Book", back_populates = "author")

class Book(Base):

    __tablename__ = "books"

    id = Column(Integer, primary_key = True, index = True)
    title = Column(String(255), index = True)
    author_id = Column(Integer, ForeignKey("authors.id"))

    author = relationship("Author", back_populates = "books")