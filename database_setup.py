# This is the beginning of configuration
from sqlalchemy import Column, ForeignKey, String, DateTime, Integer
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    email = Column(String(80), nullable=False)
    picture = Column(String(100))


class Category(Base):
    __tablename__ = 'category'
    name = Column(String(50), primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            "name": self.name
        }


class Item(Base):
    __tablename__ = 'item'
    time = Column(DateTime(timezone=True), server_default=func.now(),
                  onupdate=func.now())
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(1000))
    category_name = Column(String(50), ForeignKey('category.name'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            "category_name": self.category_name,
            "item": {
                "id": self.id,
                "name": self.name,
                "description": self.description
            }
        }


# This is the end of configuration
engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.create_all(engine)
