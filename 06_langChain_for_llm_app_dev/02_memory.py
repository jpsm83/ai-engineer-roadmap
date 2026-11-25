import os
import warnings
import datetime
from langchain_openai import ChatOpenAI
from langchain_classic.chains import ConversationChain
from langchain_classic.base_memory import BaseMemory
from langchain_classic.memory.utils import get_prompt_input_key
from langchain_classic.memory import ConversationTokenBufferMemory
from langchain_classic.memory import ConversationBufferWindowMemory
from langchain_classic.memory import ConversationSummaryBufferMemory
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, get_buffer_string
from dotenv import load_dotenv, find_dotenv
from pydantic import Field

# Local stand-in for the deprecated ConversationBufferMemory.
# It stores every turn and hands them back to ConversationChain under memory_key, "history".
# That key has to match the {history} slot in the chain's prompt.
# return_messages chooses the shape: a list of messages, or one "Human:" / "AI:" string.
# The default is the string, which is what this chain's prompt expects.
class ConversationBufferMemory(BaseMemory):
    return_messages: bool = False
    memory_key: str = "history"
    human_prefix: str = "Human"
    ai_prefix: str = "AI"
    messages: list[BaseMessage] = Field(default_factory=list)

    @property
    def memory_variables(self) -> list[str]:
        # Names this memory fills. The chain reads this to know which prompt slot to load.
        return [self.memory_key]

    @property
    def buffer(self) -> str | list[BaseMessage]:
        # The turns stored so far, in the shape the chain will paste into the prompt.
        if self.return_messages:
            return self.messages
        return get_buffer_string(
            self.messages,
            human_prefix=self.human_prefix,
            ai_prefix=self.ai_prefix,
        )

    def load_memory_variables(self, inputs: dict) -> dict:
        # The chain calls this before the model. The dict key is memory_key.
        return {self.memory_key: self.buffer}

    def save_context(self, inputs: dict, outputs: dict) -> None:
        # Store one turn. inputs is the user side, outputs is the reply.
        # get_prompt_input_key skips memory_key, so a history entry is not stored as the new user text.
        input_key = get_prompt_input_key(inputs, self.memory_variables)
        # One output key is unambiguous. With several keys, keep the one named "output".
        if len(outputs) == 1:
            output_key = next(iter(outputs.keys()))
        elif "output" in outputs:
            output_key = "output"
        else:
            raise ValueError(
                f"Got multiple output keys: {list(outputs.keys())}, cannot "
                "determine which to store in memory."
            )
        self.messages.append(HumanMessage(content=inputs[input_key]))
        self.messages.append(AIMessage(content=outputs[output_key]))

    def clear(self) -> None:
        self.messages = []

# Load the API key ChatOpenAI reads, and hide deprecation warnings from the older chain classes.
# account for deprecation of LLM model
_ = load_dotenv(find_dotenv()) # read local .env file

warnings.filterwarnings('ignore')

# After 2024-06-12 the chat model is gpt-5-nano; on or before that date it is gpt-6-luna.
# ChatOpenAI takes that name. temperature controls how much the replies vary; this call passes 1.

current_date = datetime.datetime.now().date()

target_date = datetime.date(2024, 6, 12)

if current_date > target_date:
    llm_model = "gpt-5-nano"
else:
    llm_model = "gpt-6-luna"

llm = ChatOpenAI(temperature=1, model=llm_model)

# Full history: every turn saved so far comes back under "history".
memory = ConversationBufferMemory()

# ConversationChain loads that history, calls the model, then saves the new turn.
# verbose=True prints the prompt it actually sends. This chain is built and not called.
# The predict demos sit in the unused string below. The summary section then replaces both names.
conversation = ConversationChain(
    llm=llm, 
    memory = memory,
    verbose=True
)

# Unused string, so none of this runs. In order:
# three predict calls (the name, then 1+1, then "what is my name?") and a look at
# memory.buffer versus load_memory_variables. A fresh memory filled by hand with
# save_context, with no model call. ConversationBufferWindowMemory with k=1, which
# keeps only the last exchange, then k=10 on a chain that should still know the name.
# ConversationTokenBufferMemory with max_token_limit=10, which drops older turns
# once the stored text is past that many tokens.
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

# The summary memory is the part that runs. The triple-quoted block above is skipped.
# schedule is one long day plan, long enough that the buffer has something to summarize.

# create a long string
schedule = "There is a meeting at 8am with your product team. \
You will need your powerpoint presentation prepared. \
9am-12pm have time to work on your LangChain \
project which will go quickly because Langchain is such a powerful tool. \
At Noon, lunch at the italian resturant with a customer who is driving \
from over an hour away to meet you to understand the latest in AI. \
Be sure to bring your laptop to show the latest LLM demo."

# This memory replaces the buffer memory above.
# Recent turns stay verbatim until they pass max_token_limit; older turns are summarized with llm.
# The three save_context calls write a greeting, a follow-up, and the schedule as the reply.
# The load_memory_variables call builds that dict and does not print it.
memory = ConversationSummaryBufferMemory(llm=llm, max_token_limit=100)

memory.save_context({"input": "Hello"}, {"output": "What's up"})

memory.save_context({"input": "Not much, just hanging"},
                    {"output": "Cool"})

memory.save_context({"input": "What is on the schedule today?"}, 
                    {"output": f"{schedule}"})

memory.load_memory_variables({})

# This conversation replaces the unused buffer-memory chain.
# predict asks for a demo to show, which depends on the schedule just stored.
# verbose=True prints the prompt, including the summary. The print shows the memory dict afterward.
conversation = ConversationChain(
    llm=llm, 
    memory = memory,
    verbose=True
)

conversation.predict(input="What would be a good demo to show?")

print(memory.load_memory_variables({}))
