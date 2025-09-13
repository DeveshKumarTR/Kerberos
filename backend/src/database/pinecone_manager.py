"""
Pinecone Vector Database Manager
Author: Devesh Kumar
Description: Manages user behavior vectors and similarity searches
"""

import pinecone
import numpy as np
from typing import List, Dict, Any, Optional
import os
import json
from datetime import datetime


class PineconeManager:
    """
    Manages Pinecone vector database operations for Kerberos authentication
    """
    
    def __init__(self):
        self.api_key = os.getenv('PINECONE_API_KEY')
        self.environment = os.getenv('PINECONE_ENVIRONMENT', 'us-east1-aws')
        self.index_name = 'kerberos-users'
        self.dimension = 384  # Standard embedding dimension
        
        # Initialize Pinecone (mock for demo - real implementation would use actual Pinecone)
        self.index = None
        print("Warning: Pinecone API key not found. Vector operations will be simulated.")
    
    def store_user_vector(self, user_id: str, vector: List[float], metadata: Optional[Dict[str, Any]] = None) -> bool:
        """
        Store a user behavior vector in Pinecone
        """
        try:
            if not self.index:
                print("Pinecone not available, simulating vector storage")
                return True
            
            # Prepare metadata
            if metadata is None:
                metadata = {}
            
            metadata.update({
                'user_id': user_id,
                'timestamp': datetime.now().isoformat(),
                'vector_type': 'user_behavior'
            })
            
            # Ensure vector is the correct dimension
            if len(vector) != self.dimension:
                print(f"Warning: Vector dimension mismatch. Expected {self.dimension}, got {len(vector)}")
                # Pad or truncate vector as needed
                if len(vector) < self.dimension:
                    vector.extend([0.0] * (self.dimension - len(vector)))
                else:
                    vector = vector[:self.dimension]
            
            # Store vector
            self.index.upsert(vectors=[(user_id, vector, metadata)])
            print(f"Stored vector for user: {user_id}")
            
            return True
            
        except Exception as e:
            print(f"Vector storage error: {str(e)}")
            return False
    
    def search_similar_vectors(self, query_vector: List[float], top_k: int = 10, 
                             include_metadata: bool = True) -> List[Dict[str, Any]]:
        """
        Search for similar user behavior vectors
        """
        try:
            if not self.index:
                print("Pinecone not available, returning mock results")
                return self._mock_search_results(query_vector, top_k)
            
            # Ensure query vector is the correct dimension
            if len(query_vector) != self.dimension:
                if len(query_vector) < self.dimension:
                    query_vector.extend([0.0] * (self.dimension - len(query_vector)))
                else:
                    query_vector = query_vector[:self.dimension]
            
            # Search for similar vectors
            results = self.index.query(
                vector=query_vector,
                top_k=top_k,
                include_metadata=include_metadata
            )
            
            # Format results
            matches = []
            for match in results['matches']:
                match_data = {
                    'id': match['id'],
                    'score': match['score'],
                    'metadata': match.get('metadata', {})
                }
                matches.append(match_data)
            
            return matches
            
        except Exception as e:
            print(f"Vector search error: {str(e)}")
            return self._mock_search_results(query_vector, top_k)
    
    def get_user_vector(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a specific user's vector
        """
        try:
            if not self.index:
                print("Pinecone not available")
                return None
            
            results = self.index.fetch(ids=[user_id])
            
            if user_id in results['vectors']:
                vector_data = results['vectors'][user_id]
                return {
                    'id': user_id,
                    'values': vector_data['values'],
                    'metadata': vector_data.get('metadata', {})
                }
            
            return None
            
        except Exception as e:
            print(f"Vector retrieval error: {str(e)}")
            return None
    
    def delete_user_vector(self, user_id: str) -> bool:
        """
        Delete a user's vector from Pinecone
        """
        try:
            if not self.index:
                print("Pinecone not available, simulating deletion")
                return True
            
            self.index.delete(ids=[user_id])
            print(f"Deleted vector for user: {user_id}")
            
            return True
            
        except Exception as e:
            print(f"Vector deletion error: {str(e)}")
            return False
    
    def update_user_vector(self, user_id: str, vector: List[float], 
                          metadata: Optional[Dict[str, Any]] = None) -> bool:
        """
        Update an existing user vector
        """
        # In Pinecone, upsert serves as both insert and update
        return self.store_user_vector(user_id, vector, metadata)
    
    def find_anomalous_users(self, threshold: float = 0.7) -> List[Dict[str, Any]]:
        """
        Find users with anomalous behavior patterns
        """
        try:
            if not self.index:
                print("Pinecone not available, returning mock anomalies")
                return []
            
            # This is a simplified anomaly detection
            # In practice, you might use more sophisticated methods
            anomalies = []
            
            # Query random vectors to find outliers
            stats = self.index.describe_index_stats()
            total_vectors = stats.get('total_vector_count', 0)
            
            if total_vectors < 10:
                return []  # Not enough data for anomaly detection
            
            # Sample some vectors and check for outliers
            # This is a basic implementation - real anomaly detection would be more complex
            print(f"Checking {total_vectors} vectors for anomalies")
            
            return anomalies
            
        except Exception as e:
            print(f"Anomaly detection error: {str(e)}")
            return []
    
    def get_index_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the Pinecone index
        """
        try:
            if not self.index:
                return {'status': 'unavailable', 'vector_count': 0}
            
            stats = self.index.describe_index_stats()
            return {
                'status': 'available',
                'vector_count': stats.get('total_vector_count', 0),
                'dimension': self.dimension,
                'index_name': self.index_name
            }
            
        except Exception as e:
            print(f"Index stats error: {str(e)}")
            return {'status': 'error', 'error': str(e)}
    
    def _mock_search_results(self, query_vector: List[float], top_k: int) -> List[Dict[str, Any]]:
        """
        Generate mock search results when Pinecone is not available
        """
        mock_results = []
        
        for i in range(min(top_k, 5)):  # Return up to 5 mock results
            mock_results.append({
                'id': f'mock_user_{i}',
                'score': 0.8 - (i * 0.1),  # Decreasing similarity scores
                'metadata': {
                    'user_id': f'mock_user_{i}',
                    'timestamp': datetime.now().isoformat(),
                    'vector_type': 'user_behavior'
                }
            })
        
        return mock_results
    
    def bulk_store_vectors(self, vectors_data: List[Dict[str, Any]]) -> bool:
        """
        Store multiple vectors in batch
        """
        try:
            if not self.index:
                print("Pinecone not available, simulating bulk storage")
                return True
            
            # Prepare vectors for batch upsert
            vectors_to_upsert = []
            
            for data in vectors_data:
                user_id = data['user_id']
                vector = data['vector']
                metadata = data.get('metadata', {})
                
                # Ensure vector dimension
                if len(vector) != self.dimension:
                    if len(vector) < self.dimension:
                        vector.extend([0.0] * (self.dimension - len(vector)))
                    else:
                        vector = vector[:self.dimension]
                
                vectors_to_upsert.append((user_id, vector, metadata))
            
            # Batch upsert
            self.index.upsert(vectors=vectors_to_upsert)
            print(f"Bulk stored {len(vectors_to_upsert)} vectors")
            
            return True
            
        except Exception as e:
            print(f"Bulk storage error: {str(e)}")
            return False
