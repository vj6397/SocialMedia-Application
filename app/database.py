from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Define your database URL with proper encoding for the password
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

# Create the engine and sessionmaker
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define the base class for declarative models
Base = declarative_base()



# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




#using psycopg
# while True:
#     try:
#         conn=psycopg.connect(host='localhost', dbname='fastapi',user='postgres',password='Vjjaat@123')
#         # cursor=conn.cursor()
#         print("successful connection")
#         break
#     except Exception as error:
#         print("connection failed")
#         print(error)
#         time.sleep(2)