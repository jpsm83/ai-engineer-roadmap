from dotenv import load_dotenv, find_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field, ValidationError
from rich import print

# Load OPENAI_API_KEY from a local .env file.
# ChatOpenAI reads that variable on its own.
_ = load_dotenv(find_dotenv())  # read local .env file

llm_model = "gpt-5-nano"

# A plain class stores whatever you pass. It does not check types.
# The first object is a normal user. The print would show "Joe".
class User:
    def __init__(self, name: str, age: int, email: str):
        self.name = name
        self.age = age
        self.email = email

foo = User(name="Joe", age=32, email="joe@gmail.com")

# print(foo.name)

# Replaces foo. age is the string "bar", and the plain class stores it.
foo = User(name="Joe", age="bar", email="joe@gmail.com")

# print(foo.age)

# BaseModel checks the types when the object is built.
# age=32 is an int, so this one succeeds. The print would show "Jane".
class pUser(BaseModel):
    name: str
    age: int
    email: str

foo_p = pUser(name="Jane", age=32, email="jane@gmail.com")

# print(foo_p.name)

# age="bar" fails that check. ValidationError is raised before foo_p is replaced,
# and the commented print would show the error. pass lets the lesson continue.
try:
    foo_p = pUser(name="Jane", age="bar", email="jane@gmail.com")
except ValidationError as error:
    # print(error)
    pass

# A model can hold other models. students is a list of pUser.
# The print would show the outer object and the Jane record inside it.
class Class(BaseModel):
    students: list[pUser]

obj = Class(
    students=[pUser(name="Jane", age=32, email="jane@gmail.com")]
)

# print(obj)

# Turn a Pydantic model into the JSON schema sent to the model.
# The class docstring becomes the tool description. Field(description=...)
# becomes the argument description. The model fills airport_code; this class
# is not called.
class WeatherSearch(BaseModel):
    """Call this with an airport code to get the weather at that airport"""
    airport_code: str = Field(description="airport code to get weather for")


# weather_function is that schema. The print would show the name, description,
# and airport_code. bind_tools below sends this object to the model.
weather_function = convert_to_openai_function(WeatherSearch)

# print(weather_function)

# Same field, no class docstring, so the tool description in the schema is empty.
class WeatherSearch1(BaseModel):
    airport_code: str = Field(description="airport code to get weather for")

# The print would show WeatherSearch1's schema with an empty description.
# print(convert_to_openai_function(WeatherSearch1))

# Docstring is present, so that becomes the tool description.
# The field has no Field(description=...), so the argument description is empty.
class WeatherSearch2(BaseModel):
    """Call this with an airport code to get the weather at that airport"""
    airport_code: str

# The print would show a description from the docstring and a blank argument description.
# print(convert_to_openai_function(WeatherSearch2))

# Chat model with no tools yet. Each bind_tools below returns a new runnable
# and leaves this one unchanged.
model = ChatOpenAI(model=llm_model)

# bind_tools attaches weather_function. The invoke would return a message that
# can request WeatherSearch for a San Francisco question.
# model.bind_tools([weather_function]).invoke("what is the weather in SF today?")

# Same binding, kept so the chain further down can use it.
# The model may call the tool or answer in text. The invoke would show which.
model_with_function = model.bind_tools([weather_function])
# model_with_function.invoke("what is the weather in sf?")

# tool_choice forces the function whose name is the class name, WeatherSearch.
# The weather question calls it because it was asked. "hi!" calls it anyway.
model_with_forced_function = model.bind_tools(
    [weather_function],
    tool_choice="WeatherSearch",
)

# model_with_forced_function.invoke("what is the weather in sf?")

# model_with_forced_function.invoke("hi!")

# {input} is filled by chain.invoke. The chain uses model_with_function,
# the binding that lets the model choose, not the forced one above.
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant"),
    ("user", "{input}")
])

# prompt fills the messages, then the bound model replies.
# The print would show that message for a San Francisco weather question.
chain = prompt | model_with_function

# print(chain.invoke({"input": "what is the weather in sf?"}))

# Second tool. The docstring tells the model this is for songs.
# artist_name and n are the arguments it fills. Nothing here looks up music.
class ArtistSearch(BaseModel):
    """Call this to get the names of songs by a particular artist"""
    artist_name: str = Field(description="name of artist to look up")
    n: int = Field(description="number of results")

# Both schemas, in the order the model is offered them.
tools = [
    convert_to_openai_function(WeatherSearch),
    convert_to_openai_function(ArtistSearch),
]

# The model can request either tool, or answer in text.
model_with_functions = model.bind_tools(tools)

# Weather question: a WeatherSearch tool call.
print(model_with_functions.invoke("what is the weather in sf?"))

# Song question: an ArtistSearch tool call, with n for "three".
print(model_with_functions.invoke("what are three songs by taylor swift?"))

# Greeting: a text answer, no tool call.
print(model_with_functions.invoke("hi!"))
