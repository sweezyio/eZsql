from pymongo import MongoClient
# MongoDB Credentials
# User: eZsql
# Pass: Nh7RAwhVVN8nLAsc

def get_database():
    CONNECTION_STRING = "mongodb+srv://eZsql:Nh7RAwhVVN8nLAsc@ezsql-cache.y8dxf.mongodb.net/?retryWrites=true&w=majority"
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