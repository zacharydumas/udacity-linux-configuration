from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):

    __tablename__ = 'users'
    email = Column(String(250), primary_key=True)
    name = Column(String(250))
    picture = Column(String(250))

    @property
    def serialize(self):
        # Return object data in easily serializeable format
        return {
           'name': self.name,
           'email': self.email,
           'picture': self.picture,
        }


class CatalogItem(Base):

    __tablename__ = "catalog_items"
    name = Column(String(250))
    category = Column(String(250))
    description = Column(String(250))
    user_email = Column(String(250), ForeignKey('users.email'))
    id = Column(Integer, primary_key=True)

    @property
    def serialize(self):
        # Return object data in easily serializeable format
        return {
           'name': self.name,
           'category': self.category,
           'description': self.description,
           'user email': self.user_email,
           'id': self.id
        }


# Bind to the database and create the tables
engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)
