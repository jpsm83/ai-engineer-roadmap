import csv
import warnings
# account for deprecation of LLM model
import datetime
from langchain_classic.chains import RetrievalQA
from langchain_classic.indexes import VectorstoreIndexCreator
from langchain_classic.evaluation.qa import QAGenerateChain, QAEvalChain
from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document
from langchain_core.globals import set_debug
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from dotenv import load_dotenv, find_dotenv
from rich import print
from rich.panel import Panel

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

# Get the current date
current_date = datetime.datetime.now().date()

# Define the date after which the model should be set to "gpt-3.5-turbo"
target_date = datetime.date(2024, 6, 12)

# Set the model variable based on the current date
if current_date > target_date:
    llm_model = "gpt-5-nano"
else:
    llm_model = "gpt-6-luna"

# Create our QandA application

file = 'OutdoorClothingCatalog_1000.csv'
loader = CSVLoader(file_path=file)
data = loader.load()

embeddings = OpenAIEmbeddings()

index = VectorstoreIndexCreator(
    vectorstore_cls=InMemoryVectorStore,
    embedding=embeddings,
).from_loaders([loader])

llm = ChatOpenAI(temperature = 1, model=llm_model)

qa = RetrievalQA.from_chain_type(
    llm=llm, 
    chain_type="stuff", 
    retriever=index.vectorstore.as_retriever(), 
    verbose=True,
    chain_type_kwargs = {
        "document_separator": "<<<<>>>>>"
    }
)

# Coming up with test datapoints

print(data[10])

# Hard-coded examples

examples = [
    {
        "query": "Do the Cozy Comfort Pullover Set\
        have side pockets?",
        "answer": "Yes"
    },
    {
        "query": "What collection is the Ultra-Lofty \
        850 Stretch Down Hooded Jacket from?",
        "answer": "The DownTek collection"
    }
]

# LLM-Generated examples

example_gen_chain = QAGenerateChain.from_llm(ChatOpenAI(model=llm_model))

# the warning below can be safely ignored

new_examples = example_gen_chain.apply_and_parse(
    [{"doc": t} for t in data[:5]]
)

print(new_examples[0])

print(data[0])

# Combine examples

examples += new_examples

print(qa.run(examples[0]["query"]))

# Manual Evaluation

set_debug(True)

print(qa.run(examples[0]["query"]))

# Turn off the debug mode
set_debug(False)

# LLM assisted evaluation

predictions = qa.apply(examples)

llm = ChatOpenAI(temperature=0, model=llm_model)
eval_chain = QAEvalChain.from_llm(llm)

graded_outputs = eval_chain.evaluate(examples, predictions)

for i, eg in enumerate(examples):
    print(Panel.fit(
        f"[bold]Question:[/bold] {predictions[i]['query']}\n"
        f"[bold]Real Answer:[/bold] {predictions[i]['answer']}\n"
        f"[bold]Predicted Answer:[/bold] {predictions[i]['result']}\n"
        f"[bold]Predicted Grade:[/bold] {graded_outputs[i]['text']}",
        title=f"Example {i}",
    ))

print(graded_outputs[0])
