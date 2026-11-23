# LangChain Expression Language (LCEL)

import asyncio
import json
from operator import itemgetter

from dotenv import load_dotenv, find_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from rich import print

_ = load_dotenv(find_dotenv())  # read local .env file

llm_model = "gpt-5-nano"

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# Simple Chain

prompt = ChatPromptTemplate.from_template(
    "tell me a short joke about {topic}"
)

model = ChatOpenAI(model=llm_model, temperature=1)

output_parser = StrOutputParser()

chain = prompt | model | output_parser

# print(chain.invoke({"topic": "bears"}))

# More complex chain

vectorstore = InMemoryVectorStore.from_texts(
    ["harrison worked at kensho", "bears like to eat honey"],
    embedding=OpenAIEmbeddings(model="text-embedding-3-small"),
)

retriever = vectorstore.as_retriever()

# print(retriever.invoke("where did harrison work?"))

# print(retriever.invoke("what do bears like to eat"))

template = """Answer the question based only on the following context:
{context}

Question: {question}
"""

prompt = ChatPromptTemplate.from_template(template)

chain = RunnableParallel({
# a simple way to get the context and question from the input is using the itemgetter function
    "context": itemgetter("question") | retriever | format_docs,
    "question": itemgetter("question"),
# another way to get the context and question from the input is using the lambda function
    # "context": lambda x: retriever.get_relevant_documents(x["question"]),
    # "question": lambda x: x["question"]
# we use itemgetter to get the context and question from the input because it is a simple way to get the context and question from the input
}) | prompt | model | output_parser

# print(chain.invoke({"question": "where did harrison work?"}))

inputs = RunnableParallel({
# a simple way to get the context and question from the input is using the itemgetter function
    "context": itemgetter("question") | retriever | format_docs,
    "question": itemgetter("question"),
# another way to get the context and question from the input is using the lambda function
    # "context": lambda x: retriever.get_relevant_documents(x["question"]),
    # "question": lambda x: x["question"]
# we use itemgetter to get the context and question from the input because it is a simple way to get the context and question from the input
})

# print(inputs.invoke({"question": "where did harrison work?"}))

# Bind

functions = [
    {
        "name": "weather_search",
        "description": "Search for weather given an airport code",
        "parameters": {
            "type": "object",
            "properties": {
                "airport_code": {
                    "type": "string",
                    "description": "The airport code to get the weather for",
                },
            },
            "required": ["airport_code"],
        },
    }
]

prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{input}")
    ]
)

model = ChatOpenAI(model=llm_model, temperature=1).bind_tools(functions)

runnable = prompt | model

# print(runnable.invoke({"input": "what is the weather in sf"}))

functions = [
    {
        "name": "weather_search",
        "description": "Search for weather given an airport code",
        "parameters": {
            "type": "object",
            "properties": {
                "airport_code": {
                    "type": "string",
                    "description": "The airport code to get the weather for",
                },
            },
            "required": ["airport_code"],
        },
    },
    {
        "name": "sports_search",
        "description": "Search for news of recent sport events",
        "parameters": {
            "type": "object",
            "properties": {
                "team_name": {
                    "type": "string",
                    "description": "The sports team to search for",
                },
            },
            "required": ["team_name"],
        },
    },
]

model = model.bind_tools(functions)

runnable = prompt | model

# print(runnable.invoke({"input": "how did the patriots do yesterday?"}))

# Fallbacks

simple_model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    max_tokens=1000,
)

simple_chain = simple_model | StrOutputParser() | json.loads

challenge = "write three poems in a json blob, where each poem is a json blob of a title, author, and first line"

'''
print(simple_model.invoke(challenge))

try:
    simple_chain.invoke(challenge)
except json.JSONDecodeError as error:
    print(error)
'''

chain = model | StrOutputParser() | json.loads

# print(chain.invoke(challenge))

final_chain = simple_chain.with_fallbacks([chain])

# print(final_chain.invoke(challenge))

# Interface

prompt = ChatPromptTemplate.from_template(
    "Tell me a short joke about {topic}"
)

output_parser = StrOutputParser()

chain = prompt | model | output_parser

chain.invoke({"topic": "bears"})

chain.batch([{"topic": "bears"}, {"topic": "frogs"}])

for t in chain.stream({"topic": "bears"}):
    print(t)

response = asyncio.run(chain.ainvoke({"topic": "bears"}))

print(response)
