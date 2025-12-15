'use client'

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Clock, Download, RotateCcw, Trash2, Eye } from 'lucide-react'
import { GeneratedAsset } from '@/types/fibo'

interface AssetHistoryProps {
  assets: GeneratedAsset[]
  onAssetSelect?: (asset: GeneratedAsset) => void
  onAssetRestore?: (asset: GeneratedAsset) => void
  onAssetDelete?: (assetId: string) => void
}

export function AssetHistory({ 
  assets, 
  onAssetSelect, 
  onAssetRestore, 
  onAssetDelete 
}: AssetHistoryProps) {
  const [selectedAsset, setSelectedAsset] = useState<string | null>(null)
  const [hoveredAsset, setHoveredAsset] = useState<string | null>(null)

  const handleAssetClick = (asset: GeneratedAsset) => {
    setSelectedAsset(asset.id)
    onAssetSelect?.(asset)
  }

  const handleRestore = (asset: GeneratedAsset, e: React.MouseEvent) => {
    e.stopPropagation()
    onAssetRestore?.(asset)
  }

  const handleDelete = (assetId: string, e: React.MouseEvent) => {
    e.stopPropagation()
    onAssetDelete?.(assetId)
  }

  const handleDownload = (asset: GeneratedAsset, e: React.MouseEvent) => {
    e.stopPropagation()
    // Create download link
    const link = document.createElement('a')
    link.href = asset.image_url
    link.download = `${asset.type}-${asset.id}.${asset.metadata.format}`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }

  const getAssetTypeColor = (type: string) => {
    switch (type) {
      case 'npc_portrait':
        return 'bg-blue-500/10 text-blue-400 border-blue-500/20'
      case 'weapon_item':
        return 'bg-studio-amber/10 text-studio-amber border-studio-amber/20'
      case 'environment':
        return 'bg-green-500/10 text-green-400 border-green-500/20'
      default:
        return 'bg-studio-cyan/10 text-studio-cyan border-studio-cyan/20'
    }
  }

  const formatTimeAgo = (dateString: string) => {
    const now = new Date()
    const created = new Date(dateString)
    const diffMs = now.getTime() - created.getTime()
    const diffMins = Math.floor(diffMs / 60000)
    
    if (diffMins < 1) return 'Just now'
    if (diffMins < 60) return `${diffMins}m ago`
    
    const diffHours = Math.floor(diffMins / 60)
    if (diffHours < 24) return `${diffHours}h ago`
    
    const diffDays = Math.floor(diffHours / 24)
    return `${diffDays}d ago`
  }

  return (
    <div className="h-full flex flex-col bg-studio-gray">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-studio-border">
        <div className="flex items-center space-x-3">
          <Clock className="w-4 h-4 text-studio-text-muted" />
          <h3 className="studio-section-title">Asset History</h3>
          <div className="studio-badge studio-badge-info">
            {assets.length}
          </div>
        </div>
      </div>

      {/* Asset List */}
      <div className="flex-1 overflow-y-auto">
        {assets.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full p-6 text-center">
            <div className="w-16 h-16 rounded-full bg-studio-light border-2 border-dashed border-studio-border flex items-center justify-center mb-4">
              <Clock className="w-6 h-6 text-studio-text-muted" />
            </div>
            <p className="text-studio-text-muted text-sm">
              No assets generated yet
            </p>
            <p className="text-xs text-studio-text-muted mt-1">
              Generated assets will appear here
            </p>
          </div>
        ) : (
          <div className="p-3 space-y-2">
            <AnimatePresence>
              {assets.map((asset, index) => (
                <motion.div
                  key={asset.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  transition={{ delay: index * 0.05 }}
                  className={`
                    group relative p-3 rounded-lg border cursor-pointer transition-all duration-200
                    ${selectedAsset === asset.id 
                      ? 'bg-studio-light border-studio-cyan/50 shadow-lg shadow-studio-cyan/10' 
                      : 'bg-studio-dark border-studio-border hover:border-studio-border/60 hover:bg-studio-light/50'
                    }
                  `}
                  onClick={() => handleAssetClick(asset)}
                  onMouseEnter={() => setHoveredAsset(asset.id)}
                  onMouseLeave={() => setHoveredAsset(null)}
                >
                  <div className="flex items-start space-x-3">
                    {/* Thumbnail */}
                    <div className="relative flex-shrink-0">
                      <div className="w-12 h-12 rounded-lg overflow-hidden bg-studio-gray border border-studio-border">
                        <img
                          src={asset.thumbnail_url || asset.image_url}
                          alt={`${asset.type} thumbnail`}
                          className="w-full h-full object-cover"
                          onError={(e) => {
                            // Fallback to type-based placeholder
                            const canvas = document.createElement('canvas')
                            canvas.width = 48
                            canvas.height = 48
                            const ctx = canvas.getContext('2d')
                            if (ctx) {
                              ctx.fillStyle = '#2A2D35'
                              ctx.fillRect(0, 0, 48, 48)
                              ctx.fillStyle = '#4ECDC4'
                              ctx.fillRect(12, 12, 24, 24)
                            }
                            e.currentTarget.src = canvas.toDataURL()
                          }}
                        />
                      </div>
                      
                      {/* Type Badge */}
                      <div className={`
                        absolute -top-1 -right-1 px-1.5 py-0.5 rounded text-xs font-medium border
                        ${getAssetTypeColor(asset.type)}
                      `}>
                        {asset.type === 'npc_portrait' ? 'NPC' : 
                         asset.type === 'weapon_item' ? 'ITEM' : 'ENV'}
                      </div>
                    </div>

                    {/* Content */}
                    <div className="flex-1 min-w-0">
                      <div className="flex items-start justify-between">
                        <div className="min-w-0 flex-1">
                          <p className="text-sm font-medium text-studio-text-primary truncate">
                            {asset.type.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                          </p>
                          <p className="text-xs text-studio-text-muted font-mono mt-0.5">
                            {asset.metadata.dimensions.width}×{asset.metadata.dimensions.height}
                          </p>
                        </div>
                        
                        <div className="text-right">
                          <p className="text-xs text-studio-text-muted">
                            {formatTimeAgo(asset.created_at)}
                          </p>
                          <p className="text-xs text-studio-text-muted mt-0.5">
                            {(asset.metadata.file_size / 1024).toFixed(1)}KB
                          </p>
                        </div>
                      </div>

                      {/* Metadata */}
                      <div className="flex items-center space-x-2 mt-2">
                        <span className="text-xs text-studio-text-muted font-mono">
                          {asset.id.slice(-8)}
                        </span>
                        <span className="text-xs text-studio-text-muted">
                          {asset.metadata.generation_time}s
                        </span>
                      </div>
                    </div>
                  </div>

                  {/* Action Buttons */}
                  <AnimatePresence>
                    {(hoveredAsset === asset.id || selectedAsset === asset.id) && (
                      <motion.div
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={{ opacity: 1, scale: 1 }}
                        exit={{ opacity: 0, scale: 0.9 }}
                        className="absolute top-2 right-2 flex items-center space-x-1"
                      >
                        <button
                          onClick={(e) => handleAssetClick(asset)}
                          className="p-1.5 bg-studio-dark/80 backdrop-blur-sm rounded-md border border-studio-border hover:bg-studio-gray transition-colors"
                          title="View Asset"
                        >
                          <Eye className="w-3 h-3 text-studio-text-secondary" />
                        </button>
                        
                        {onAssetRestore && (
                          <button
                            onClick={(e) => handleRestore(asset, e)}
                            className="p-1.5 bg-studio-dark/80 backdrop-blur-sm rounded-md border border-studio-border hover:bg-studio-gray transition-colors"
                            title="Restore Configuration"
                          >
                            <RotateCcw className="w-3 h-3 text-studio-text-secondary" />
                          </button>
                        )}
                        
                        <button
                          onClick={(e) => handleDownload(asset, e)}
                          className="p-1.5 bg-studio-cyan/80 backdrop-blur-sm rounded-md border border-studio-cyan hover:bg-studio-cyan transition-colors"
                          title="Download Asset"
                        >
                          <Download className="w-3 h-3 text-studio-dark" />
                        </button>
                        
                        {onAssetDelete && (
                          <button
                            onClick={(e) => handleDelete(asset.id, e)}
                            className="p-1.5 bg-red-500/80 backdrop-blur-sm rounded-md border border-red-500 hover:bg-red-500 transition-colors"
                            title="Delete Asset"
                          >
                            <Trash2 className="w-3 h-3 text-white" />
                          </button>
                        )}
                      </motion.div>
                    )}
                  </AnimatePresence>
                </motion.div>
              ))}
            </AnimatePresence>
          </div>
        )}
      </div>

      {/* Footer Stats */}
      {assets.length > 0 && (
        <div className="p-3 border-t border-studio-border bg-studio-dark/30">
          <div className="flex items-center justify-between text-xs text-studio-text-muted">
            <span>{assets.length} assets generated</span>
            <span>
              {(assets.reduce((sum, asset) => sum + asset.metadata.file_size, 0) / 1024 / 1024).toFixed(1)}MB total
            </span>
          </div>
        </div>
      )}
    </div>
  )
}