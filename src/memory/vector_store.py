import chromadb
from chromadb.config import Settings
import os
from typing import List, Dict, Any
from src.utils.logger import setup_logger

from chromadb import Documents, EmbeddingFunction, Embeddings
import google.generativeai as genai
from src.utils.logger import setup_logger

logger = setup_logger("VectorStore")

class GeminiEmbeddingFunction(EmbeddingFunction):
    """
    Custom embedding function using Google Gemini API.
    Removes dependency on onnxruntime and uses the same API key.
    """
    def __call__(self, input: Documents) -> Embeddings:
        model = 'models/text-embedding-004'
        try:
            # Batch embed content
            embeddings = [
                genai.embed_content(
                    model=model,
                    content=text,
                    task_type="retrieval_document"
                )['embedding']
                for text in input
            ]
            return embeddings
        except Exception as e:
            logger.error(f"Embedding error: {e}")
            # Return empty embeddings or re-raise? 
            # For robustness, we'll try to return zero vectors or raise
            raise e

class VectorStore:
    """
    Long-term memory bank using ChromaDB.
    Stores business rules and allows retrieval for context in future analyses.
    """
    
    def __init__(self, persist_directory: str = "./chroma_db_data"):
        """
        Initialize the vector store.
        
        Args:
            persist_directory: Directory to persist the ChromaDB data
        """
        self.persist_directory = persist_directory
        
        # Create the directory if it doesn't exist
        os.makedirs(persist_directory, exist_ok=True)
        
        # Initialize ChromaDB client with persistence
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Initialize Gemini Embedding Function
        self.embedding_function = GeminiEmbeddingFunction()
        
        # Get or create collection for business rules
        self.collection = self.client.get_or_create_collection(
            name="business_rules",
            embedding_function=self.embedding_function,
            metadata={"description": "Extracted business rules from legacy code"}
        )
        
        logger.info(f"✅ Vector store initialized at {persist_directory}")
        logger.info(f"📊 Current collection size: {self.collection.count()} rules")
    
    def store_rules(self, rules: List[str], metadata: Dict[str, Any] = None):
        """
        Store business rules in the vector database.
        
        Args:
            rules: List of business rule strings
            metadata: Optional metadata about the source (file, project, etc.)
        """
        if not rules:
            logger.warning("No rules to store")
            return
        
        # Generate unique IDs for each rule
        ids = [f"rule_{self.collection.count() + i}" for i in range(len(rules))]
        
        # Prepare metadata for each rule
        metadatas = []
        for rule in rules:
            rule_metadata = metadata.copy() if metadata else {}
            rule_metadata['rule_text'] = rule[:100]  # Store snippet in metadata
            metadatas.append(rule_metadata)
        
        # Add to collection
        self.collection.add(
            documents=rules,
            metadatas=metadatas,
            ids=ids
        )
        
        logger.info(f"💾 Stored {len(rules)} rules in memory bank")
    
    def search_similar_rules(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar business rules.
        
        Args:
            query: Query text to search for
            n_results: Number of results to return
            
        Returns:
            List of similar rules with metadata
        """
        if self.collection.count() == 0:
            logger.info("🧠 No prior memory found. Starting fresh.")
            return []
        
        results = self.collection.query(
            query_texts=[query],
            n_results=min(n_results, self.collection.count())
        )
        
        # Format results
        similar_rules = []
        if results['documents'] and results['documents'][0]:
            for i, doc in enumerate(results['documents'][0]):
                similar_rules.append({
                    'rule': doc,
                    'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                    'distance': results['distances'][0][i] if results['distances'] else None
                })
        
        logger.info(f"🔍 Found {len(similar_rules)} similar rules from memory")
        return similar_rules
    
    def get_all_rules(self) -> List[str]:
        """
        Retrieve all stored business rules.
        
        Returns:
            List of all business rules
        """
        if self.collection.count() == 0:
            return []
        
        results = self.collection.get()
        return results['documents'] if results['documents'] else []
    
    def clear_memory(self):
        """Clear all stored rules (use with caution)."""
        self.client.delete_collection("business_rules")
        self.collection = self.client.get_or_create_collection(
            name="business_rules",
            metadata={"description": "Extracted business rules from legacy code"}
        )
        logger.warning("🗑️ Memory bank cleared")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the memory bank."""
        return {
            'total_rules': self.collection.count(),
            'persist_directory': self.persist_directory
        }
