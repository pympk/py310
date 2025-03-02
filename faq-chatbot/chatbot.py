from langchain.vectorstores import Chroma
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.chains import RetrievalQA

class ChatBot:
    def __init__(self):
        self.embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vectordb = Chroma(
            # persist_directory="db",
            persist_directory = 'faq-chatbot/db',
            embedding_function=self.embeddings
        )
        self.qa = RetrievalQA.from_chain_type(
            llm=None,  # We'll use pure semantic search
            chain_type="stuff",
            retriever=self.vectordb.as_retriever(search_kwargs={"k": 3})
        )

    def get_answer(self, query):
        try:
            # First try semantic search
            docs = self.vectordb.similarity_search(query, k=2)
            if docs:
                # Combine top results with context
                context = "\n\n".join([doc.page_content for doc in docs])
                return f"Based on our information:\n\n{context}"
        except Exception as e:
            return "I'm having trouble accessing that information. Please try rephrasing your question."