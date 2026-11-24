from operator import attrgetter
from typing import Literal
from urllib.request import Request, urlopen
from operator import itemgetter
import bs4
from dotenv import load_dotenv, find_dotenv
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.utils.function_calling import convert_to_openai_function
from pydantic import BaseModel, Field
from langchain_openai.output_parsers import JsonOutputKeyToolsParser
from rich import print

_ = load_dotenv(find_dotenv())  # read local .env file

llm_model = "gpt-5-nano"
model = ChatOpenAI(model=llm_model)

# Tagging

class Tagging(BaseModel):
    """Tag the piece of text with particular info."""
    sentiment: Literal["pos", "neg", "neutral"] = Field(
        description="sentiment of the text"
    )
    language: str = Field(description="language of the text (ISO 639-1 code)")

tagging_function = convert_to_openai_function(Tagging)

# print(tagging_function)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Think carefully, and then tag the text as instructed"),
    ("user", "{input}")
])

model_with_function = model.bind_tools(
    [tagging_function],
    tool_choice={"type": "function", "function": {"name": "Tagging"}},
)

tagging_chain = prompt | model_with_function

# print(tagging_chain.invoke({"input": "I love langchain"}))

# print(tagging_chain.invoke({"input": "non mi piace questo cibo"}))

tagging_chain = prompt | model_with_function | JsonOutputKeyToolsParser(key_name="Tagging", first_tool_only=True)

#print(tagging_chain.invoke({"input": "non mi piace questo cibo"}))

# Extraction

class Person(BaseModel):
    """Information about a person."""
    name: str = Field(description="person's name")
    age: int | None = Field(default=None, description="person's age")

class Information(BaseModel):
    """Information to extract."""
    people: list[Person] = Field(description="List of info about people")

extraction_functions = [convert_to_openai_function(Information)]

# print(extraction_functions)

extraction_model = model.bind_tools(extraction_functions, tool_choice={"type": "function", "function": {"name": "Information"}})

# print(extraction_model.invoke("Joe is 30, his mom is Martha"))

prompt = ChatPromptTemplate.from_messages([
    ("system", "Extract the relevant information, if not explicitly provided do not guess. Extract partial info"),
    ("human", "{input}")
])

extraction_chain = prompt | extraction_model

# print(extraction_chain.invoke({"input": "Joe is 30, his mom is Martha"}))

extraction_chain = prompt | extraction_model | JsonOutputKeyToolsParser(key_name="Information", first_tool_only=True)

# print(extraction_chain.invoke({"input": "Joe is 30, his mom is Martha"}))

extraction_chain = (prompt | extraction_model | JsonOutputKeyToolsParser(key_name="Information", first_tool_only=True) | itemgetter("people"))

# print(extraction_chain.invoke({"input": "Joe is 30, his mom is Martha"}))

# Doing it for real

url = "https://lilianweng.github.io/posts/2023-06-23-agent/"

request = Request(url, headers={"User-Agent": "ai-engineer-roadmap"})

with urlopen(request, timeout=30) as response:
    html = response.read().decode("utf-8")

doc = Document(
    page_content=bs4.BeautifulSoup(html, "html.parser").get_text(),
    metadata={"source": url},
)

page_content = doc.page_content[:10000]

# print(page_content[:1000])

class Overview(BaseModel):
    """Overview of a section of text."""
    summary: str = Field(description="Provide a concise summary of the content.")
    language: str = Field(description="Provide the language that the content is written in.")
    keywords: str = Field(description="Provide keywords related to the content.")

overview_tagging_function = [
    convert_to_openai_function(Overview)
]

tagging_model = model.bind_tools(
    overview_tagging_function,
    tool_choice={"type": "function", "function": {"name": "Overview"}}
)

tagging_chain = prompt | tagging_model | JsonOutputKeyToolsParser(key_name="Overview", first_tool_only=True)

# print(tagging_chain.invoke({"input": page_content}))

class Paper(BaseModel):
    """Information about papers mentioned."""
    title: str
    author: str | None = None

class Info(BaseModel):
    """Information to extract"""
    papers: list[Paper]

paper_extraction_function = [
    convert_to_openai_function(Info)
]

extraction_model = model.bind_tools(
    paper_extraction_function,
    tool_choice={"type": "function", "function": {"name": "Info"}}
)

extraction_chain = (prompt | extraction_model | JsonOutputKeyToolsParser(key_name="Info", first_tool_only=True) | itemgetter("papers"))

# print(extraction_chain.invoke({"input": page_content}))

template = """A article will be passed to you. Extract from it all papers that are mentioned by this article follow by its author. 
    Do not extract the name of the article itself. If no papers are mentioned that's fine - you don't need to extract any! Just return an empty list.
    Do not make up or guess ANY extra information. Only extract what exactly is in the text."""
    
prompt = ChatPromptTemplate.from_messages([
    ("system", template),
    ("human", "{input}")
])

extraction_chain = (prompt | extraction_model | JsonOutputKeyToolsParser(key_name="Info", first_tool_only=True) | itemgetter("papers"))

# print(extraction_chain.invoke({"input": page_content}))

# print(extraction_chain.invoke({"input": "hi"}))

text_splitter = RecursiveCharacterTextSplitter(chunk_overlap=0)

splits = text_splitter.split_text(doc.page_content)

len(splits)

def flatten(matrix):
    flat_list = []
    for row in matrix:
        flat_list += row
    return flat_list

flatten([[1, 2], [3, 4]])

# print(splits[0])

prep = RunnableLambda(
    lambda x: [{"input": doc} for doc in text_splitter.split_text(x)]
)

# print(prep.invoke("hi"))

chain = prep | extraction_chain.map() | flatten

print(chain.invoke(doc.page_content))
