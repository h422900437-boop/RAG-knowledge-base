from langchain_community.vectorstores import Chroma #we can't directly import from chroma, so we need to import from langchain_community.vectorstores
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import tiktoken 

def tokenizer_len(text: str) -> int:
    """Returns the number of tokens in a text string."""
    tokenizer = tiktoken.get_encoding("cl100k_base") #give the tokenizer a name, here we use cl100k_base, which is the tokenizer used by OpenAI's GPT-4 and GPT-3.5 models
    tokens = tokenizer.encode(text, disallowed_special=())
    return len(tokens)

#  Embedding model: BAAI/bge-small-zh-v1.5
print("Loading Embedding model (BAAI/bge-small-zh-v1.5)...")
embedding_model = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-zh-v1.5",
    model_kwargs={'device': 'cpu'}
)

file_path = "../company_policy.txt"
print(f"reading file: {file_path}")

try:
    with open(file_path, "r", encoding="utf-8") as f:
        raw_text = f.read()
except FileNotFoundError:
    print(f"Something wrong with {file_path} file, please check if the file exists in the root directory")
    exit()

print("performing text splitting...")
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,        # maximum chunk size in characters
    chunk_overlap=50,      # number of characters to overlap between chunks
    length_function=tokenizer_len, # function to calculate the length of the text in tokens
    separators=["\n\n", "\n", "。", "！", "？", "，", " "] # separators to split the text into chunks
)

docs = text_splitter.create_documents([raw_text])
print(f"📑 Text splitting completed! A total of {len(docs)} knowledge chunks have been generated.")


Chroma.from_documents( #store the knowledge chunks into a local vector database
    documents=docs,
    embedding=embedding_model,
    persist_directory="../chroma_db" # directory to store the local vector database
)

print("🎉 Success! The local vector database chroma_db has been built successfully, and the attendance and cafeteria regulations have been stored!")