import os
import cohere
import chromadb
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
from src.utilities.llms import init_llms_mini
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


load_dotenv(find_dotenv())
work_dir = os.getenv("WORK_DIR")
cohere_key = os.getenv("COHERE_API_KEY")
if cohere_key:
    cohere_client = cohere.Client(cohere_key)
collection_name = f"clean_coder_{Path(work_dir).name}_file_descriptions"


def get_collection():
    if cohere_key:
        chroma_client = chromadb.PersistentClient(path=os.getenv('WORK_DIR') + '/.clean_coder/chroma_base')
        try:
            return chroma_client.get_collection(name=collection_name)
        except:
            # print("Vector database does not exist. (Optional) create it by running src/tools/rag/write_descriptions.py to improve file research capabilities")
            return False
    return False


def vdb_available():
    return True if get_collection() else False


def retrieve(question: str) -> str:
    """
    Retrieve files descriptions by semantic query.

    Parameters:
    question (str): The query to retrieve information for.

    Returns:
    str: A formatted response with file descriptions of found files.
    """
    collection = get_collection()
    retrieval = collection.query(query_texts=[question], n_results=8)
    response = ""
    for i, description in enumerate(retrieval["documents"][0]):
        filename = retrieval["ids"][0][i]
        response += f"{filename}:\n\n{description}\n\n###\n\n"
    response += "\n\nRemember to see files before adding to final response!"
    return response

    reranked_docs = cohere_client.rerank(
        query=question,
        documents=retrieval["documents"][0],
        top_n=4,
        model="rerank-english-v3.0",
        #return_documents=True,
    )
    reranked_indexes = [result.index for result in reranked_docs.results]

    for index in reranked_indexes:
        filename = retrieval["ids"][0][index]
        description = retrieval["documents"][0][index]
        response += f"{filename}:\n{description}\n\n###"
    response += "\n\nRemember to see files before adding to final response!"

    return response
# New class added for binary ranking with lazy loading.
class BinaryRanker:
    def __init__(self):
        # Lazy-loaded chain; not initialized until rank() is called.
        self.chain = None

    def initialize_chain(self):
        if self.chain is None:
            # Define prompt template for binary ranking.
            template = (
                "You are a binary ranker. Evaluate the relevance of a document to a given question.\n"
                "Question: {question}\n"
                "Document: {document}\n\n"
                "If the document is relevant to the question, output only '1'. "
                "If it may be useful for programmer as contains similar code, but no relevant directly, also output '1'. "
                "If it is not relevant at all, output only '0'."
            )
            prompt = ChatPromptTemplate.from_template(template)
            # Initialize LLMs with minimal intelligence and set run name to 'BinaryRanker'
            llms = init_llms_mini(tools=[], run_name='BinaryRanker')
            llm = llms[0].with_fallbacks(llms[1:])
            # Build the chain by combining the prompt template, the LLM instance, and StrOutputParser.
            self.chain = prompt | llm | StrOutputParser()

    def rank(self, question: str, retrieval: dict) -> list:
        # Ensure the chain is initialized (lazy loading)
        self.initialize_chain()
        # Extract list of documents and their ids from the retrieval result.
        documents_list = retrieval["documents"][0]
        id_list = retrieval["ids"][0]
        # Build input for batch processing: list of dicts containing question and document.
        batch_inputs = []
        for doc in documents_list:
            batch_inputs.append({"question": question, "document": doc})
        # Use the chain batch function to get binary outputs.
        results = self.chain.batch(batch_inputs)
        # Pair each document id with its binary ranking result.
        ranking = []
        for idx, result in enumerate(results):
            ranking.append((id_list[idx], result.strip()))
        return ranking


if __name__ == "__main__":
    # Example usage of BinaryRanker for testing.
    question = "Common styles, used in the main page"
    collection = get_collection()
    retrieval = collection.query(query_texts=[question], n_results=8)
    binary_ranker = BinaryRanker()
    ranking = binary_ranker.rank(question, retrieval)
    print("Binary Ranking Results:", ranking)
    
    # Test the retrieve function
    results = retrieve(question)
    print("\n\n")
    print("results: ", results)
