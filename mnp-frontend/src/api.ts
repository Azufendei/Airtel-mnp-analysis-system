import axios, { AxiosInstance } from 'axios'
import { MNPRequest, MNPAnalysisResponse } from './types'

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

    // Add response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          localStorage.removeItem('olm_id')
          window.location.href = '/login'
        }
        return Promise.reject(error)
      }
    )
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
