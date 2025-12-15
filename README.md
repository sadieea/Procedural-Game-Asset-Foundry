# Procedural Game Asset Foundry

A full-stack application for generating procedural game assets using AI, built with Next.js frontend and FastAPI backend, integrated with Bria FIBO API through ComfyUI workflows.

## Features

- **Three Asset Types**: Generate NPC portraits, weapon items, and environment concepts
- **Real AI Generation**: Integrated with Bria FIBO API for high-quality image generation
- **JSON Schema Validation**: Strict validation using Pydantic schemas
- **Interactive UI**: Real-time configuration with live validation
- **Asset History**: Browse and restore previously generated assets
- **Fallback Services**: Multiple AI service integrations for reliability

## Tech Stack

### Frontend
- **Next.js 14** with TypeScript
- **Tailwind CSS** for styling
- **React Hooks** for state management
- **Real-time validation** and error handling

### Backend
- **FastAPI** with async/await support
- **SQLAlchemy** with async database operations
- **Pydantic** for data validation
- **Structured logging** with structlog
- **ComfyUI integration** for AI workflows

### AI Services
- **Bria FIBO API** (primary)
- **ComfyUI workflows** for local generation
- **External AI services** as fallbacks

## Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- npm or yarn

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
# Copy .env.example to .env and configure your API keys
cp .env.example .env
# Start the backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup
```bash
cd frontend
npm install
# Start the development server
npm run dev
```

### Environment Variables
Create a `.env` file in the backend directory with:
```
BRIA_API_KEY=your_bria_api_key_here
STORAGE_PATH=./storage
DATABASE_URL=sqlite+aiosqlite:///./assets.db
```

## Usage

1. **Select Asset Type**: Choose from NPC Portrait, Weapon Item, or Environment Concept
2. **Configure Parameters**: Use the interactive controls to set generation parameters
3. **Validate Configuration**: Real-time validation ensures valid JSON schemas
4. **Generate Asset**: Click generate to create your asset using AI
5. **Browse History**: View and restore previously generated assets

## API Endpoints

- `POST /api/generate` - Generate a single asset
- `POST /api/generate/batch` - Generate multiple asset variants
- `POST /api/generate/validate` - Validate configuration
- `GET /api/generate/history` - Get asset history
- `GET /api/generate/defaults/{asset_type}` - Get default configuration
- `GET /api/health` - Health check

## Asset Types

### NPC Portrait
Generate character portraits with customizable:
- Race, gender, age, build
- Hair color/style, eye color
- Armor type, weapons
- Mood and art style

### Weapon Item
Create weapon items with:
- Weapon type and material
- Rarity and enchantments
- Visual effects
- Art style variations

### Environment Concept
Design environments featuring:
- Biome and terrain features
- Civilization levels
- Weather and time of day
- Atmospheric mood

## Development

### Project Structure
```
├── frontend/          # Next.js frontend application
├── backend/           # FastAPI backend application
├── schemas/           # JSON schemas and validation
├── ComfyUI/          # ComfyUI integration and workflows
└── storage/          # Generated asset storage
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built for hackathon submission
- Powered by Bria FIBO API
- Uses ComfyUI for local AI generation
- Inspired by the need for procedural game asset creation