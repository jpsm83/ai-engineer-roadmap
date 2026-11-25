import csv
import warnings
# account for deprecation of LLM model
import datetime
from langchain_classic.chains import RetrievalQA
from langchain_classic.indexes import VectorstoreIndexCreator
from langchain_classic.evaluation.qa import QAGenerateChain, QAEvalChain
from langchain_classic.output_parsers.regex import RegexParser
from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document
from langchain_core.globals import set_debug
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from dotenv import load_dotenv, find_dotenv
from rich import print
from rich.panel import Panel

# Load OPENAI_API_KEY from a local .env. The chat model and the embeddings call both read it.
_ = load_dotenv(find_dotenv()) # read local .env file

# One catalog row becomes one Document of "column: value" lines.
# page_content is what the retriever returns. metadata holds the path and the row number.
# data below is the list load() collects. The example generator reads those texts.
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

# After 2024-06-12 the chat model is gpt-5-nano; on or before that date it is gpt-6-luna.
current_date = datetime.datetime.now().date()
target_date = datetime.date(2024, 6, 12)
if current_date > target_date:
    llm_model = "gpt-5-nano"
else:
    llm_model = "gpt-6-luna"

# The app under test. data is every catalog row, used later to invent test questions.
# The index embeds those rows into an in-memory store. RetrievalQA searches that store.
# chain_type "stuff" joins the retrieved rows and asks once.
# document_separator is the string placed between those rows inside the prompt.
# verbose=True prints the prompt. temperature=1 is the value the chat model is called with.
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

# data[10] would show one catalog row, a source for a test question.
# print(data[10])

# Two known question/answer pairs. The keys are query and answer.
# The grader and the prediction loop below look up those same names.
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

# QAGenerateChain asks the model for a question and answer drawn from one document.
# This ChatOpenAI is a separate model from the qa chain's llm.
# RegexParser replaces the default parser. output_keys are query and answer,
# the same names as the hand-written examples.
# Default parser expects "ANSWER: ..." on one line; newer models often
# put a newline (or a bullet list) after ANSWER:.
example_gen_chain = QAGenerateChain.from_llm(
    ChatOpenAI(model=llm_model),
    output_parser=RegexParser(
        regex=r"(?s)QUESTION:\s*(.*?)\n+ANSWER:\s*(.*)",
        output_keys=["query", "answer"],
    ),
)

# the warning below can be safely ignored

# Run the generator on the first five documents. Each result nests the pair under "qa_pairs".
# The second assignment replaces that raw list with flat query/answer dicts,
# the same shape as the hand-written examples.
# The prints would show the first generated pair and the first document.
new_examples = example_gen_chain.apply_and_parse(
    [{"doc": t.page_content} for t in data[:5]]
)
new_examples = [
    {
        "query": example["qa_pairs"]["query"].strip(),
        "answer": example["qa_pairs"]["answer"].strip(),
    }
    for example in new_examples
]

# print(new_examples[0])

# print(data[0])

# Hand-written pairs stay first. Generated ones are appended.
# The commented run would answer examples[0], the cozy-pullover question, with no grade yet.
examples += new_examples

# print(qa.run(examples[0]["query"]))

# set_debug(True) prints the chain's prompts and outputs. The run itself stays commented.
# set_debug(False) turns that tracing off before the graded pass.
set_debug(True)

# print(qa.run(examples[0]["query"]))

# Turn off the debug mode
set_debug(False)

# qa.apply runs every example. Each prediction keeps query, the real answer, and result,
# which is the chain's answer. QAEvalChain grades result against that answer.
# evaluate returns one grade dict per example. output_key is the field that holds the grade.
# The loop prints the question, both answers, and the grade. The last print is the first grade dict.
predictions = qa.apply(examples)

# print(predictions)

eval_chain = QAEvalChain.from_llm(llm)

graded_outputs = eval_chain.evaluate(examples, predictions)

for i, eg in enumerate(examples):
    print(Panel.fit(
        f"[bold]Question:[/bold] {predictions[i]['query']}\n"
        f"[bold]Real Answer:[/bold] {predictions[i]['answer']}\n"
        f"[bold]Predicted Answer:[/bold] {predictions[i]['result']}\n"
        f"[bold]Predicted Grade:[/bold] {graded_outputs[i][eval_chain.output_key]}",
        title=f"Example {i}",
    ))

print(graded_outputs[0])
