'use client'

import { motion, AnimatePresence } from 'framer-motion'
import { useState } from 'react'
import { Download, Maximize2, RotateCcw, Zap } from 'lucide-react'
import { GeneratedAsset } from '@/types/fibo'

interface AssetCanvasProps {
  asset: GeneratedAsset | null
  isGenerating: boolean
  onRegenerate?: () => void
  onDownload?: () => void
}

export function AssetCanvas({ asset, isGenerating, onRegenerate, onDownload }: AssetCanvasProps) {
  const [isFullscreen, setIsFullscreen] = useState(false)
  const [aspectRatio, setAspectRatio] = useState<'16:9' | '1:1' | '9:16' | 'free'>('free')

  const aspectRatios = [
    { value: 'free' as const, label: 'Free', ratio: null },
    { value: '16:9' as const, label: '16:9', ratio: 16/9 },
    { value: '1:1' as const, label: '1:1', ratio: 1 },
    { value: '9:16' as const, label: '9:16', ratio: 9/16 },
  ]

  const getCanvasStyle = () => {
    if (aspectRatio === 'free') return {}
    
    const ratio = aspectRatios.find(ar => ar.value === aspectRatio)?.ratio
    if (!ratio) return {}
    
    return {
      aspectRatio: ratio.toString(),
      maxWidth: '100%',
      maxHeight: '100%',
    }
  }

  const renderLoadingState = () => (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="flex flex-col items-center justify-center h-full text-studio-text-muted"
    >
      {/* Animated Loading Indicator */}
      <div className="relative mb-8">
        <div className="w-24 h-24 border-4 border-studio-border rounded-full"></div>
        <motion.div
          className="absolute inset-0 w-24 h-24 border-4 border-studio-cyan border-t-transparent rounded-full"
          animate={{ rotate: 360 }}
          transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
        />
        <div className="absolute inset-0 flex items-center justify-center">
          <Zap className="w-8 h-8 text-studio-cyan" />
        </div>
      </div>
      
      {/* Loading Text */}
      <div className="text-center space-y-2">
        <h3 className="text-lg font-semibold text-studio-text-primary">
          Generating Asset
        </h3>
        <p className="text-sm">
          FIBO is processing your configuration...
        </p>
        <div className="flex items-center justify-center space-x-1 mt-4">
          {[0, 1, 2].map((i) => (
            <motion.div
              key={i}
              className="w-2 h-2 bg-studio-cyan rounded-full"
              animate={{ 
                scale: [1, 1.2, 1],
                opacity: [0.5, 1, 0.5] 
              }}
              transition={{ 
                duration: 1.5, 
                repeat: Infinity,
                delay: i * 0.2 
              }}
            />
          ))}
        </div>
      </div>
    </motion.div>
  )

  const renderEmptyState = () => (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className="flex flex-col items-center justify-center h-full text-studio-text-muted"
    >
      <div className="w-32 h-32 rounded-full bg-studio-light border-2 border-dashed border-studio-border flex items-center justify-center mb-6">
        <div className="w-16 h-16 rounded-lg bg-studio-cyan/20 flex items-center justify-center">
          <div className="w-8 h-8 bg-studio-cyan rounded-sm opacity-60"></div>
        </div>
      </div>
      
      <h3 className="text-xl font-semibold text-studio-text-primary mb-2">
        No Asset Generated
      </h3>
      <p className="text-center text-studio-text-secondary max-w-md leading-relaxed">
        Configure your asset parameters in the control panel and click Generate to create your first asset.
      </p>
      
      <div className="mt-8 flex items-center space-x-4 text-xs text-studio-text-muted">
        <div className="flex items-center space-x-2">
          <div className="w-2 h-2 bg-studio-cyan rounded-full"></div>
          <span>JSON-Native Generation</span>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-2 h-2 bg-studio-amber rounded-full"></div>
          <span>Deterministic Output</span>
        </div>
      </div>
    </motion.div>
  )

  const renderAsset = () => (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.3, ease: 'easeOut' }}
      className="relative min-h-full flex items-center justify-center p-8"
    >
      <div 
        className="relative max-w-full max-h-full"
        style={getCanvasStyle()}
      >
        <img
          src={asset!.image_url}
          alt="Generated Asset"
          className="w-full h-full object-contain rounded-lg shadow-2xl"
          onError={(e) => {
            // Fallback to placeholder
            e.currentTarget.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjQwMCIgdmlld0JveD0iMCAwIDQwMCA0MDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSI0MDAiIGhlaWdodD0iNDAwIiBmaWxsPSIjMUExRDIzIi8+CjxjaXJjbGUgY3g9IjIwMCIgY3k9IjE4MCIgcj0iNDAiIGZpbGw9IiM0RUNEQUM0Ii8+CjxyZWN0IHg9IjE2MCIgeT0iMjQwIiB3aWR0aD0iODAiIGhlaWdodD0iNDAiIHJ4PSI4IiBmaWxsPSIjNEVDREE0Ii8+Cjx0ZXh0IHg9IjIwMCIgeT0iMzIwIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmaWxsPSIjQjhCQ0M4IiBmb250LWZhbWlseT0ibW9ub3NwYWNlIiBmb250LXNpemU9IjEyIj5Bc3NldCBQbGFjZWhvbGRlcjwvdGV4dD4KPC9zdmc+'
          }}
        />
        
        {/* Asset Overlay Controls */}
        <div className="absolute top-4 right-4 flex items-center space-x-2 opacity-0 hover:opacity-100 transition-opacity duration-200">
          <button
            onClick={() => setIsFullscreen(true)}
            className="p-2 bg-studio-dark/80 backdrop-blur-sm rounded-lg border border-studio-border hover:bg-studio-gray transition-colors"
          >
            <Maximize2 className="w-4 h-4 text-studio-text-primary" />
          </button>
          
          {onRegenerate && (
            <button
              onClick={onRegenerate}
              className="p-2 bg-studio-dark/80 backdrop-blur-sm rounded-lg border border-studio-border hover:bg-studio-gray transition-colors"
            >
              <RotateCcw className="w-4 h-4 text-studio-text-primary" />
            </button>
          )}
          
          {onDownload && (
            <button
              onClick={onDownload}
              className="p-2 bg-studio-cyan/90 backdrop-blur-sm rounded-lg border border-studio-cyan hover:bg-studio-cyan transition-colors"
            >
              <Download className="w-4 h-4 text-studio-dark" />
            </button>
          )}
        </div>
      </div>
      
      {/* Asset Metadata */}
      {asset && (
        <div className="absolute bottom-4 left-4 right-4">
          <div className="bg-studio-dark/90 backdrop-blur-sm rounded-lg border border-studio-border p-4">
            <div className="flex items-center justify-between">
              <div className="space-y-1">
                <div className="flex items-center space-x-3">
                  <span className="studio-badge studio-badge-info">
                    {asset.type.replace('_', ' ').toUpperCase()}
                  </span>
                  <span className="text-xs text-studio-text-muted font-mono">
                    {asset.metadata.dimensions.width} × {asset.metadata.dimensions.height}
                  </span>
                </div>
                <div className="flex items-center space-x-4 text-xs text-studio-text-muted">
                  <span>Generated in {asset.metadata.generation_time}s</span>
                  <span>{(asset.metadata.file_size / 1024).toFixed(1)}KB</span>
                  <span className="font-mono">{asset.id}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </motion.div>
  )

  return (
    <div className="flex-1 flex flex-col">
      {/* Canvas Controls */}
      <div className="flex items-center justify-between p-4 border-b border-studio-border bg-studio-gray/50">
        <div className="flex items-center space-x-4">
          <span className="studio-label">Aspect Ratio</span>
          <div className="flex items-center space-x-1 bg-studio-light rounded-lg p-1 border border-studio-border">
            {aspectRatios.map((ar) => (
              <button
                key={ar.value}
                onClick={() => setAspectRatio(ar.value)}
                className={`
                  px-3 py-1 rounded-md text-xs font-medium transition-all duration-200
                  ${aspectRatio === ar.value 
                    ? 'bg-studio-cyan text-studio-dark' 
                    : 'text-studio-text-secondary hover:text-studio-text-primary'
                  }
                `}
              >
                {ar.label}
              </button>
            ))}
          </div>
        </div>
        
        {asset && (
          <div className="flex items-center space-x-2">
            <span className="text-xs text-studio-text-muted">
              Last generated: {new Date(asset.created_at).toLocaleTimeString()}
            </span>
          </div>
        )}
      </div>

      {/* Main Canvas Area */}
      <div className="flex-1 studio-canvas relative overflow-auto">
        <AnimatePresence mode="wait">
          {isGenerating ? (
            <motion.div key="loading" className="absolute inset-0 flex items-center justify-center">
              {renderLoadingState()}
            </motion.div>
          ) : asset ? (
            <motion.div key="asset" className="min-h-full min-w-full">
              {renderAsset()}
            </motion.div>
          ) : (
            <motion.div key="empty" className="absolute inset-0 flex items-center justify-center">
              {renderEmptyState()}
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Fullscreen Modal */}
      <AnimatePresence>
        {isFullscreen && asset && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 bg-studio-dark/95 backdrop-blur-sm flex items-center justify-center p-8"
            onClick={() => setIsFullscreen(false)}
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              className="max-w-full max-h-full"
              onClick={(e) => e.stopPropagation()}
            >
              <img
                src={asset.image_url}
                alt="Generated Asset (Fullscreen)"
                className="max-w-full max-h-full object-contain rounded-lg shadow-2xl"
              />
            </motion.div>
            
            <button
              onClick={() => setIsFullscreen(false)}
              className="absolute top-8 right-8 p-3 bg-studio-gray rounded-lg border border-studio-border hover:bg-studio-light transition-colors"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}