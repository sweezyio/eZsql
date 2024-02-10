#%%
from transformers import AutoTokenizer
import transformers
import torch

model = "nextai-team/Moe-2x7b-QA-Code" 

tokenizer = AutoTokenizer.from_pretrained(model)
tokenizer.pad_token = tokenizer.eos_token
pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    device_map="auto",
    model_kwargs={"torch_dtype": torch.float16},
)

def generate_resposne(query):
    messages = [{"role": "user", "content": query}]
    prompt = pipeline.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    outputs = pipeline(prompt, max_new_tokens=256, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
    return outputs[0]['generated_text']

response = generate_resposne("How to learn coding .Please provide a step by step procedure")
print(response)

#%%
# sqlDict={"query (with subquery) to show stations with year-round average temperature above 50 degrees:":"""SELECT * FROM STATION
# WHERE 50 < (SELECT AVG(TEMP_F) FROM STATS
# WHERE STATION.ID = STATS.ID);""", "update two rows, Denver's rainfall readings:":"""UPDATE STATS SET RAIN_I = 4.50
# WHERE ID = 44;"""}

# prompt="Translate this english query to SQL:\n"+query"
# if schema not none:
# 	prompt+="\nUsing this schema:\n"+schema
# prompt+="\nWith these examples"+sqlDict+"\nSQL Query:"