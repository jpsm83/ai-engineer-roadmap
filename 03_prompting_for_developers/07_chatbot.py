import os
import panel as pn  # GUI
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI
from rich import print

# Load OPENAI_API_KEY from a local .env file into the environment.
_ = load_dotenv(find_dotenv())  # read local .env file

# Client for every chat.completions.create call below.
# api_key is the value just loaded; the SDK sends it on each request.
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Single-prompt helper from the earlier lessons: one user string in,
# assistant text out. create() returns a completion; the text is
# choices[0].message.content. The chat below calls get_completion_from_messages instead.
def get_completion(prompt, model="gpt-5-nano"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        # temperature=1,  # course uses 0 for deterministic output; gpt-5-nano only allows 1
    )
    return response.choices[0].message.content

# Chat call. messages is a list of {"role", "content"} dicts, system turn
# included. create() returns a completion; this hands back only the
# assistant text. The temperature argument is not forwarded: the create()
# line leaves it commented out. The commented print would show the whole
# message object.
def get_completion_from_messages(messages, model="gpt-5-nano", temperature=1):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        # temperature=temperature,  # course uses 0; gpt-5-nano only allows default 1
    )
#   print(str(response.choices[0].message))
    return response.choices[0].message.content

# Runs on each Chat click. The argument is the button event, unused here.
# inp.value_input is the submitted text; setting inp.value to '' clears the box.
# That user turn is appended to context, the whole list is sent, and the
# assistant reply is appended too, so the next click still sees earlier turns.
# panels is only the display: a user row and an assistant row.
# The returned column is what Panel redraws.
def collect_messages(_):
    prompt = inp.value_input
    inp.value = ''
    context.append({'role':'user', 'content':f"{prompt}"})
    response = get_completion_from_messages(context) 
    context.append({'role':'assistant', 'content':f"{response}"})
    panels.append(
        pn.Row('User:', pn.pane.Markdown(prompt, width=600)))
    panels.append(
        pn.Row('Assistant:', pn.pane.Markdown(response, width=600, styles={'background-color': '#F6F6F6'})))
 
    return pn.Column(*panels)

# Examples 1–4 are unused. Each one sends a fresh messages list, which is
# all the model can see on that call:
# 1. A Shakespeare system turn, then a joke the model is meant to finish.
# 2. The user says their name. Nothing is kept after the call returns.
# 3. A new list asks for the name and never includes it, so the model cannot know.
# 4. The same question, but the name is already in the assistant turn, so it can.
'''
# ============================== example 1 ==============================

messages =  [  
{'role':'system', 'content':'You are an assistant that speaks like Shakespeare.'},    
{'role':'user', 'content':'tell me a joke'},   
{'role':'assistant', 'content':'Why did the chicken cross the road'},   
{'role':'user', 'content':'I don\'t know'}  ]

response = get_completion_from_messages(messages, temperature=1)
print(response)

# ============================== example 2 ==============================

messages =  [  
{'role':'system', 'content':'You are friendly chatbot.'},    
{'role':'user', 'content':'Hi, my name is Isa'}  ]
response = get_completion_from_messages(messages, temperature=1)
print(response)

# ============================== example 3 ==============================

messages =  [  
{'role':'system', 'content':'You are friendly chatbot.'},    
{'role':'user', 'content':'Yes,  can you remind me, What is my name?'}  ]
response = get_completion_from_messages(messages, temperature=1)
print(response)

# ============================== example 4 ==============================

messages =  [  
{'role':'system', 'content':'You are friendly chatbot.'},
{'role':'user', 'content':'Hi, my name is Isa'},
{'role':'assistant', 'content': "Hi Isa! It's nice to meet you. \
Is there anything I can help you with today?"},
{'role':'user', 'content':'Yes, you can remind me, What is my name?'}  ]
response = get_completion_from_messages(messages, temperature=1)
print(response)
'''

# ==============================================================================
# ==============================================================================
# ==============================================================================

# Load Panel before building widgets.
pn.extension()

panels = [] # collect display 

# Conversation the model sees. It starts as the OrderBot system prompt:
# greet, take the whole order, ask pickup or delivery, summarize, then
# collect payment, using the menu prices in that text. Clicks append
# user and assistant turns onto this same list. panels above is display only.
context = [ {'role':'system', 'content':"""
You are OrderBot, an automated service to collect orders for a pizza restaurant. \
You first greet the customer, then collects the order, \
and then asks if it's a pickup or delivery. \
You wait to collect the entire order, then summarize it and check for a final \
time if the customer wants to add anything else. \
If it's a delivery, you ask for an address. \
Finally you collect the payment.\
Make sure to clarify all options, extras and sizes to uniquely \
identify the item from the menu.\
You respond in a short, very conversational friendly style. \
The menu includes \
pepperoni pizza  12.95, 10.00, 7.00 \
cheese pizza   10.95, 9.25, 6.50 \
eggplant pizza   11.95, 9.75, 6.75 \
fries 4.50, 3.50 \
greek salad 7.25 \
Toppings: \
extra cheese 2.00, \
mushrooms 1.50 \
sausage 3.00 \
canadian bacon 3.50 \
AI sauce 1.50 \
peppers 1.00 \
Drinks: \
coke 3.00, 2.00, 1.00 \
sprite 3.00, 2.00, 1.00 \
bottled water 5.00 \
"""} ]  # accumulate messages

# ============================== example 5 ==============================

# Text box and the Chat button. bind runs collect_messages on each click.
# pn.panel shows the column that callback returns, with a loading indicator
# while the model call is in flight. The column is the page: input, button,
# then that transcript.
inp = pn.widgets.TextInput(value="Hi", placeholder='Enter text here…')
button_conversation = pn.widgets.Button(name="Chat!")

interactive_conversation = pn.bind(collect_messages, button_conversation)

dashboard = pn.Column(
    inp,
    pn.Row(button_conversation),
    pn.panel(interactive_conversation, loading_indicator=True, height=300),
)

# In a notebook, a bare `dashboard` is enough to render. From a .py file
# you need .show() to start a local server and open the browser.
dashboard.show()

# ============================== example 6 ==============================

# After show() returns, copy the chat so far and append a system turn that
# asks for JSON: pizza and size, toppings, drinks and size, sides and size,
# and the total price. copy() leaves the OrderBot context unchanged.
# The commented line under the message is an alternate field list, left as written.
messages =  context.copy()
messages.append(
{'role':'system', 'content':'create a json summary of the previous food order. Itemize the price for each item\
 The fields should be 1) pizza, include size 2) list of toppings 3) list of drinks, include size   4) list of sides include size  5)total price '},    
)
 #The fields should be 1) pizza, price 2) list of toppings 3) list of drinks, include size include price  4) list of sides include size include price, 5)total price '},    

response = get_completion_from_messages(messages, temperature=1)
print(response)
