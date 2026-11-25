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

_ = load_dotenv(find_dotenv()) # read local .env file
openai.api_key = os.environ['OPENAI_API_KEY']

llm_model = "gpt-5-nano"

@tool
def search(query: str) -> str:
    """Search for weather online"""
    return "42f"

# print(search.name, search.description, search.args)

class SearchInput(BaseModel):
    query: str = Field(description="Thing to search for")

@tool(args_schema=SearchInput)
def search(query: str) -> str:
    """Search for the weather online."""
    return "42f"

# print(search.args)

# print(search.run("sf"))

# Define the input schema
class OpenMeteoInput(BaseModel):
    latitude: float = Field(..., description="Latitude of the location to fetch weather data for")
    longitude: float = Field(..., description="Longitude of the location to fetch weather data for")

@tool(args_schema=OpenMeteoInput)
def get_current_temperature(latitude: float, longitude: float) -> dict:
    """Fetch current temperature for given coordinates."""
    
    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    
    # Parameters for the request
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'hourly': 'temperature_2m',
        'forecast_days': 1,
    }

    # Make the request
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        results = response.json()
    else:
        raise Exception(f"API Request failed with status code: {response.status_code}")

    current_utc_time = datetime.datetime.now(datetime.UTC)

    time_list = []
    for time_str in results['hourly']['time']:
        parsed = datetime.datetime.fromisoformat(time_str.replace('Z', '+00:00'))
        time_list.append(parsed if parsed.tzinfo else parsed.replace(tzinfo=datetime.UTC))

    temperature_list = results['hourly']['temperature_2m']
    
    closest_time_index = min(range(len(time_list)), key=lambda i: abs(time_list[i] - current_utc_time))

    current_temperature = temperature_list[closest_time_index]
    
    return f'The current temperature is {current_temperature}°C'

# print(get_current_temperature.name, get_current_temperature.description, get_current_temperature.args)

# print(convert_to_openai_function(get_current_temperature))

# print(get_current_temperature.invoke({"latitude": 13, "longitude": 14}))

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

# print(search_wikipedia.name, search_wikipedia.description, search_wikipedia.args)

# print(convert_to_openai_function(search_wikipedia))

# print(search_wikipedia.invoke({"query": "langchain"}))

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

spec = parse_obj(json.loads(text))

_PARAM_LOCATIONS = {
    "query": "params",
    "header": "headers",
    "cookie": "cookies",
    "path": "path_params",
}

pet_openai_functions = []

for path_item in (spec.paths or {}).values():
    for method in ("get", "put", "post", "delete", "options", "head", "patch", "trace"):
        operation = getattr(path_item, method)
        if operation is None:
            continue
        grouped = {}
        required = {}
        for parameter in [*(path_item.parameters or []), *(operation.parameters or [])]:
            arg_name = _PARAM_LOCATIONS[parameter.param_in]
            schema = parameter.param_schema.model_dump(mode="json", by_alias=True, exclude_none=True)
            if parameter.description and "description" not in schema:
                schema["description"] = parameter.description
            grouped.setdefault(arg_name, {})[parameter.name] = schema
            if parameter.required:
                required.setdefault(arg_name, []).append(parameter.name)
        properties = {
            arg_name: {
                "type": "object",
                "properties": params,
                "required": required.get(arg_name, []),
            }
            for arg_name, params in grouped.items()
        }
        pet_openai_functions.append({
            "name": operation.operationId,
            "description": operation.description or operation.summary or "",
            "parameters": {"type": "object", "properties": properties},
        })

# print(pet_openai_functions)

model = ChatOpenAI(model=llm_model, temperature=1).bind_tools(pet_openai_functions)

# print(model.invoke("what are three pets names"))

# print(model.invoke("tell me about pet with id 42"))

# Routing

functions = [
    convert_to_openai_function(f) for f in [
        search_wikipedia, get_current_temperature
    ]
]

model = ChatOpenAI(model=llm_model, temperature=1).bind_tools(functions)

# print(model.invoke("what is the weather in sf right now"))

# print(model.invoke("what is langchain"))

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are helpful but sassy assistant"),
    ("user", "{input}"),
])

chain = prompt | model

# print(chain.invoke({"input": "what is the weather in sf right now"}))

chain = prompt | model | OpenAIToolsAgentOutputParser()

result = chain.invoke({"input": "what is the weather in sf right now"})

# print(result)

# print(result[0].tool)

# print(result[0].tool_input)

# print(get_current_temperature.invoke(result[0].tool_input))

result = chain.invoke({"input": "hi!"})

# print(type(result))

# print(result.return_values)

def route(result):
    if isinstance(result, AgentFinish):
        return result.return_values['output']
    else:
        tools = {
            "search_wikipedia": search_wikipedia, 
            "get_current_temperature": get_current_temperature,
        }
        return tools[result[0].tool].invoke(result[0].tool_input)

chain = prompt | model | OpenAIToolsAgentOutputParser() | route

result = chain.invoke({"input": "What is the weather in san francisco right now?"})

print(result)

result = chain.invoke({"input": "What is langchain?"})

print(result)

result = chain.invoke({"input": "hi!"})

print(result)