'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Copy, Download, RotateCcw, Eye, EyeOff } from 'lucide-react'
import { AssetConfig } from '@/types/fibo'
import { ValidationResponse } from '@/services/api'

interface JSONInspectorProps {
  config: Partial<AssetConfig> | null
  validationResult?: ValidationResponse | null
  onConfigRestore?: (config: AssetConfig) => void
}

export function JSONInspector({ config, validationResult, onConfigRestore }: JSONInspectorProps) {
  const [isExpanded, setIsExpanded] = useState(true)
  const [copySuccess, setCopySuccess] = useState(false)
  const [formattedJSON, setFormattedJSON] = useState<string>('')

  useEffect(() => {
    if (config) {
      setFormattedJSON(JSON.stringify(config, null, 2))
    } else {
      setFormattedJSON('{\n  // No configuration loaded\n  // Adjust parameters to see JSON output\n}')
    }
  }, [config])

  const handleCopy = async () => {
    if (!config) return
    
    try {
      await navigator.clipboard.writeText(formattedJSON)
      setCopySuccess(true)
      setTimeout(() => setCopySuccess(false), 2000)
    } catch (err) {
      console.error('Failed to copy JSON:', err)
    }
  }

  const handleDownload = () => {
    if (!config) return
    
    const blob = new Blob([formattedJSON], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `asset-config-${config.assetType}-${Date.now()}.json`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  const handleRestore = () => {
    if (config && onConfigRestore) {
      onConfigRestore(config as AssetConfig)
    }
  }

  // Syntax highlighting for JSON
  const highlightJSON = (json: string) => {
    return json
      .replace(/(".*?")\s*:/g, '<span class="json-key">$1</span>:')
      .replace(/:\s*(".*?")/g, ': <span class="json-string">$1</span>')
      .replace(/:\s*(\d+\.?\d*)/g, ': <span class="json-number">$1</span>')
      .replace(/:\s*(true|false)/g, ': <span class="json-boolean">$1</span>')
  }

  return (
    <div className="h-full flex flex-col bg-studio-gray border-l border-studio-border">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-studio-border bg-studio-light/50">
        <div className="flex items-center space-x-3">
          <h3 className="studio-section-title">JSON Inspector</h3>
          <div className="studio-badge studio-badge-info">
            FIBO Schema
          </div>
        </div>
        
        <div className="flex items-center space-x-2">
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="p-1.5 rounded-md hover:bg-studio-border transition-colors"
            title={isExpanded ? 'Collapse' : 'Expand'}
          >
            {isExpanded ? (
              <EyeOff className="w-4 h-4 text-studio-text-muted" />
            ) : (
              <Eye className="w-4 h-4 text-studio-text-muted" />
            )}
          </button>
        </div>
      </div>

      {/* JSON Content */}
      <motion.div
        animate={{ height: isExpanded ? 'auto' : '0' }}
        className="flex-1 overflow-hidden"
      >
        <div className="h-full flex flex-col">
          {/* Controls */}
          <div className="flex items-center justify-between p-3 border-b border-studio-border bg-studio-dark/30">
            <div className="flex items-center space-x-2">
              <span className="text-xs text-studio-text-muted font-mono">
                {config ? `${config.assetType}.json` : 'config.json'}
              </span>
              {config && (
                <span className="text-xs text-studio-text-muted">
                  {formattedJSON.split('\n').length} lines
                </span>
              )}
            </div>
            
            <div className="flex items-center space-x-1">
              <button
                onClick={handleCopy}
                disabled={!config}
                className={`
                  p-1.5 rounded-md transition-all duration-200 text-xs
                  ${config 
                    ? 'hover:bg-studio-border text-studio-text-secondary hover:text-studio-text-primary' 
                    : 'text-studio-text-muted cursor-not-allowed'
                  }
                  ${copySuccess ? 'text-green-400' : ''}
                `}
                title="Copy JSON"
              >
                <Copy className="w-3.5 h-3.5" />
              </button>
              
              <button
                onClick={handleDownload}
                disabled={!config}
                className={`
                  p-1.5 rounded-md transition-all duration-200 text-xs
                  ${config 
                    ? 'hover:bg-studio-border text-studio-text-secondary hover:text-studio-text-primary' 
                    : 'text-studio-text-muted cursor-not-allowed'
                  }
                `}
                title="Download JSON"
              >
                <Download className="w-3.5 h-3.5" />
              </button>
              
              {onConfigRestore && (
                <button
                  onClick={handleRestore}
                  disabled={!config}
                  className={`
                    p-1.5 rounded-md transition-all duration-200 text-xs
                    ${config 
                      ? 'hover:bg-studio-border text-studio-text-secondary hover:text-studio-text-primary' 
                      : 'text-studio-text-muted cursor-not-allowed'
                    }
                  `}
                  title="Restore Configuration"
                >
                  <RotateCcw className="w-3.5 h-3.5" />
                </button>
              )}
            </div>
          </div>

          {/* JSON Display */}
          <div className="flex-1 overflow-auto min-h-0">
            <div className="studio-json">
              <pre 
                className="text-xs leading-relaxed whitespace-pre-wrap break-words p-4 min-h-full"
                dangerouslySetInnerHTML={{ 
                  __html: highlightJSON(formattedJSON) 
                }}
              />
            </div>
          </div>

          {/* Footer Info */}
          {config && (
            <div className="p-3 border-t border-studio-border bg-studio-dark/30">
              <div className="flex items-center justify-between text-xs">
                <div className="flex items-center space-x-4 text-studio-text-muted">
                  <span>Type: {config.assetType}</span>
                  <span>Resolution: {config.output?.resolution || 'Not set'}</span>
                  {config.seed && <span>Seed: {config.seed}</span>}
                </div>
                
                <div className="flex items-center space-x-2">
                  {validationResult ? (
                    <>
                      <div className={`w-2 h-2 rounded-full ${
                        validationResult.success ? 'bg-green-400' : 'bg-red-400'
                      }`}></div>
                      <span className="text-studio-text-muted">
                        {validationResult.success ? 'Valid Schema' : 'Invalid Schema'}
                      </span>
                    </>
                  ) : (
                    <>
                      <div className="w-2 h-2 bg-amber-400 rounded-full"></div>
                      <span className="text-studio-text-muted">Not Validated</span>
                    </>
                  )}
                </div>
              </div>
            </div>
          )}
        </div>
      </motion.div>

      {/* Copy Success Notification */}
      {copySuccess && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: 10 }}
          className="absolute top-16 right-4 bg-green-500/90 text-white px-3 py-2 rounded-lg text-xs font-medium shadow-lg"
        >
          JSON copied to clipboard!
        </motion.div>
      )}
    </div>
  )
}