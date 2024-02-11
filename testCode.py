#%%
# from transformers import AutoTokenizer
# import transformers
# import torch

# model = "nextai-team/Moe-2x7b-QA-Code" 

# tokenizer = AutoTokenizer.from_pretrained(model)
# tokenizer.pad_token = tokenizer.eos_token
# pipeline = transformers.pipeline(
#     "text-generation",
#     model=model,
#     device_map="auto",
#     pad_token_id=50256,
#     model_kwargs={"torch_dtype": torch.float16},
# )

# def generate_resposne(query):
#     messages = [{"role": "user", "content": query}]
#     prompt = pipeline.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
#     outputs = pipeline(prompt, max_new_tokens=256, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
#     return outputs[0]['generated_text']

# response = generate_resposne("How to learn coding .Please provide a step by step procedure")
# print(response)

#%%
# from transformers import AutoTokenizer, AutoModelForCausalLM
# import torch

# # Initialize the model
# model_path = "beowolx/CodeNinja-1.0-OpenChat-7B"
# model = AutoModelForCausalLM.from_pretrained(model_path, device_map="auto",load_in_4bit=True)
# # Load the OpenChat tokenizer
# tokenizer = AutoTokenizer.from_pretrained("openchat/openchat-3.5-1210", use_fast=True)

# def generate_one_completion(prompt: str):
#     messages = [
#         {"role": "user", "content": prompt},
#         {"role": "assistant", "content": ""}  # Model response placeholder
#     ]

#     # Generate token IDs using the chat template
#     input_ids = tokenizer.apply_chat_template(messages, add_generation_prompt=True)

#     # Produce completion
#     generate_ids = model.generate(
#         torch.tensor([input_ids]).to("cuda"),
#         max_length=256,
#         pad_token_id=tokenizer.pad_token_id,
#         eos_token_id=tokenizer.eos_token_id
#     )

#     # Process the completion
#     completion = tokenizer.decode(generate_ids[0], skip_special_tokens=True)
#     completion = completion.split("\n\n\n")[0].strip()

#     return completion

# generate_one_completion("create some code")
#%%
# # pip install -q transformers
# from transformers import AutoModelForCausalLM, AutoTokenizer
# device = "cuda" # for GPU usage or "cpu" for CPU usage

# tokenizer = AutoTokenizer.from_pretrained("defog/sqlcoder-7b-2",device_map="auto")
# model = AutoModelForCausalLM.from_pretrained("defog/sqlcoder-7b-2",device_map="auto")

# inputs = tokenizer.encode("Generate sample sql code", return_tensors="pt").to(device)
# outputs = model.generate(inputs,max_new_tokens=256)
# print(tokenizer.decode(outputs[0]))

#%%
# # Use a pipeline as a high-level helper
# from transformers import pipeline

# pipe = pipeline("text-generation", model="defog/sqlcoder-7b-2",device_map="auto")
# print(pipe('write sample sql code',max_new_tokens=256))
#%%
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM,BitsAndBytesConfig	
torch.cuda.is_available()
available_memory = torch.cuda.get_device_properties(0).total_memory
print(available_memory)
model_name = "defog/sqlcoder-7b-2"
device_map = {
    "transformer.word_embeddings": 0,
    "transformer.word_embeddings_layernorm": 0,
    "lm_head": "cpu",
    "transformer.h": 0,
    "transformer.ln_f": 0,
}

quantization_config = BitsAndBytesConfig(llm_int8_enable_fp32_cpu_offload=True)
tokenizer = AutoTokenizer.from_pretrained(model_name)
# else, load in 8 bits – this is a bit slower
model = AutoModelForCausalLM.from_pretrained(
	model_name,
	trust_remote_code=True,
	# torch_dtype=torch.float16,
	# load_in_4bit=True,
	quantization_config=quantization_config,
	device_map="auto",
	use_cache=True,
)
#%%
prompt = """### Task
Generate a SQL query to answer [QUESTION]{question}[/QUESTION]

### Instructions
- If you cannot answer the question with the available database schema, return 'I do not know'
- Remember that revenue is price multiplied by quantity
- Remember that cost is supply_price multiplied by quantity

### Database Schema
This query will run on a database whose schema is represented in this string:
CREATE TABLE products (
  product_id INTEGER PRIMARY KEY, -- Unique ID for each product
  name VARCHAR(50), -- Name of the product
  price DECIMAL(10,2), -- Price of each unit of the product
  quantity INTEGER  -- Current quantity in stock
);

CREATE TABLE customers (
   customer_id INTEGER PRIMARY KEY, -- Unique ID for each customer
   name VARCHAR(50), -- Name of the customer
   address VARCHAR(100) -- Mailing address of the customer
);

CREATE TABLE salespeople (
  salesperson_id INTEGER PRIMARY KEY, -- Unique ID for each salesperson
  name VARCHAR(50), -- Name of the salesperson
  region VARCHAR(50) -- Geographic sales region
);

CREATE TABLE sales (
  sale_id INTEGER PRIMARY KEY, -- Unique ID for each sale
  product_id INTEGER, -- ID of product sold
  customer_id INTEGER,  -- ID of customer who made purchase
  salesperson_id INTEGER, -- ID of salesperson who made the sale
  sale_date DATE, -- Date the sale occurred
  quantity INTEGER -- Quantity of product sold
);

CREATE TABLE product_suppliers (
  supplier_id INTEGER PRIMARY KEY, -- Unique ID for each supplier
  product_id INTEGER, -- Product ID supplied
  supply_price DECIMAL(10,2) -- Unit price charged by supplier
);

-- sales.product_id can be joined with products.product_id
-- sales.customer_id can be joined with customers.customer_id
-- sales.salesperson_id can be joined with salespeople.salesperson_id
-- product_suppliers.product_id can be joined with products.product_id

### Answer
Given the database schema, here is the SQL query that answers [QUESTION]{question}[/QUESTION]
[SQL]
"""
#%%
import sqlparse

def generate_query(question):
    updated_prompt = prompt.format(question=question)
#     updated_prompt=question
    inputs = tokenizer(updated_prompt, return_tensors="pt").to("cuda")
    generated_ids = model.generate(
        **inputs,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.eos_token_id,
        max_new_tokens=400,
        do_sample=False,
        num_beams=1,
    )
    outputs = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)

    torch.cuda.empty_cache()
    torch.cuda.synchronize()
    # empty cache so that you do generate more results w/o memory crashing
    # particularly important on Colab – memory management is much more straightforward
    # when running on an inference service
#     return outputs
    return sqlparse.format(outputs[0].split("[SQL]")[-1], reindent=True)
#%%
question = "What was our revenue by product in the new york region last month?"
generated_sql = generate_query(question)
print(generated_sql)
#%%
from transformers import AutoTokenizer
import transformers
import torch

model = "nextai-team/Moe-2x7b-QA-Code" 

tokenizer = AutoTokenizer.from_pretrained(model,load_in_4bit=True,device_map="auto")
pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    device_map="auto",
#     load_in_4bit=True,
    model_kwargs={"torch_dtype": torch.float16},
#     model_kwargs={"load_in_4bit": True},
)

def generate_resposne(query):
    messages = [{"role": "user", "content": query}]
    prompt = pipeline.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    outputs = pipeline(prompt, max_new_tokens=256, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
    return outputs[0]['generated_text']

response = generate_resposne("How to learn coding .Please provide a step by step procedure")
print(response)
#%%
import llm
model=llm.get_embedding_model("Starcoder")
model.prompt('asdf')
#%%
# Use a pipeline as a high-level helper
from transformers import pipeline

pipe = pipeline("text-generation", model="NousResearch/Nous-Hermes-Llama2-13b",device_map=auto)
print(pipe('write sample sql code',max_new_tokens=256))
#%%
from transformers import pipeline
pipe = pipeline("text-generation", model="uukuguy/speechless-nl2sql-ds-6.7b",device_map="auto")  
print(pipe('write sample sql code',max_new_tokens=256))
#%%
# Use a pipeline as a high-level helper
from transformers import pipeline

pipe = pipeline("text-generation", model="NousResearch/Nous-Hermes-llama-2-7b",device_map="auto")
print(pipe('write sample sql code',max_new_tokens=256,do_sample=True))