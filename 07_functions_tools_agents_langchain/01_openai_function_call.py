import os
import json
from rich import print

from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

# Load OPENAI_API_KEY from a local .env file.
# The client below is given that key directly.
_ = load_dotenv(find_dotenv())  # read local .env file
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Stand-in for a weather API. It always reports 72 degrees, sunny and windy.
# The model never runs this function. The live path below calls it with the
# arguments the model chose, and sends the JSON string back as the tool result.
# The docstring is for a reader. The schema in `tools` is what the model sees.
def get_current_weather(location, unit="fahrenheit"):
    """Get the current weather in a given location"""
    weather_info = {
        "location": location,
        "temperature": "72",
        "unit": unit,
        "forecast": ["sunny", "windy"],
    }

    return json.dumps(weather_info)


# The tool list sent with the request. This describes the function; it does not call it.
# "name" is get_current_weather, the same name the forced tool_choice uses later.
# The model fills "location" (required) and, when it wants, "unit".
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

# A weather question, so a model that is allowed to choose would be expected
# to call get_current_weather. The live path further down replaces this list
# with a slightly different wording of the same question.
messages = [
    {
        "role": "user",
        "content": "What's the weather like in Barcelona?"
    }
]

# The block below is a string, so none of it runs. It walks tool_choice.
# Only the first call prints the message, the tool call, the arguments, and
# the dummy JSON. Every call prints the completion:
#   - tool_choice omitted: the model decides
#   - "hi!" with tools available: the model can answer in text and skip the tool
#   - "auto": the same decision as omitting tool_choice
#   - "none" on "hi!": the model must answer in text
#   - "none" on a weather question: the model still cannot call the tool
#   - a forced function on "hi!": the model must call get_current_weather anyway
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

# Live path. The question already asks for weather; forcing the tool makes this
# call about the tool-call shape, not about whether the model chooses the tool.
messages = [
    {
        "role": "user",
        "content": "What's the weather like in Barcelona!",
    }
]

# tools is the schema above. tool_choice names get_current_weather, which has
# to match the function name in that schema. The reply's tool_calls hold the
# arguments the model filled in. The text content is usually empty on this path.
response = client.chat.completions.create(
    model="gpt-5-nano",
    messages=messages,
    tools=tools,
    tool_choice={"type": "function", "function": {"name": "get_current_weather"}},
)

# The full completion: id, model, and the choice that contains the assistant message.
# print(response)

# Keep that assistant message, tool call included, so the next request
# can attach a result to it.
messages.append(response.choices[0].message)

# One forced call, so the first tool call is the one to run.
# arguments is a JSON string; the dummy function wants those keys as keywords.
tool_call = response.choices[0].message.tool_calls[0]
args = json.loads(tool_call.function.arguments)

# Run the local function. observation is the JSON weather string.
observation = get_current_weather(**args)

# A tool message answers one call. tool_call_id has to be tool_call.id,
# so the model can tell which request this result belongs to.
messages.append(
        {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": observation,
        }
)

# The conversation so far: user question, assistant tool call, tool result.
# print(messages)

# Second request. tools is omitted, so the model is not choosing a function.
# It reads the tool result already in messages and writes the weather answer.
response = client.chat.completions.create(
    model="gpt-5-nano",
    messages=messages,
)

print(response)
