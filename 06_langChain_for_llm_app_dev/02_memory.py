import os
import warnings
from langchain_openai import ChatOpenAI
from langchain_classic.chains import ConversationChain
from langchain_classic.memory import ConversationBufferMemory
from dotenv import load_dotenv, find_dotenv
from langchain_classic.memory import ConversationTokenBufferMemory
from langchain_classic.memory import ConversationBufferWindowMemory
from langchain_classic.memory import ConversationSummaryBufferMemory
# account for deprecation of LLM model
import datetime

_ = load_dotenv(find_dotenv()) # read local .env file

warnings.filterwarnings('ignore')

# ConversationBufferMemory

# Get the current date
current_date = datetime.datetime.now().date()

# Define the date after which the model should be set to "gpt-3.5-turbo"
target_date = datetime.date(2024, 6, 12)

# Set the model variable based on the current date
if current_date > target_date:
    llm_model = "gpt-5-nano"
else:
    llm_model = "gpt-6-luna"

llm = ChatOpenAI(temperature=1, model=llm_model)

memory = ConversationBufferMemory()

conversation = ConversationChain(
    llm=llm, 
    memory = memory,
    verbose=True
)

'''
print(conversation.predict(input="Hi, my name is Joao"))

print(conversation.predict(input="What is 1+1?"))

print(conversation.predict(input="What is my name?"))

print(memory.buffer)

print(memory.load_memory_variables({}))

memory = ConversationBufferMemory()

memory.save_context({"input": "Hi"}, 
                    {"output": "What's up"})

print(memory.buffer)

memory.load_memory_variables({})

memory.save_context({"input": "Not much, just hanging"}, 
                    {"output": "Cool"})

memory.load_memory_variables({})

print(memory.load_memory_variables({}))

# ConversationBufferWindowMemory

memory = ConversationBufferWindowMemory(k=1) # k is the number of messages to keep in memory              

memory.save_context({"input": "Hi"},
                    {"output": "What's up"})
memory.save_context({"input": "Not much, just hanging"},
                    {"output": "Cool"})

print(memory.load_memory_variables({}))

memory = ConversationBufferWindowMemory(k=10) # k is the number of messages to keep in memory

conversation = ConversationChain(
    llm=llm, 
    memory = memory,
    verbose=False
)
print(conversation.predict(input="Hi, my name is Joao"))

print(conversation.predict(input="What is 1+1?"))

print(conversation.predict(input="What is my name?"))

# ConversationTokenBufferMemory

memory = ConversationTokenBufferMemory(llm=llm, max_token_limit=10)

memory.save_context({"input": "AI is what?!"},
                    {"output": "Amazing!"})
memory.save_context({"input": "Backpropagation is what?"},
                    {"output": "Beautiful!"})
memory.save_context({"input": "Chatbots are what?"}, 
                    {"output": "Charming!"})

print(memory.load_memory_variables({}))
'''

# ConversationSummaryMemory

# create a long string
schedule = "There is a meeting at 8am with your product team. \
You will need your powerpoint presentation prepared. \
9am-12pm have time to work on your LangChain \
project which will go quickly because Langchain is such a powerful tool. \
At Noon, lunch at the italian resturant with a customer who is driving \
from over an hour away to meet you to understand the latest in AI. \
Be sure to bring your laptop to show the latest LLM demo."

memory = ConversationSummaryBufferMemory(llm=llm, max_token_limit=100)

memory.save_context({"input": "Hello"}, {"output": "What's up"})

memory.save_context({"input": "Not much, just hanging"},
                    {"output": "Cool"})

memory.save_context({"input": "What is on the schedule today?"}, 
                    {"output": f"{schedule}"})

memory.load_memory_variables({})

conversation = ConversationChain(
    llm=llm, 
    memory = memory,
    verbose=True
)

conversation.predict(input="What would be a good demo to show?")

print(memory.load_memory_variables({}))
