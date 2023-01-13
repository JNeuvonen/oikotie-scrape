import os
from dotenv import load_dotenv
load_dotenv()

TARGET_URL = "https://asunnot.oikotie.fi/myytavat-asunnot?pagination={}&locations=%5B%5B1,9,%22Suomi%22%5D%5D&cardType=100"
DB_USER = os.environ.get(
    "DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
PQ_DB = os.environ.get("PQ_DB")
