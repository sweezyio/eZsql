from taipy.gui import Gui, notify

page="""
<|container|
# **Generate**{: .color-primary} Tweets

This websites generates SQL queries using an [open-source master of experts model](https://huggingface.co/nextai-team/Moe-2x7b-QA-Code).

<br/>

<|layout|columns=1 1|gap=30px|class_name=card|
<topic|
## **English**{: .color-primary}

<|{topic}|input|multiline|label=English|class_name=fullwidth|>
|topic>

### Generated **Tweet**{: .color-primary}
<|{tweet}|input|multiline|label=Resulting query|class_name=fullwidth|>

<|Generate text|button|on_action=generate_text|label=Generate text|>
|>

<br/>


<center><|Generate image|button|on_action=generate_image|label=Generate image|active={prompt!="" and tweet!=""}|></center>

<image|part|render={prompt != "" and tweet != "" and image is not None}|class_name=card|
### **Image**{: .color-primary} from Dall-e

<center><|{image}|image|height=400px|></center>
|image>
|>
"""


if __name__ == "__main__":
    Gui(page).run()
