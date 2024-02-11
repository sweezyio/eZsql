import requests
import mongo

API_BASE_URL = "https://api.cloudflare.com/client/v4/accounts/{secret}/ai/run/"
headers = {"Authorization": "Bearer {secret}"}

def run(query,schema):
	dbResponse = mongo.searchQuery(query);
	if(dbResponse != None): 
		return dbResponse;
	examples = [
    {"input": "List all artists.", "query": "SELECT * FROM Artist;"},
    {
        "input": "Find all albums for the artist 'AC/DC'.",
        "query": "SELECT * FROM Album WHERE ArtistId = (SELECT ArtistId FROM Artist WHERE Name = 'AC/DC');",
    },
    {
        "input": "List all tracks in the 'Rock' genre.",
        "query": "SELECT * FROM Track WHERE GenreId = (SELECT GenreId FROM Genre WHERE Name = 'Rock');",
    },
    {
        "input": "Find the total duration of all tracks.",
        "query": "SELECT SUM(Milliseconds) FROM Track;",
    },
    {
        "input": "List all customers from Canada.",
        "query": "SELECT * FROM Customer WHERE Country = 'Canada';",
    },
    {
        "input": "How many tracks are there in the album with ID 5?",
        "query": "SELECT COUNT(*) FROM Track WHERE AlbumId = 5;",
    },
    {
        "input": "Find the total number of invoices.",
        "query": "SELECT COUNT(*) FROM Invoice;",
    },
    {
        "input": "List all tracks that are longer than 5 minutes.",
        "query": "SELECT * FROM Track WHERE Milliseconds > 300000;",
    },
    {
        "input": "Who are the top 5 customers by total purchase?",
        "query": "SELECT CustomerId, SUM(Total) AS TotalPurchase FROM Invoice GROUP BY CustomerId ORDER BY TotalPurchase DESC LIMIT 5;",
    },
    {
        "input": "Which albums are from the year 2000?",
        "query": "SELECT * FROM Album WHERE strftime('%Y', ReleaseDate) = '2000';",
    },
    {
        "input": "How many employees are there",
        "query": 'SELECT COUNT(*) FROM "Employee"',
    },
]

	prompt="Translate this english query to SQL: "+query
	if schema!="":
		prompt+="\nUsing this table schema: "+schema
	# prompt+="\nWith these example pairs"+str(sqlDict)+"\nSQL Query:"
	prompt+="\nSQL Query: "
	input = {
	"messages": [
	{ "role": "system", "content": "You are to only return SQL queries, referencing but not copying these example pairs: "+str(examples) },
	{ "role": "user", "content": prompt }
	]
	}
	response = requests.post(f"{API_BASE_URL}@hf/thebloke/codellama-7b-instruct-awq", headers=headers, json=input)
	response = response.json()
	mongo.cacheQueryAndResponse(prompt, response["result"]["response"])
	return response["result"]["response"].strip()

# output = run("test")
# print(output)
