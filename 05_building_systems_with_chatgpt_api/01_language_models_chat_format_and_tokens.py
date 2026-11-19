import os
import tiktoken
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

_ = load_dotenv(find_dotenv())  # read local .env file

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_completion(prompt, model="gpt-5-nano"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        # temperature=0,  # course uses 0 for deterministic output; gpt-5-nano only allows 1
    )
    return response.choices[0].message.content

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
