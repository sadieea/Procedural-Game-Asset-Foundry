'use client'

import { motion } from 'framer-motion'
import { Download, FileJson, Wifi, WifiOff, AlertCircle } from 'lucide-react'


interface TopBarProps {
  activeAssetType: 'npc_portrait' | 'weapon_item' | 'environment_concept'
  onAssetTypeChange: (type: 'npc_portrait' | 'weapon_item' | 'environment_concept') => void
  connectionStatus: 'connected' | 'disconnected' | 'error'
  onExportPNG: () => void
  onExportJSON: () => void
}

const assetModes = [
  { id: 'npc_portrait' as const, label: 'NPC Portraits' },
  { id: 'weapon_item' as const, label: 'Weapons & Items' },
  { id: 'environment_concept' as const, label: 'Environments' },
]

export function TopBar({ 
  activeAssetType, 
  onAssetTypeChange, 
  connectionStatus,
  onExportPNG,
  onExportJSON 
}: TopBarProps) {
  const getStatusIcon = () => {
    switch (connectionStatus) {
      case 'connected':
        return <Wifi className="w-4 h-4 text-green-400" />
      case 'disconnected':
        return <WifiOff className="w-4 h-4 text-studio-text-muted" />
      case 'error':
        return <AlertCircle className="w-4 h-4 text-red-400" />
    }
  }

  const getStatusText = () => {
    switch (connectionStatus) {
      case 'connected':
        return 'FIBO Connected'
      case 'disconnected':
        return 'Disconnected'
      case 'error':
        return 'Connection Error'
    }
  }

  const getStatusBadgeClass = () => {
    switch (connectionStatus) {
      case 'connected':
        return 'studio-badge-success'
      case 'disconnected':
        return 'studio-badge-info'
      case 'error':
        return 'studio-badge-error'
    }
  }

  return (
    <div className="h-16 bg-studio-dark/95 backdrop-blur-studio border-b border-studio-border flex items-center justify-between px-6 relative z-50">
      {/* Left: Logo & Title */}
      <div className="flex items-center space-x-4">
        <div className="w-8 h-8 bg-studio-cyan rounded-lg flex items-center justify-center">
          <div className="w-4 h-4 bg-studio-dark rounded-sm"></div>
        </div>
        <div>
          <h1 className="text-studio-text-primary font-semibold text-lg leading-none">
            Procedural Game Asset Foundry
          </h1>
          <p className="text-studio-text-muted text-xs uppercase tracking-wide mt-0.5">
            JSON-Native Visual Asset Generator
          </p>
        </div>
      </div>

      {/* Center: Asset Mode Tabs */}
      <div className="flex items-center space-x-1 bg-studio-gray rounded-lg p-1 border border-studio-border">
        {assetModes.map((mode) => {
          const isActive = activeAssetType === mode.id
          
          return (
            <motion.button
              key={mode.id}
              onClick={() => onAssetTypeChange(mode.id)}
              className={`
                relative px-4 py-2 rounded-md text-sm font-medium transition-all duration-200
                ${isActive 
                  ? 'text-studio-text-primary' 
                  : 'text-studio-text-secondary hover:text-studio-text-primary'
                }
              `}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              {isActive && (
                <motion.div
                  layoutId="activeAssetTab"
                  className="absolute inset-0 bg-studio-light rounded-md border border-studio-border"
                  initial={false}
                  transition={{ type: "spring", stiffness: 500, damping: 30 }}
                />
              )}
              
              <span className="relative z-10">{mode.label}</span>
            </motion.button>
          )
        })}
      </div>

      {/* Right: Export & Status */}
      <div className="flex items-center space-x-4">
        {/* Export Buttons */}
        <div className="flex items-center space-x-2">
          <button
            onClick={onExportPNG}
            className="studio-button flex items-center space-x-2"
          >
            <Download className="w-4 h-4" />
            <span>Export PNG</span>
          </button>
          
          <button
            onClick={onExportJSON}
            className="studio-button flex items-center space-x-2"
          >
            <FileJson className="w-4 h-4" />
            <span>Export JSON</span>
          </button>
        </div>

        {/* Connection Status */}
        <div className={`studio-badge ${getStatusBadgeClass()} flex items-center space-x-2`}>
          {getStatusIcon()}
          <span className="text-xs font-mono uppercase tracking-wide">
            {getStatusText()}
          </span>
        </div>
      </div>
    </div>
  )
}