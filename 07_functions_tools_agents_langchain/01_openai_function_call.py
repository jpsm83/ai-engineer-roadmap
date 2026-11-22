import os
import json
from rich import print

from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

_ = load_dotenv(find_dotenv())  # read local .env file
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Example dummy function hard coded to return the same weather
# In production, this could be your backend API or an external API
def get_current_weather(location, unit="fahrenheit"):
    """Get the current weather in a given location"""
    weather_info = {
        "location": location,
        "temperature": "72",
        "unit": unit,
        "forecast": ["sunny", "windy"],
    }

    return json.dumps(weather_info)


# define a tool
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location"],
            },
        },
    }
]

messages = [
    {
        "role": "user",
        "content": "What's the weather like in Barcelona?"
    }
]

'''
# Call the chat completions endpoint
response = client.chat.completions.create(
    model="gpt-5-nano",
    messages=messages,
    tools=tools,
)

print(response)

response_message = response.choices[0].message

print(response_message)

print(response_message.content)

print(response_message.tool_calls)

args = json.loads(response_message.tool_calls[0].function.arguments)

print(args)

print(get_current_weather(**args))

messages = [
    {
        "role": "user",
        "content": "hi!",
    }
]

response = client.chat.completions.create(
    model="gpt-5-nano",
    messages=messages,
    tools=tools,
)

print(response)

messages = [
    {
        "role": "user",
        "content": "hi!",
    }
]

response = client.chat.completions.create(
    model="gpt-5-nano",
    messages=messages,
    tools=tools,
    tool_choice="auto",
)

print(response)

messages = [
    {
        "role": "user",
        "content": "hi!",
    }
]

response = client.chat.completions.create(
    model="gpt-5-nano",
    messages=messages,
    tools=tools,
    tool_choice="none",
)

print(response)

messages = [
    {
        "role": "user",
        "content": "What's the weather in Barcelona?",
    }
]

response = client.chat.completions.create(
    model="gpt-5-nano",
    messages=messages,
    tools=tools,
    tool_choice="none",
)

print(response)

messages = [
    {
        "role": "user",
        "content": "hi!",
    }
]

response = client.chat.completions.create(
    model="gpt-5-nano",
    messages=messages,
    tools=tools,
    tool_choice={"type": "function", "function": {"name": "get_current_weather"}},
)

print(response)
'''

messages = [
    {
        "role": "user",
        "content": "What's the weather like in Barcelona!",
    }
]

response = client.chat.completions.create(
    model="gpt-5-nano",
    messages=messages,
    tools=tools,
    tool_choice={"type": "function", "function": {"name": "get_current_weather"}},
)

# print(response)

messages.append(response.choices[0].message)

tool_call = response.choices[0].message.tool_calls[0]
args = json.loads(tool_call.function.arguments)

observation = get_current_weather(**args)

messages.append(
        {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": observation,
        }
)

# print(messages)

response = client.chat.completions.create(
    model="gpt-5-nano",
    messages=messages,
)

print(response)
