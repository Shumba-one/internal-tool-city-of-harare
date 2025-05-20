import os
from typing import List, Dict
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader
)
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Pinecone
import pinecone

class DocumentProcessor:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        
        # Initialize Pinecone
        pinecone.init(
            api_key=os.getenv("PINECONE_API_KEY"),
            environment=os.getenv("PINECONE_ENVIRONMENT")
        )
        
        # Create or get existing index
        if "harare-it-support" not in pinecone.list_indexes():
            pinecone.create_index(
                name="harare-it-support",
                dimension=384,  # all-MiniLM-L6-v2 embeddings dimension
                metric="cosine"
            )
        
        self.vectorstore = Pinecone.from_existing_index(
            index_name="harare-it-support",
            embedding=self.embeddings
        )

    def load_document(self, file_path: str) -> List[Dict]:
        """
        Load and process a document based on its file type.
        
        Args:
            file_path (str): Path to the document
            
        Returns:
            List[Dict]: List of processed document chunks
        """
        # Determine file type and load accordingly
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension == '.pdf':
            loader = PyPDFLoader(file_path)
        elif file_extension == '.docx':
            loader = Docx2txtLoader(file_path)
        elif file_extension == '.txt':
            loader = TextLoader(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")
        
        # Load and split document
        documents = loader.load()
        chunks = self.text_splitter.split_documents(documents)
        
        # Add metadata
        for chunk in chunks:
            chunk.metadata.update({
                "source": os.path.basename(file_path),
                "file_type": file_extension[1:],
                "chunk_index": chunks.index(chunk)
            })
        
        return chunks

    def add_documents(self, documents: List[Dict]) -> None:
        """
        Add processed documents to the vector store.
        
        Args:
            documents (List[Dict]): List of processed document chunks
        """
        self.vectorstore.add_documents(documents)

    def process_directory(self, directory_path: str) -> None:
        """
        Process all supported documents in a directory.
        
        Args:
            directory_path (str): Path to the directory containing documents
        """
        supported_extensions = {'.pdf', '.docx', '.txt'}
        
        for root, _, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_extension = os.path.splitext(file)[1].lower()
                
                if file_extension in supported_extensions:
                    try:
                        chunks = self.load_document(file_path)
                        self.add_documents(chunks)
                        print(f"Successfully processed: {file}")
                    except Exception as e:
                        print(f"Error processing {file}: {str(e)}") 