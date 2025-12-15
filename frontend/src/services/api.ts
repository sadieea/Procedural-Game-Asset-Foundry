/**
 * API service for communicating with the FIBO backend.
 * Handles all HTTP requests with proper error handling and type safety.
 */

import { AssetConfig, GeneratedAsset } from '@/types/fibo'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'
const BACKEND_BASE_URL = API_BASE_URL.replace('/api', '')

export interface ValidationResponse {
  success: boolean
  errorType?: string
  message?: string
  errors?: string[]
  warnings?: string[]
  validated_config?: AssetConfig
}

export interface GenerationResponse {
  success: boolean
  asset_url?: string
  metadata?: {
    asset_id: string
    asset_type: string
    parameters: AssetConfig
    created_at: string
    file_size: number
    dimensions: { width: number; height: number }
    format: string
  }
  errorType?: string
  message?: string
}

export interface DefaultConfigResponse {
  success: boolean
  asset_type: string
  schema_version: string
  default_config: AssetConfig
  validation_status: string
  warnings?: string[]
}

class ApiService {
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`
    
    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    }

    try {
      const response = await fetch(url, config)
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.message || `HTTP ${response.status}: ${response.statusText}`)
      }

      return await response.json()
    } catch (error) {
      console.error(`API request failed: ${endpoint}`, error)
      throw error
    }
  }

  /**
   * Validate a configuration against strict FIBO schemas
   */
  async validateConfiguration(config: Partial<AssetConfig>): Promise<ValidationResponse> {
    return this.request<ValidationResponse>('/generate/validate', {
      method: 'POST',
      body: JSON.stringify(config),
    })
  }

  /**
   * Generate an asset from a validated configuration
   */
  async generateAsset(config: AssetConfig): Promise<GenerationResponse> {
    // The backend expects the full config as parameters, not nested
    const request = {
      asset_type: config.assetType,
      schema_version: config.schemaVersion || 'v1',
      parameters: config, // Send the entire config as parameters
      notes: '',
      tags: []
    }

    const response = await this.request<GenerationResponse>('/generate', {
      method: 'POST',
      body: JSON.stringify(request),
    })

    // Convert relative asset URLs to absolute URLs
    if (response.success && response.asset_url && response.asset_url.startsWith('/')) {
      response.asset_url = `${BACKEND_BASE_URL}${response.asset_url}`
    }

    return response
  }

  /**
   * Get default configuration for an asset type
   */
  async getDefaultConfiguration(assetType: string): Promise<DefaultConfigResponse> {
    return this.request<DefaultConfigResponse>(`/generate/defaults/${assetType}`)
  }

  /**
   * Get JSON schema for an asset type
   */
  async getAssetSchema(assetType: string): Promise<any> {
    return this.request(`/generate/schemas/${assetType}`)
  }

  /**
   * Validate multiple configurations in batch
   */
  async validateBatch(configs: Partial<AssetConfig>[]): Promise<any> {
    return this.request('/generate/batch/validate', {
      method: 'POST',
      body: JSON.stringify(configs),
    })
  }

  /**
   * Get asset history from storage
   */
  async getAssetHistory(): Promise<{ success: boolean; assets: GeneratedAsset[]; count: number }> {
    const response = await this.request<{ success: boolean; assets: any[]; count: number }>('/generate/history')
    
    // Convert relative asset URLs to absolute URLs
    if (response.success && response.assets) {
      response.assets = response.assets.map(asset => ({
        ...asset,
        image_url: asset.image_url.startsWith('/') ? `${BACKEND_BASE_URL}${asset.image_url}` : asset.image_url,
        thumbnail_url: asset.thumbnail_url?.startsWith('/') ? `${BACKEND_BASE_URL}${asset.thumbnail_url}` : asset.thumbnail_url
      }))
    }
    
    return response as { success: boolean; assets: GeneratedAsset[]; count: number }
  }

  /**
   * Check backend health
   */
  async healthCheck(): Promise<{ status: string; timestamp: string }> {
    // Health endpoint is not under /api prefix
    const url = `${API_BASE_URL.replace('/api', '')}/health`
    const response = await fetch(url)
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`)
    }
    return await response.json()
  }
}

export const apiService = new ApiService()
export default apiService