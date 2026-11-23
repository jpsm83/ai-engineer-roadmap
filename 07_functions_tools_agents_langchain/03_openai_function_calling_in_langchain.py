from dotenv import load_dotenv, find_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field, ValidationError
from rich import print

_ = load_dotenv(find_dotenv())  # read local .env file

llm_model = "gpt-5-nano"

# Pydantic Syntax

class User:
    def __init__(self, name: str, age: int, email: str):
        self.name = name
        self.age = age
        self.email = email

foo = User(name="Joe", age=32, email="joe@gmail.com")

# print(foo.name)

# A plain class does not validate types.
foo = User(name="Joe", age="bar", email="joe@gmail.com")

# print(foo.age)

class pUser(BaseModel):
    name: str
    age: int
    email: str

foo_p = pUser(name="Jane", age=32, email="jane@gmail.com")

# print(foo_p.name)

try:
    foo_p = pUser(name="Jane", age="bar", email="jane@gmail.com")
except ValidationError as error:
    # print(error)
    pass

class Class(BaseModel):
    students: list[pUser]

obj = Class(
    students=[pUser(name="Jane", age=32, email="jane@gmail.com")]
)

# print(obj)

# Pydantic to OpenAI function definition

class WeatherSearch(BaseModel):
    """Call this with an airport code to get the weather at that airport"""
    airport_code: str = Field(description="airport code to get weather for")


weather_function = convert_to_openai_function(WeatherSearch)

# print(weather_function)

class WeatherSearch1(BaseModel):
    airport_code: str = Field(description="airport code to get weather for")

# No class docstring, so the function description is empty.
# print(convert_to_openai_function(WeatherSearch1))

class WeatherSearch2(BaseModel):
    """Call this with an airport code to get the weather at that airport"""
    airport_code: str

# Docstring is used as the description; the field has no description of its own.
# print(convert_to_openai_function(WeatherSearch2))

model = ChatOpenAI(model=llm_model)

# model.bind_tools([weather_function]).invoke("what is the weather in SF today?")

model_with_function = model.bind_tools([weather_function])
# model_with_function.invoke("what is the weather in sf?")

# Forcing it to use a function

model_with_forced_function = model.bind_tools(
    [weather_function],
    tool_choice="WeatherSearch",
)

# model_with_forced_function.invoke("what is the weather in sf?")

# model_with_forced_function.invoke("hi!")

# Using in a chain

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant"),
    ("user", "{input}")
])

chain = prompt | model_with_function

# print(chain.invoke({"input": "what is the weather in sf?"}))

# Using multiple functions

class ArtistSearch(BaseModel):
    """Call this to get the names of songs by a particular artist"""
    artist_name: str = Field(description="name of artist to look up")
    n: int = Field(description="number of results")

tools = [
    convert_to_openai_function(WeatherSearch),
    convert_to_openai_function(ArtistSearch),
]

model_with_functions = model.bind_tools(tools)

print(model_with_functions.invoke("what is the weather in sf?"))

print(model_with_functions.invoke("what are three songs by taylor swift?"))

print(model_with_functions.invoke("hi!"))
