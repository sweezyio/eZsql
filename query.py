import requests
import mongo

API_BASE_URL = "https://api.cloudflare.com/client/v4/accounts/bfa77c9395f9d84a019dd987b57983f9/ai/run/"
headers = {"Authorization": "Bearer CMRzBi1PY5W-KS4Nf147dIzC9t15kZT34D1hR8Mi"}

def run(prompt):
  dbResponse = mongo.searchQuery(prompt);
  if(dbResponse != None): 
    return dbResponse;

  input = {
    "messages": [
      { "role": "system", "content": "You are to only return SQL queries" },
      { "role": "user", "content": prompt }
    ]
  }
  response = requests.post(f"{API_BASE_URL}@hf/thebloke/codellama-7b-instruct-awq", headers=headers, json=input)
  response = response.json()
  mongo.cacheQueryAndResponse(prompt, response["result"]["response"])
  return response["result"]["response"]

output = run("Select all rows whose value is greater than 5")
print(output)
