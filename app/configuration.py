import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Config:
    DB_CONNECT_PATH = os.environ.get("DB_CONNECT_PATH")
