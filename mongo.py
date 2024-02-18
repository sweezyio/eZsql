from pymongo import MongoClient
import os
from dotenv import load_dotenv
from os import getenv

# MongoDB Credentials
# User: {secret}
# Pass: {secret}

load_dotenv()

conn=getenv('CONNECTION_STRING')


def get_database(conn):
    CONNECTION_STRING = f"{conn}"
    client = MongoClient(CONNECTION_STRING)
    return client['eZsql']

dbname = get_database(conn)
queries = dbname["queries"]

# Searches the DB for the queryString, returns the cached response if it exists, None if otherwise
def searchQuery(queryString):
    curQuery = queries.find_one({ "query": queryString })
    return curQuery["response"] if curQuery != None else None

# Inserts new query and response 
def cacheQueryAndResponse(queryString, responseString):
    queries.insert_one({
        "query": queryString,
        "response": responseString
    })
