# Procedural Game Asset Foundry - Frontend

A professional, studio-grade frontend for the Procedural Game Asset Foundry - a JSON-native visual asset generator built specifically for game development workflows.

## 🎨 Design System

This frontend implements a strict, AAA studio-grade design system:

### Color Palette
- **Base Background**: `#0F1115` (studio-dark)
- **Panel Background**: `#1A1D23` (studio-gray)  
- **Elevated Surfaces**: `#2A2D35` (studio-light)
- **Primary Accent**: `#4ECDC4` (studio-cyan)
- **Secondary Accent**: `#F7B731` (studio-amber)
- **Text Primary**: `#FFFFFF`
- **Text Secondary**: `#B8BCC8`
- **Text Muted**: `#6B7280`

### Typography
- **Primary UI Font**: Inter
- **Code/JSON Font**: JetBrains Mono

## 🏗️ Architecture

### Component Structure
```
src/
├── app/
│   ├── layout.tsx          # Root layout with global styles
│   ├── page.tsx            # Main application shell
│   └── globals.css         # Global CSS with design system
├── components/
│   ├── TopBar.tsx          # Header with asset type tabs & controls
│   ├── ControlPanel.tsx    # Left panel with generation controls
│   ├── AssetCanvas.tsx     # Center canvas for asset preview
│   ├── JSONInspector.tsx   # JSON schema viewer/editor
│   └── AssetHistory.tsx    # Asset history & management
└── types/
    └── fibo.ts             # TypeScript definitions for FIBO schemas
```

### Key Features

#### 🎮 Asset Generation Modes
- **NPC Portraits**: Character dialogue and UI portraits
- **Weapons & Items**: Inventory icons and equipment renders  
- **Environment Concepts**: Worldbuilding and level ideation

#### 🧠 JSON-Native Workflow
- Live JSON schema updates as you adjust controls
- Syntax-highlighted JSON inspector
- Export/import configurations
- Deterministic, reproducible generation

#### 🎨 Professional UI/UX
- Studio-grade dark theme optimized for long sessions
- Subtle, purposeful animations (no bounce/elastic)
- Desktop-first, widescreen layout
- Film grain overlay for cinematic feel

#### 📊 Asset Management
- Complete generation history
- Thumbnail previews
- Metadata tracking (generation time, file size, etc.)
- One-click restore of previous configurations

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ 
- npm or yarn

### Installation
```bash
cd frontend
npm install
```

### Development
```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to view the application.

### Build for Production
```bash
npm run build
npm start
```

## 🛠️ Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS with custom design system
- **Animations**: Framer Motion
- **Icons**: Lucide React

## 🎯 Design Principles

1. **Predictability**: Every interaction should feel deterministic
2. **Precision**: Controls must feel precise and professional
3. **Performance**: Smooth 60fps animations, optimized rendering
4. **Professionalism**: This is a production tool, not a demo
5. **Consistency**: One design system, zero deviations

## 🔧 Configuration

The application uses a strict TypeScript configuration with path mapping:
- `@/*` maps to `./src/*`

Tailwind is configured with the exact design system colors and typography scales.

## 📱 Responsive Design

While desktop-first, the application gracefully handles different screen sizes:
- **Desktop (1920px+)**: Full 3-column layout
- **Laptop (1440px+)**: Optimized spacing
- **Tablet (768px+)**: Collapsible panels

## 🎨 Animation System

Subtle, professional animations only:
- **fade-in**: 150ms ease-out
- **slide-in**: 200ms ease-out  
- **dissolve**: 300ms ease-out
- **shimmer**: Loading states
- **grain**: Ambient film grain effect

No bounce, elastic, or distracting animations.

## 🧪 Mock Data

The frontend includes comprehensive mock data generation for development:
- Procedural placeholder images based on asset type
- Realistic generation timing simulation
- Proper metadata structure matching FIBO schemas

## 🔌 FIBO Integration

Ready for FIBO API integration:
- Complete TypeScript schemas for all asset types
- Proper error handling and loading states
- JSON export/import for configuration management
- Batch generation support (planned)

## 📄 License

This project is part of the Procedural Game Asset Foundry suite.