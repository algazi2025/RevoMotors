import axios, { AxiosInstance, AxiosError, AxiosRequestConfig } from 'axios';

// API Response wrapper
interface ApiResponse<T> {
  data?: T;
  error?: string;
  detail?: string;
  status: number;
}

// Create axios instance with default config
const createApiClient = (): AxiosInstance => {
  const baseURL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

  const client = axios.create({
    baseURL,
    timeout: 30000,
    headers: {
      'Content-Type': 'application/json',
    },
  });

  // Request interceptor - add auth token
  client.interceptors.request.use(
    (config) => {
      // Get token from localStorage or sessionStorage
      const token = typeof window !== 'undefined' 
        ? localStorage.getItem('access_token')
        : null;

      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }

      return config;
    },
    (error) => Promise.reject(error)
  );

  // Response interceptor - handle errors
  client.interceptors.response.use(
    (response) => response,
    (error: AxiosError) => {
      // Handle 401 Unauthorized - redirect to login
      if (error.response?.status === 401) {
        if (typeof window !== 'undefined') {
          localStorage.removeItem('access_token');
          window.location.href = '/dealer/login';
        }
      }

      // Handle 403 Forbidden
      if (error.response?.status === 403) {
        console.error('Access forbidden');
      }

      return Promise.reject(error);
    }
  );

  return client;
};

export const apiClient = createApiClient();

// API Service Methods
export const api = {
  // Auth endpoints
  auth: {
    login: (email: string, password: string) =>
      apiClient.post('/api/auth/login', { email, password }),
    register: (email: string, password: string, role: 'dealer' | 'seller') =>
      apiClient.post('/api/auth/register', { email, password, role }),
    logout: () => {
      localStorage.removeItem('access_token');
      return Promise.resolve();
    },
  },

  // Dealer endpoints
  dealers: {
    getProfile: () => apiClient.get('/api/dealers/profile'),
    updateProfile: (data: any) => apiClient.put('/api/dealers/profile', data),
    getSettings: () => apiClient.get('/api/dealers/settings'),
    updateSettings: (data: any) => apiClient.put('/api/dealers/settings', data),
  },

  // Leads endpoints
  leads: {
    getAll: (source?: string, status?: string) =>
      apiClient.get('/api/leads/', {
        params: { source, status },
      }),
    getById: (id: number) => apiClient.get(`/api/leads/${id}`),
    updateStatus: (id: number, status: string) =>
      apiClient.put(`/api/leads/${id}/status`, { status }),
  },

  // Offers endpoints
  offers: {
    getAll: () => apiClient.get('/api/offers/'),
    getById: (id: number) => apiClient.get(`/api/offers/${id}`),
    create: (data: any) => apiClient.post('/api/offers/', data),
    update: (id: number, data: any) =>
      apiClient.put(`/api/offers/${id}`, data),
  },

  // Messages endpoints
  messages: {
    getAll: (leadId: number) =>
      apiClient.get('/api/messages/', { params: { lead_id: leadId } }),
    send: (leadId: number, message: string) =>
      apiClient.post('/api/messages/', { lead_id: leadId, content: message }),
  },

  // Car database endpoints
  cars: {
    getMakes: () => apiClient.get('/api/cars/makes'),
    getModels: (make: string) =>
      apiClient.get('/api/cars/models', { params: { make } }),
    getTrims: (make: string, model: string) =>
      apiClient.get('/api/cars/trims', {
        params: { make, model },
      }),
    getYears: (make: string, model: string) =>
      apiClient.get('/api/cars/years', {
        params: { make, model },
      }),
    getBodyTypes: (make: string, model: string) =>
      apiClient.get('/api/cars/body_types', {
        params: { make, model },
      }),
  },
};

// Error handling utility
export const handleApiError = (error: any): string => {
  if (axios.isAxiosError(error)) {
    const message = error.response?.data?.detail || error.message;
    return typeof message === 'string' ? message : JSON.stringify(message);
  }
  return 'An unexpected error occurred';
};

// Success handler utility
export const handleApiSuccess = <T>(data: T): T => {
  return data;
};

export default apiClient;
