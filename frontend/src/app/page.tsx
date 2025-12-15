'use client'

import { useState, useCallback } from 'react'
import { motion } from 'framer-motion'
import { TopBar } from '@/components/TopBar'
import { ControlPanel } from '@/components/ControlPanel'
import { AssetCanvas } from '@/components/AssetCanvas'
import { JSONInspector } from '@/components/JSONInspector'
import { AssetHistory } from '@/components/AssetHistory'
import { AssetConfig, GeneratedAsset } from '@/types/fibo'
import { useAssetGeneration } from '@/hooks/useAssetGeneration'

export default function Home() {
  const [activeAssetType, setActiveAssetType] = useState<'npc_portrait' | 'weapon_item' | 'environment_concept'>('npc_portrait')
  
  const {
    config,
    isValidating,
    validationResult,
    isGenerating,
    generatedAssets,
    error,
    isConnected,
    updateConfig,
    generateAsset,
    loadDefaultConfig,
    clearError,
    resetConfig,
  } = useAssetGeneration(activeAssetType)

  // Handle asset type switching
  const handleAssetTypeChange = useCallback((type: AssetConfig['assetType']) => {
    setActiveAssetType(type)
    resetConfig()
    loadDefaultConfig(type)
  }, [resetConfig, loadDefaultConfig])

  // Handle configuration changes from control panel
  const handleConfigChange = useCallback((path: string, value: any) => {
    updateConfig(path, value)
  }, [updateConfig])

  // Handle asset generation
  const handleGenerate = useCallback(async () => {
    if (!config || !validationResult?.success) {
      return
    }
    
    await generateAsset()
  }, [config, validationResult, generateAsset])

  // Handle error dismissal
  const handleErrorDismiss = useCallback(() => {
    clearError()
  }, [clearError])

  // Handle asset selection from history
  const handleAssetSelect = useCallback((asset: GeneratedAsset) => {
    // Asset selection logic can be implemented here
    console.log('Asset selected:', asset.id)
  }, [])

  // Handle configuration restoration from history
  const handleConfigRestore = useCallback((config: AssetConfig) => {
    // Switch to the asset type if different
    if (config.assetType !== activeAssetType) {
      setActiveAssetType(config.assetType)
    }
    
    // Update the configuration
    resetConfig()
    // Apply the restored config
    Object.entries(config).forEach(([key, value]) => {
      updateConfig(key, value)
    })
  }, [activeAssetType, resetConfig, updateConfig])

  // Handle asset deletion
  const handleAssetDelete = useCallback((assetId: string) => {
    // Asset deletion logic can be implemented here
    console.log('Asset deleted:', assetId)
  }, [])

  // Export handlers
  const handleExportPNG = useCallback(() => {
    const currentAsset = generatedAssets[0]
    if (currentAsset) {
      const link = document.createElement('a')
      link.href = currentAsset.image_url
      link.download = `${currentAsset.type}-${currentAsset.id}.png`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    }
  }, [generatedAssets])

  const handleExportJSON = useCallback(() => {
    if (config) {
      const blob = new Blob([JSON.stringify(config, null, 2)], { 
        type: 'application/json' 
      })
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `${config.assetType}-config-${Date.now()}.json`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      URL.revokeObjectURL(url)
    }
  }, [config])

  return (
    <div className="h-screen w-screen bg-studio-dark flex flex-col overflow-hidden">
      {/* Top Bar */}
      <TopBar
        activeAssetType={activeAssetType}
        onAssetTypeChange={handleAssetTypeChange}
        connectionStatus={isConnected ? 'connected' : 'disconnected'}
        onExportPNG={handleExportPNG}
        onExportJSON={handleExportJSON}
      />

      {/* Main Workspace */}
      <div className="flex-1 flex min-h-0">
        {/* Left Panel - Control Panel */}
        <motion.div
          key={activeAssetType}
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.3, ease: 'easeOut' }}
        >
          <ControlPanel
            assetType={activeAssetType}
            config={config}
            validationResult={validationResult}
            isValidating={isValidating}
            onConfigChange={handleConfigChange}
            onGenerate={handleGenerate}
            isGenerating={isGenerating}
          />
        </motion.div>

        {/* Center Panel - Asset Canvas */}
        <AssetCanvas
          asset={generatedAssets[0] || null}
          isGenerating={isGenerating}
          onRegenerate={handleGenerate}
          onDownload={handleExportPNG}
        />

        {/* Right Panel - JSON Inspector & History */}
        <div className="w-96 flex flex-col min-h-0">
          {/* JSON Inspector */}
          <div className="flex-1 min-h-0">
            <JSONInspector
              config={config}
              validationResult={validationResult}
              onConfigRestore={handleConfigRestore}
            />
          </div>

          {/* Asset History */}
          <div className="h-80 border-t border-studio-border min-h-0">
            <AssetHistory
              assets={generatedAssets}
              onAssetSelect={handleAssetSelect}
              onAssetRestore={(asset) => handleConfigRestore(asset.config)}
              onAssetDelete={handleAssetDelete}
            />
          </div>
        </div>
      </div>

      {/* Error Toast */}
      {error && (
        <motion.div
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: 50 }}
          className="fixed bottom-6 right-6 bg-red-500/90 text-white px-4 py-3 rounded-lg shadow-lg max-w-sm"
        >
          <p className="text-sm font-medium">{error}</p>
          <button
            onClick={handleErrorDismiss}
            className="absolute top-2 right-2 text-white/80 hover:text-white"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </motion.div>
      )}
    </div>
  )
}