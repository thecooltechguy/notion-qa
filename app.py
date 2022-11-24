"""Ask a question to the notion database."""
from gevent import monkey; monkey.patch_all()
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

import faiss
from langchain import OpenAI
from langchain.chains.vector_db_qa.base import VectorDBQA
import pickle
import os
from flask import Flask, request, jsonify

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
OPENAI_MODEL_NAME = os.environ['OPENAI_MODEL_NAME']

# Load the LangChain.
index = faiss.read_index("docs.index")

with open("faiss_store.pkl", "rb") as f:
    store = pickle.load(f)

store.index = index
chain = VectorDBQA(llm=OpenAI(
  temperature=0, 
  openai_api_key=OPENAI_API_KEY, 
  model_name=OPENAI_MODEL_NAME), 
  vectorstore=store)

app = Flask(__name__)

@app.route("/api/notion_qa", methods=['post'])
def api_notion_qa():
    try:
        body = request.get_json()

        input = body['input']
        uminal_user_id = body['user']['id']
        configuration = body['user']['configuration']

        output = chain.run(input)
        return jsonify(success=True, output=output)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify(success=False, error=f"Running the Notion Q&A chain failed: {e}"), 500

# if __name__ == "__main__":
#     app.run(debug=True, port=8081)