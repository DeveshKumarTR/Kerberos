# API Documentation
**Author:** Devesh Kumar  
**Copyright:** © 2025 Devesh Kumar. All rights reserved.

## Overview

The Kerberos Protocol Implementation provides a comprehensive REST API for authentication, authorization, and security management. This API follows the three-headed Cerberus approach with separate endpoints for each authentication phase.

## Base URL

```
Development: http://localhost:8000/api
Production: https://your-domain.com/api
```

## Authentication

All protected endpoints require authentication via JWT tokens obtained through the login process.

### Authorization Header
```
Authorization: Bearer <jwt_token>
```

### Service Ticket Header (for protected resources)
```
Service-Ticket: <service_ticket>
```

## Rate Limiting

- **General endpoints**: 100 requests per minute per IP
- **Authentication endpoints**: 10 requests per minute per IP
- **AI analysis endpoints**: 50 requests per minute per user

## Response Format

### Success Response
```json
{
  "success": true,
  "data": { ... },
  "message": "Operation completed successfully",
  "timestamp": "2025-01-XX:XX:XX"
}
```

### Error Response
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable error message",
    "details": { ... }
  },
  "timestamp": "2025-01-XX:XX:XX"
}
```

## Authentication Endpoints

### POST /auth/login

**Description:** Initial user authentication (Authentication Server - AS)

**Request:**
```json
{
  "username": "string",
  "password": "string",
  "mfa_code": "string (optional)",
  "device_id": "string (optional)"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "string",
      "username": "string",
      "roles": ["array", "of", "strings"],
      "last_login": "2025-01-XX:XX:XX",
      "mfa_enabled": boolean
    },
    "token": "jwt_token_string",
    "expires_at": "2025-01-XX:XX:XX",
    "requires_mfa": boolean
  }
}
```

**Status Codes:**
- `200`: Successful authentication
- `400`: Invalid request data
- `401`: Invalid credentials
- `403`: Account locked or MFA required
- `429`: Rate limit exceeded

**Example:**
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }'
```

### POST /auth/logout

**Description:** User logout and token invalidation

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Response:**
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

### POST /auth/refresh

**Description:** Refresh JWT token

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Response:**
```json
{
  "success": true,
  "data": {
    "token": "new_jwt_token",
    "expires_at": "2025-01-XX:XX:XX"
  }
}
```

## Kerberos Protocol Endpoints

### POST /kerberos/tgt

**Description:** Request Ticket Granting Ticket (TGS - Second Head)

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Request:**
```json
{
  "username": "string",
  "service_realm": "string (optional)"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "tgt": "encrypted_tgt_string",
    "session_key": "session_key_string",
    "expires_at": "2025-01-XX:XX:XX",
    "renewable_until": "2025-01-XX:XX:XX"
  }
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/api/kerberos/tgt \
  -H "Authorization: Bearer your_jwt_token" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin"
  }'
```

### POST /kerberos/service-ticket

**Description:** Request Service Ticket (Service Server - SS - Third Head)

**Request:**
```json
{
  "tgt": "encrypted_tgt_string",
  "service_name": "string",
  "service_realm": "string (optional)"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "service_ticket": "encrypted_service_ticket",
    "session_key": "service_session_key",
    "expires_at": "2025-01-XX:XX:XX",
    "permissions": ["read", "write", "execute"]
  }
}
```

### GET /kerberos/ticket-info

**Description:** Get information about a ticket without validating it

**Query Parameters:**
- `ticket`: Ticket string (URL encoded)
- `type`: "tgt" or "service"

**Response:**
```json
{
  "success": true,
  "data": {
    "username": "string",
    "service_name": "string (for service tickets)",
    "issued_at": "2025-01-XX:XX:XX",
    "expires_at": "2025-01-XX:XX:XX",
    "permissions": ["array", "of", "permissions"]
  }
}
```

## Protected Resource Endpoints

### GET /resources/{resource_id}

**Description:** Access protected resource

**Headers:**
```
Service-Ticket: <encrypted_service_ticket>
```

**Response:**
```json
{
  "success": true,
  "data": {
    "resource_id": "string",
    "resource_type": "string",
    "content": { ... },
    "accessed_at": "2025-01-XX:XX:XX",
    "access_level": "string"
  }
}
```

**Status Codes:**
- `200`: Successful access
- `401`: Service ticket required
- `403`: Invalid or expired service ticket
- `404`: Resource not found

### GET /resources

**Description:** List accessible resources

**Headers:**
```
Service-Ticket: <encrypted_service_ticket>
```

**Query Parameters:**
- `type`: Filter by resource type
- `limit`: Number of results (default: 50, max: 100)
- `offset`: Pagination offset

**Response:**
```json
{
  "success": true,
  "data": {
    "resources": [
      {
        "id": "string",
        "name": "string",
        "type": "string",
        "permissions": ["read", "write"],
        "last_accessed": "2025-01-XX:XX:XX"
      }
    ],
    "total": 123,
    "limit": 50,
    "offset": 0
  }
}
```

## AI Integration Endpoints

### POST /ai/analyze

**Description:** Analyze authentication patterns with Claude AI

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Request:**
```json
{
  "auth_data": {
    "username": "string",
    "timestamp": "2025-01-XX:XX:XX",
    "ip_address": "string",
    "user_agent": "string",
    "location": {
      "country": "string",
      "city": "string"
    },
    "device_info": {
      "type": "string",
      "os": "string",
      "browser": "string"
    }
  },
  "analysis_type": "threat_detection|behavior_analysis|pattern_recognition"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "threat_level": "low|medium|high",
    "threat_score": 0.25,
    "risk_factors": [
      "unusual_location",
      "new_device",
      "off_hours_access"
    ],
    "recommendations": [
      "Require additional authentication",
      "Monitor for suspicious activity"
    ],
    "confidence_score": 0.85,
    "analysis_timestamp": "2025-01-XX:XX:XX"
  }
}
```

### POST /ai/behavior-profile

**Description:** Generate or update user behavior profile

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Request:**
```json
{
  "user_id": "string",
  "behavioral_data": {
    "login_patterns": { ... },
    "device_usage": { ... },
    "location_history": { ... },
    "application_usage": { ... }
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "profile_id": "string",
    "risk_score": 0.15,
    "profile_strength": "high",
    "last_updated": "2025-01-XX:XX:XX",
    "key_patterns": [
      "consistent_office_hours",
      "stable_location_pattern",
      "regular_device_usage"
    ]
  }
}
```

## Vector Database Endpoints

### POST /vectors/store

**Description:** Store user behavior vector in Pinecone

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Request:**
```json
{
  "user_id": "string",
  "vector": [0.1, 0.2, 0.3, ...],  // 384-dimensional array
  "metadata": {
    "timestamp": "2025-01-XX:XX:XX",
    "event_type": "authentication",
    "confidence": 0.9
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "vector_id": "string",
    "stored_at": "2025-01-XX:XX:XX",
    "dimension": 384
  }
}
```

### POST /vectors/search

**Description:** Search for similar behavior vectors

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Request:**
```json
{
  "query_vector": [0.1, 0.2, 0.3, ...],
  "top_k": 10,
  "include_metadata": true,
  "filter": {
    "event_type": "authentication",
    "timestamp_range": {
      "start": "2025-01-01T00:00:00Z",
      "end": "2025-01-31T23:59:59Z"
    }
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "matches": [
      {
        "id": "vector_id",
        "score": 0.95,
        "metadata": {
          "user_id": "string",
          "timestamp": "2025-01-XX:XX:XX",
          "event_type": "authentication"
        }
      }
    ],
    "query_time_ms": 45
  }
}
```

### GET /vectors/user/{user_id}

**Description:** Get user's behavior vectors

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Query Parameters:**
- `limit`: Number of vectors to return (default: 10)
- `start_date`: ISO date string
- `end_date`: ISO date string

**Response:**
```json
{
  "success": true,
  "data": {
    "user_id": "string",
    "vectors": [
      {
        "id": "string",
        "timestamp": "2025-01-XX:XX:XX",
        "metadata": { ... }
      }
    ],
    "total_count": 25
  }
}
```

## System Management Endpoints

### GET /health

**Description:** System health check

**Response:**
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "timestamp": "2025-01-XX:XX:XX",
    "version": "1.0.0",
    "components": {
      "database": "healthy",
      "ai_service": "healthy",
      "vector_db": "healthy",
      "cache": "healthy"
    },
    "uptime_seconds": 86400
  }
}
```

### GET /metrics

**Description:** System metrics (requires admin role)

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Response:**
```json
{
  "success": true,
  "data": {
    "authentication": {
      "total_requests": 12345,
      "success_rate": 0.98,
      "avg_response_time_ms": 150
    },
    "kerberos": {
      "active_tgts": 245,
      "active_service_tickets": 1520,
      "ticket_renewal_rate": 0.85
    },
    "ai_analysis": {
      "requests_per_hour": 450,
      "threat_detections": 12,
      "avg_confidence": 0.87
    },
    "vector_operations": {
      "vectors_stored": 50000,
      "search_requests": 2340,
      "avg_search_time_ms": 25
    }
  }
}
```

## Error Codes

### Authentication Errors
- `AUTH_001`: Invalid credentials
- `AUTH_002`: Account locked
- `AUTH_003`: MFA required
- `AUTH_004`: Token expired
- `AUTH_005`: Token invalid

### Kerberos Errors
- `KRB_001`: TGT generation failed
- `KRB_002`: Invalid TGT
- `KRB_003`: Service ticket generation failed
- `KRB_004`: Service ticket validation failed
- `KRB_005`: Ticket expired

### AI Service Errors
- `AI_001`: Analysis service unavailable
- `AI_002`: Invalid analysis request
- `AI_003`: Confidence threshold not met
- `AI_004`: Rate limit exceeded

### Vector Database Errors
- `VDB_001`: Vector storage failed
- `VDB_002`: Vector search failed
- `VDB_003`: Invalid vector dimension
- `VDB_004`: Database connection error

### System Errors
- `SYS_001`: Internal server error
- `SYS_002`: Service unavailable
- `SYS_003`: Maintenance mode
- `SYS_004`: Rate limit exceeded

## SDK Examples

### Python SDK Example
```python
import requests
from kerberos_client import KerberosClient

# Initialize client
client = KerberosClient('http://localhost:8000/api')

# Authenticate
response = client.login('username', 'password')
if response.success:
    token = response.data['token']
    
    # Request TGT
    tgt_response = client.request_tgt('username')
    tgt = tgt_response.data['tgt']
    
    # Request service ticket
    service_ticket_response = client.request_service_ticket(tgt, 'file_service')
    service_ticket = service_ticket_response.data['service_ticket']
    
    # Access protected resource
    resource = client.access_resource('file_123', service_ticket)
    print(resource.data)
```

### JavaScript SDK Example
```javascript
import { KerberosClient } from '@kerberos/client';

const client = new KerberosClient('http://localhost:8000/api');

async function authenticateAndAccess() {
  try {
    // Login
    const loginResponse = await client.login('username', 'password');
    const token = loginResponse.data.token;
    
    // Request TGT
    const tgtResponse = await client.requestTGT('username');
    const tgt = tgtResponse.data.tgt;
    
    // Request service ticket
    const serviceTicketResponse = await client.requestServiceTicket(tgt, 'api_service');
    const serviceTicket = serviceTicketResponse.data.service_ticket;
    
    // Access protected resource
    const resource = await client.accessResource('data_456', serviceTicket);
    console.log(resource.data);
    
  } catch (error) {
    console.error('Authentication failed:', error);
  }
}
```

## Testing

### Postman Collection

A comprehensive Postman collection is available with pre-configured requests for all endpoints:

1. Import the collection from `/docs/postman/kerberos-api.postman_collection.json`
2. Set environment variables:
   - `base_url`: API base URL
   - `username`: Test username
   - `password`: Test password
3. Run the authentication flow to automatically set tokens

### cURL Examples

**Complete authentication flow:**
```bash
# 1. Login
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' | \
  jq -r '.data.token')

# 2. Request TGT
TGT=$(curl -s -X POST http://localhost:8000/api/kerberos/tgt \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin"}' | \
  jq -r '.data.tgt')

# 3. Request service ticket
SERVICE_TICKET=$(curl -s -X POST http://localhost:8000/api/kerberos/service-ticket \
  -H "Content-Type: application/json" \
  -d "{\"tgt\":\"$TGT\",\"service_name\":\"file_service\"}" | \
  jq -r '.data.service_ticket')

# 4. Access protected resource
curl -X GET http://localhost:8000/api/resources/file_123 \
  -H "Service-Ticket: $SERVICE_TICKET"
```

This API documentation provides comprehensive guidance for integrating with the Kerberos Protocol Implementation system.
