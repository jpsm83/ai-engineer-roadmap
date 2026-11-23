from operator import attrgetter
from typing import Literal
from urllib.request import Request, urlopen

import bs4
from dotenv import load_dotenv, find_dotenv
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pydantic import BaseModel, Field
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

tagging_prompt = ChatPromptTemplate.from_messages([
    ("system", "Think carefully, and then tag the text as instructed"),
    ("user", "{input}"),
])

tagging_model = model.with_structured_output(Tagging)
tagging_chain = tagging_prompt | tagging_model

print(tagging_chain.invoke({"input": "I love langchain"}))
print(tagging_chain.invoke({"input": "non mi piace questo cibo"}))

# Extraction

class Person(BaseModel):
    """Information about a person."""
    name: str = Field(description="person's name")
    age: int | None = Field(default=None, description="person's age")

class Information(BaseModel):
    """Information to extract."""
    people: list[Person] = Field(description="List of info about people")

extraction_prompt = ChatPromptTemplate.from_messages([
    ("system", "Extract the relevant information, if not explicitly provided do not guess. Extract partial info"),
    ("user", "{input}"),
])

extraction_model = model.with_structured_output(Information)
extraction_chain = extraction_prompt | extraction_model

print(extraction_chain.invoke({"input": "Joe is 30, his mom is Martha"}))

people_chain = extraction_chain | attrgetter("people")

print(people_chain.invoke({"input": "Joe is 30, his mom is Martha"}))

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

print(page_content[:1000])

class Overview(BaseModel):
    """Overview of a section of text."""
    summary: str = Field(description="Provide a concise summary of the content.")
    language: str = Field(description="Provide the language that the content is written in.")
    keywords: str = Field(description="Provide keywords related to the content.")

overview_model = model.with_structured_output(Overview)
overview_chain = tagging_prompt | overview_model

print(overview_chain.invoke({"input": page_content}))

class Paper(BaseModel):
    """Information about papers mentioned."""
    title: str = Field(description="title of the paper")
    author: str | None = Field(default=None, description="author of the paper")

class Info(BaseModel):
    """Information to extract"""
    papers: list[Paper] = Field(description="list of papers mentioned in the text")

paper_model = model.with_structured_output(Info)
paper_chain = extraction_prompt | paper_model | attrgetter("papers")

print(paper_chain.invoke({"input": page_content}))

template = """A article will be passed to you. Extract from it all papers that are mentioned by this article follow by its author. 

Do not extract the name of the article itself. If no papers are mentioned that's fine - you don't need to extract any! Just return an empty list.

Do not make up or guess ANY extra information. Only extract what exactly is in the text."""

paper_prompt = ChatPromptTemplate.from_messages([
    ("system", template),
    ("user", "{input}"),
])

paper_chain = paper_prompt | paper_model | attrgetter("papers")

print(paper_chain.invoke({"input": page_content}))
print(paper_chain.invoke({"input": "hi"}))

text_splitter = RecursiveCharacterTextSplitter(chunk_overlap=0)
splits = text_splitter.split_text(doc.page_content)

print(len(splits))

def flatten(matrix):
    flat_list = []
    for row in matrix:
        flat_list += row
    return flat_list

print(flatten([[1, 2], [3, 4]]))
print(splits[0])

prep = RunnableLambda(
    lambda text: [{"input": chunk} for chunk in text_splitter.split_text(text)]
)

print(prep.invoke("hi"))

chain = prep | paper_chain.map() | flatten

print(chain.invoke(doc.page_content))
