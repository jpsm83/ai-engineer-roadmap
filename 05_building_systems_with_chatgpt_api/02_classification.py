import os
import tiktoken
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI
from rich import print

# Load OPENAI_API_KEY from a local .env file into the environment.
_ = load_dotenv(find_dotenv())  # read local .env file

# Client for the chat call in get_completion_from_messages.
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Chat call. messages is a list of {"role", "content"} dicts.
# create() returns a completion; this hands back only the assistant text.
# max_completion_tokens also counts reasoning tokens on gpt-5-nano.
def get_completion_from_messages(messages,
                                 model="gpt-5-nano",
                                 temperature=1,
                                 max_completion_tokens=5000):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_completion_tokens=max_completion_tokens,  # includes reasoning tokens on gpt-5-nano
    )
    return response.choices[0].message.content

# Classify customer queries to handle different cases
# The model must return JSON with keys primary and secondary, chosen from
# the lists in the system text. delimiter is ####. The user message wraps
# the query in that same string, so the model can see where the query
# starts and ends. Those two spellings have to match.

delimiter = "####"
system_message = f"""
You will be provided with customer service queries. \
The customer service query will be delimited with \
{delimiter} characters.
Classify each query into a primary category \
and a secondary category. 
Provide your output in json format with the \
keys: primary and secondary.

Primary categories: Billing, Technical Support, \
Account Management, or General Inquiry.

Billing secondary categories:
Unsubscribe or upgrade
Add a payment method
Explanation for charge
Dispute a charge

Technical Support secondary categories:
General troubleshooting
Device compatibility
Software updates

Account Management secondary categories:
Password reset
Update personal information
Close account
Account security

General Inquiry secondary categories:
Product information
Pricing
Feedback
Speak to a human

"""

# Unused query: deleting a profile would be Account Management / Close
# account. Left in this string so it does not call the API.
'''
user_message = f"""\
I want you to delete my profile and all of my user data"""
messages =  [  
{'role':'system', 
 'content': system_message},    
{'role':'user', 
 'content': f"{delimiter}{user_message}{delimiter}"},  
]

response = get_completion_from_messages(messages)

print(response)
'''

# Live query. A question about flat screen TVs should land in
# General Inquiry / Product information. The user content is that query
# wrapped in ####, matching delimiter in the system message.
user_message = f"""\
Tell me more about your flat screen tvs"""
messages =  [  
{'role':'system', 
 'content': system_message},    
{'role':'user', 
 'content': f"{delimiter}{user_message}{delimiter}"},  
]

response = get_completion_from_messages(messages)

print(response)
