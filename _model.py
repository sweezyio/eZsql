#%%
from gpt4all import GPT4All
model = GPT4All("wizardlm-13b-v1.2.Q4_0.gguf")
#%%
def get_output(query,schema=None):
	print('asdf')
	sqlDict={"query (with subquery) to show stations with year-round average temperature above 50 degrees:":"""SELECT * FROM STATION
	WHERE 50 < (SELECT AVG(TEMP_F) FROM STATS
	WHERE STATION.ID = STATS.ID);""",
	"update two rows, Denver's rainfall readings:":"""UPDATE STATS SET RAIN_I = 4.50
	WHERE ID = 44;"""}

	prompt="Translate this english query to SQL:\n"+query
	if schema is not None:
		prompt+="\nUsing this schema:\n"+schema
	prompt+="\nWith these examples"+str(sqlDict)+"\nSQL Query:"
	print('b')
	output = model.generate(prompt, max_tokens=256)
	print(output)
	return output

#%%
