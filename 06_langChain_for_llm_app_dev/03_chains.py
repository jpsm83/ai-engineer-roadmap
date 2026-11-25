import os
import warnings
# account for deprecation of LLM model
import datetime
import pandas as pd
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_classic.chains import LLMChain
from langchain_classic.chains import SimpleSequentialChain
from langchain_classic.chains import SequentialChain
from langchain_classic.chains.router import MultiPromptChain
from langchain_classic.chains.router.llm_router import LLMRouterChain, RouterOutputParser
from rich import print

from dotenv import load_dotenv, find_dotenv
# Load the API key ChatOpenAI reads, and silence warnings from the older chain classes.
_ = load_dotenv(find_dotenv()) # read local .env file

warnings.filterwarnings('ignore')

# After 2024-06-12 the chat model is gpt-5-nano; on or before that date it is gpt-6-luna.
current_date = datetime.datetime.now().date()
target_date = datetime.date(2024, 6, 12)
if current_date > target_date:
    llm_model = "gpt-5-nano"
else:
    llm_model = "gpt-6-luna"

# Product reviews. The sequential-chain demo inside the unused string reads df.Review[5].
# head() returns the first rows, and nothing prints them.
# The router chain that runs at the bottom does not use this table.
df = pd.read_csv('Data.csv')

df.head()

# Chat model for every chain in this file. temperature=1 is the value this call sends.
llm = ChatOpenAI(temperature=1, model=llm_model)

# The product name the naming chains inside the unused string would describe.
product = "Queen Size Sheet Set"

# Unused string, so none of these chains run. In order:
# LLMChain: one prompt, a company name for a maker of {product}, then chain.run(product).
# SimpleSequentialChain: chain_one names the company, chain_two writes 20 words from {company_name}.
# That chain passes the first chain's text straight through as the only input of the next.
# SequentialChain: four named steps on one review. Each output_key is the slot the next prompt fills
# by the same name: English_Review, summary, language, then followup_message.
# input_variables is Review. language is computed and used, and it is left out of output_variables.
# overall_chain is called on df.Review[5]. A second ChatOpenAI inside this string would replace llm.
'''
prompt = ChatPromptTemplate.from_template(
    "What is the best name to describe \
    a company that makes {product}?"
)

chain = LLMChain(llm=llm, prompt=prompt)

chain.run(product)

# SimpleSequentialChain

# prompt template 1
first_prompt = ChatPromptTemplate.from_template(
    "What is the best name to describe \
    a company that makes {product}?"
)

# Chain 1
chain_one = LLMChain(llm=llm, prompt=first_prompt)

# prompt template 2
second_prompt = ChatPromptTemplate.from_template(
    "Write a 20 words description for the following \
    company:{company_name}"
)

# chain 2
chain_two = LLMChain(llm=llm, prompt=second_prompt)

overall_simple_chain = SimpleSequentialChain(chains=[chain_one, chain_two], verbose=True)

print(overall_simple_chain.run(product))

# SequentialChain

llm = ChatOpenAI(temperature=0.9, model=llm_model)

# prompt template 1: translate to english
first_prompt = ChatPromptTemplate.from_template(
    "Translate the following review to english:"
    "\n\n{Review}"
)

# chain 1: input= Review and output= English_Review
chain_one = LLMChain(llm=llm, prompt=first_prompt, 
                     output_key="English_Review"
                    )

second_prompt = ChatPromptTemplate.from_template(
    "Can you summarize the following review in 1 sentence:"
    "\n\n{English_Review}"
)

# chain 2: input= English_Review and output= summary
chain_two = LLMChain(llm=llm, prompt=second_prompt, 
                     output_key="summary"
                    )

# prompt template 3: translate to english
third_prompt = ChatPromptTemplate.from_template(
    "What language is the following review:\n\n{Review}"
)

# chain 3: input= Review and output= language
chain_three = LLMChain(llm=llm, prompt=third_prompt,
                       output_key="language"
                      )


# prompt template 4: follow up message
fourth_prompt = ChatPromptTemplate.from_template(
    "Write a follow up response to the following "
    "summary in the specified language:"
    "\n\nSummary: {summary}\n\nLanguage: {language}"
)

# chain 4: input= summary, language and output= followup_message
chain_four = LLMChain(llm=llm, prompt=fourth_prompt,
                      output_key="followup_message"
                     )

# overall_chain: input= Review 
# and output= English_Review, summary, followup_message
overall_chain = SequentialChain(
    chains=[chain_one, chain_two, chain_three, chain_four],
    input_variables=["Review"],
    output_variables=["English_Review", "summary","followup_message"],
    verbose=True
)

review = df.Review[5]
print(overall_chain(review))

'''
# The router is the chain this file actually runs.
# Four destination prompts, each with an {input} slot. The persona is what that chain's model sees.
physics_template = """You are a very smart physics professor. \
You are great at answering questions about physics in a concise\
and easy to understand manner. \
When you don't know the answer to a question you admit\
that you don't know.

Here is a question:
{input}"""


math_template = """You are a very good mathematician. \
You are great at answering math questions. \
You are so good because you are able to break down \
hard problems into their component parts, 
answer the component parts, and then put them together\
to answer the broader question.

Here is a question:
{input}"""

history_template = """You are a very good historian. \
You have an excellent knowledge of and understanding of people,\
events and contexts from a range of historical periods. \
You have the ability to think, reflect, debate, discuss and \
evaluate the past. You have a respect for historical evidence\
and the ability to make use of it to support your explanations \
and judgements.

Here is a question:
{input}"""


computerscience_template = """ You are a successful computer scientist.\
You have a passion for creativity, collaboration,\
forward-thinking, confidence, strong problem-solving capabilities,\
understanding of theories and algorithms, and excellent communication \
skills. You are great at answering coding questions. \
You are so good because you know how to solve a problem by \
describing the solution in imperative steps \
that a machine can easily interpret and you know how to \
choose a solution that has a good balance between \
time complexity and space complexity. 

Here is a question:
{input}"""

# name is the string the router must return. description is the menu line the router reads.
# "History" is capitalized. The other names are not. The template is the persona prompt above.
prompt_infos = [
    {
        "name": "physics", 
        "description": "Good for answering questions about physics", 
        "prompt_template": physics_template
    },
    {
        "name": "math", 
        "description": "Good for answering math questions", 
        "prompt_template": math_template
    },
    {
        "name": "History", 
        "description": "Good for answering history questions", 
        "prompt_template": history_template
    },
    {
        "name": "computer science", 
        "description": "Good for answering computer science questions", 
        "prompt_template": computerscience_template
    }
]


# One LLMChain per destination, stored under the name the router will choose.
# Nothing runs here. MultiPromptChain calls the chosen chain later.
destination_chains = {}
for p_info in prompt_infos:
    name = p_info["name"]
    prompt_template = p_info["prompt_template"]
    prompt = ChatPromptTemplate.from_template(template=prompt_template)
    chain = LLMChain(llm=llm, prompt=prompt)
    destination_chains[name] = chain  
    
# The menu the router prompt will read: "name: description", one destination per line.
destinations = [f"{p['name']}: {p['description']}" for p in prompt_infos]
destinations_str = "\n".join(destinations)

# Fallback for destination DEFAULT. The prompt is only {input}, so this chain has no persona.
default_prompt = ChatPromptTemplate.from_template("{input}")
default_chain = LLMChain(llm=llm, prompt=default_prompt)

# Instructions for the router model. .format below fills {destinations}.
# {{input}} stays as the literal slot {input}, which PromptTemplate fills on each question.
# The model is told to return JSON with destination and next_inputs.
# destination has to be one of the names above, or DEFAULT.
MULTI_PROMPT_ROUTER_TEMPLATE = """Given a raw text input to a \
language model select the model prompt best suited for the input. \
You will be given the names of the available prompts and a \
description of what the prompt is best suited for. \
You may also revise the original input if you think that revising\
it will ultimately lead to a better response from the language model.

<< FORMATTING >>
Return a markdown code snippet with a JSON object formatted to look like:
```json
{{{{
    "destination": string \
        "DEFAULT" or name of the prompt to use in {destinations}
    "next_inputs": string \
        a potentially modified version of the original input
}}}}
```

REMEMBER: The value of “destination” MUST match one of \
the candidate prompts listed below.\
If “destination” does not fit any of the specified prompts, set it to “DEFAULT.”
REMEMBER: "next_inputs" can just be the original input \
if you don't think any modifications are needed.

<< CANDIDATE PROMPTS >>
{destinations}

<< INPUT >>
{{input}}

<< OUTPUT (remember to include the ```json)>>"""

# Fill the menu now. input is still open. RouterOutputParser turns the model's JSON
# into the destination name and the text the chosen chain receives.
router_template = MULTI_PROMPT_ROUTER_TEMPLATE.format(
    destinations=destinations_str
)
router_prompt = PromptTemplate(
    template=router_template,
    input_variables=["input"],
    output_parser=RouterOutputParser(),
)

# Runs the router prompt on the question and returns the parsed route.
router_chain = LLMRouterChain.from_llm(llm, router_prompt)

# Asks the router, then runs that destination chain, or default_chain when the route is DEFAULT.
# verbose=True prints which destination was chosen.
chain = MultiPromptChain(router_chain=router_chain, 
                         destination_chains=destination_chains, 
                         default_chain=default_chain, verbose=True
                        )

# Physics question, so the route should be the physics chain.
# The commented calls would send a math question, then a biology question.
# Biology is not one of the four destinations, so that call is the DEFAULT path.
print(chain.run("What is black body radiation?"))

# print(chain.run("what is 2 + 2"))

# print(chain.run("Why does every cell in our body contain DNA?"))
