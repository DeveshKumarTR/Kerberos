"""
Kerberos Protocol Implementation with Claude AI and Pinecone Integration
Author: Devesh Kumar
Description: A secure three-headed authentication system
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import os
import logging
from dotenv import load_dotenv

# Import custom modules
from src.auth.kerberos_auth import KerberosAuth
from src.ai.claude_integration import ClaudeIntegration
from src.database.pinecone_manager import PineconeManager
from src.models.user import User
from src.utils.crypto_utils import CryptoUtils

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-jwt-secret-key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=8)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///kerberos.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
cors = CORS(app)
jwt = JWTManager(app)
db = SQLAlchemy(app)

# Initialize services
kerberos_auth = KerberosAuth()
claude_ai = ClaudeIntegration()
pinecone_manager = PineconeManager()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': '🐕‍🦺 Kerberos Protocol Server is running',
        'author': 'Devesh Kumar',
        'version': '1.0.0'
    })

@app.route('/api/auth/login', methods=['POST'])
def login():
    """User authentication endpoint"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({
                'success': False,
                'message': 'Username and password are required'
            }), 400

        # Phase 1: Authentication Server (AS) validation
        user = kerberos_auth.authenticate_user(username, password)
        if not user:
            return jsonify({
                'success': False,
                'message': 'Invalid credentials'
            }), 401

        # Phase 2: Claude AI threat analysis
        threat_analysis = claude_ai.analyze_authentication_attempt({
            'username': username,
            'timestamp': datetime.now().isoformat(),
            'ip_address': request.remote_addr,
            'user_agent': request.headers.get('User-Agent')
        })

        if threat_analysis.get('threat_level', 'low') == 'high':
            logger.warning(f"High threat level detected for user: {username}")
            return jsonify({
                'success': False,
                'message': 'Authentication blocked due to security concerns'
            }), 403

        # Phase 3: Generate JWT token
        access_token = create_access_token(identity=user.id)

        # Store user behavior vector in Pinecone
        user_vector = claude_ai.generate_user_vector(user.to_dict())
        pinecone_manager.store_user_vector(user.id, user_vector)

        return jsonify({
            'success': True,
            'message': 'Authentication successful',
            'user': {
                'id': user.id,
                'username': user.username,
                'roles': user.roles
            },
            'token': access_token
        })

    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Internal server error'
        }), 500

@app.route('/api/kerberos/tgt', methods=['POST'])
@jwt_required()
def request_tgt():
    """Request Ticket Granting Ticket (TGT)"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        username = data.get('username')

        # Generate TGT
        tgt = kerberos_auth.generate_tgt(user_id, username)
        
        return jsonify({
            'tgt': tgt,
            'expiry': (datetime.now() + timedelta(hours=8)).isoformat()
        })

    except Exception as e:
        logger.error(f"TGT request error: {str(e)}")
        return jsonify({'error': 'Failed to generate TGT'}), 500

@app.route('/api/kerberos/service-ticket', methods=['POST'])
def request_service_ticket():
    """Request Service Ticket"""
    try:
        data = request.get_json()
        service_name = data.get('serviceName')
        tgt = data.get('tgt')

        if not service_name or not tgt:
            return jsonify({'error': 'Service name and TGT are required'}), 400

        # Validate TGT and generate service ticket
        service_ticket = kerberos_auth.generate_service_ticket(tgt, service_name)
        
        return jsonify({
            'serviceTicket': service_ticket,
            'expiry': (datetime.now() + timedelta(hours=2)).isoformat()
        })

    except Exception as e:
        logger.error(f"Service ticket request error: {str(e)}")
        return jsonify({'error': 'Failed to generate service ticket'}), 500

@app.route('/api/resources/<resource_id>', methods=['GET'])
def access_resource(resource_id):
    """Access protected resource"""
    try:
        service_ticket = request.headers.get('Service-Ticket')
        
        if not service_ticket:
            return jsonify({'error': 'Service ticket required'}), 401

        # Validate service ticket
        if not kerberos_auth.validate_service_ticket(service_ticket):
            return jsonify({'error': 'Invalid service ticket'}), 403

        # Return protected resource
        return jsonify({
            'resource_id': resource_id,
            'data': f'Protected data for resource {resource_id}',
            'accessed_at': datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Resource access error: {str(e)}")
        return jsonify({'error': 'Failed to access resource'}), 500

@app.route('/api/ai/analyze', methods=['POST'])
@jwt_required()
def analyze_auth_pattern():
    """Analyze authentication patterns with Claude AI"""
    try:
        data = request.get_json()
        auth_data = data.get('authData')

        analysis = claude_ai.analyze_authentication_pattern(auth_data)
        
        return jsonify(analysis)

    except Exception as e:
        logger.error(f"AI analysis error: {str(e)}")
        return jsonify({'error': 'Failed to analyze authentication pattern'}), 500

@app.route('/api/vectors/store', methods=['POST'])
@jwt_required()
def store_vector():
    """Store user vector in Pinecone"""
    try:
        data = request.get_json()
        user_id = data.get('userId')
        vector = data.get('vector')

        pinecone_manager.store_user_vector(user_id, vector)
        
        return jsonify({'message': 'Vector stored successfully'})

    except Exception as e:
        logger.error(f"Vector storage error: {str(e)}")
        return jsonify({'error': 'Failed to store vector'}), 500

@app.route('/api/vectors/search', methods=['POST'])
@jwt_required()
def search_vectors():
    """Search similar vectors in Pinecone"""
    try:
        data = request.get_json()
        vector = data.get('vector')

        matches = pinecone_manager.search_similar_vectors(vector)
        
        return jsonify({'matches': matches})

    except Exception as e:
        logger.error(f"Vector search error: {str(e)}")
        return jsonify({'error': 'Failed to search vectors'}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Run the application
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 8000)),
        debug=os.getenv('FLASK_ENV') == 'development'
    )
