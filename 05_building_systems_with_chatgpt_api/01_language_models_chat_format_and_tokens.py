import os
import tiktoken
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI
from rich import print

# Load OPENAI_API_KEY from a local .env file into the environment.
_ = load_dotenv(find_dotenv())  # read local .env file

# Client for every chat.completions.create call below.
# api_key is the value just loaded; the SDK sends it on each request.
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# One user string in, the assistant's reply text out.
# The string is wrapped as a single user message. create() returns a
# completion object; the text is choices[0].message.content.
# Temperature stays commented out because gpt-5-nano only accepts its default.
def get_completion(prompt, model="gpt-5-nano"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        # temperature=0,  # course uses 0 for deterministic output; gpt-5-nano only allows 1
    )
    return response.choices[0].message.content

# Same call, but messages is already a list of {"role", "content"} dicts,
# so a system turn can sit in front of the user turn.
# temperature and max_completion_tokens are forwarded. On gpt-5-nano the
# token cap also counts reasoning tokens, not just the visible reply.
# Returns only the assistant text.
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

# Same chat call as get_completion_from_messages, plus the usage counts.
# content is the assistant text. token_dict holds prompt_tokens,
# completion_tokens, and total_tokens from response.usage.
# The live demo prints both, so the reply and its size show up together.
def get_completion_and_token_count(messages,
                                   model="gpt-5-nano",
                                   temperature=1,
                                   max_completion_tokens=5000):

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_completion_tokens=max_completion_tokens,
    )

    content = response.choices[0].message.content

    token_dict = {
'prompt_tokens': response.usage.prompt_tokens,
'completion_tokens': response.usage.completion_tokens,
'total_tokens': response.usage.total_tokens,
    }

    return content, token_dict

# Earlier demos stay in one unused string so they do not call the API.
# In order: capital of France; reverse "lollipop" as a word, then as
# hyphenated letters (splitting the letters changes the token task); a system
# turn that asks for Dr Seuss; one that forces a single sentence; both
# instructions in one system turn.
'''
# Prompt the model and get a completion

response = get_completion("What is the capital of France?")

print(response)

# tokens

response = get_completion("Take the letters in lollipop \
and reverse them")

print(response)

response = get_completion("""Take the letters in \
l-o-l-l-i-p-o-p and reverse them""")

print(response)

# Helper function (chat format)

messages =  [
{'role':'system',
 'content':"""You are an assistant who\
 responds in the style of Dr Seuss."""},
{'role':'user',
 'content':"""write me a very short poem\
 about a happy carrot"""},
]

response = get_completion_from_messages(messages, temperature=1)

print(response)

# length
messages =  [
{'role':'system',
 'content':'All your responses must be \
one sentence long.'},
{'role':'user',
 'content':'write me a story about a happy carrot'},
]

response = get_completion_from_messages(messages, temperature=1)

print(response)

# combined
messages =  [
{'role':'system',
 'content':"""You are an assistant who \
responds in the style of Dr Seuss. \
All your responses must be one sentence long."""},
{'role':'user',
 'content':"""write me a story about a happy carrot"""},
]

response = get_completion_from_messages(messages, temperature=1)

print(response)
'''

# Live call. The system turn sets the Dr Seuss voice; the user turn asks
# for a short poem. get_completion_and_token_count returns the poem and
# the three usage counts, and the two prints show them.
messages = [
{'role':'system',
 'content':"""You are an assistant who responds\
 in the style of Dr Seuss."""},
{'role':'user',
 'content':"""write me a very short poem \
 about a happy carrot"""},
]

response, token_dict = get_completion_and_token_count(messages)

print(response)

print(token_dict)
