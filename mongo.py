from pymongo import MongoClient
# MongoDB Credentials
# User: {secret}
# Pass: {secret}

def get_database():
    CONNECTION_STRING = "{secret}"
    client = MongoClient(CONNECTION_STRING)
    return client['eZsql']

dbname = get_database()
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
