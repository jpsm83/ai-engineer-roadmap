import warnings
# account for deprecation of LLM model
import datetime
import panel as pn
from IPython.display import Markdown
from langchain_classic.chains import RetrievalQA
from langchain_classic.indexes import VectorstoreIndexCreator
from langchain_community.document_loaders import CSVLoader
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from dotenv import load_dotenv, find_dotenv
from rich import print

pn.extension()

_ = load_dotenv(find_dotenv()) # read local .env file

warnings.filterwarnings('ignore')

_DISPLAY_PANES = []

def display(obj):
    if isinstance(obj, Markdown):
        text = obj.data or ""
    else:
        text = str(obj)
    _DISPLAY_PANES.append(pn.pane.Markdown(text, sizing_mode="stretch_width"))

# Get the current date
current_date = datetime.datetime.now().date()

# Define the date after which the model should be set to "gpt-3.5-turbo"
target_date = datetime.date(2024, 6, 12)

# Set the model variable based on the current date
if current_date > target_date:
    llm_model = "gpt-5-nano"
else:
    llm_model = "gpt-6-luna"

file = 'OutdoorClothingCatalog_1000.csv'
loader = CSVLoader(file_path=file)

embeddings = OpenAIEmbeddings()

index = VectorstoreIndexCreator(
    vectorstore_cls=DocArrayInMemorySearch,
    embedding=embeddings,
).from_loaders([loader])

query ="Please list all your shirts with sun protection \
in a table in markdown and summarize each one."

llm_replacement_model = ChatOpenAI(temperature=1, model=llm_model)

response = index.query(query, 
                       llm = llm_replacement_model)

display(Markdown(response))

# Step By Step

loader = CSVLoader(file_path=file)

docs = loader.load()

print(docs[0])

embeddings = OpenAIEmbeddings()

embed = embeddings.embed_query("Hi my name is Harrison")

print(len(embed))

print(embed[:5])

db = DocArrayInMemorySearch.from_documents(
    docs, 
    embeddings
)

query = "Please suggest a shirt with sunblocking"

docs = db.similarity_search(query)

print(len(docs))

print(docs[0])

retriever = db.as_retriever()

llm = ChatOpenAI(temperature = 1, model=llm_model)

qdocs = "".join([docs[i].page_content for i in range(len(docs))])

response = llm.invoke(f"{qdocs} Question: Please list all your \
shirts with sun protection in a table in markdown and summarize each one.").content

display(Markdown(response))

qa_stuff = RetrievalQA.from_chain_type(
    llm=llm, 
    chain_type="stuff", 
    retriever=retriever, 
    verbose=True
)

query =  "Please list all your shirts with sun protection in a table \
in markdown and summarize each one."

response = qa_stuff.run(query)

display(Markdown(response))

response = index.query(query, llm=llm)

index = VectorstoreIndexCreator(
    vectorstore_cls=DocArrayInMemorySearch,
    embedding=embeddings,
).from_loaders([loader])

# In a notebook, display(Markdown(...)) renders inline. From a .py file
# you need .show() to start a local server and open the browser.
dashboard = pn.Column(*_DISPLAY_PANES)
dashboard.show()
