
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

engine = create_engine('sqlite:///movie_library.db')
Session = sessionmaker(bind=engine)
session = Session()