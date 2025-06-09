from sqlalchemy import create_engine
import sqlalchemy

# Database setup
DATABASE_URL = "sqlite:///./instance/easyGrade.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sqlalchemy.orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = sqlalchemy.orm.declarative_base()

# Create tables
Base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
