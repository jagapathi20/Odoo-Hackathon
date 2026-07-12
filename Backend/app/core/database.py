from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine

# Base class for our SQLAlchemy ORM models
Base = declarative_base()

# Note: In production/dev, engine configurations and sessionmakers 
# will be wired up here using configuration parameters.