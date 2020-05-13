import os
from dotenv import load_dotenv

load_dotenv()

username = os.getenv('MYSQL_USER')
password = os.getenv('MYSQL_PASSWORD')
database = os.getenv('MYSQL_DATABASE')
if username and password and database:
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{username}:{password}@localhost/{database}'
