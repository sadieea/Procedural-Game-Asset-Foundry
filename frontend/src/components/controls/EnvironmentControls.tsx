'use client'

import { Mountain, Layout, Cloud, Lightbulb, Palette } from 'lucide-react'
import { SliderControl, SegmentedControl, DropdownControl } from './BaseControls'
import { ControlSection } from '../ControlPanel'
import { EnvironmentConfig } from '@/types/fibo'

interface EnvironmentControlsProps {
  config: Partial<EnvironmentConfig>
  onChange: (path: string, value: any) => void
  errors?: Record<string, string>
  warnings?: Record<string, string>
}

export function EnvironmentControls({ config, onChange, errors, warnings }: EnvironmentControlsProps) {
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
      {/* Scene Definition Section */}
      <ControlSection title="Scene Definition" icon={Mountain} defaultExpanded>
        <DropdownControl
          value={getValue('scene.type', 'forest')}
          onChange={(value) => onChange('scene.type', value)}
          label="Environment Type"
          description="Primary environment category and setting"
          jsonPath="scene.type"
          error={errors?.['scene.type']}
          warning={warnings?.['scene.type']}
          searchable
          options={[
            { value: 'city', label: 'City', description: 'Urban settlement', group: 'Civilized' },
            { value: 'village', label: 'Village', description: 'Small rural settlement', group: 'Civilized' },
            { value: 'forest', label: 'Forest', description: 'Dense woodland area', group: 'Natural' },
            { value: 'desert', label: 'Desert', description: 'Arid wasteland', group: 'Natural' },
            { value: 'mountains', label: 'Mountains', description: 'Rocky peaks and valleys', group: 'Natural' },
            { value: 'ruins', label: 'Ruins', description: 'Ancient abandoned structures', group: 'Historical' },
            { value: 'dungeon', label: 'Dungeon', description: 'Underground complex', group: 'Structures' },
            { value: 'castle', label: 'Castle', description: 'Fortified stronghold', group: 'Structures' },
            { value: 'temple', label: 'Temple', description: 'Sacred religious site', group: 'Structures' },
            { value: 'sci_fi_interior', label: 'Sci-Fi Interior', description: 'Futuristic indoor space', group: 'Futuristic' },
            { value: 'space_station', label: 'Space Station', description: 'Orbital facility', group: 'Futuristic' },
            { value: 'underwater', label: 'Underwater', description: 'Subaquatic environment', group: 'Exotic' }
          ]}
        />

        <SegmentedControl
          value={getValue('scene.era', 'medieval')}
          onChange={(value) => onChange('scene.era', value)}
          label="Historical Era"
          description="Technological and cultural time period"
          jsonPath="scene.era"
          error={errors?.['scene.era']}
          warning={warnings?.['scene.era']}
          options={[
            { value: 'prehistoric', label: 'Prehistoric' },
            { value: 'ancient', label: 'Ancient' },
            { value: 'medieval', label: 'Medieval' },
            { value: 'renaissance', label: 'Renaissance' },
            { value: 'industrial', label: 'Industrial' },
            { value: 'modern', label: 'Modern' },
            { value: 'futuristic', label: 'Futuristic' },
            { value: 'post_apocalyptic', label: 'Post-Apocalyptic' }
          ]}
        />

        <SegmentedControl
          value={getValue('scene.scale', 'medium')}
          onChange={(value) => onChange('scene.scale', value)}
          label="Scene Scale"
          description="Scope and grandeur of the environment"
          jsonPath="scene.scale"
          error={errors?.['scene.scale']}
          warning={warnings?.['scene.scale']}
          options={[
            { value: 'intimate', label: 'Intimate' },
            { value: 'medium', label: 'Medium' },
            { value: 'wide', label: 'Wide' },
            { value: 'epic', label: 'Epic' },
            { value: 'panoramic', label: 'Panoramic' }
          ]}
        />

        <SegmentedControl
          value={getValue('scene.biome', 'temperate')}
          onChange={(value) => onChange('scene.biome', value)}
          label="Biome Type"
          description="Climate and ecological characteristics"
          jsonPath="scene.biome"
          error={errors?.['scene.biome']}
          warning={warnings?.['scene.biome']}
          options={[
            { value: 'temperate', label: 'Temperate' },
            { value: 'tropical', label: 'Tropical' },
            { value: 'arctic', label: 'Arctic' },
            { value: 'desert', label: 'Desert' },
            { value: 'swamp', label: 'Swamp' },
            { value: 'volcanic', label: 'Volcanic' },
            { value: 'alien', label: 'Alien' },
            { value: 'magical', label: 'Magical' }
          ]}
        />
      </ControlSection>

      {/* Composition Section */}
      <ControlSection title="Composition" icon={Layout} defaultExpanded>
        <SegmentedControl
          value={getValue('composition.cameraHeight', 'eye_level')}
          onChange={(value) => onChange('composition.cameraHeight', value)}
          label="Camera Height"
          description="Viewing elevation and perspective"
          jsonPath="composition.cameraHeight"
          error={errors?.['composition.cameraHeight']}
          warning={warnings?.['composition.cameraHeight']}
          options={[
            { value: 'ground', label: 'Ground' },
            { value: 'eye_level', label: 'Eye Level' },
            { value: 'elevated', label: 'Elevated' },
            { value: 'aerial', label: 'Aerial' },
            { value: 'birds_eye', label: 'Bird\'s Eye' }
          ]}
        />

        <SliderControl
          value={getValue('composition.horizonPosition', 0.33)}
          onChange={(value) => onChange('composition.horizonPosition', value)}
          label="Horizon Position"
          description="Horizon line placement: 0.33 and 0.66 follow rule of thirds"
          jsonPath="composition.horizonPosition"
          error={errors?.['composition.horizonPosition']}
          warning={warnings?.['composition.horizonPosition']}
          min={0.0}
          max={1.0}
          step={0.01}
          formatDisplay={(value) => {
            if (Math.abs(value - 0.33) < 0.02) return "Lower Third"
            if (Math.abs(value - 0.66) < 0.02) return "Upper Third"
            return `${Math.round(value * 100)}%`
          }}
        />

        <SegmentedControl
          value={getValue('composition.depthLayers', 'medium')}
          onChange={(value) => onChange('composition.depthLayers', value)}
          label="Depth Layers"
          description="Compositional depth and layering complexity"
          jsonPath="composition.depthLayers"
          error={errors?.['composition.depthLayers']}
          warning={warnings?.['composition.depthLayers']}
          options={[
            { value: 'shallow', label: 'Shallow' },
            { value: 'medium', label: 'Medium' },
            { value: 'deep', label: 'Deep' },
            { value: 'infinite', label: 'Infinite' }
          ]}
        />

        <SegmentedControl
          value={getValue('composition.focalPoint', 'center')}
          onChange={(value) => onChange('composition.focalPoint', value)}
          label="Focal Point"
          description="Primary point of interest placement"
          jsonPath="composition.focalPoint"
          error={errors?.['composition.focalPoint']}
          warning={warnings?.['composition.focalPoint']}
          options={[
            { value: 'center', label: 'Center' },
            { value: 'left_third', label: 'Left Third' },
            { value: 'right_third', label: 'Right Third' },
            { value: 'foreground', label: 'Foreground' },
            { value: 'background', label: 'Background' }
          ]}
        />
      </ControlSection>

      {/* Atmosphere Section */}
      <ControlSection title="Atmosphere" icon={Cloud} defaultExpanded>
        <SegmentedControl
          value={getValue('atmosphere.timeOfDay', 'dusk')}
          onChange={(value) => onChange('atmosphere.timeOfDay', value)}
          label="Time of Day"
          description="Lighting conditions and mood timing"
          jsonPath="atmosphere.timeOfDay"
          error={errors?.['atmosphere.timeOfDay']}
          warning={warnings?.['atmosphere.timeOfDay']}
          options={[
            { value: 'dawn', label: 'Dawn' },
            { value: 'morning', label: 'Morning' },
            { value: 'midday', label: 'Midday' },
            { value: 'afternoon', label: 'Afternoon' },
            { value: 'dusk', label: 'Dusk' },
            { value: 'night', label: 'Night' },
            { value: 'midnight', label: 'Midnight' }
          ]}
        />

        <DropdownControl
          value={getValue('atmosphere.weather', 'clear')}
          onChange={(value) => onChange('atmosphere.weather', value)}
          label="Weather Conditions"
          description="Atmospheric conditions and precipitation"
          jsonPath="atmosphere.weather"
          error={errors?.['atmosphere.weather']}
          warning={warnings?.['atmosphere.weather']}
          options={[
            { value: 'clear', label: 'Clear', description: 'Bright and cloudless' },
            { value: 'partly_cloudy', label: 'Partly Cloudy', description: 'Some cloud cover' },
            { value: 'overcast', label: 'Overcast', description: 'Heavy cloud cover' },
            { value: 'foggy', label: 'Foggy', description: 'Dense fog or mist' },
            { value: 'rainy', label: 'Rainy', description: 'Active precipitation' },
            { value: 'stormy', label: 'Stormy', description: 'Severe weather conditions' },
            { value: 'snowy', label: 'Snowy', description: 'Snow precipitation' },
            { value: 'sandstorm', label: 'Sandstorm', description: 'Desert dust storm' }
          ]}
        />

        <SliderControl
          value={getValue('atmosphere.fogDensity', 0.3)}
          onChange={(value) => onChange('atmosphere.fogDensity', value)}
          label="Fog Density"
          description="Atmospheric haze and fog thickness: 0.0=clear air, 1.0=heavy fog"
          jsonPath="atmosphere.fogDensity"
          error={errors?.['atmosphere.fogDensity']}
          warning={warnings?.['atmosphere.fogDensity']}
          min={0.0}
          max={1.0}
          step={0.01}
        />

        <SliderControl
          value={getValue('atmosphere.visibility', 0.8)}
          onChange={(value) => onChange('atmosphere.visibility', value)}
          label="Visibility Range"
          description="Atmospheric clarity and viewing distance"
          jsonPath="atmosphere.visibility"
          error={errors?.['atmosphere.visibility']}
          warning={warnings?.['atmosphere.visibility']}
          min={0.1}
          max={1.0}
          step={0.01}
          formatDisplay={(value) => `${Math.round(value * 100)}%`}
        />
      </ControlSection>

      {/* Lighting Section */}
      <ControlSection title="Lighting & Mood" icon={Lightbulb} defaultExpanded>
        <SegmentedControl
          value={getValue('lighting.lightStyle', 'cinematic')}
          onChange={(value) => onChange('lighting.lightStyle', value)}
          label="Light Style"
          description="Overall lighting approach and character"
          jsonPath="lighting.lightStyle"
          error={errors?.['lighting.lightStyle']}
          warning={warnings?.['lighting.lightStyle']}
          options={[
            { value: 'soft', label: 'Soft' },
            { value: 'dramatic', label: 'Dramatic' },
            { value: 'cinematic', label: 'Cinematic' },
            { value: 'natural', label: 'Natural' },
            { value: 'artificial', label: 'Artificial' },
            { value: 'magical', label: 'Magical' }
          ]}
        />

        <SliderControl
          value={getValue('lighting.contrast', 0.7)}
          onChange={(value) => onChange('lighting.contrast', value)}
          label="Lighting Contrast"
          description="Dynamic range between light and shadow areas"
          jsonPath="lighting.contrast"
          error={errors?.['lighting.contrast']}
          warning={warnings?.['lighting.contrast']}
          min={0.0}
          max={1.0}
          step={0.01}
        />

        <SliderControl
          value={getValue('lighting.godRays', 0.4)}
          onChange={(value) => onChange('lighting.godRays', value)}
          label="God Rays"
          description="Volumetric light shafts through atmosphere: requires fog or particles"
          jsonPath="lighting.godRays"
          error={errors?.['lighting.godRays']}
          warning={warnings?.['lighting.godRays']}
          min={0.0}
          max={1.0}
          step={0.01}
        />

        <SegmentedControl
          value={getValue('lighting.colorTemperature', 'warm')}
          onChange={(value) => onChange('lighting.colorTemperature', value)}
          label="Color Temperature"
          description="Light color cast and emotional tone"
          jsonPath="lighting.colorTemperature"
          error={errors?.['lighting.colorTemperature']}
          warning={warnings?.['lighting.colorTemperature']}
          options={[
            { value: 'warm', label: 'Warm' },
            { value: 'neutral', label: 'Neutral' },
            { value: 'cool', label: 'Cool' },
            { value: 'golden_hour', label: 'Golden Hour' },
            { value: 'blue_hour', label: 'Blue Hour' },
            { value: 'artificial', label: 'Artificial' }
          ]}
        />

        <SliderControl
          value={getValue('lighting.ambientOcclusion', 0.6)}
          onChange={(value) => onChange('lighting.ambientOcclusion', value)}
          label="Ambient Occlusion"
          description="Shadow detail in crevices and contact areas"
          jsonPath="lighting.ambientOcclusion"
          error={errors?.['lighting.ambientOcclusion']}
          warning={warnings?.['lighting.ambientOcclusion']}
          min={0.0}
          max={1.0}
          step={0.01}
        />
      </ControlSection>

      {/* Style Section */}
      <ControlSection title="Style & Rendering" icon={Palette} defaultExpanded>
        <SegmentedControl
          value={getValue('style.renderStyle', 'matte_painting')}
          onChange={(value) => onChange('style.renderStyle', value)}
          label="Render Style"
          description="Overall artistic approach and technique"
          jsonPath="style.renderStyle"
          error={errors?.['style.renderStyle']}
          warning={warnings?.['style.renderStyle']}
          options={[
            { value: 'photorealistic', label: 'Photo' },
            { value: 'cinematic_realism', label: 'Cinematic' },
            { value: 'matte_painting', label: 'Matte Paint' },
            { value: 'stylized', label: 'Stylized' },
            { value: 'concept_art', label: 'Concept' },
            { value: 'impressionistic', label: 'Impressionist' }
          ]}
        />

        <SegmentedControl
          value={getValue('style.detailLevel', 'high')}
          onChange={(value) => onChange('style.detailLevel', value)}
          label="Detail Level"
          description="Environmental complexity and surface detail (affects generation time)"
          jsonPath="style.detailLevel"
          error={errors?.['style.detailLevel']}
          warning={warnings?.['style.detailLevel']}
          options={[
            { value: 'sketch', label: 'Sketch' },
            { value: 'medium', label: 'Medium' },
            { value: 'high', label: 'High' },
            { value: 'ultra', label: 'Ultra' },
            { value: 'architectural', label: 'Architectural' }
          ]}
        />

        <SegmentedControl
          value={getValue('style.colorPalette', 'cinematic')}
          onChange={(value) => onChange('style.colorPalette', value)}
          label="Color Palette"
          description="Color scheme and grading approach"
          jsonPath="style.colorPalette"
          error={errors?.['style.colorPalette']}
          warning={warnings?.['style.colorPalette']}
          options={[
            { value: 'natural', label: 'Natural' },
            { value: 'desaturated', label: 'Desaturated' },
            { value: 'vibrant', label: 'Vibrant' },
            { value: 'monochrome', label: 'Monochrome' },
            { value: 'complementary', label: 'Complementary' },
            { value: 'analogous', label: 'Analogous' },
            { value: 'cinematic', label: 'Cinematic' }
          ]}
        />
      </ControlSection>
    </div>
  )
}