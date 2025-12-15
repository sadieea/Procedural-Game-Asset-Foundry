'use client'

import { User, Eye, Camera, Lightbulb, Palette } from 'lucide-react'
import { SliderControl, SegmentedControl, DropdownControl } from './BaseControls'
import { ControlSection } from '../ControlPanel'
import { NPCPortraitConfig } from '@/types/fibo'

interface NPCPortraitControlsProps {
  config: Partial<NPCPortraitConfig>
  onChange: (path: string, value: any) => void
  errors?: Record<string, string>
  warnings?: Record<string, string>
}

export function NPCPortraitControls({ config, onChange, errors, warnings }: NPCPortraitControlsProps) {
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

  return (
    <div className="space-y-6">
      {/* Identity Section */}
      <ControlSection title="Identity" icon={User} defaultExpanded>
        <SegmentedControl
          value={getValue('identity.ageRange', 'adult')}
          onChange={(value) => onChange('identity.ageRange', value)}
          label="Age Range"
          description="Character age category affecting facial structure and features"
          jsonPath="identity.ageRange"
          error={errors?.['identity.ageRange']}
          warning={warnings?.['identity.ageRange']}
          options={[
            { value: 'young', label: 'Young' },
            { value: 'adult', label: 'Adult' },
            { value: 'middle_aged', label: 'Middle Aged' },
            { value: 'elderly', label: 'Elderly' }
          ]}
        />

        <SegmentedControl
          value={getValue('identity.genderPresentation', 'masculine')}
          onChange={(value) => onChange('identity.genderPresentation', value)}
          label="Gender Presentation"
          description="Gender presentation affecting facial feature softness and structure"
          jsonPath="identity.genderPresentation"
          error={errors?.['identity.genderPresentation']}
          warning={warnings?.['identity.genderPresentation']}
          options={[
            { value: 'masculine', label: 'Masculine' },
            { value: 'feminine', label: 'Feminine' },
            { value: 'androgynous', label: 'Androgynous' }
          ]}
        />

        <DropdownControl
          value={getValue('identity.ethnicity', 'caucasian')}
          onChange={(value) => onChange('identity.ethnicity', value)}
          label="Ethnicity"
          description="Ethnic background for facial structure variation and cultural features"
          jsonPath="identity.ethnicity"
          error={errors?.['identity.ethnicity']}
          warning={warnings?.['identity.ethnicity']}
          searchable
          options={[
            { value: 'east_asian', label: 'East Asian', group: 'Human' },
            { value: 'south_asian', label: 'South Asian', group: 'Human' },
            { value: 'african', label: 'African', group: 'Human' },
            { value: 'caucasian', label: 'Caucasian', group: 'Human' },
            { value: 'middle_eastern', label: 'Middle Eastern', group: 'Human' },
            { value: 'latino', label: 'Latino', group: 'Human' },
            { value: 'mixed', label: 'Mixed Heritage', group: 'Human' },
            { value: 'fantasy_elf', label: 'Elf', group: 'Fantasy' },
            { value: 'fantasy_dwarf', label: 'Dwarf', group: 'Fantasy' },
            { value: 'fantasy_orc', label: 'Orc', group: 'Fantasy' }
          ]}
        />

        <DropdownControl
          value={getValue('identity.archetype', 'warrior')}
          onChange={(value) => onChange('identity.archetype', value)}
          label="Archetype"
          description="Character class affecting styling, accessories, and overall presentation"
          jsonPath="identity.archetype"
          error={errors?.['identity.archetype']}
          warning={warnings?.['identity.archetype']}
          options={[
            { value: 'warrior', label: 'Warrior', description: 'Battle-hardened fighter' },
            { value: 'mage', label: 'Mage', description: 'Arcane spellcaster' },
            { value: 'rogue', label: 'Rogue', description: 'Stealthy infiltrator' },
            { value: 'noble', label: 'Noble', description: 'Aristocratic leader' },
            { value: 'merchant', label: 'Merchant', description: 'Trader and negotiator' },
            { value: 'scholar', label: 'Scholar', description: 'Learned researcher' },
            { value: 'assassin', label: 'Assassin', description: 'Silent killer' },
            { value: 'paladin', label: 'Paladin', description: 'Holy warrior' },
            { value: 'villager', label: 'Villager', description: 'Common folk' },
            { value: 'blacksmith', label: 'Blacksmith', description: 'Master craftsperson' }
          ]}
        />
      </ControlSection>

      {/* Facial Features Section */}
      <ControlSection title="Facial Features" icon={Eye} defaultExpanded>
        <SliderControl
          value={getValue('facialFeatures.jawWidth', 0.5)}
          onChange={(value) => onChange('facialFeatures.jawWidth', value)}
          label="Jaw Width"
          description="Jaw width: 0.0=narrow, 0.5=average, 1.0=wide and pronounced"
          jsonPath="facialFeatures.jawWidth"
          error={errors?.['facialFeatures.jawWidth']}
          warning={warnings?.['facialFeatures.jawWidth']}
          min={0.0}
          max={1.0}
          step={0.01}
        />

        <SliderControl
          value={getValue('facialFeatures.cheekboneHeight', 0.5)}
          onChange={(value) => onChange('facialFeatures.cheekboneHeight', value)}
          label="Cheekbone Height"
          description="Cheekbone prominence: 0.0=low and soft, 1.0=high and sharp"
          jsonPath="facialFeatures.cheekboneHeight"
          error={errors?.['facialFeatures.cheekboneHeight']}
          warning={warnings?.['facialFeatures.cheekboneHeight']}
          min={0.0}
          max={1.0}
          step={0.01}
        />

        <SliderControl
          value={getValue('facialFeatures.noseLength', 0.5)}
          onChange={(value) => onChange('facialFeatures.noseLength', value)}
          label="Nose Length"
          description="Nose length: 0.0=short and button, 1.0=long and prominent"
          jsonPath="facialFeatures.noseLength"
          error={errors?.['facialFeatures.noseLength']}
          warning={warnings?.['facialFeatures.noseLength']}
          min={0.0}
          max={1.0}
          step={0.01}
        />

        <SliderControl
          value={getValue('facialFeatures.eyeSize', 0.5)}
          onChange={(value) => onChange('facialFeatures.eyeSize', value)}
          label="Eye Size"
          description="Eye size: 0.0=small and narrow, 1.0=large and prominent"
          jsonPath="facialFeatures.eyeSize"
          error={errors?.['facialFeatures.eyeSize']}
          warning={warnings?.['facialFeatures.eyeSize']}
          min={0.0}
          max={1.0}
          step={0.01}
        />

        <SliderControl
          value={getValue('facialFeatures.browIntensity', 0.5)}
          onChange={(value) => onChange('facialFeatures.browIntensity', value)}
          label="Brow Intensity"
          description="Eyebrow thickness and prominence: 0.0=thin, 1.0=thick and heavy"
          jsonPath="facialFeatures.browIntensity"
          error={errors?.['facialFeatures.browIntensity']}
          warning={warnings?.['facialFeatures.browIntensity']}
          min={0.0}
          max={1.0}
          step={0.01}
        />

        <SegmentedControl
          value={getValue('facialFeatures.scars', 'none')}
          onChange={(value) => onChange('facialFeatures.scars', value)}
          label="Battle Scars"
          description="Facial scarring level and pattern"
          jsonPath="facialFeatures.scars"
          error={errors?.['facialFeatures.scars']}
          warning={warnings?.['facialFeatures.scars']}
          options={[
            { value: 'none', label: 'None' },
            { value: 'light', label: 'Light' },
            { value: 'heavy', label: 'Heavy' },
            { value: 'ritual', label: 'Ritual' },
            { value: 'battle', label: 'Battle' }
          ]}
        />

        <DropdownControl
          value={getValue('facialFeatures.facialHair', 'none')}
          onChange={(value) => onChange('facialFeatures.facialHair', value)}
          label="Facial Hair"
          description="Facial hair style and coverage"
          jsonPath="facialFeatures.facialHair"
          error={errors?.['facialFeatures.facialHair']}
          warning={warnings?.['facialFeatures.facialHair']}
          options={[
            { value: 'none', label: 'Clean Shaven' },
            { value: 'stubble', label: 'Stubble' },
            { value: 'beard', label: 'Full Beard' },
            { value: 'mustache', label: 'Mustache' },
            { value: 'goatee', label: 'Goatee' },
            { value: 'full', label: 'Full Coverage' }
          ]}
        />
      </ControlSection>

      {/* Expression Section */}
      <ControlSection title="Expression" icon={Eye} defaultExpanded>
        <DropdownControl
          value={getValue('expression.emotion', 'neutral')}
          onChange={(value) => onChange('expression.emotion', value)}
          label="Primary Emotion"
          description="Base facial expression and emotional state"
          jsonPath="expression.emotion"
          error={errors?.['expression.emotion']}
          warning={warnings?.['expression.emotion']}
          options={[
            { value: 'neutral', label: 'Neutral', description: 'Calm and composed' },
            { value: 'stern', label: 'Stern', description: 'Serious and authoritative' },
            { value: 'friendly', label: 'Friendly', description: 'Warm and approachable' },
            { value: 'angry', label: 'Angry', description: 'Fierce and intimidating' },
            { value: 'mysterious', label: 'Mysterious', description: 'Enigmatic and secretive' },
            { value: 'wise', label: 'Wise', description: 'Thoughtful and knowing' },
            { value: 'fierce', label: 'Fierce', description: 'Intense and determined' },
            { value: 'sad', label: 'Sad', description: 'Melancholic and sorrowful' },
            { value: 'determined', label: 'Determined', description: 'Focused and resolute' }
          ]}
        />

        <SliderControl
          value={getValue('expression.intensity', 0.4)}
          onChange={(value) => onChange('expression.intensity', value)}
          label="Expression Intensity"
          description="Strength of the emotional expression: 0.0=subtle, 1.0=pronounced"
          jsonPath="expression.intensity"
          error={errors?.['expression.intensity']}
          warning={warnings?.['expression.intensity']}
          min={0.0}
          max={1.0}
          step={0.01}
        />
      </ControlSection>

      {/* Camera Section */}
      <ControlSection title="Camera & Composition" icon={Camera} defaultExpanded>
        <SegmentedControl
          value={getValue('camera.angle', 'three_quarter_left')}
          onChange={(value) => onChange('camera.angle', value)}
          label="Camera Angle"
          description="Camera position relative to subject"
          jsonPath="camera.angle"
          error={errors?.['camera.angle']}
          warning={warnings?.['camera.angle']}
          options={[
            { value: 'frontal', label: 'Front' },
            { value: 'three_quarter_left', label: '3/4 Left' },
            { value: 'three_quarter_right', label: '3/4 Right' },
            { value: 'profile_left', label: 'Profile L' },
            { value: 'profile_right', label: 'Profile R' }
          ]}
        />

        <SliderControl
          value={getValue('camera.fov', 50)}
          onChange={(value) => onChange('camera.fov', value)}
          label="Field of View"
          description="Lens focal length equivalent: 35mm=wide angle, 85mm=portrait lens"
          jsonPath="camera.fov"
          error={errors?.['camera.fov']}
          warning={warnings?.['camera.fov']}
          min={35}
          max={85}
          step={1}
          formatDisplay={(value) => `${value}mm`}
        />

        <SliderControl
          value={getValue('camera.headTilt', 0.0)}
          onChange={(value) => onChange('camera.headTilt', value)}
          label="Head Tilt"
          description="Head rotation angle: negative=left tilt, positive=right tilt"
          jsonPath="camera.headTilt"
          error={errors?.['camera.headTilt']}
          warning={warnings?.['camera.headTilt']}
          min={-0.3}
          max={0.3}
          step={0.01}
          formatDisplay={(value) => `${Math.round(value * 180 / Math.PI)}°`}
        />

        <SegmentedControl
          value={getValue('camera.distance', 'medium')}
          onChange={(value) => onChange('camera.distance', value)}
          label="Camera Distance"
          description="Framing distance affecting crop and perspective"
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
          value={getValue('lighting.keyLight', 'studio')}
          onChange={(value) => onChange('lighting.keyLight', value)}
          label="Key Light Style"
          description="Primary light source quality and character"
          jsonPath="lighting.keyLight"
          error={errors?.['lighting.keyLight']}
          warning={warnings?.['lighting.keyLight']}
          options={[
            { value: 'soft', label: 'Soft' },
            { value: 'dramatic', label: 'Dramatic' },
            { value: 'studio', label: 'Studio' },
            { value: 'natural', label: 'Natural' }
          ]}
        />

        <SliderControl
          value={getValue('lighting.fillRatio', 0.4)}
          onChange={(value) => onChange('lighting.fillRatio', value)}
          label="Fill Light Ratio"
          description="Fill light strength: 0.0=high contrast, 1.0=flat lighting"
          jsonPath="lighting.fillRatio"
          error={errors?.['lighting.fillRatio']}
          warning={warnings?.['lighting.fillRatio']}
          min={0.0}
          max={1.0}
          step={0.01}
          formatDisplay={(value) => `1:${(1/Math.max(value, 0.1)).toFixed(1)}`}
        />

        <SegmentedControl
          value={getValue('lighting.rimLight', 'subtle')}
          onChange={(value) => onChange('lighting.rimLight', value)}
          label="Rim Lighting"
          description="Edge lighting for subject separation"
          jsonPath="lighting.rimLight"
          error={errors?.['lighting.rimLight']}
          warning={warnings?.['lighting.rimLight']}
          options={[
            { value: 'none', label: 'None' },
            { value: 'subtle', label: 'Subtle' },
            { value: 'strong', label: 'Strong' }
          ]}
        />

        <SegmentedControl
          value={getValue('lighting.colorTemperature', 'neutral')}
          onChange={(value) => onChange('lighting.colorTemperature', value)}
          label="Color Temperature"
          description="Light color cast and mood"
          jsonPath="lighting.colorTemperature"
          error={errors?.['lighting.colorTemperature']}
          warning={warnings?.['lighting.colorTemperature']}
          options={[
            { value: 'warm', label: 'Warm' },
            { value: 'neutral', label: 'Neutral' },
            { value: 'cool', label: 'Cool' },
            { value: 'candlelight', label: 'Candle' },
            { value: 'daylight', label: 'Daylight' },
            { value: 'moonlight', label: 'Moonlight' }
          ]}
        />
      </ControlSection>

      {/* Style Section */}
      <ControlSection title="Style & Rendering" icon={Palette} defaultExpanded>
        <SegmentedControl
          value={getValue('style.renderStyle', 'photorealistic')}
          onChange={(value) => onChange('style.renderStyle', value)}
          label="Render Style"
          description="Overall rendering approach and aesthetic"
          jsonPath="style.renderStyle"
          error={errors?.['style.renderStyle']}
          warning={warnings?.['style.renderStyle']}
          options={[
            { value: 'photorealistic', label: 'Photo' },
            { value: 'stylized', label: 'Stylized' },
            { value: 'painterly', label: 'Painterly' },
            { value: 'cel_shaded', label: 'Cel Shaded' },
            { value: 'concept_art', label: 'Concept' }
          ]}
        />

        <SegmentedControl
          value={getValue('style.detailLevel', 'high')}
          onChange={(value) => onChange('style.detailLevel', value)}
          label="Detail Level"
          description="Surface detail complexity (affects generation time)"
          jsonPath="style.detailLevel"
          error={errors?.['style.detailLevel']}
          warning={warnings?.['style.detailLevel']}
          options={[
            { value: 'low', label: 'Low' },
            { value: 'medium', label: 'Medium' },
            { value: 'high', label: 'High' },
            { value: 'ultra', label: 'Ultra' }
          ]}
        />

        <SegmentedControl
          value={getValue('style.skinTexture', 'natural')}
          onChange={(value) => onChange('style.skinTexture', value)}
          label="Skin Texture"
          description="Surface treatment and texture detail"
          jsonPath="style.skinTexture"
          error={errors?.['style.skinTexture']}
          warning={warnings?.['style.skinTexture']}
          options={[
            { value: 'smooth', label: 'Smooth' },
            { value: 'natural', label: 'Natural' },
            { value: 'rough', label: 'Rough' },
            { value: 'weathered', label: 'Weathered' },
            { value: 'fantasy', label: 'Fantasy' }
          ]}
        />
      </ControlSection>
    </div>
  )
}