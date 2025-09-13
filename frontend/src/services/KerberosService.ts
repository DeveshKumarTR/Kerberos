import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000'; // Python backend URL

export interface AuthResult {
  success: boolean;
  message: string;
  user?: {
    username: string;
    id: string;
    roles: string[];
  };
  token?: string;
}

export interface KerberosTicket {
  tgt: string;
  serviceTicket: string;
  expiry: Date;
}

export class KerberosService {
  private static instance: KerberosService;
  private authToken?: string;

  public static getInstance(): KerberosService {
    if (!KerberosService.instance) {
      KerberosService.instance = new KerberosService();
    }
    return KerberosService.instance;
  }

  // Authenticate user with Kerberos protocol
  public static async authenticate(username: string, password: string): Promise<AuthResult> {
    try {
      const response = await axios.post(`${API_BASE_URL}/api/auth/login`, {
        username,
        password,
      });

      if (response.data.success) {
        return {
          success: true,
          message: 'Authentication successful',
          user: response.data.user,
          token: response.data.token,
        };
      } else {
        return {
          success: false,
          message: response.data.message || 'Authentication failed',
        };
      }
    } catch (error) {
      console.error('Authentication error:', error);
      return {
        success: false,
        message: 'Network error during authentication',
      };
    }
  }

  // Request Ticket Granting Ticket (TGT)
  public static async requestTGT(username: string, authToken: string): Promise<KerberosTicket> {
    try {
      const response = await axios.post(
        `${API_BASE_URL}/api/kerberos/tgt`,
        { username },
        {
          headers: {
            Authorization: `Bearer ${authToken}`,
          },
        }
      );

      return response.data;
    } catch (error) {
      console.error('TGT request error:', error);
      throw new Error('Failed to obtain TGT');
    }
  }

  // Request Service Ticket
  public static async requestServiceTicket(
    serviceName: string,
    tgt: string
  ): Promise<string> {
    try {
      const response = await axios.post(`${API_BASE_URL}/api/kerberos/service-ticket`, {
        serviceName,
        tgt,
      });

      return response.data.serviceTicket;
    } catch (error) {
      console.error('Service ticket request error:', error);
      throw new Error('Failed to obtain service ticket');
    }
  }

  // Access protected resource
  public static async accessResource(
    resourceId: string,
    serviceTicket: string
  ): Promise<any> {
    try {
      const response = await axios.get(
        `${API_BASE_URL}/api/resources/${resourceId}`,
        {
          headers: {
            'Service-Ticket': serviceTicket,
          },
        }
      );

      return response.data;
    } catch (error) {
      console.error('Resource access error:', error);
      throw new Error('Failed to access resource');
    }
  }

  // Claude AI integration for threat detection
  public static async analyzeAuthPattern(authData: any): Promise<any> {
    try {
      const response = await axios.post(`${API_BASE_URL}/api/ai/analyze`, {
        authData,
      });

      return response.data;
    } catch (error) {
      console.error('AI analysis error:', error);
      throw new Error('Failed to analyze authentication pattern');
    }
  }

  // Pinecone vector database operations
  public static async storeUserVector(userId: string, vector: number[]): Promise<void> {
    try {
      await axios.post(`${API_BASE_URL}/api/vectors/store`, {
        userId,
        vector,
      });
    } catch (error) {
      console.error('Vector storage error:', error);
      throw new Error('Failed to store user vector');
    }
  }

  public static async searchSimilarUsers(vector: number[]): Promise<any[]> {
    try {
      const response = await axios.post(`${API_BASE_URL}/api/vectors/search`, {
        vector,
      });

      return response.data.matches;
    } catch (error) {
      console.error('Vector search error:', error);
      throw new Error('Failed to search similar users');
    }
  }
}
