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

# Load OPENAI_API_KEY from a local .env file.
# ChatOpenAI reads that variable on its own.
_ = load_dotenv(find_dotenv())  # read local .env file

llm_model = "gpt-5-nano"
model = ChatOpenAI(model=llm_model)

# Schema for a tag, not a function that runs.
# The docstring is the tool description. sentiment is limited to those three
# strings, and language is the ISO code the model fills in.
class Tagging(BaseModel):
    """Tag the piece of text with particular info."""
    sentiment: Literal["pos", "neg", "neutral"] = Field(
        description="sentiment of the text"
    )
    language: str = Field(description="language of the text (ISO 639-1 code)")

# The JSON schema for Tagging. The print would show the name, description,
# and the two fields. The name is the class name, which tool_choice uses below.
tagging_function = convert_to_openai_function(Tagging)

# print(tagging_function)

# {input} is the text to tag, filled at invoke time.
prompt = ChatPromptTemplate.from_messages([
    ("system", "Think carefully, and then tag the text as instructed"),
    ("user", "{input}")
])

# bind_tools attaches the schema. tool_choice forces Tagging, the class name,
# so the model must call it instead of answering in text.
model_with_function = model.bind_tools(
    [tagging_function],
    tool_choice={"type": "function", "function": {"name": "Tagging"}},
)

# prompt fills the messages, then the bound model replies with a tool call.
# The prints would show that message for an English sentence and an Italian one.
tagging_chain = prompt | model_with_function

# print(tagging_chain.invoke({"input": "I love langchain"}))

# print(tagging_chain.invoke({"input": "non mi piace questo cibo"}))

# tagging_chain is defined again. JsonOutputKeyToolsParser reads the tool-call
# arguments out of the message. key_name has to be "Tagging", the function name.
# first_tool_only=True returns that one call's arguments as a dict.
# The print would show sentiment and language for the Italian sentence.
tagging_chain = prompt | model_with_function | JsonOutputKeyToolsParser(key_name="Tagging", first_tool_only=True)

#print(tagging_chain.invoke({"input": "non mi piace questo cibo"}))

# A person to extract. name is required. age can be missing, and then it stays None.
# The docstring and field descriptions are what the model sees.
class Person(BaseModel):
    """Information about a person."""
    name: str = Field(description="person's name")
    age: int | None = Field(default=None, description="person's age")

# The tool the model is forced to call. people is a list of Person.
class Information(BaseModel):
    """Information to extract."""
    people: list[Person] = Field(description="List of info about people")

# One schema, in a list, because bind_tools expects a list.
# The print would show the Information schema, including the nested person fields.
extraction_functions = [convert_to_openai_function(Information)]

# print(extraction_functions)

# Same forced-tool binding as Tagging. The name here is Information.
# The print would show the message for a sentence about Joe and Martha.
extraction_model = model.bind_tools(extraction_functions, tool_choice={"type": "function", "function": {"name": "Information"}})

# print(extraction_model.invoke("Joe is 30, his mom is Martha"))

# This prompt replaces the tagging prompt. {input} is the sentence to extract from.
prompt = ChatPromptTemplate.from_messages([
    ("system", "Extract the relevant information, if not explicitly provided do not guess. Extract partial info"),
    ("human", "{input}")
])

# Message only, same shape as the first tagging chain.
# The print would show the tool call for Joe and Martha.
extraction_chain = prompt | extraction_model

# print(extraction_chain.invoke({"input": "Joe is 30, his mom is Martha"}))

# Defined again. The parser returns the Information arguments, a dict with "people".
# key_name matches the forced function name. The print would show that dict.
extraction_chain = prompt | extraction_model | JsonOutputKeyToolsParser(key_name="Information", first_tool_only=True)

# print(extraction_chain.invoke({"input": "Joe is 30, his mom is Martha"}))

# Defined again. itemgetter("people") takes that list off the dict,
# so the result is the people themselves. The print would show the list.
extraction_chain = (prompt | extraction_model | JsonOutputKeyToolsParser(key_name="Information", first_tool_only=True) | itemgetter("people"))

# print(extraction_chain.invoke({"input": "Joe is 30, his mom is Martha"}))

# Download Lilian Weng's agent post. The User-Agent is sent with the request.
# read().decode() is the HTML. BeautifulSoup strips the tags, and Document
# keeps that text plus the url on metadata["source"].
url = "https://lilianweng.github.io/posts/2023-06-23-agent/"

request = Request(url, headers={"User-Agent": "ai-engineer-roadmap"})

with urlopen(request, timeout=30) as response:
    html = response.read().decode("utf-8")

doc = Document(
    page_content=bs4.BeautifulSoup(html, "html.parser").get_text(),
    metadata={"source": url},
)

# First 10_000 characters. The single-shot calls below use this slice,
# not the full post. The print would show the first 1_000 of those characters.
page_content = doc.page_content[:10000]

# print(page_content[:1000])

# Tag schema for a section: summary, language, and keywords.
# The docstring and field descriptions are what the model sees.
class Overview(BaseModel):
    """Overview of a section of text."""
    summary: str = Field(description="Provide a concise summary of the content.")
    language: str = Field(description="Provide the language that the content is written in.")
    keywords: str = Field(description="Provide keywords related to the content.")

# Overview's schema, wrapped in a list because bind_tools expects a list.
overview_tagging_function = [
    convert_to_openai_function(Overview)
]

# Forces Overview. The function name matches the class name.
tagging_model = model.bind_tools(
    overview_tagging_function,
    tool_choice={"type": "function", "function": {"name": "Overview"}}
)

# tagging_chain is built again. prompt is still the extraction prompt.
# The parser returns the Overview arguments. The print would show that dict
# for the 10_000-character slice.
tagging_chain = prompt | tagging_model | JsonOutputKeyToolsParser(key_name="Overview", first_tool_only=True)

# print(tagging_chain.invoke({"input": page_content}))

# A paper mention. title is required. author can be missing.
# Info is the tool: a list of those papers. Neither class runs.
class Paper(BaseModel):
    """Information about papers mentioned."""
    title: str
    author: str | None = None

class Info(BaseModel):
    """Information to extract"""
    papers: list[Paper]

# Info's schema, in a list for bind_tools.
paper_extraction_function = [
    convert_to_openai_function(Info)
]

# extraction_model is built again, now forcing Info instead of Information.
extraction_model = model.bind_tools(
    paper_extraction_function,
    tool_choice={"type": "function", "function": {"name": "Info"}}
)

# Same chain shape as the people extractor: parse Info, then take "papers".
# prompt is still the generic extraction prompt. The print would show papers
# found in the 10_000-character slice.
extraction_chain = (prompt | extraction_model | JsonOutputKeyToolsParser(key_name="Info", first_tool_only=True) | itemgetter("papers"))

# print(extraction_chain.invoke({"input": page_content}))

# Paper-only instructions: extract mentioned papers and their authors, skip the
# article's own title, and return an empty list when the passage names none.
template = """A article will be passed to you. Extract from it all papers that are mentioned by this article follow by its author. 
    Do not extract the name of the article itself. If no papers are mentioned that's fine - you don't need to extract any! Just return an empty list.
    Do not make up or guess ANY extra information. Only extract what exactly is in the text."""
    
# This prompt replaces the generic extraction prompt. The system text is the
# paper instructions above. {input} is still the passage.
prompt = ChatPromptTemplate.from_messages([
    ("system", template),
    ("human", "{input}")
])

# extraction_chain is built again with that prompt. The model and the parser
# are unchanged. The first print would show papers from the slice. The second
# would show an empty list for "hi", which mentions no papers.
extraction_chain = (prompt | extraction_model | JsonOutputKeyToolsParser(key_name="Info", first_tool_only=True) | itemgetter("papers"))

# print(extraction_chain.invoke({"input": page_content}))

# print(extraction_chain.invoke({"input": "hi"}))

# Splits on paragraphs, then lines, then spaces, and only then on characters.
# chunk_overlap=0 means adjacent chunks do not share text.
text_splitter = RecursiveCharacterTextSplitter(chunk_overlap=0)

# Chunks of the full post, not the 10_000-character slice.
splits = text_splitter.split_text(doc.page_content)

# The chunk count. The number is unused; the line is there to inspect.
len(splits)

# map() below returns a list of paper lists, one per chunk.
# This concatenates them. The call on [[1, 2], [3, 4]] is a dry run
# of that shape, and its return value is unused.
def flatten(matrix):
    flat_list = []
    for row in matrix:
        flat_list += row
    return flat_list

flatten([[1, 2], [3, 4]])

# The first chunk of the full post.
# print(splits[0])

# A chain step from a function. Each chunk is wrapped as {"input": chunk}.
# "input" has to match {input} in the prompt. The print would show that
# list for the short string "hi".
prep = RunnableLambda(
    lambda x: [{"input": doc} for doc in text_splitter.split_text(x)]
)

# print(prep.invoke("hi"))

# prep builds one dict per chunk of the full post. map() runs the paper
# chain on each dict. flatten joins those lists into one. The print is
# the papers extracted from every chunk.
chain = prep | extraction_chain.map() | flatten

print(chain.invoke(doc.page_content))
