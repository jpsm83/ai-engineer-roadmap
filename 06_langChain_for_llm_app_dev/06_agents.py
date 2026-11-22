import warnings
warnings.filterwarnings("ignore")
from datetime import date
# account for deprecation of LLM model
import datetime
from langchain_classic.agents import AgentExecutor, AgentType, create_tool_calling_agent
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_core.globals import set_debug
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_experimental.tools import PythonREPLTool
from langchain_openai import ChatOpenAI as _ChatOpenAI

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

# gpt-5-nano rejects the `stop` sequences used by classic ReAct / LLMMathChain.
class ChatOpenAI(_ChatOpenAI):
    def _get_request_payload(self, input_, *, stop=None, **kwargs):
        return super()._get_request_payload(input_, stop=None, **kwargs)

# Native tool calling instead of CHAT_ZERO_SHOT_REACT_DESCRIPTION / create_python_agent.
# Those ReAct agents need `stop`, which this model does not support.
def initialize_agent(
    tools,
    llm,
    agent=None,
    handle_parsing_errors=True,
    verbose=True,
    system="You are a helpful assistant. Use tools when they help you answer.",
    **kwargs,
):
    prompt = ChatPromptTemplate.from_messages([
        ("system", system),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])
    return AgentExecutor(
        agent=create_tool_calling_agent(llm, tools, prompt),
        tools=tools,
        handle_parsing_errors=handle_parsing_errors,
        verbose=verbose,
        **kwargs,
    )

def create_python_agent(llm, tool, verbose=True, **kwargs):
    return initialize_agent(
        [tool],
        llm,
        verbose=verbose,
        system=(
            "You are an agent designed to write and execute python code to answer "
            "questions. You have access to a python REPL. If you get an error, debug "
            "your code and try again. Only use the output of your code to answer the "
            "question. You might know the answer without running any code, but you "
            "should still run the code to get the answer."
        ),
        **kwargs,
    )

# Get the current date
current_date = datetime.datetime.now().date()

# Define the date after which the model should be set to "gpt-3.5-turbo"
target_date = datetime.date(2024, 6, 12)

# Set the model variable based on the current date
if current_date > target_date:
    llm_model = "gpt-4o-mini"
else:
    llm_model = "gpt-5-nano"

# Built-in LangChain tools

llm = ChatOpenAI(temperature=1, model=llm_model)

tools = load_tools(["llm-math","wikipedia"], llm=llm)

agent= initialize_agent(
    tools, 
    llm, 
    agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    handle_parsing_errors=True,
    verbose = True)

# print(agent.invoke({"input": "What is the 25% of 300?"}))

'''
# Wikipedia example

question = "Tom M. Mitchell is an American computer scientist \
and the Founders University Professor at Carnegie Mellon University (CMU)\
what book did he write?"

result = agent.invoke({"input": question}) 

print(result)
'''

# Python Agent

agent = create_python_agent(
    llm,
    tool=PythonREPLTool(),
    verbose=True
)

customer_list = [["Harrison", "Chase"], 
                 ["Lang", "Chain"],
                 ["Dolly", "Too"],
                 ["Elle", "Elem"], 
                 ["Geoff","Fusion"], 
                 ["Trance","Former"],
                 ["Jen","Ayai"]
                ]

# print(agent.invoke({"input": f"""Sort these customers by \
# last name and then first name \
# and print the output: {customer_list}"""}))

set_debug(True)

# print(agent.invoke({"input": f"""Sort these customers by \
# last name and then first name \
# and print the output: {customer_list}"""})) 

set_debug(False)

# Define your own tool

@tool
def time(text: str) -> str:
    """Returns todays date, use this for any \
    questions related to knowing todays date. \
    The input should always be an empty string, \
    and this function will always return todays \
    date - any date mathmatics should occur \
    outside this function."""
    return str(date.today())

agent= initialize_agent(
    tools + [time], 
    llm, 
    agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    handle_parsing_errors=True,
    verbose = True)

try:
    result = agent.invoke({"input": "whats the date today?"}) 
except: 
    print("exception on external access")
