import os
import json
import openai
from langchain.tools import tool
from dotenv import load_dotenv, find_dotenv
from pydantic import BaseModel, Field
import requests
import datetime
from langchain_core.utils.function_calling import convert_to_openai_function
import wikipedia
from openapi_pydantic import parse_obj
from langchain_openai import ChatOpenAI
from langchain_classic.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.agents import AgentFinish
from rich import print

# Load OPENAI_API_KEY from a local .env file.
# openai.api_key is set from that variable. ChatOpenAI reads the env var itself.
_ = load_dotenv(find_dotenv()) # read local .env file
openai.api_key = os.environ['OPENAI_API_KEY']

llm_model = "gpt-5-nano"

# @tool wraps the function as a LangChain tool.
# The docstring becomes the description the model uses to decide when to call it.
# No args_schema: LangChain infers one string argument, query, from the signature.
# The body always returns "42f". The print would show name, description, and args.
@tool
def search(query: str) -> str:
    """Search for weather online"""
    return "42f"

# print(search.name, search.description, search.args)

# Schema the model fills for query. The class itself does not run.
class SearchInput(BaseModel):
    query: str = Field(description="Thing to search for")

# search is defined again, so this tool replaces the one above.
# args_schema uses SearchInput instead of the inferred signature.
# The body still returns "42f".
# The prints would show the new args, then that dummy result for "sf".
@tool(args_schema=SearchInput)
def search(query: str) -> str:
    """Search for the weather online."""
    return "42f"

# print(search.args)

# print(search.run("sf"))

# Argument schema for the weather tool.
# The model sees the field names and descriptions and fills them in
# when it decides to call the tool. It does not run this class itself.
class OpenMeteoInput(BaseModel):
    latitude: float = Field(..., description="Latitude of the location to fetch weather data for")
    longitude: float = Field(..., description="Longitude of the location to fetch weather data for")

# @tool wraps the function. The docstring becomes the description.
# args_schema is OpenMeteoInput, so the model fills latitude and longitude
# instead of a schema inferred from the signature.
@tool(args_schema=OpenMeteoInput)
def get_current_temperature(latitude: float, longitude: float) -> dict:
    """Fetch current temperature for given coordinates."""
    
    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    
    # Ask Open-Meteo for today's hourly temperatures at this point.
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'hourly': 'temperature_2m',
        'forecast_days': 1,
    }

    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        results = response.json()
    else:
        raise Exception(f"API Request failed with status code: {response.status_code}")

    # The API returns a list of hours, not "now".
    # Pick the hour closest to the current UTC time and return that temperature.
    current_utc_time = datetime.datetime.now(datetime.UTC)

    time_list = []
    for time_str in results['hourly']['time']:
        parsed = datetime.datetime.fromisoformat(time_str.replace('Z', '+00:00'))
        time_list.append(parsed if parsed.tzinfo else parsed.replace(tzinfo=datetime.UTC))

    temperature_list = results['hourly']['temperature_2m']
    
    closest_time_index = min(range(len(time_list)), key=lambda i: abs(time_list[i] - current_utc_time))

    current_temperature = temperature_list[closest_time_index]
    
    return f'The current temperature is {current_temperature}°C'

# These prints inspect the tool LangChain built:
# name and description come from the function, args come from the schema.
# print(get_current_temperature.name, get_current_temperature.description, get_current_temperature.args)

# convert_to_openai_function turns the tool into the JSON schema sent to the model.
# print(convert_to_openai_function(get_current_temperature))

# invoke runs the tool with a dict of arguments. Tools are not called like normal functions.
# print(get_current_temperature.invoke({"latitude": 13, "longitude": 14}))

# No args_schema: LangChain infers one string argument, query, from the signature.
# The docstring is the description the model sees: search Wikipedia and return summaries.
@tool
def search_wikipedia(query: str) -> str:
    """Run Wikipedia search and get page summaries."""
    page_titles = wikipedia.search(query)
    summaries = []
    for page_title in page_titles[: 3]:
        try:
            wiki_page =  wikipedia.page(title=page_title, auto_suggest=False)
            summaries.append(f"Page: {page_title}\nSummary: {wiki_page.summary}")
        except (
            self.wiki_client.exceptions.PageError,
            self.wiki_client.exceptions.DisambiguationError,
        ):
            pass
    if not summaries:
        return "No good Wikipedia Search Result was found"
    return "\n\n".join(summaries)

# Same three inspections as the weather tool: the tool object, its JSON schema,
# and a real invoke. This invoke would show Wikipedia summaries for "langchain".
# print(search_wikipedia.name, search_wikipedia.description, search_wikipedia.args)

# print(convert_to_openai_function(search_wikipedia))

# print(search_wikipedia.invoke({"query": "langchain"}))

# An OpenAPI Petstore document, pasted in as text. This lesson does not call
# that server. The loop below turns each operation into a function schema.
text = """
{
  "openapi": "3.0.0",
  "info": {
    "version": "1.0.0",
    "title": "Swagger Petstore",
    "license": {
      "name": "MIT"
    }
  },
  "servers": [
    {
      "url": "http://petstore.swagger.io/v1"
    }
  ],
  "paths": {
    "/pets": {
      "get": {
        "summary": "List all pets",
        "operationId": "listPets",
        "tags": [
          "pets"
        ],
        "parameters": [
          {
            "name": "limit",
            "in": "query",
            "description": "How many items to return at one time (max 100)",
            "required": false,
            "schema": {
              "type": "integer",
              "maximum": 100,
              "format": "int32"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "A paged array of pets",
            "headers": {
              "x-next": {
                "description": "A link to the next page of responses",
                "schema": {
                  "type": "string"
                }
              }
            },
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/Pets"
                }
              }
            }
          },
          "default": {
            "description": "unexpected error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/Error"
                }
              }
            }
          }
        }
      },
      "post": {
        "summary": "Create a pet",
        "operationId": "createPets",
        "tags": [
          "pets"
        ],
        "responses": {
          "201": {
            "description": "Null response"
          },
          "default": {
            "description": "unexpected error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/Error"
                }
              }
            }
          }
        }
      }
    },
    "/pets/{petId}": {
      "get": {
        "summary": "Info for a specific pet",
        "operationId": "showPetById",
        "tags": [
          "pets"
        ],
        "parameters": [
          {
            "name": "petId",
            "in": "path",
            "required": true,
            "description": "The id of the pet to retrieve",
            "schema": {
              "type": "string"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Expected response to a valid request",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/Pet"
                }
              }
            }
          },
          "default": {
            "description": "unexpected error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/Error"
                }
              }
            }
          }
        }
      }
    }
  },
  "components": {
    "schemas": {
      "Pet": {
        "type": "object",
        "required": [
          "id",
          "name"
        ],
        "properties": {
          "id": {
            "type": "integer",
            "format": "int64"
          },
          "name": {
            "type": "string"
          },
          "tag": {
            "type": "string"
          }
        }
      },
      "Pets": {
        "type": "array",
        "maxItems": 100,
        "items": {
          "$ref": "#/components/schemas/Pet"
        }
      },
      "Error": {
        "type": "object",
        "required": [
          "code",
          "message"
        ],
        "properties": {
          "code": {
            "type": "integer",
            "format": "int32"
          },
          "message": {
            "type": "string"
          }
        }
      }
    }
  }
}
"""

# json.loads reads the text into a dict. parse_obj turns that dict into a spec.
spec = parse_obj(json.loads(text))

# OpenAPI records where a parameter lives. The function schema groups those
# under the names on the right, which is what the model is asked to fill.
_PARAM_LOCATIONS = {
    "query": "params",
    "header": "headers",
    "cookie": "cookies",
    "path": "path_params",
}

# One function dict per operation that the spec actually defines.
pet_openai_functions = []

for path_item in (spec.paths or {}).values():
    for method in ("get", "put", "post", "delete", "options", "head", "patch", "trace"):
        operation = getattr(path_item, method)
        if operation is None:
            continue
        grouped = {}
        required = {}
        # Parameters on the path and on this operation both become arguments.
        # param_in (query, path, ...) picks the group from _PARAM_LOCATIONS.
        for parameter in [*(path_item.parameters or []), *(operation.parameters or [])]:
            arg_name = _PARAM_LOCATIONS[parameter.param_in]
            schema = parameter.param_schema.model_dump(mode="json", by_alias=True, exclude_none=True)
            # Copy the parameter description onto the schema when the schema
            # does not already have one. That text is what the model reads.
            if parameter.description and "description" not in schema:
                schema["description"] = parameter.description
            grouped.setdefault(arg_name, {})[parameter.name] = schema
            if parameter.required:
                required.setdefault(arg_name, []).append(parameter.name)
        # Each group is one object argument, such as params or path_params.
        properties = {
            arg_name: {
                "type": "object",
                "properties": params,
                "required": required.get(arg_name, []),
            }
            for arg_name, params in grouped.items()
        }
        # name is the operationId. description prefers the long text, then the summary.
        pet_openai_functions.append({
            "name": operation.operationId,
            "description": operation.description or operation.summary or "",
            "parameters": {"type": "object", "properties": properties},
        })

# The print would show one schema per operation: listPets, createPets, showPetById.
# print(pet_openai_functions)

# bind_tools attaches those schemas. The model can request one of them.
# Nothing here calls the petstore. The prints would show the tool call for
# a list of pet names, and the tool call for pet id 42.
model = ChatOpenAI(model=llm_model, temperature=1).bind_tools(pet_openai_functions)

# print(model.invoke("what are three pets names"))

# print(model.invoke("tell me about pet with id 42"))

# Weather and Wikipedia as the JSON schemas bind_tools expects.
functions = [
    convert_to_openai_function(f) for f in [
        search_wikipedia, get_current_temperature
    ]
]

# New chat model bound to those two tools. This replaces the petstore binding.
# A weather question should request get_current_temperature.
# A LangChain question should request search_wikipedia.
model = ChatOpenAI(model=llm_model, temperature=1).bind_tools(functions)

# print(model.invoke("what is the weather in sf right now"))

# print(model.invoke("what is langchain"))

# {input} is filled by invoke. The system message sets the assistant's tone.
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are helpful but sassy assistant"),
    ("user", "{input}"),
])

# prompt fills the messages, then the bound model replies.
# The print would show the message, including a weather tool call.
chain = prompt | model

# print(chain.invoke({"input": "what is the weather in sf right now"}))

# chain is defined again. OpenAIToolsAgentOutputParser reads the reply and returns
# either a list of tool actions, when the model wants a tool, or AgentFinish,
# when the model is giving the final answer.
chain = prompt | model | OpenAIToolsAgentOutputParser()

# A weather question should come back as a tool action, not a finished answer.
result = chain.invoke({"input": "what is the weather in sf right now"})

# The action list. [0] is the first action.
# print(result)

# .tool is the tool name. .tool_input is the argument dict.
# print(result[0].tool)

# print(result[0].tool_input)

# Run the weather tool with the arguments the model chose.
# print(get_current_temperature.invoke(result[0].tool_input))

# "hi!" needs no tool, so this result should be an AgentFinish.
result = chain.invoke({"input": "hi!"})

# AgentFinish, rather than a list of actions.
# print(type(result))

# return_values holds the text answer, under "output".
# print(result.return_values)

# AgentFinish: return the text answer.
# A tool action is a list. [0].tool must match a key below, and
# [0].tool_input is the dict invoke passes to that tool.
def route(result):
    if isinstance(result, AgentFinish):
        return result.return_values['output']
    else:
        tools = {
            "search_wikipedia": search_wikipedia, 
            "get_current_temperature": get_current_temperature,
        }
        return tools[result[0].tool].invoke(result[0].tool_input)

# chain is defined again. route now sits at the end, so invoke returns
# either the tool's output or the text answer.
chain = prompt | model | OpenAIToolsAgentOutputParser() | route

# Weather path: get_current_temperature runs, and result is its sentence.
result = chain.invoke({"input": "What is the weather in san francisco right now?"})

print(result)

# Wikipedia path: search_wikipedia runs, and result is the joined summaries.
result = chain.invoke({"input": "What is langchain?"})

print(result)

# No tool. route returns the model's text answer.
result = chain.invoke({"input": "hi!"})

print(result)