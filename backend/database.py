import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Get the DB URL from docker-compose environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# 2. Create the Engine (The connection pool)
# We use standard synchronous Postgres connection (psycopg2)
engine = create_engine(DATABASE_URL)

# 3. Create the SessionLocal class
# Each request will create a new instance of this "Session" to talk to DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Base class
# All our models (tables) will inherit from this class so SQLAlchemy knows about them
Base = declarative_base()

# 5. Dependency (To be used in FastAPI routes later)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()