from langchain_community.document_loaders import DirectoryLoader  # THIS LINE WAS MISSING
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

# Configure paths
current_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_dir, "data", "txt")

# Debugging info
print("\n=== PATH DIAGNOSTICS ===")
print("Current working directory:", os.getcwd())
print("Computed data path:", data_path)
print("Directory exists:", os.path.exists(data_path))
if os.path.exists(data_path):
    print("Files in directory:", os.listdir(data_path))
else:
    print("ERROR: Create folder structure 'data/txt' with your .txt files!")

# Only proceed if directory exists
if not os.path.exists(data_path):
    raise SystemExit("Fatal error: Missing data directory")

# Configure text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", ". ", "! ", "? ", ", "]
)

try:
    print("\nLoading documents...")
    loader = DirectoryLoader(data_path, glob="**/*.txt")  # USE data_path HERE
    documents = loader.load()
    texts = text_splitter.split_documents(documents)
    
    print(f"\nProcessed {len(texts)} chunks from {len(documents)} documents")
    
    # Create embeddings
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Create Chroma DB
    persist_directory = 'faq-chatbot/db'
    vectordb = Chroma.from_documents(
        documents=texts,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    vectordb.persist()
    
    print("\nSuccess! Database created in 'db' folder")

except Exception as e:
    print(f"\nERROR: {str(e)}")