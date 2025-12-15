'use client'

import { motion, AnimatePresence } from 'framer-motion'
import { ChevronDown } from 'lucide-react'
import { useState } from 'react'

interface ControlSectionProps {
  title: string
  children: React.ReactNode
  defaultExpanded?: boolean
  icon?: React.ComponentType<{ className?: string }>
}

export function ControlSection({ title, children, defaultExpanded = true, icon: Icon }: ControlSectionProps) {
  const [isExpanded, setIsExpanded] = useState(defaultExpanded)

  return (
    <div className="studio-section">
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full flex items-center justify-between text-left group"
      >
        <div className="flex items-center space-x-2">
          {Icon && <Icon className="w-4 h-4 text-studio-text-muted" />}
          <h3 className="studio-section-title">{title}</h3>
        </div>
        <motion.div
          animate={{ rotate: isExpanded ? 0 : -90 }}
          transition={{ duration: 0.2 }}
          className="text-studio-text-muted group-hover:text-studio-text-secondary"
        >
          <ChevronDown className="w-4 h-4" />
        </motion.div>
      </button>
      
      <AnimatePresence>
        {isExpanded && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.2, ease: 'easeOut' }}
            className="overflow-hidden"
          >
            <div className="pt-3 space-y-4">
              {children}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

import { NPCPortraitControls } from './controls/NPCPortraitControls'
import { WeaponItemControls } from './controls/WeaponItemControls'
import { EnvironmentControls } from './controls/EnvironmentControls'
import { AssetConfig } from '@/types/fibo'
import { ToggleControl } from './controls/BaseControls'
import { SliderControl } from './controls/BaseControls'
import { ValidationResponse } from '@/services/api'

interface ControlPanelProps {
  assetType: 'npc_portrait' | 'weapon_item' | 'environment_concept'
  config: Partial<AssetConfig> | null
  validationResult: ValidationResponse | null
  isValidating: boolean
  onConfigChange: (path: string, value: any) => void
  onGenerate: () => void
  isGenerating: boolean
}

export function ControlPanel({ 
  assetType, 
  config, 
  validationResult, 
  isValidating, 
  onConfigChange, 
  onGenerate, 
  isGenerating 
}: ControlPanelProps) {
  // Extract errors and warnings from validation result
  const errors = validationResult?.errors || []
  const warnings = validationResult?.warnings || []
  
  // Convert errors array to record for field-specific errors
  const fieldErrors: Record<string, string> = {}
  errors.forEach(error => {
    // Parse field path from error message (simple implementation)
    const match = error.match(/^([^:]+):/)
    if (match) {
      fieldErrors[match[1]] = error
    }
  })
  
  const fieldWarnings: Record<string, string> = {}
  warnings.forEach(warning => {
    // Parse field path from warning message (simple implementation)
    const match = warning.match(/^([^:]+):/)
    if (match) {
      fieldWarnings[match[1]] = warning
    }
  })

  const renderControls = () => {
    switch (assetType) {
      case 'npc_portrait':
        return (
          <NPCPortraitControls
            config={config as any}
            onChange={onConfigChange}
            errors={fieldErrors}
            warnings={fieldWarnings}
          />
        )
      case 'weapon_item':
        return (
          <WeaponItemControls
            config={config as any}
            onChange={onConfigChange}
            errors={fieldErrors}
            warnings={fieldWarnings}
          />
        )
      case 'environment_concept':
        return (
          <EnvironmentControls
            config={config as any}
            onChange={onConfigChange}
            errors={fieldErrors}
            warnings={fieldWarnings}
          />
        )
    }
  }

  return (
    <div className="w-80 bg-studio-gray border-r border-studio-border h-full flex flex-col">
      <div className="flex-1 overflow-y-auto scroll-container">
        <div className="p-6 space-y-6">
        {renderControls()}
        
        {/* Validation Status */}
        {isValidating && (
          <div className="flex items-center space-x-2 text-studio-text-muted text-sm">
            <div className="w-3 h-3 border-2 border-studio-cyan border-t-transparent rounded-full animate-spin" />
            <span>Validating configuration...</span>
          </div>
        )}
        
        {validationResult && !validationResult.success && (
          <div className="bg-red-500/10 border border-red-500/20 rounded-lg p-3">
            <h4 className="text-red-400 font-medium text-sm mb-2">Validation Errors</h4>
            <ul className="text-red-300 text-xs space-y-1">
              {errors.map((error, index) => (
                <li key={index}>• {error}</li>
              ))}
            </ul>
          </div>
        )}
        
        {validationResult && validationResult.success && warnings.length > 0 && (
          <div className="bg-amber-500/10 border border-amber-500/20 rounded-lg p-3">
            <h4 className="text-amber-400 font-medium text-sm mb-2">Warnings</h4>
            <ul className="text-amber-300 text-xs space-y-1">
              {warnings.map((warning, index) => (
                <li key={index}>• {warning}</li>
              ))}
            </ul>
          </div>
        )}

        {/* Generate Button */}
        <div className="pt-6 border-t border-studio-border">
          <motion.button
            onClick={onGenerate}
            disabled={isGenerating || !validationResult?.success}
            className={`
              w-full studio-button-primary py-4 text-base font-semibold
              ${(isGenerating || !validationResult?.success) ? 'opacity-50 cursor-not-allowed' : ''}
            `}
            whileHover={(!isGenerating && validationResult?.success) ? { scale: 1.02 } : {}}
            whileTap={(!isGenerating && validationResult?.success) ? { scale: 0.98 } : {}}
          >
            {isGenerating ? (
              <div className="flex items-center justify-center space-x-2">
                <div className="w-4 h-4 border-2 border-studio-dark border-t-transparent rounded-full animate-spin" />
                <span>Generating...</span>
              </div>
            ) : !validationResult?.success ? (
              'Fix Validation Errors'
            ) : (
              'Generate Asset'
            )}
          </motion.button>
          </div>
        </div>
      </div>
    </div>
  )
}

// Export individual control components for reuse
export { SliderControl, ToggleControl }