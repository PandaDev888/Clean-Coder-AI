
import getpass
import os

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = getpass.getpass()



response = graph.invoke({"question": "What is Task Decomposition?"})
print(response["answer"])

# from dotenv import load_dotenv, find_dotenv
# from langchain.agents import initialize_agent
# from langchain_community.llms import OpenAI
# from langchain.chains import RetrievalQA
# from langchain_community.document_loaders import TextLoader
# from langchain.memory import ConversationBufferMemory
# from langchain_openai.embeddings import OpenAIEmbeddings
# from langchain_community.vectorstores import FAISS
# from pathlib import Path
# import os

# load_dotenv(find_dotenv())
# mistral_api_key = os.getenv("MISTRAL_API_KEY")
# anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
# openai_api_key = os.getenv("OPENAI_API_KEY")
# work_dir = os.getenv("WORK_DIR")
# if not work_dir:
#     raise Exception("work_dir environment variable is not set!")

# # Load your documents
# loader = TextLoader(str(Path(work_dir).joinpath(".clean_coder").joinpath("rag_documents.txt")))
# documents = loader.load()

# # Create embeddings 
# embeddings = OpenAIEmbeddings()

# # Create a vectorstore 
# vectorstore = FAISS.from_documents(documents, embeddings)

# # Create a retriever
# retriever = vectorstore.as_retriever(n_results=2)

# # Create a RetrievalQA chain
# qa_chain = RetrievalQA.from_chain_type(
#     llm=OpenAI(),
#     chain_type="stuff",
#     retriever=retriever,
#     verbose=True
# )

# # Initialize the agent
# agent = initialize_agent(
#     llm=OpenAI(),
#     # agent=agent_tools,
#     tools=[qa_chain],
#     memory=ConversationBufferMemory(),
#     verbose=True
# )


# if __name__ == "__main__":
#     task = "What is the capital of France?"
#     # Now you can interact with the agent
#     agent.run(task)
