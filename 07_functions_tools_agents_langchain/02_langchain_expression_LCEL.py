# LangChain Expression Language (LCEL).
# The | operator passes each step's output into the next step.
# The file builds that up: a joke chain, a retrieval chain, tool binding,
# a fallback when JSON parsing fails, then invoke, batch, stream, and ainvoke.

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

# Load OPENAI_API_KEY from a local .env file.
# ChatOpenAI and OpenAIEmbeddings read that variable on their own.
_ = load_dotenv(find_dotenv())  # read local .env file

llm_model = "gpt-5-nano"

# The retriever below returns documents. This joins their page text into
# one string the prompt can take as {context}.
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# Smallest chain. {topic} is filled from the dict passed to invoke.
# The model returns a message. StrOutputParser returns that message's text.
# The print would show one joke about bears.
prompt = ChatPromptTemplate.from_template(
    "tell me a short joke about {topic}"
)

model = ChatOpenAI(model=llm_model, temperature=1)

output_parser = StrOutputParser()

chain = prompt | model | output_parser

# print(chain.invoke({"topic": "bears"}))

# Two short texts, embedded and stored in memory. as_retriever() searches
# that store. invoke returns a list of documents, closest first. With two
# texts stored, both can come back. The prints would show that list for
# each question: where Harrison worked, and what bears eat.
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

# This prompt replaces the joke prompt. {context} and {question} are filled
# by the dict the parallel step returns. The model is told to use that context only.
prompt = ChatPromptTemplate.from_template(template)

# RunnableParallel runs both branches on the same input and returns one dict.
# itemgetter("question") pulls that string out of the input.
# "context" then retrieves documents and format_docs joins them into a string.
# "question" passes the same string through, so the template can fill {question}.
# Those keys have to match the placeholders above.
# The commented context lambda stops at the retriever and returns documents.
# The live context branch also runs format_docs, so the prompt receives a string.
# The question lambda and itemgetter("question") both pass the question through.
# | prompt | model | output_parser is the joke chain's shape: fill the prompt,
# call the model, return the text. The print would show the Harrison answer.
chain = RunnableParallel({
    "context": itemgetter("question") | retriever | format_docs,
    "question": itemgetter("question"),
    # The context lambda returns documents and does not join them.
    # "context": lambda x: retriever.get_relevant_documents(x["question"]),
    # "question": lambda x: x["question"]
}) | prompt | model | output_parser

# print(chain.invoke({"question": "where did harrison work?"}))

# The parallel step on its own. invoke returns the dict the prompt receives,
# context plus question, not an answer. The print would show that dict.
inputs = RunnableParallel({
    "context": itemgetter("question") | retriever | format_docs,
    "question": itemgetter("question"),
    # Same unused lambdas as in the chain above. The context one returns documents.
    # "context": lambda x: retriever.get_relevant_documents(x["question"]),
    # "question": lambda x: x["question"]
})

# print(inputs.invoke({"question": "where did harrison work?"}))

# Schema for one tool, weather_search. The model sees the name, the description,
# and airport_code. Nothing here runs a weather lookup.

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

# This prompt replaces the retrieval prompt: one human message, {input} filled later.
prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{input}")
    ]
)

# bind_tools attaches the weather schema. On a call the model can answer in
# text or request weather_search. This replaces the plain chat model above.
model = ChatOpenAI(model=llm_model, temperature=1).bind_tools(functions)

# No output parser, so invoke returns the message, including any tool call.
# The print would show that message for a San Francisco weather question.
runnable = prompt | model

# print(runnable.invoke({"input": "what is the weather in sf"}))

# `functions` is defined again and now includes sports_search as well.
# bind_tools below attaches this list, so the runnable can request either tool.
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

# The print would show the message for a Patriots question, aimed at sports_search.
# print(runnable.invoke({"input": "how did the patriots do yesterday?"}))

# A smaller model used only by the JSON chain below.
# max_tokens caps the reply. temperature=0 keeps the wording steadier.
simple_model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    max_tokens=1000,
)

# Text from simple_model, then json.loads. If that text is not JSON,
# json.loads raises JSONDecodeError and this chain fails.
simple_chain = simple_model | StrOutputParser() | json.loads

challenge = "write three poems in a json blob, where each poem is a json blob of a title, author, and first line"

# The block below is a string, so none of it runs. It would print the raw
# reply, then run simple_chain and print the error when the poems are not JSON.
'''
print(simple_model.invoke(challenge))

try:
    simple_chain.invoke(challenge)
except json.JSONDecodeError as error:
    print(error)
'''

# Same JSON steps, on the tool-bound model from the sports section.
# The print would show the parsed object, or raise if that text is not JSON.
chain = model | StrOutputParser() | json.loads

# print(chain.invoke(challenge))

# Try simple_chain first. If it raises, run chain instead.
# The print would show whichever chain returns a parsed object.
final_chain = simple_chain.with_fallbacks([chain])

# print(final_chain.invoke(challenge))

# Joke chain again, used to show the runnable interface.
# model is still the tool-bound model. output_parser is a new text parser.
prompt = ChatPromptTemplate.from_template(
    "Tell me a short joke about {topic}"
)

output_parser = StrOutputParser()

chain = prompt | model | output_parser

# invoke runs one bears joke. The return value is unused.
chain.invoke({"topic": "bears"})

# batch runs each topic dict on its own. That return value is unused too.
chain.batch([{"topic": "bears"}, {"topic": "frogs"}])

# stream yields pieces of the bears joke as they are produced. Each piece is printed.
for t in chain.stream({"topic": "bears"}):
    print(t)

# ainvoke is the one-shot call, waited on from the event loop. response is that joke.
response = asyncio.run(chain.ainvoke({"topic": "bears"}))

print(response)
