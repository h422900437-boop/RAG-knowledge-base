from langchain_community.vectorstores import Chroma 
from langchain_community.embeddings import HuggingFaceEmbeddings
import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

token_api=os.environ.get("DEEPSEEK_TOKEN") #get the token from environment variable

print("Loading Embedding model (BAAI/bge-small-zh-v1.5)...")
embedding_model = HuggingFaceEmbeddings( #define and load the embedding model
    model_name="BAAI/bge-small-zh-v1.5",    
    model_kwargs={'device': 'cpu'}
)

#Connect to the local vector database (Chroma) and load the stored embeddings
print("reading local stored text ...")
vector_store = Chroma(
    persist_directory="./chroma_db", # directory to store the local vector database
    embedding_function=embedding_model
)

#Connect to the LLM model and set the system prompt for the RAG process
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

prompt = PromptTemplate(#define the prompt template for the RAG process-提示词模版
    template=rag_prompt_template, #-静态模版
    input_variables=["context", "question"]#-动态输入
)

print("the system is ready to answer questions based on the knowledge in the local vector database chroma_db!")
print("-" * 50)

#input loop to continuously accept user queries and provide answers based on the retrieved context from the vector database
while True:
    user_query = input("Please enter your question (or type 'exit' to quit): ").strip()

    if user_query.lower() == 'exit' or not user_query:
        print("Exiting the program. Goodbye!")
        break       

    print("Chroma is processing your question...")

#embedding the user query and doing a similarity search in the vector database to retrieve relevant documents by function 'similarity_search'
    results = vector_store.similarity_search(user_query, k=5)  

#combining the retrieved documents into a single context string to be used in the prompt for the LLM model
    context_text = "\n\n".join([
        f"---[Chunk {i+1} ]---\n" # Add a header for each retrieved chunk
        f"Source File: {doc.metadata.get('source', 'Unknown')}\n" # Add the source file information
        f"Content: \n{doc.page_content}" # Add the content of the retrieved document
        for i, doc in enumerate(results)
    ])

    print("Generating answer using the LLM model...")
    #formatting the prompt with the retrieved context and the user's question, then invoking the LLM model to generate an answer
    final_prompt = prompt.format(context=context_text, question=user_query)
    answer = llm.invoke(final_prompt)

    print("-" * 50)
    print(f"final answer: {answer.content}")
    print("-" * 50)

    