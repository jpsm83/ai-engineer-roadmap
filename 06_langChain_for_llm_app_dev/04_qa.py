import csv
import warnings
# account for deprecation of LLM model
import datetime
from IPython.display import Markdown
from langchain_classic.chains import RetrievalQA
from langchain_classic.indexes import VectorstoreIndexCreator
from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from dotenv import load_dotenv, find_dotenv
from rich import print
from rich.markdown import Markdown as RichMarkdown

_ = load_dotenv(find_dotenv()) # read local .env file

class CSVLoader(BaseLoader):
    """Load a CSV file as one Document per row (column: value lines)."""

    def __init__(self, file_path, encoding="utf-8"):
        self.file_path = file_path
        self.encoding = encoding

    def lazy_load(self):
        with open(self.file_path, newline="", encoding=self.encoding) as csvfile:
            for i, row in enumerate(csv.DictReader(csvfile)):
                content = "\n".join(f"{k}: {v}" for k, v in row.items())
                yield Document(
                    page_content=content,
                    metadata={"source": str(self.file_path), "row": i},
                )

warnings.filterwarnings('ignore')

def display(obj):
    text = obj.data if isinstance(obj, Markdown) else str(obj)
    print(RichMarkdown(text or ""))

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

file = 'OutdoorClothingCatalog_1000.csv'
loader = CSVLoader(file_path=file)

embeddings = OpenAIEmbeddings()

index = VectorstoreIndexCreator(
    vectorstore_cls=InMemoryVectorStore,
    embedding=embeddings,
).from_loaders([loader])

query ="Please list all your shirts with sun protection \
in a table in markdown and summarize each one."

# response = index.query(query, llm = llm)

# display(Markdown(response))

# Step By Step

docs = loader.load()

# print(docs[0])


embed = embeddings.embed_query("Hi my name is Joao")

# print(len(embed))

# print(embed[:5])

db = InMemoryVectorStore.from_documents(
    docs, 
    embeddings
)

query = "Please suggest a shirt with sunblocking"

docs = db.similarity_search(query)

# print(len(docs))

# print(docs[0])

retriever = db.as_retriever()

qdocs = "".join([docs[i].page_content for i in range(len(docs))])

# response = llm.invoke(f"{qdocs} Question: Please list all your \
# shirts with sun protection in a table in markdown and summarize each one.").content

# display(Markdown(response))

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

response2 = index.query(query, llm=llm)

display(Markdown(response2))

'''
index = VectorstoreIndexCreator(
    vectorstore_cls=InMemoryVectorStore,
    embedding=embeddings,
).from_loaders([loader])
'''
