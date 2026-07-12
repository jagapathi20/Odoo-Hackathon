from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

# FIX: the original module called `sessionmaker()` with no `bind=engine`,
# and never actually called `create_engine`. Any real (non-test-overridden)
# call to get_db() would raise sqlalchemy.exc.UnboundExecutionError the
# moment a query executed. This now builds a real, bound engine/session.
connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    connect_args=connect_args,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our SQLAlchemy ORM models
Base = declarative_base()


def get_db():
    """Database session generator dependency."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()