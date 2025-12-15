'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { ChevronDown, AlertCircle, AlertTriangle } from 'lucide-react'

// Base control interface - every control implements this
interface BaseControlProps<T> {
  value: T
  onChange: (value: T) => void
  label: string
  description?: string
  disabled?: boolean
  error?: string
  warning?: string
  jsonPath: string // Exact JSON path this control maps to
}

// Validation status display
interface ValidationStatusProps {
  error?: string
  warning?: string
}

function ValidationStatus({ error, warning }: ValidationStatusProps) {
  if (error) {
    return (
      <div className="flex items-center space-x-1 text-red-400 text-xs mt-1">
        <AlertCircle className="w-3 h-3" />
        <span>{error}</span>
      </div>
    )
  }
  
  if (warning) {
    return (
      <div className="flex items-center space-x-1 text-studio-amber text-xs mt-1">
        <AlertTriangle className="w-3 h-3" />
        <span>{warning}</span>
      </div>
    )
  }
  
  return null
}

// Control wrapper with consistent styling and validation
interface ControlWrapperProps {
  label: string
  description?: string
  error?: string
  warning?: string
  jsonPath: string
  children: React.ReactNode
}

function ControlWrapper({ label, description, error, warning, jsonPath, children }: ControlWrapperProps) {
  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between">
        <label className="studio-label">
          {label}
        </label>
        <span className="text-xs font-mono text-studio-text-muted">
          {jsonPath}
        </span>
      </div>
      
      <div className={`
        ${error ? 'ring-2 ring-red-500/50' : ''}
        ${warning ? 'ring-2 ring-studio-amber/50' : ''}
      `}>
        {children}
      </div>
      
      {description && (
        <p className="text-xs text-studio-text-muted leading-relaxed">
          {description}
        </p>
      )}
      
      <ValidationStatus error={error} warning={warning} />
    </div>
  )
}

// Slider Control - Maps to numeric JSON fields
interface SliderControlProps extends BaseControlProps<number> {
  min: number
  max: number
  step: number
  formatDisplay?: (value: number) => string
  unit?: string
}

export function SliderControl({ 
  value, 
  onChange, 
  label, 
  description, 
  disabled, 
  error, 
  warning, 
  jsonPath,
  min, 
  max, 
  step, 
  formatDisplay,
  unit = ''
}: SliderControlProps) {
  const displayValue = formatDisplay ? formatDisplay(value) : `${value}${unit}`
  
  return (
    <ControlWrapper 
      label={label} 
      description={description} 
      error={error} 
      warning={warning}
      jsonPath={jsonPath}
    >
      <div className="flex items-center space-x-3">
        <input
          type="range"
          min={min}
          max={max}
          step={step}
          value={value}
          onChange={(e) => onChange(Number(e.target.value))}
          disabled={disabled}
          className="studio-slider flex-1"
        />
        <div className="w-16 text-right">
          <span className="font-mono text-numeric text-studio-text-secondary">
            {displayValue}
          </span>
        </div>
      </div>
    </ControlWrapper>
  )
}

// Segmented Control - Maps to enum JSON fields with 2-5 options
interface SegmentedOption<T> {
  value: T
  label: string
  icon?: React.ComponentType<{ className?: string }>
  color?: string
}

interface SegmentedControlProps<T> extends BaseControlProps<T> {
  options: SegmentedOption<T>[]
}

export function SegmentedControl<T extends string>({ 
  value, 
  onChange, 
  label, 
  description, 
  disabled, 
  error, 
  warning, 
  jsonPath,
  options 
}: SegmentedControlProps<T>) {
  return (
    <ControlWrapper 
      label={label} 
      description={description} 
      error={error} 
      warning={warning}
      jsonPath={jsonPath}
    >
      <div className="flex items-center space-x-1 bg-studio-light rounded-lg p-1 border border-studio-border">
        {options.map((option) => {
          const isActive = value === option.value
          const Icon = option.icon
          
          return (
            <motion.button
              key={String(option.value)}
              onClick={() => !disabled && onChange(option.value)}
              disabled={disabled}
              className={`
                relative flex-1 px-3 py-2 rounded-md text-xs font-medium transition-all duration-200
                ${isActive 
                  ? 'bg-studio-cyan text-studio-dark' 
                  : 'text-studio-text-secondary hover:text-studio-text-primary hover:bg-studio-border'
                }
                ${disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
              `}
              whileHover={!disabled ? { scale: 1.02 } : {}}
              whileTap={!disabled ? { scale: 0.98 } : {}}
              style={{ backgroundColor: isActive && option.color ? option.color : undefined }}
            >
              <div className="flex items-center justify-center space-x-1">
                {Icon && <Icon className="w-3 h-3" />}
                <span>{option.label}</span>
              </div>
              
              {isActive && (
                <motion.div
                  layoutId={`segmented-${jsonPath}`}
                  className="absolute inset-0 bg-studio-cyan rounded-md -z-10"
                  initial={false}
                  transition={{ type: "spring", stiffness: 500, damping: 30 }}
                />
              )}
            </motion.button>
          )
        })}
      </div>
    </ControlWrapper>
  )
}

// Dropdown Control - Maps to enum JSON fields with 5+ options
interface DropdownOption<T> {
  value: T
  label: string
  description?: string
  icon?: React.ComponentType<{ className?: string }>
  group?: string
}

interface DropdownControlProps<T> extends BaseControlProps<T> {
  options: DropdownOption<T>[]
  searchable?: boolean
  placeholder?: string
}

export function DropdownControl<T extends string>({ 
  value, 
  onChange, 
  label, 
  description, 
  disabled, 
  error, 
  warning, 
  jsonPath,
  options, 
  searchable = false,
  placeholder = "Select option..."
}: DropdownControlProps<T>) {
  const [isOpen, setIsOpen] = useState(false)
  const [searchTerm, setSearchTerm] = useState('')
  
  const filteredOptions = searchable 
    ? options.filter(option => 
        option.label.toLowerCase().includes(searchTerm.toLowerCase()) ||
        option.description?.toLowerCase().includes(searchTerm.toLowerCase())
      )
    : options
  
  const selectedOption = options.find(option => option.value === value)
  
  return (
    <ControlWrapper 
      label={label} 
      description={description} 
      error={error} 
      warning={warning}
      jsonPath={jsonPath}
    >
      <div className="relative">
        <button
          onClick={() => !disabled && setIsOpen(!isOpen)}
          disabled={disabled}
          className={`
            studio-select w-full flex items-center justify-between
            ${disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
          `}
        >
          <div className="flex items-center space-x-2">
            {selectedOption?.icon && (
              <selectedOption.icon className="w-4 h-4 text-studio-text-muted" />
            )}
            <span>
              {selectedOption?.label || placeholder}
            </span>
          </div>
          <ChevronDown className={`w-4 h-4 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
        </button>
        
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="absolute top-full left-0 right-0 z-50 mt-1 bg-studio-light border border-studio-border rounded-lg shadow-lg max-h-60 overflow-y-auto"
          >
            {searchable && (
              <div className="p-2 border-b border-studio-border">
                <input
                  type="text"
                  placeholder="Search options..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="studio-input w-full text-sm"
                  autoFocus
                />
              </div>
            )}
            
            <div className="py-1">
              {filteredOptions.map((option) => {
                const isSelected = option.value === value
                const Icon = option.icon
                
                return (
                  <button
                    key={String(option.value)}
                    onClick={() => {
                      onChange(option.value)
                      setIsOpen(false)
                      setSearchTerm('')
                    }}
                    className={`
                      w-full px-3 py-2 text-left flex items-center space-x-2 hover:bg-studio-border transition-colors
                      ${isSelected ? 'bg-studio-cyan/10 text-studio-cyan' : 'text-studio-text-primary'}
                    `}
                  >
                    {Icon && <Icon className="w-4 h-4" />}
                    <div>
                      <div className="font-medium">{option.label}</div>
                      {option.description && (
                        <div className="text-xs text-studio-text-muted">{option.description}</div>
                      )}
                    </div>
                  </button>
                )
              })}
              
              {filteredOptions.length === 0 && (
                <div className="px-3 py-2 text-studio-text-muted text-sm">
                  No options found
                </div>
              )}
            </div>
          </motion.div>
        )}
      </div>
      
      {/* Click outside to close */}
      {isOpen && (
        <div 
          className="fixed inset-0 z-40" 
          onClick={() => setIsOpen(false)}
        />
      )}
    </ControlWrapper>
  )
}

// Toggle Control - Maps to boolean-like enum fields (none/subtle/strong, etc.)
interface ToggleControlProps extends BaseControlProps<boolean> {
  size?: 'sm' | 'md' | 'lg'
}

export function ToggleControl({ 
  value, 
  onChange, 
  label, 
  description, 
  disabled, 
  error, 
  warning, 
  jsonPath,
  size = 'md'
}: ToggleControlProps) {
  const sizeClasses = {
    sm: 'h-4 w-7',
    md: 'h-6 w-11', 
    lg: 'h-8 w-14'
  }
  
  const thumbSizeClasses = {
    sm: 'h-3 w-3',
    md: 'h-4 w-4',
    lg: 'h-6 w-6'
  }
  
  return (
    <ControlWrapper 
      label={label} 
      description={description} 
      error={error} 
      warning={warning}
      jsonPath={jsonPath}
    >
      <button
        onClick={() => !disabled && onChange(!value)}
        disabled={disabled}
        className={`
          studio-toggle ${sizeClasses[size]}
          ${disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
        `}
        data-checked={value}
      >
        <span className={`studio-toggle-thumb ${thumbSizeClasses[size]}`} />
      </button>
    </ControlWrapper>
  )
}

// Read-only Label Control - Maps to computed or fixed JSON fields
interface LabelControlProps extends Omit<BaseControlProps<string>, 'onChange'> {
  copyable?: boolean
}

export function LabelControl({ 
  value, 
  label, 
  description, 
  jsonPath,
  copyable = false
}: LabelControlProps) {
  const handleCopy = async () => {
    if (copyable) {
      try {
        await navigator.clipboard.writeText(value)
      } catch (err) {
        console.error('Failed to copy:', err)
      }
    }
  }
  
  return (
    <ControlWrapper 
      label={label} 
      description={description}
      jsonPath={jsonPath}
    >
      <div 
        className={`
          studio-input bg-studio-dark text-studio-text-muted font-mono cursor-default
          ${copyable ? 'cursor-pointer hover:bg-studio-light' : ''}
        `}
        onClick={copyable ? handleCopy : undefined}
        title={copyable ? 'Click to copy' : undefined}
      >
        {value}
      </div>
    </ControlWrapper>
  )
}