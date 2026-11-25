import warnings
# Hide warnings from the agent and tool libraries for the rest of this file.
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
# Load OPENAI_API_KEY from a local .env. ChatOpenAI reads it on its own.
_ = load_dotenv(find_dotenv()) # read local .env file

# gpt-5-nano rejects the stop sequences classic ReAct agents send.
# This subclass drops stop before the request is built. Every ChatOpenAI(...) below is this class,
# so a stop list never reaches the API. The messages themselves are unchanged.
class ChatOpenAI(_ChatOpenAI):
    def _get_request_payload(self, input_, *, stop=None, **kwargs):
        return super()._get_request_payload(input_, stop=None, **kwargs)

# Local stand-in for the old initialize_agent.
# The agent= argument is accepted so the calls below can still pass AgentType, and this function does not use it.
# It always builds a tool-calling agent. The model sees the system text, the {input} question,
# and {agent_scratchpad}, where earlier tool calls and results are inserted on the next turn.
# That placeholder name has to stay agent_scratchpad, because create_tool_calling_agent writes that key.
# AgentExecutor runs the loop: the model picks a tool or a final answer, the tool runs,
# and the observation goes back onto the scratchpad. handle_parsing_errors keeps the loop
# going when a step does not parse. verbose prints each step.
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

# Same executor, with one tool and a system prompt that tells the model to use the Python REPL.
# The system string is what the model sees. The REPL is what runs the code.
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

# After 2024-06-12 the model is gpt-4o-mini; on or before that date it is gpt-5-nano.
current_date = datetime.datetime.now().date()

target_date = datetime.date(2024, 6, 12)

if current_date > target_date:
    llm_model = "gpt-4o-mini"
else:
    llm_model = "gpt-5-nano"

# llm-math and wikipedia are ready-made tools. load_tools builds them and passes llm through,
# because llm-math needs its own model call. The model sees each tool's name and description.
# The tool runs when the agent calls it.
# temperature controls how much the replies vary; this call passes 1.
# initialize_agent here is the function above. The 25% question is the math-tool path, left commented.

llm = ChatOpenAI(temperature=1, model=llm_model)

tools = load_tools(["llm-math","wikipedia"], llm=llm)

agent= initialize_agent(
    tools, 
    llm, 
    agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    handle_parsing_errors=True,
    verbose = True)

# print(agent.invoke({"input": "What is the 25% of 300?"}))

# Unused string. A Wikipedia question: which book Tom Mitchell wrote.
# invoke would return the agent's result dict, and the print would show it.
# Nothing calls the math-and-wikipedia agent before this block, and the block itself does not run.
'''
# Wikipedia example

question = "Tom M. Mitchell is an American computer scientist \
and the Founders University Professor at Carnegie Mellon University (CMU)\
what book did he write?"

result = agent.invoke({"input": question}) 

print(result)
'''

# This agent replaces the math-and-wikipedia agent. Nothing called that one.
# PythonREPLTool is a REPL: the model writes code, the tool executes it, and the output comes back.

agent = create_python_agent(
    llm,
    tool=PythonREPLTool(),
    verbose=True
)

# The table the commented calls would ask the agent to sort by last name, then first name.
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

# The second commented call is that same sort with tracing on, so the prompts would be visible.
# set_debug(False) turns the tracing off again.
set_debug(True)

# print(agent.invoke({"input": f"""Sort these customers by \
# last name and then first name \
# and print the output: {customer_list}"""})) 

set_debug(False)

# @tool publishes time to the model. The docstring is the description the model reads.
# The function body is what runs. text is ignored. The return is today's date as a string.

@tool
def time(text: str) -> str:
    """Returns todays date, use this for any \
    questions related to knowing todays date. \
    The input should always be an empty string, \
    and this function will always return todays \
    date - any date mathmatics should occur \
    outside this function."""
    return str(date.today())

# This agent replaces the Python agent. The tool list is llm-math, wikipedia, and time.
agent= initialize_agent(
    tools + [time], 
    llm, 
    agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    handle_parsing_errors=True,
    verbose = True)

# The only agent call this file makes. The question should select the time tool.
# On any failure the bare except prints a fixed message and the lesson ends.
try:
    result = agent.invoke({"input": "whats the date today?"}) 
except: 
    print("exception on external access")
