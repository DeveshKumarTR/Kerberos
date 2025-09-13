"""
Claude AI Integration for Kerberos Authentication
Author: Devesh Kumar
Description: AI-powered threat detection and user behavior analysis
"""

import json
import numpy as np
from datetime import datetime
from typing import Dict, List, Any, Optional
import requests
import os
from anthropic import Anthropic


class ClaudeIntegration:
    """
    Claude AI integration for intelligent security features
    """
    
    def __init__(self):
        try:
            self.client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
            self.model = "claude-3-sonnet-20240229"
        except Exception as e:
            print(f"Warning: Could not initialize Anthropic client: {e}")
            print("Running in demo mode without Claude AI integration")
            self.client = None
            self.model = "claude-3-sonnet-20240229"
        
    def analyze_authentication_attempt(self, auth_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze authentication attempt for potential threats
        """
        try:
            prompt = f"""
            Analyze this authentication attempt for security threats:
            
            Username: {auth_data.get('username')}
            Timestamp: {auth_data.get('timestamp')}
            IP Address: {auth_data.get('ip_address')}
            User Agent: {auth_data.get('user_agent')}
            
            Please analyze and provide:
            1. Threat level (low, medium, high)
            2. Risk factors identified
            3. Recommendations
            
            Respond in JSON format with keys: threat_level, risk_factors, recommendations, confidence_score
            """
            
            if self.client is None:
                # Demo mode - return mock analysis
                return {
                    "threat_level": "low",
                    "risk_factors": ["Demo mode - no actual analysis"],
                    "recommendations": ["Set up Anthropic API key for real threat analysis"],
                    "confidence_score": 0.0
                }
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Parse the response
            try:
                analysis = json.loads(response.content[0].text)
            except json.JSONDecodeError:
                # Fallback analysis if JSON parsing fails
                analysis = {
                    "threat_level": "low",
                    "risk_factors": [],
                    "recommendations": ["Monitor for unusual patterns"],
                    "confidence_score": 0.5
                }
            
            return analysis
            
        except Exception as e:
            print(f"Claude AI analysis error: {str(e)}")
            return {
                "threat_level": "low",
                "risk_factors": ["Analysis unavailable"],
                "recommendations": ["Manual review recommended"],
                "confidence_score": 0.0
            }
    
    def analyze_authentication_pattern(self, auth_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze authentication patterns over time
        """
        try:
            prompt = f"""
            Analyze this authentication pattern data:
            
            {json.dumps(auth_data, indent=2)}
            
            Look for:
            1. Unusual login times
            2. Geographic anomalies
            3. Device/browser inconsistencies
            4. Frequency patterns
            
            Provide analysis in JSON format with: pattern_type, anomaly_score, details, recommendations
            """
            
            if self.client is None:
                # Demo mode - return mock analysis
                return {
                    "pattern_type": "demo",
                    "anomaly_score": 0.0,
                    "details": ["Demo mode - no actual analysis"],
                    "recommendations": ["Set up Anthropic API key for real pattern analysis"]
                }
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1200,
                messages=[{"role": "user", "content": prompt}]
            )
            
            try:
                analysis = json.loads(response.content[0].text)
            except json.JSONDecodeError:
                analysis = {
                    "pattern_type": "normal",
                    "anomaly_score": 0.1,
                    "details": "Pattern analysis completed",
                    "recommendations": ["Continue monitoring"]
                }
            
            return analysis
            
        except Exception as e:
            print(f"Pattern analysis error: {str(e)}")
            return {
                "pattern_type": "unknown",
                "anomaly_score": 0.5,
                "details": "Analysis error occurred",
                "recommendations": ["Manual review required"]
            }
    
    def generate_user_vector(self, user_data: Dict[str, Any]) -> List[float]:
        """
        Generate a vector representation of user behavior for Pinecone storage
        """
        try:
            # Create a behavioral vector based on user characteristics
            vector = []
            
            # Basic user features (384 dimensions for compatibility with Pinecone)
            # Time-based features
            current_hour = datetime.now().hour
            vector.extend([
                float(current_hour) / 24.0,  # Normalized hour
                float(datetime.now().weekday()) / 7.0,  # Normalized day of week
            ])
            
            # User role features
            roles = user_data.get('roles', [])
            role_features = [
                1.0 if 'admin' in roles else 0.0,
                1.0 if 'user' in roles else 0.0,
                1.0 if 'guest' in roles else 0.0,
            ]
            vector.extend(role_features)
            
            # Username characteristics
            username = user_data.get('username', '')
            username_features = [
                float(len(username)) / 20.0,  # Normalized username length
                1.0 if username.isalnum() else 0.0,  # Alphanumeric username
            ]
            vector.extend(username_features)
            
            # Pad vector to reach 384 dimensions (common embedding size)
            current_length = len(vector)
            if current_length < 384:
                # Use pseudo-random but deterministic padding based on user data
                seed_value = hash(str(user_data)) % 1000
                np.random.seed(seed_value)
                padding = np.random.normal(0, 0.1, 384 - current_length).tolist()
                vector.extend(padding)
            
            return vector[:384]  # Ensure exactly 384 dimensions
            
        except Exception as e:
            print(f"Vector generation error: {str(e)}")
            # Return a default vector if generation fails
            return [0.0] * 384
    
    def detect_anomalies(self, user_vectors: List[List[float]], threshold: float = 0.8) -> List[Dict[str, Any]]:
        """
        Detect anomalies in user behavior vectors
        """
        try:
            anomalies = []
            
            if len(user_vectors) < 2:
                return anomalies
            
            # Calculate pairwise similarities
            for i, vector1 in enumerate(user_vectors):
                similarities = []
                for j, vector2 in enumerate(user_vectors):
                    if i != j:
                        similarity = self._cosine_similarity(vector1, vector2)
                        similarities.append(similarity)
                
                avg_similarity = np.mean(similarities) if similarities else 0.0
                
                if avg_similarity < threshold:
                    anomalies.append({
                        'vector_index': i,
                        'similarity_score': avg_similarity,
                        'anomaly_type': 'behavioral_deviation',
                        'severity': 'high' if avg_similarity < 0.5 else 'medium'
                    })
            
            return anomalies
            
        except Exception as e:
            print(f"Anomaly detection error: {str(e)}")
            return []
    
    def _cosine_similarity(self, vector1: List[float], vector2: List[float]) -> float:
        """
        Calculate cosine similarity between two vectors
        """
        try:
            v1 = np.array(vector1)
            v2 = np.array(vector2)
            
            dot_product = np.dot(v1, v2)
            norm1 = np.linalg.norm(v1)
            norm2 = np.linalg.norm(v2)
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            return dot_product / (norm1 * norm2)
            
        except Exception as e:
            print(f"Cosine similarity calculation error: {str(e)}")
            return 0.0
    
    def generate_security_recommendations(self, analysis_data: Dict[str, Any]) -> List[str]:
        """
        Generate security recommendations based on analysis
        """
        try:
            prompt = f"""
            Based on this security analysis data:
            {json.dumps(analysis_data, indent=2)}
            
            Generate specific, actionable security recommendations.
            Focus on:
            1. Immediate actions needed
            2. Long-term security improvements
            3. Monitoring strategies
            
            Return as a JSON list of recommendation strings.
            """
            
            if self.client is None:
                # Demo mode - return mock recommendations
                return [
                    "Demo mode: Set up Anthropic API key for AI-powered recommendations",
                    "Enable multi-factor authentication",
                    "Monitor login patterns regularly",
                    "Implement IP whitelisting for sensitive accounts"
                ]
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=800,
                messages=[{"role": "user", "content": prompt}]
            )
            
            try:
                recommendations = json.loads(response.content[0].text)
                if isinstance(recommendations, list):
                    return recommendations
                else:
                    return ["Review security settings", "Enable additional monitoring"]
            except json.JSONDecodeError:
                return ["Enable two-factor authentication", "Monitor login patterns", "Review access logs"]
            
        except Exception as e:
            print(f"Recommendation generation error: {str(e)}")
            return ["Standard security measures recommended"]
