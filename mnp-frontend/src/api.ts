import axios, { AxiosInstance } from 'axios'
import { MNPRequest, MNPAnalysisResponse, UserProfile } from './types'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

class APIClient {
  private client: AxiosInstance

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json'
      }
    })

    // Request interceptor to attach JWT Bearer token
    this.client.interceptors.request.use((config) => {
      const token = localStorage.getItem('access_token')
      if (token && config.headers) {
        config.headers.Authorization = `Bearer ${token}`
      }
      return config
    })

    // Response interceptor for session expiration
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          localStorage.removeItem('access_token')
          localStorage.removeItem('olm_id')
          localStorage.removeItem('user_profile')
        }
        return Promise.reject(error)
      }
    )
  }

  async login(olm_id: string, password: string): Promise<{ access_token: string; user: UserProfile }> {
    const response = await this.client.post('/auth/login', { olm_id, password })
    return response.data
  }

  async analyzeMNP(request: MNPRequest): Promise<MNPAnalysisResponse> {
    const response = await this.client.post('/analyze', request)
    return response.data
  }

  async getHealth() {
    const response = await this.client.get('/health')
    return response.data
  }

  async getUsers() {
    const response = await this.client.get('/users')
    return response.data
  }

  async insertSampleData() {
    const response = await this.client.post('/test/insert_sample_data')
    return response.data
  }
}

export const apiClient = new APIClient()
