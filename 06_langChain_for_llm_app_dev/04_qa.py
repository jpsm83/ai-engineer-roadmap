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

# Load OPENAI_API_KEY from a local .env. ChatOpenAI and OpenAIEmbeddings read it on their own.
_ = load_dotenv(find_dotenv()) # read local .env file

# One catalog row becomes one Document.
# page_content is "column: value" lines, the text the retriever later returns.
# metadata records the file path and the row number. lazy_load yields the rows; load() collects them.
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

# Hide warnings from the older chain and vectorstore classes.
warnings.filterwarnings('ignore')

# Render an IPython Markdown value in the terminal.
# Markdown carries the text on .data. Anything else is turned into a string.
# RichMarkdown is what draws it.
def display(obj):
    text = obj.data if isinstance(obj, Markdown) else str(obj)
    print(RichMarkdown(text or ""))

# After 2024-06-12 the chat model is gpt-5-nano; on or before that date it is gpt-6-luna.
# temperature controls how much the replies vary; this call passes 1.
current_date = datetime.datetime.now().date()

target_date = datetime.date(2024, 6, 12)

if current_date > target_date:
    llm_model = "gpt-5-nano"
else:
    llm_model = "gpt-6-luna"

llm = ChatOpenAI(temperature=1, model=llm_model)

# Short path: point the loader at the catalog, embed every row, and build an in-memory index in one call.
# OpenAIEmbeddings turns text into vectors. from_loaders reads the loader, embeds each document,
# and stores the vectors. index.query is the whole retrieve-then-answer step.
# It stays commented so the same path can be built in the open below.
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

# The same retrieve-and-answer path, built in the open. The store below is a second one, not index.
# loader.load() runs lazy_load and returns every row as a Document. docs[0] would be the first product.

docs = loader.load()

# print(docs[0])


# embed_query turns one sentence into a vector. The prints would show its length and the first five numbers.
# The vector is not used again. It is here so you can see what a query becomes before the search.
embed = embeddings.embed_query("Hi my name is Joao")

# print(len(embed))

# print(embed[:5])

# from_documents embeds the catalog into a new store, db.
# index above is a different store, the one VectorstoreIndexCreator built.
# qa_stuff searches db. index.query still searches index.
db = InMemoryVectorStore.from_documents(
    docs, 
    embeddings
)

# This query replaces the table question above. similarity_search returns the nearest documents.
# This docs replaces the full catalog. From here on, docs is only the search hits.
# The prints would show how many came back and the top document.
query = "Please suggest a shirt with sunblocking"

docs = db.similarity_search(query)

# print(len(docs))

# print(docs[0])

# as_retriever wraps the store so RetrievalQA can call it with a question.
retriever = db.as_retriever()

# Join the hit texts into one string. The commented invoke is the manual version of "stuff":
# the retrieved rows and the question go in one prompt, and .content is the reply.
# RetrievalQA below is the library object that takes over that join-and-ask step.
qdocs = "".join([docs[i].page_content for i in range(len(docs))])

# response = llm.invoke(f"{qdocs} Question: Please list all your \
# shirts with sun protection in a table in markdown and summarize each one.").content

# display(Markdown(response))

# chain_type "stuff" joins the retrieved documents into one prompt and asks once.
# verbose=True prints that prompt. retriever is the store wrapper from the line above.
qa_stuff = RetrievalQA.from_chain_type(
    llm=llm, 
    chain_type="stuff", 
    retriever=retriever, 
    verbose=True
)

# This query replaces the short suggestion. Both calls below use it.
# qa_stuff.run answers from db, the step-by-step store.
# index.query is the one-liner from the top, and it answers from index.
# The two displays are there so those two stores' answers can be compared.
query =  "Please list all your shirts with sun protection in a table \
in markdown and summarize each one."

response = qa_stuff.run(query)

display(Markdown(response))

response2 = index.query(query, llm=llm)

display(Markdown(response2))

# Unused string. It rebuilds the index the same way as the first block and does not run.
'''
index = VectorstoreIndexCreator(
    vectorstore_cls=InMemoryVectorStore,
    embedding=embeddings,
).from_loaders([loader])
'''
