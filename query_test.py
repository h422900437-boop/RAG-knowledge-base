from langchain_community.vectorstores import Chroma 
from langchain_community.embeddings import HuggingFaceEmbeddings
import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

token_api=os.environ.get("DEEPSEEK_TOKEN")

print("Loading Embedding model (BAAI/bge-small-zh-v1.5)...")
embedding_model = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-zh-v1.5",    
    model_kwargs={'device': 'cpu'}
)


print("reading local stored text ...")
vector_store = Chroma(
    persist_directory="./chroma_db", # directory to store the local vector database
    embedding_function=embedding_model
)

print("connecting to the LLM model")
llm = ChatOpenAI(
    model_name="deepseek-v4-flash",
    temperature=0.2,
    openai_api_key=token_api,
    openai_api_base="https://api.deepseek.com",
)

rag_prompt_template = """You are a helpful and strict corporate HR assistant. 
Use the following pieces of retrieved attendance policies to answer the user's question. 
If you don't know the answer or if the provided policy doesn't contain enough information, say that you cannot find the explicit answer in the policy. Do not try to make up an answer.

Retrieved Attendance Policies (Context):
----------------------------------
{context}
----------------------------------

User's Question: {question}

Your Professional Answer:"""

prompt = PromptTemplate(
    template=rag_prompt_template, 
    input_variables=["context", "question"]
)

print("the system is ready to answer questions based on the knowledge in the local vector database chroma_db!")
print("-" * 50)


while True:
    user_query = input("Please enter your question (or type 'exit' to quit): ").strip()

    if user_query.lower() == 'exit' or not user_query:
        print("Exiting the program. Goodbye!")
        break       

    print("Chroma is processing your question...")

    results = vector_store.similarity_search(user_query, k=5)  # Retrieve top 3 similar documents

    context_text = "\n\n".join([
        f"---[Chunk {i+1} ]---\n" 
        f"Source File: {doc.metadata.get('source', 'Unknown')}\n"
        f"Content: \n{doc.page_content}"
        for i, doc in enumerate(results)
    ])
    print("Generating answer using the LLM model...")
    final_prompt = prompt.format(context=context_text, question=user_query)
    answer = llm.invoke(final_prompt)

    print("-" * 50)
    print(f"final answer: {answer.content}")
    print("-" * 50)

    