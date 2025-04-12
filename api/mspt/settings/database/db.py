from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from mspt.settings import config


engine = create_engine(config.SQLALCHEMY_DATABASE_URI) # connect_args={'check_same_thread': False}) #pool_pre_ping=True, connect_args are only for sqlite
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SessionScoped = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()