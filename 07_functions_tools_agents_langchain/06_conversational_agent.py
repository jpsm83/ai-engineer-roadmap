import os
import json
import openai
from langchain.tools import tool
from dotenv import load_dotenv, find_dotenv
from pydantic import BaseModel, Field
import requests
import datetime
from langchain_core.utils.function_calling import convert_to_openai_function
import wikipedia
from openapi_pydantic import parse_obj
from langchain_openai import ChatOpenAI
from langchain_classic.agents import AgentExecutor
from langchain_classic.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain_classic.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain_classic.base_memory import BaseMemory
from langchain_classic.memory.utils import get_prompt_input_key
from langchain_core.agents import AgentFinish
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, get_buffer_string
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from rich import print
import panel as pn  # GUI
import panel as pn
import param

# Load OPENAI_API_KEY from a local .env file.
# ChatOpenAI reads that environment variable on its own.
_ = load_dotenv(find_dotenv()) # read local .env file
openai.api_key = os.environ['OPENAI_API_KEY']

llm_model = "gpt-5-nano"

# Argument schema for the weather tool.
# The model sees the field names and descriptions and fills them in
# when it decides to call the tool. It does not run this class itself.
class OpenMeteoInput(BaseModel):
    latitude: float = Field(..., description="Latitude of the location to fetch weather data for")
    longitude: float = Field(..., description="Longitude of the location to fetch weather data for")

# @tool wraps the function as a LangChain tool.
# The docstring becomes the description the model uses to decide when to call it.
# args_schema replaces the schema LangChain would otherwise infer from the signature.
@tool(args_schema=OpenMeteoInput)
def get_current_temperature(latitude: float, longitude: float) -> dict:
    """Fetch current temperature for given coordinates."""

    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    # Ask Open-Meteo for today's hourly temperatures at this point.
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'hourly': 'temperature_2m',
        'forecast_days': 1,
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        results = response.json()
    else:
        raise Exception(f"API Request failed with status code: {response.status_code}")

    # The API returns a list of hours, not "now".
    # Pick the hour closest to the current UTC time and return that temperature.
    current_utc_time = datetime.datetime.now(datetime.UTC)

    time_list = []
    for time_str in results['hourly']['time']:
        parsed = datetime.datetime.fromisoformat(time_str.replace('Z', '+00:00'))
        time_list.append(parsed if parsed.tzinfo else parsed.replace(tzinfo=datetime.UTC))

    temperature_list = results['hourly']['temperature_2m']

    closest_time_index = min(range(len(time_list)), key=lambda i: abs(time_list[i] - current_utc_time))

    current_temperature = temperature_list[closest_time_index]

    return f'The current temperature is {current_temperature}°C'

# These prints inspect the tool LangChain built:
# name and description come from the function, args come from the schema.
# print(get_current_temperature.name, get_current_temperature.description, get_current_temperature.args)

# convert_to_openai_function turns the tool into the JSON schema sent to the model.
# print(convert_to_openai_function(get_current_temperature))

# invoke runs the tool with a dict of arguments. Tools are not called like normal functions.
# print(get_current_temperature.invoke({"latitude": 13, "longitude": 14}))

# Second tool. No args_schema: LangChain infers one string argument, query, from the signature.
# The docstring is what tells the model this tool is for general knowledge, not weather.
@tool
def search_wikipedia(query: str) -> str:
    """Run Wikipedia search and get page summaries."""
    page_titles = wikipedia.search(query)
    summaries = []
    for page_title in page_titles[: 3]:
        try:
            wiki_page =  wikipedia.page(title=page_title, auto_suggest=False)
            summaries.append(f"Page: {page_title}\nSummary: {wiki_page.summary}")
        except (
            self.wiki_client.exceptions.PageError,
            self.wiki_client.exceptions.DisambiguationError,
        ):
            pass
    if not summaries:
        return "No good Wikipedia Search Result was found"
    return "\n\n".join(summaries)

# print(search_wikipedia.name, search_wikipedia.description, search_wikipedia.args)

# print(convert_to_openai_function(search_wikipedia))

# print(search_wikipedia.invoke({"query": "langchain"}))

# The list of tools the agent is allowed to call.
tools = [get_current_temperature, search_wikipedia]

# Same tools, expressed as OpenAI function JSON. Kept so you can see that shape.
# The model below is bound to the tool objects directly, which produces the same schema.
functions = [convert_to_openai_function(f) for f in tools]

# bind_tools attaches the tool schemas to the model.
# On each call the model can either answer in text or request one of these tools.
# temperature=1 keeps the choice stable from run to run.
model = ChatOpenAI(model=llm_model, temperature=1).bind_tools(tools)

# ChatPromptTemplate builds the message list from these tuples.
# {input} is filled in later by chain.invoke.
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are helpful but sassy assistant"),
    ("user", "{input}"),
])

# LCEL: the | operator passes each step's output into the next step.
# prompt fills the messages, the model replies, and the parser reads that reply.
# OpenAIToolsAgentOutputParser returns either:
#   - a list of tool actions, when the model wants a tool, or
#   - AgentFinish, when the model is giving the final answer.
chain = prompt | model | OpenAIToolsAgentOutputParser()

# A weather question should produce a tool action, not a finished answer,
# because the model has no live weather of its own.
result = chain.invoke({"input": "what is the weather is sf?"})

# The parser returns a list because the model may request more than one tool.
# [0] is the first action. .tool is the tool name, .tool_input is the argument dict.
# print(result[0].tool)

# print(result[0].tool_input)

# The prompt needs a place to put earlier tool calls and their results.
# MessagesPlaceholder is that slot: at invoke time it is replaced by a list of messages.
# "agent_scratchpad" is the working notes for the current question, not the chat history.
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are helpful but sassy assistant"),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

chain = prompt | model | OpenAIToolsAgentOutputParser()

# First turn: scratchpad is empty, so this is the same decision as above.
result1 = chain.invoke({
    "input": "what is the weather is sf?",
    "agent_scratchpad": []
})

#print(result1[0].tool)

# Run the tool the model asked for. tool_input is the dict of arguments it chose.
observation = get_current_temperature.invoke(result1[0].tool_input)

# print(observation)

# A tool action is a list; a finished answer is an AgentFinish.
# print(type(result1))

# message_log is the original assistant message that requested the tool.
# The next call has to send that message back, followed by the tool result.
# print(result1[0].message_log)

# format_to_openai_tool_messages turns (action, tool output) pairs into
# an assistant message plus a tool message. That is the shape the model expects
# on the next turn. One pair is enough to show the format.
formatted_messages = format_to_openai_tool_messages([(result1[0], observation)])

# print(formatted_messages)

# Second turn: same question, but the scratchpad now contains the tool result.
# The model should answer from that result and return AgentFinish instead of another tool call.
result2 = chain.invoke({
    "input": "what is the weather is sf?",
    "agent_scratchpad": formatted_messages
})

# print(result2)

# Manual agent loop. This is the same cycle AgentExecutor runs for you later:
# ask the model, stop if it is finished, otherwise run the tool and ask again.
def run_agent(user_input):
    intermediate_steps = []

    while True:
        # Rebuild the scratchpad from every (action, observation) so far.
        result = chain.invoke({
            "input": user_input,
            "agent_scratchpad": format_to_openai_tool_messages(intermediate_steps)
        })

        # AgentFinish means the model answered in text. return_values["output"] holds it.
        if isinstance(result, AgentFinish):
            return result

        # Otherwise result is a list of tool actions. Run the first one.
        action = result[0]

        tool = {
            "search_wikipedia": search_wikipedia,
            "get_current_temperature": get_current_temperature,
        }[action.tool]

        observation = tool.run(action.tool_input)

        # Remember this step so the next model call can see it.
        intermediate_steps.append((action, observation))

# Move scratchpad formatting into the chain so the caller only passes intermediate_steps.
# RunnablePassthrough.assign copies the input dict through and adds agent_scratchpad.
# The lambda reads intermediate_steps and formats them as tool messages.
# The result is piped into the chain defined above, which still expects agent_scratchpad.
agent_chain = RunnablePassthrough.assign(
    agent_scratchpad= lambda x: format_to_openai_tool_messages(x["intermediate_steps"])
) | chain

# Same loop as above. The only change is that agent_chain formats the scratchpad.
# Defining run_agent again replaces the previous function.
def run_agent(user_input):
    intermediate_steps = []

    while True:
        result = agent_chain.invoke({
            "input": user_input,
            "intermediate_steps": intermediate_steps
        })

        if isinstance(result, AgentFinish):
            return result

        action = result[0]
        tool = {
            "search_wikipedia": search_wikipedia,
            "get_current_temperature": get_current_temperature,
        }[action.tool]

        observation = tool.run(action.tool_input)

        intermediate_steps.append((action, observation))

# Weather needs the temperature tool. "What is langchain?" needs Wikipedia.
# "hi!" needs no tool: the model should finish on the first turn.
# print(run_agent("what is the weather is sf?"))

# print(run_agent("what is langchain?"))

# print(run_agent("hi!"))

# AgentExecutor is that while-loop as a library object.
# It calls the agent, runs the matching tool from `tools`, appends the observation,
# and repeats until AgentFinish or it hits its iteration limit.
# verbose=True prints each step.
agent_executor = AgentExecutor(agent=agent_chain, tools=tools, verbose=True)

# print(agent_executor.invoke({"input": "what is langchain?"}))

# This executor has no memory. It answers the first message, then forgets the name.
# print(agent_executor.invoke({"input": "my name is bob"}))

# print(agent_executor.invoke({"input": "what is my name"}))

# New prompt. chat_history is previous user/assistant turns.
# agent_scratchpad is still only the tool calls for the question being answered now.
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are helpful but sassy assistant"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

# Rebuild the chain with the new prompt. prompt, model, and parser are in one pipeline
# so chat_history and input are available to the prompt, and the scratchpad is added first.
agent_chain = RunnablePassthrough.assign(
    agent_scratchpad= lambda x: format_to_openai_tool_messages(x["intermediate_steps"])
) | prompt | model | OpenAIToolsAgentOutputParser()

# Stores the conversation and returns it as chat messages.
# This is the same job as the deprecated ConversationBufferMemory class:
# AgentExecutor loads these messages into chat_history before each call
# and appends the new user message and answer afterward.
# return_messages=True gives a list of messages, which is what MessagesPlaceholder needs.
# memory_key must match the placeholder name above.
# Messages are kept in a list, so this does not use the deprecated history classes.
class ConversationBufferMemory(BaseMemory):
    return_messages: bool = False
    memory_key: str = "history"
    human_prefix: str = "Human"
    ai_prefix: str = "AI"
    messages: list[BaseMessage] = Field(default_factory=list)

    @property
    def memory_variables(self) -> list[str]:
        return [self.memory_key]

    @property
    def buffer(self) -> str | list[BaseMessage]:
        if self.return_messages:
            return self.messages
        return get_buffer_string(
            self.messages,
            human_prefix=self.human_prefix,
            ai_prefix=self.ai_prefix,
        )

    def load_memory_variables(self, inputs: dict) -> dict:
        return {self.memory_key: self.buffer}

    def save_context(self, inputs: dict, outputs: dict) -> None:
        input_key = get_prompt_input_key(inputs, self.memory_variables)
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

memory = ConversationBufferMemory(return_messages=True,memory_key="chat_history")

# Passing memory makes the executor load chat_history before each call
# and save the new user message and answer afterward.
agent_executor = AgentExecutor(agent=agent_chain, tools=tools, verbose=True, memory=memory)

# print(agent_executor.invoke({"input": "my name is bob"}))

# This can answer from memory. The previous executor could not.
# print(agent_executor.invoke({"input": "whats my name"}))

# print(agent_executor.invoke({"input": "whats the weather in sf?"}))

# Create a chatbot

# A third tool with no real behavior, so you can see how a new tool is added.
# The model learns what it does from the docstring. Here it only reverses the string.
@tool
def create_your_own(query: str) -> str:
    """This function can do whatever you would like once you fill it in """
    print(type(query))
    return query[::-1]

tools = [get_current_temperature, search_wikipedia, create_your_own]

# Panel is the small web UI below. This loads its extensions.
pn.extension()

# Holds the agent and the list of chat bubbles drawn on screen.
class cbfs(param.Parameterized):

    def __init__(self, tools, **params):
        super(cbfs, self).__init__( **params)
        self.panels = []
        # Function JSON for the three tools, then attach them to a new model.
        self.functions = [convert_to_openai_function(f) for f in tools]
        self.model = ChatOpenAI(model=llm_model, temperature=1).bind_tools(self.functions)
        # Separate memory for the UI conversation.
        self.memory = ConversationBufferMemory(return_messages=True,memory_key="chat_history")
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are helpful but sassy assistant"),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
        # Same chain as the memory section above: scratchpad, prompt, model, parser.
        self.chain = RunnablePassthrough.assign(
            agent_scratchpad = lambda x: format_to_openai_tool_messages(x["intermediate_steps"])
        ) | self.prompt | self.model | OpenAIToolsAgentOutputParser()
        # verbose=False keeps the tool trace out of the UI.
        self.qa = AgentExecutor(agent=self.chain, tools=tools, verbose=False, memory=self.memory)

    def convchain(self, query):
        # Panel calls this with the text-box value, including when it is cleared.
        if not query:
            return
        inp.value = ''
        # invoke runs the full agent loop. The final text is in result["output"].
        result = self.qa.invoke({"input": query})
        self.answer = result['output']
        # Append the user line and the answer to the bubbles already on screen.
        self.panels.extend([
            pn.Row('User:', pn.pane.Markdown(query, width=450)),
            pn.Row('ChatBot:', pn.pane.Markdown(self.answer, width=450, styles={'background-color': '#F6F6F6'}))
        ])
        return pn.WidgetBox(*self.panels, scroll=True)

    def clr_history(self,count=0):
        self.chat_history = []
        return

cb = cbfs(tools)

inp = pn.widgets.TextInput( placeholder='Enter text here…')

# Run convchain whenever the text box changes.
conversation = pn.bind(cb.convchain, inp)

tab1 = pn.Column(
    pn.Row(inp),
    pn.layout.Divider(),
    pn.panel(conversation,  loading_indicator=True, height=400),
    pn.layout.Divider(),
)

dashboard = pn.Column(
    pn.Row(pn.pane.Markdown('# QnA_Bot')),
    pn.Tabs(('Conversation', tab1))
)

# Running this file as a script does not display the last expression.
# show() starts a local server and opens the app in a browser.
dashboard.show()
