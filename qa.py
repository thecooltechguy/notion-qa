"""Ask a question to the notion database."""
import faiss
from langchain import OpenAI
from langchain.chains.vector_db_qa.base import VectorDBQA
import pickle
import argparse

parser = argparse.ArgumentParser(description='Ask a question to the notion DB.')
parser.add_argument('question', type=str, help='The question to ask the notion DB')
args = parser.parse_args()

# Load the LangChain.
index = faiss.read_index("docs.index")

with open("faiss_store.pkl", "rb") as f:
    store = pickle.load(f)

store.index = index
chain = VectorDBQA(llm=OpenAI(temperature=0), vectorstore=store)
print(chain.run(args.question))
