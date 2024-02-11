from taipy.gui import Gui, notify
import query as model
import pyperclip

def generate_sql(state):
	# Check if the user has put a topic
	if state.query == "":
		notify(state, "error", "Please enter a query")
		return
	if state.oldQuery==state.query:
		notify(state,"error", "Same query!")
	else:
		state.oldQuery=state.query
		state.output = model.run(state.query,schema)
		# state.output='test'
		notify(state, "success", "SQL created!")
def copy(state):
	pyperclip.copy(state.output)
	notify(state,'success','Copied to clipboard!')

query=""
output=""
oldQuery=""
schema=""
page="""
<|container|
# **eZsql**{: .color-primary}

This websites generates SQL queries using an [open-source CodeLlama 7B-AWQ](https://huggingface.co/TheBloke/CodeLlama-7B-AWQ).

<br/>

<|layout|columns=1 1 1|gap=30px|class_name=card|
<topic|
### **English**{: .color-primary}
<|{query}|input|multiline|label=English|class_name=fullwidth|lines_shown=2|>
<|{schema}|input|label=Schema (optional)|multiline|lines_shown=0|>
|topic>

<middle|
###&nbsp;
<center><|Generate SQL|button|on_action=generate_sql|label=Generate SQL|></center>
|>

<output|
### Generated **SQL**{: .color-primary}
<|{output}|input|multiline|label=Resulting query|class_name=fullwidth|active=False|lines_shown=2|>
|output>
|>
Made with ❤️ in Atlanta.
|>
"""
# <|copy|button|on_action=copy|label=copy|>
Gui(page).run(title='eZsql', watermark="", favicon=r"drawing.png")