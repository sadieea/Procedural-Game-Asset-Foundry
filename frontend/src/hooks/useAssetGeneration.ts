/**
 * React hook for asset generation with validation and state management.
 * Provides a clean interface for the UI to interact with the backend.
 */

import { useState, useCallback, useEffect } from 'react'
import { AssetConfig, GeneratedAsset } from '@/types/fibo'
import { apiService, ValidationResponse, GenerationResponse } from '@/services/api'

interface UseAssetGenerationState {
  // Current configuration
  config: Partial<AssetConfig> | null
  
  // Validation state
  isValidating: boolean
  validationResult: ValidationResponse | null
  
  // Generation state
  isGenerating: boolean
  generatedAssets: GeneratedAsset[]
  
  // Error state
  error: string | null
  
  // Connection state
  isConnected: boolean
}

interface UseAssetGenerationActions {
  updateConfig: (path: string, value: any) => void
  validateConfig: () => Promise<void>
  generateAsset: () => Promise<void>
  loadDefaultConfig: (assetType: string) => Promise<void>
  clearError: () => void
  resetConfig: () => void
}

export function useAssetGeneration(
  initialAssetType: 'npc_portrait' | 'weapon_item' | 'environment_concept' = 'npc_portrait'
): UseAssetGenerationState & UseAssetGenerationActions {
  const [state, setState] = useState<UseAssetGenerationState>({
    config: null,
    isValidating: false,
    validationResult: null,
    isGenerating: false,
    generatedAssets: [],
    error: null,
    isConnected: false,
  })

  // Check backend connection on mount
  useEffect(() => {
    const checkConnection = async () => {
      try {
        await apiService.healthCheck()
        setState(prev => ({ ...prev, isConnected: true }))
      } catch (error) {
        setState(prev => ({ 
          ...prev, 
          isConnected: false,
          error: 'Backend connection failed'
        }))
      }
    }

    checkConnection()
    
    // Check connection every 30 seconds
    const interval = setInterval(checkConnection, 30000)
    return () => clearInterval(interval)
  }, [])

  // Load asset history on mount
  useEffect(() => {
    const loadHistory = async () => {
      try {
        const historyResponse = await apiService.getAssetHistory()
        if (historyResponse.success) {
          setState(prev => ({ 
            ...prev, 
            generatedAssets: historyResponse.assets 
          }))
        }
      } catch (error) {
        console.warn('Failed to load asset history:', error)
        // Don't set error state for history loading failure
      }
    }

    loadHistory()
  }, [])

  // Load default config on mount
  useEffect(() => {
    loadDefaultConfig(initialAssetType)
  }, [initialAssetType]) // Remove loadDefaultConfig from dependencies

  const updateConfig = useCallback((path: string, value: any) => {
    setState(prev => {
      const newConfig = { ...prev.config }
      const keys = path.split('.')
      let current: any = newConfig
      
      // Create nested objects if they don't exist
      for (let i = 0; i < keys.length - 1; i++) {
        if (!current[keys[i]]) current[keys[i]] = {}
        current = current[keys[i]]
      }
      
      // Set the value
      current[keys[keys.length - 1]] = value
      
      return {
        ...prev,
        config: newConfig,
        validationResult: null, // Clear previous validation
        error: null
      }
    })
  }, [])

  const validateConfig = useCallback(async () => {
    if (!state.config) return

    setState(prev => ({ ...prev, isValidating: true, error: null }))

    try {
      const result = await apiService.validateConfiguration(state.config)
      
      setState(prev => ({
        ...prev,
        isValidating: false,
        validationResult: result,
        config: result.success ? result.validated_config || prev.config : prev.config
      }))
    } catch (error) {
      setState(prev => ({
        ...prev,
        isValidating: false,
        error: error instanceof Error ? error.message : 'Validation failed'
      }))
    }
  }, [state.config])

  const generateAsset = useCallback(async () => {
    if (!state.config || !state.validationResult?.success) {
      setState(prev => ({ 
        ...prev, 
        error: 'Configuration must be validated before generation' 
      }))
      return
    }

    setState(prev => ({ ...prev, isGenerating: true, error: null }))

    try {
      const result = await apiService.generateAsset(state.config as AssetConfig)
      
      if (result.success && result.metadata) {
        const newAsset: GeneratedAsset = {
          id: result.metadata.asset_id,
          type: result.metadata.asset_type as any,
          config: result.metadata.parameters,
          image_url: result.asset_url || '',
          created_at: result.metadata.created_at,
          metadata: {
            generation_time: 2.5, // Mock value
            file_size: result.metadata.file_size,
            dimensions: result.metadata.dimensions,
            format: result.metadata.format as any,
            has_transparency: result.metadata.format === 'png'
          },
          tags: []
        }

        setState(prev => ({
          ...prev,
          isGenerating: false,
          generatedAssets: [newAsset, ...prev.generatedAssets]
        }))
      } else {
        throw new Error(result.message || 'Generation failed')
      }
    } catch (error) {
      setState(prev => ({
        ...prev,
        isGenerating: false,
        error: error instanceof Error ? error.message : 'Generation failed'
      }))
    }
  }, [state.config, state.validationResult])

  const loadDefaultConfig = useCallback(async (assetType: string) => {
    setState(prev => ({ ...prev, error: null }))

    try {
      const result = await apiService.getDefaultConfiguration(assetType)
      
      if (result.success) {
        setState(prev => ({
          ...prev,
          config: result.default_config,
          validationResult: {
            success: true,
            validated_config: result.default_config,
            warnings: result.warnings || []
          }
        }))
      } else {
        throw new Error('Failed to load default configuration')
      }
    } catch (error) {
      setState(prev => ({
        ...prev,
        error: error instanceof Error ? error.message : 'Failed to load default configuration'
      }))
    }
  }, [])

  const clearError = useCallback(() => {
    setState(prev => ({ ...prev, error: null }))
  }, [])

  const resetConfig = useCallback(() => {
    setState(prev => ({
      ...prev,
      config: null,
      validationResult: null,
      error: null
    }))
  }, [])

  // Auto-validate when config changes (debounced)
  useEffect(() => {
    if (!state.config) return

    const timeoutId = setTimeout(() => {
      validateConfig()
    }, 500) // 500ms debounce

    return () => clearTimeout(timeoutId)
  }, [state.config, validateConfig])

  return {
    ...state,
    updateConfig,
    validateConfig,
    generateAsset,
    loadDefaultConfig,
    clearError,
    resetConfig,
  }
}