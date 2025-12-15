'use client'

import { Sword, Box, Sparkles, Camera, Lightbulb, Image } from 'lucide-react'
import { SliderControl, SegmentedControl, DropdownControl } from './BaseControls'
import { ControlSection } from '../ControlPanel'
import { WeaponItemConfig } from '@/types/fibo'

interface WeaponItemControlsProps {
  config: Partial<WeaponItemConfig>
  onChange: (path: string, value: any) => void
  errors?: Record<string, string>
  warnings?: Record<string, string>
}

export function WeaponItemControls({ config, onChange, errors, warnings }: WeaponItemControlsProps) {
  // Helper to get nested values safely
  const getValue = (path: string, defaultValue: any) => {
    const keys = path.split('.')
    let current: any = config
    for (const key of keys) {
      if (current?.[key] === undefined) return defaultValue
      current = current[key]
    }
    return current
  }

  // Rarity color mapping for visual feedback
  const getRarityColor = (rarity: string) => {
    const colors = {
      common: '#9CA3AF',
      uncommon: '#10B981', 
      rare: '#3B82F6',
      epic: '#8B5CF6',
      legendary: '#F59E0B',
      artifact: '#EF4444',
      unique: '#EC4899'
    }
    return colors[rarity as keyof typeof colors] || colors.common
  }

  return (
    <div className="space-y-6">
      {/* Item Identity Section */}
      <ControlSection title="Item Identity" icon={Sword} defaultExpanded>
        <DropdownControl
          value={getValue('item.category', 'sword')}
          onChange={(value) => onChange('item.category', value)}
          label="Item Category"
          description="Base item type determining form and function"
          jsonPath="item.category"
          error={errors?.['item.category']}
          warning={warnings?.['item.category']}
          options={[
            { value: 'sword', label: 'Sword', description: 'Bladed melee weapon' },
            { value: 'axe', label: 'Axe', description: 'Heavy chopping weapon' },
            { value: 'bow', label: 'Bow', description: 'Ranged projectile weapon' },
            { value: 'staff', label: 'Staff', description: 'Magical focus weapon' },
            { value: 'dagger', label: 'Dagger', description: 'Light piercing weapon' },
            { value: 'hammer', label: 'Hammer', description: 'Blunt crushing weapon' },
            { value: 'gun', label: 'Gun', description: 'Firearm or energy weapon' },
            { value: 'potion', label: 'Potion', description: 'Consumable liquid item' },
            { value: 'artifact', label: 'Artifact', description: 'Unique magical item' },
            { value: 'shield', label: 'Shield', description: 'Defensive equipment' },
            { value: 'armor', label: 'Armor', description: 'Protective gear' },
            { value: 'accessory', label: 'Accessory', description: 'Jewelry or trinket' }
          ]}
        />

        <SegmentedControl
          value={getValue('item.rarity', 'common')}
          onChange={(value) => onChange('item.rarity', value)}
          label="Rarity Level"
          description="Item rarity affecting visual complexity and effects"
          jsonPath="item.rarity"
          error={errors?.['item.rarity']}
          warning={warnings?.['item.rarity']}
          options={[
            { value: 'common', label: 'Common', color: getRarityColor('common') },
            { value: 'uncommon', label: 'Uncommon', color: getRarityColor('uncommon') },
            { value: 'rare', label: 'Rare', color: getRarityColor('rare') },
            { value: 'epic', label: 'Epic', color: getRarityColor('epic') },
            { value: 'legendary', label: 'Legendary', color: getRarityColor('legendary') },
            { value: 'artifact', label: 'Artifact', color: getRarityColor('artifact') },
            { value: 'unique', label: 'Unique', color: getRarityColor('unique') }
          ]}
        />

        <DropdownControl
          value={getValue('item.material', 'steel')}
          onChange={(value) => onChange('item.material', value)}
          label="Primary Material"
          description="Base material affecting surface properties and appearance"
          jsonPath="item.material"
          error={errors?.['item.material']}
          warning={warnings?.['item.material']}
          searchable
          options={[
            { value: 'steel', label: 'Steel', description: 'Durable metal alloy', group: 'Metals' },
            { value: 'iron', label: 'Iron', description: 'Basic metal material', group: 'Metals' },
            { value: 'bronze', label: 'Bronze', description: 'Ancient metal alloy', group: 'Metals' },
            { value: 'silver', label: 'Silver', description: 'Precious metal', group: 'Metals' },
            { value: 'gold', label: 'Gold', description: 'Valuable precious metal', group: 'Metals' },
            { value: 'crystal', label: 'Crystal', description: 'Magical crystalline material', group: 'Magical' },
            { value: 'wood', label: 'Wood', description: 'Natural organic material', group: 'Natural' },
            { value: 'bone', label: 'Bone', description: 'Carved skeletal material', group: 'Natural' },
            { value: 'obsidian', label: 'Obsidian', description: 'Volcanic glass', group: 'Natural' },
            { value: 'mithril', label: 'Mithril', description: 'Legendary light metal', group: 'Legendary' },
            { value: 'adamantine', label: 'Adamantine', description: 'Indestructible metal', group: 'Legendary' },
            { value: 'ethereal', label: 'Ethereal', description: 'Otherworldly substance', group: 'Magical' }
          ]}
        />

        <SegmentedControl
          value={getValue('item.styleTheme', 'fantasy')}
          onChange={(value) => onChange('item.styleTheme', value)}
          label="Style Theme"
          description="Cultural and technological aesthetic"
          jsonPath="item.styleTheme"
          error={errors?.['item.styleTheme']}
          warning={warnings?.['item.styleTheme']}
          options={[
            { value: 'fantasy', label: 'Fantasy' },
            { value: 'sci_fi', label: 'Sci-Fi' },
            { value: 'modern', label: 'Modern' },
            { value: 'steampunk', label: 'Steampunk' },
            { value: 'medieval', label: 'Medieval' },
            { value: 'ancient', label: 'Ancient' },
            { value: 'tribal', label: 'Tribal' },
            { value: 'elven', label: 'Elven' },
            { value: 'dwarven', label: 'Dwarven' },
            { value: 'orcish', label: 'Orcish' }
          ]}
        />
      </ControlSection>

      {/* Form & Shape Section */}
      <ControlSection title="Form & Shape" icon={Box} defaultExpanded>
        <SliderControl
          value={getValue('form.length', 0.6)}
          onChange={(value) => onChange('form.length', value)}
          label="Item Length"
          description="Overall length scale: 0.1=dagger size, 1.0=greatsword size"
          jsonPath="form.length"
          error={errors?.['form.length']}
          warning={warnings?.['form.length']}
          min={0.1}
          max={1.0}
          step={0.01}
        />

        <SliderControl
          value={getValue('form.thickness', 0.4)}
          onChange={(value) => onChange('form.thickness', value)}
          label="Item Thickness"
          description="Cross-sectional thickness: 0.1=thin and delicate, 1.0=thick and bulky"
          jsonPath="form.thickness"
          error={errors?.['form.thickness']}
          warning={warnings?.['form.thickness']}
          min={0.1}
          max={1.0}
          step={0.01}
        />

        <SegmentedControl
          value={getValue('form.symmetry', 'symmetrical')}
          onChange={(value) => onChange('form.symmetry', value)}
          label="Form Symmetry"
          description="Overall shape symmetry and balance"
          jsonPath="form.symmetry"
          error={errors?.['form.symmetry']}
          warning={warnings?.['form.symmetry']}
          options={[
            { value: 'symmetrical', label: 'Symmetrical' },
            { value: 'asymmetrical', label: 'Asymmetrical' },
            { value: 'curved', label: 'Curved' },
            { value: 'twisted', label: 'Twisted' }
          ]}
        />

        <SliderControl
          value={getValue('form.ornamentation', 0.5)}
          onChange={(value) => onChange('form.ornamentation', value)}
          label="Ornamentation"
          description="Decorative detail level: 0.0=plain and functional, 1.0=highly ornate"
          jsonPath="form.ornamentation"
          error={errors?.['form.ornamentation']}
          warning={warnings?.['form.ornamentation']}
          min={0.0}
          max={1.0}
          step={0.01}
        />
      </ControlSection>

      {/* Surface Details Section */}
      <ControlSection title="Surface Details" icon={Sparkles} defaultExpanded>
        <SliderControl
          value={getValue('surface.wearLevel', 0.3)}
          onChange={(value) => onChange('surface.wearLevel', value)}
          label="Wear Level"
          description="Age and usage wear: 0.0=pristine condition, 1.0=heavily worn"
          jsonPath="surface.wearLevel"
          error={errors?.['surface.wearLevel']}
          warning={warnings?.['surface.wearLevel']}
          min={0.0}
          max={1.0}
          step={0.01}
        />

        <SegmentedControl
          value={getValue('surface.scratches', 'light')}
          onChange={(value) => onChange('surface.scratches', value)}
          label="Surface Scratches"
          description="Scratch pattern and intensity"
          jsonPath="surface.scratches"
          error={errors?.['surface.scratches']}
          warning={warnings?.['surface.scratches']}
          options={[
            { value: 'none', label: 'None' },
            { value: 'light', label: 'Light' },
            { value: 'heavy', label: 'Heavy' },
            { value: 'battle_worn', label: 'Battle Worn' },
            { value: 'ritual', label: 'Ritual Marks' }
          ]}
        />

        <SliderControl
          value={getValue('surface.emissiveGlow', 0.2)}
          onChange={(value) => onChange('surface.emissiveGlow', value)}
          label="Emissive Glow"
          description="Magical or energy glow intensity: 0.0=no glow, 1.0=bright emission"
          jsonPath="surface.emissiveGlow"
          error={errors?.['surface.emissiveGlow']}
          warning={warnings?.['surface.emissiveGlow']}
          min={0.0}
          max={1.0}
          step={0.01}
        />

        <SegmentedControl
          value={getValue('surface.patina', 'none')}
          onChange={(value) => onChange('surface.patina', value)}
          label="Surface Patina"
          description="Oxidation and aging effects"
          jsonPath="surface.patina"
          error={errors?.['surface.patina']}
          warning={warnings?.['surface.patina']}
          options={[
            { value: 'none', label: 'None' },
            { value: 'light', label: 'Light' },
            { value: 'heavy', label: 'Heavy' },
            { value: 'verdigris', label: 'Verdigris' },
            { value: 'rust', label: 'Rust' },
            { value: 'tarnish', label: 'Tarnish' }
          ]}
        />

        <SegmentedControl
          value={getValue('surface.inscriptions', 'none')}
          onChange={(value) => onChange('surface.inscriptions', value)}
          label="Surface Inscriptions"
          description="Markings, text, or symbols on the surface"
          jsonPath="surface.inscriptions"
          error={errors?.['surface.inscriptions']}
          warning={warnings?.['surface.inscriptions']}
          options={[
            { value: 'none', label: 'None' },
            { value: 'runes', label: 'Runes' },
            { value: 'text', label: 'Text' },
            { value: 'symbols', label: 'Symbols' },
            { value: 'geometric', label: 'Geometric' }
          ]}
        />
      </ControlSection>

      {/* Camera & Presentation Section */}
      <ControlSection title="Camera & Presentation" icon={Camera} defaultExpanded>
        <SegmentedControl
          value={getValue('camera.mode', 'hero_render')}
          onChange={(value) => onChange('camera.mode', value)}
          label="Camera Mode"
          description="Presentation style and viewing angle"
          jsonPath="camera.mode"
          error={errors?.['camera.mode']}
          warning={warnings?.['camera.mode']}
          options={[
            { value: 'isometric', label: 'Isometric' },
            { value: 'flat_icon', label: 'Flat Icon' },
            { value: 'hero_render', label: 'Hero Render' },
            { value: 'three_quarter', label: 'Three Quarter' },
            { value: 'profile', label: 'Profile' }
          ]}
        />

        <SliderControl
          value={getValue('camera.angle', 315)}
          onChange={(value) => onChange('camera.angle', value)}
          label="Rotation Angle"
          description="Item rotation around vertical axis"
          jsonPath="camera.angle"
          error={errors?.['camera.angle']}
          warning={warnings?.['camera.angle']}
          min={0}
          max={360}
          step={1}
          formatDisplay={(value) => `${value}°`}
        />

        <SliderControl
          value={getValue('camera.fov', 45)}
          onChange={(value) => onChange('camera.fov', value)}
          label="Field of View"
          description="Camera lens angle: lower=telephoto, higher=wide angle"
          jsonPath="camera.fov"
          error={errors?.['camera.fov']}
          warning={warnings?.['camera.fov']}
          min={25}
          max={75}
          step={1}
          formatDisplay={(value) => `${value}°`}
        />

        <SegmentedControl
          value={getValue('camera.distance', 'medium')}
          onChange={(value) => onChange('camera.distance', value)}
          label="Camera Distance"
          description="Framing distance for composition"
          jsonPath="camera.distance"
          error={errors?.['camera.distance']}
          warning={warnings?.['camera.distance']}
          options={[
            { value: 'close', label: 'Close' },
            { value: 'medium', label: 'Medium' },
            { value: 'far', label: 'Far' }
          ]}
        />
      </ControlSection>

      {/* Lighting Section */}
      <ControlSection title="Lighting" icon={Lightbulb} defaultExpanded>
        <SegmentedControl
          value={getValue('lighting.keyLight', 'dramatic')}
          onChange={(value) => onChange('lighting.keyLight', value)}
          label="Key Light Style"
          description="Primary lighting setup and mood"
          jsonPath="lighting.keyLight"
          error={errors?.['lighting.keyLight']}
          warning={warnings?.['lighting.keyLight']}
          options={[
            { value: 'studio', label: 'Studio' },
            { value: 'dramatic', label: 'Dramatic' },
            { value: 'soft', label: 'Soft' },
            { value: 'harsh', label: 'Harsh' },
            { value: 'ambient', label: 'Ambient' }
          ]}
        />

        <SliderControl
          value={getValue('lighting.contrast', 0.6)}
          onChange={(value) => onChange('lighting.contrast', value)}
          label="Lighting Contrast"
          description="Light-to-shadow ratio: 0.0=flat lighting, 1.0=high contrast"
          jsonPath="lighting.contrast"
          error={errors?.['lighting.contrast']}
          warning={warnings?.['lighting.contrast']}
          min={0.0}
          max={1.0}
          step={0.01}
        />

        <SegmentedControl
          value={getValue('lighting.rimLight', 'strong')}
          onChange={(value) => onChange('lighting.rimLight', value)}
          label="Rim Lighting"
          description="Edge lighting for object separation"
          jsonPath="lighting.rimLight"
          error={errors?.['lighting.rimLight']}
          warning={warnings?.['lighting.rimLight']}
          options={[
            { value: 'none', label: 'None' },
            { value: 'subtle', label: 'Subtle' },
            { value: 'strong', label: 'Strong' },
            { value: 'colored', label: 'Colored' }
          ]}
        />

        <SliderControl
          value={getValue('lighting.reflections', 0.9)}
          onChange={(value) => onChange('lighting.reflections', value)}
          label="Surface Reflections"
          description="Material reflection intensity: 0.0=matte, 1.0=mirror-like"
          jsonPath="lighting.reflections"
          error={errors?.['lighting.reflections']}
          warning={warnings?.['lighting.reflections']}
          min={0.0}
          max={1.0}
          step={0.01}
        />
      </ControlSection>

      {/* Background Section */}
      <ControlSection title="Background & Effects" icon={Image} defaultExpanded>
        <SegmentedControl
          value={getValue('background.type', 'radial_glow')}
          onChange={(value) => onChange('background.type', value)}
          label="Background Type"
          description="Background treatment and style"
          jsonPath="background.type"
          error={errors?.['background.type']}
          warning={warnings?.['background.type']}
          options={[
            { value: 'transparent', label: 'Transparent' },
            { value: 'studio_gray', label: 'Studio Gray' },
            { value: 'radial_glow', label: 'Radial Glow' },
            { value: 'solid_color', label: 'Solid Color' },
            { value: 'gradient', label: 'Gradient' }
          ]}
        />

        <SegmentedControl
          value={getValue('background.shadow', 'drop_shadow')}
          onChange={(value) => onChange('background.shadow', value)}
          label="Shadow Type"
          description="Shadow casting and ground contact"
          jsonPath="background.shadow"
          error={errors?.['background.shadow']}
          warning={warnings?.['background.shadow']}
          options={[
            { value: 'none', label: 'None' },
            { value: 'drop_shadow', label: 'Drop Shadow' },
            { value: 'contact_shadow', label: 'Contact Shadow' },
            { value: 'ambient_occlusion', label: 'Ambient Occlusion' }
          ]}
        />

        <SegmentedControl
          value={getValue('background.particles', 'magic')}
          onChange={(value) => onChange('background.particles', value)}
          label="Atmospheric Particles"
          description="Environmental effects and atmosphere"
          jsonPath="background.particles"
          error={errors?.['background.particles']}
          warning={warnings?.['background.particles']}
          options={[
            { value: 'none', label: 'None' },
            { value: 'dust', label: 'Dust' },
            { value: 'sparks', label: 'Sparks' },
            { value: 'magic', label: 'Magic' },
            { value: 'smoke', label: 'Smoke' }
          ]}
        />
      </ControlSection>
    </div>
  )
}