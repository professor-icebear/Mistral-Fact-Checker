# Mistral Fact Checker

<div align="center">

![Mistral AI](https://img.shields.io/badge/Powered%20by-Mistral%20AI-FF7000?style=for-the-badge)
![Next.js](https://img.shields.io/badge/Next.js-14-black?style=for-the-badge&logo=next.js)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi)
![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?style=for-the-badge&logo=typescript)
![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python)

**AI-Powered Fact Checking Application**

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [API Documentation](#-api-documentation)
- [Architecture](#-architecture)
- [Best Practices](#-best-practices)
- [Testing](#-testing)
- [Troubleshooting](#-troubleshooting)

## 🎯 Overview

Mistral Fact Checker is a production-ready web application that leverages Mistral AI's powerful language models to verify and fact-check information from multiple sources: text, URLs, and images. Built with modern best practices, clean architecture, and beautiful UI following Mistral's design guidelines.

**Built for Mistral AI Interview Process**

This project demonstrates:
- ✅ Clean code architecture with separation of concerns
- ✅ Production-ready backend with proper error handling
- ✅ Type-safe frontend and backend
- ✅ Modern UI/UX following Mistral design system
- ✅ Comprehensive documentation
- ✅ Best practices in both Python and TypeScript

## ✨ Features

### Core Functionality
- 📝 **Text Fact-Checking** - Verify claims and statements
- 🔗 **URL Analysis** - Extract and analyze web content
- 🖼️ **Image Verification** - Use Pixtral vision model for image analysis
- 📊 **Comprehensive Reports** - Rating (0-10), confidence, detailed analysis, sources
- 📤 **Share Results** - Easy sharing functionality
- ⚡ **Real-time Processing** - Fast analysis with beautiful loading states

### Technical Features
- 🎨 **Mistral Design System** - Official color palette and styling
- 📱 **Responsive Design** - Works on all devices
- 🔒 **Type Safety** - Full TypeScript + Pydantic validation
- 🪵 **Logging** - Structured logging throughout
- 🛡️ **Error Handling** - Custom exceptions and proper HTTP codes
- ⚙️ **Configuration** - Environment-based, validated config
- 🚀 **Production Ready** - Async/await, connection pooling, security

## 🛠️ Tech Stack

### Frontend
- **Next.js 14** (App Router) + **TypeScript 5**
- **Tailwind CSS 3** (Mistral design tokens)
- **Axios** for API calls
- **Lucide React** for icons

### Backend
- **FastAPI 0.115** + **Python 3.9+**
- **Mistral AI API** (`mistral-large-latest`, `pixtral-large-latest`)
- **Pydantic** for validation
- **httpx** for async HTTP
- **Uvicorn** ASGI server

### Architecture
- **Modular Backend**: Separate modules for config, models, services, exceptions
- **Clean Frontend**: Component-based with proper separation
- **Dependency Injection**: FastAPI DI for services
- **Async/Await**: Non-blocking I/O throughout

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.9+
- Mistral AI API key from [console.mistral.ai](https://console.mistral.ai/)

### Setup

**1. Clone and navigate:**
```bash
cd mistral-interview
```

**2. Backend setup:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
echo "MISTRAL_API_KEY=your_key_here" > .env
```

**3. Frontend setup:**
```bash
cd ../frontend
npm install
```

**4. Run both:**

Terminal 1 (Backend):
```bash
cd backend
source venv/bin/activate
python main.py
```

Terminal 2 (Frontend):
```bash
cd frontend
npm run dev
```

**5. Open browser:**
```
http://localhost:3000
```

## 📁 Project Structure

```
mistral-interview/
├── backend/                    # FastAPI Backend
│   ├── main.py                # Application routes and startup
│   ├── config.py              # Configuration management
│   ├── models.py              # Pydantic request/response models
│   ├── services.py            # Business logic (Mistral, URL, Image)
│   ├── exceptions.py          # Custom exception classes
│   ├── requirements.txt       # Python dependencies
│   └── .env                   # Environment variables
│
├── frontend/                   # Next.js Frontend
│   ├── app/
│   │   ├── layout.tsx         # Root layout
│   │   ├── page.tsx           # Main page with state management
│   │   └── globals.css        # Global styles + Mistral tokens
│   ├── components/
│   │   ├── FactChecker.tsx    # Input component (text/url/image)
│   │   └── FactCard.tsx       # Results display component
│   ├── lib/
│   │   └── api.ts             # API client functions
│   ├── types/
│   │   └── index.ts           # TypeScript type definitions
│   ├── package.json           # Node dependencies
│   ├── tailwind.config.js     # Tailwind + Mistral colors
│   └── tsconfig.json          # TypeScript configuration
│
├── .gitignore
└── README.md                   # This file
```

## 💻 Installation

### Backend Setup (Detailed)

1. **Create virtual environment:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

Dependencies include:
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `mistralai` - Mistral AI SDK
- `pydantic` & `pydantic-settings` - Validation & config
- `httpx` - Async HTTP client
- `python-dotenv` - Environment variables

3. **Configure environment:**
```bash
# Create .env file
cat > .env << EOF
MISTRAL_API_KEY=your_mistral_api_key_here

# Optional settings with defaults:
API_TITLE="Mistral Fact Checker API"
API_VERSION="1.0.0"
HOST="0.0.0.0"
PORT=8000
MISTRAL_TEXT_MODEL="mistral-large-latest"
MISTRAL_VISION_MODEL="pixtral-large-latest"
MISTRAL_TEMPERATURE=0.3
MAX_IMAGE_SIZE_MB=10
URL_TIMEOUT_SECONDS=30
EOF
```

4. **Run the server:**
```bash
# Development (auto-reload)
uvicorn main:app --reload --port 8000

# Production
python main.py
```

Server runs at `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`
- Health: `http://localhost:8000/health`

### Frontend Setup (Detailed)

1. **Install dependencies:**
```bash
cd frontend
npm install
```

Dependencies include:
- `next` - React framework
- `react` & `react-dom` - UI library
- `typescript` - Type safety
- `tailwindcss` - Styling
- `axios` - HTTP client
- `lucide-react` - Icons

2. **Configure (optional):**
```bash
# Create .env.local if backend isn't on localhost:8000
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
```

3. **Run development server:**
```bash
npm run dev
```

4. **Build for production:**
```bash
npm run build
npm start
```

Frontend runs at `http://localhost:3000`

## 📚 API Documentation

### Endpoints

#### Health Check
```
GET /
GET /health
```

Response:
```json
{
  "status": "healthy",
  "service": "Mistral Fact Checker API",
  "version": "1.0.0",
  "mistral_connection": "connected"
}
```

#### Fact-Check Text
```
POST /api/fact-check/text
Content-Type: application/json
```

Request:
```json
{
  "text": "The Earth is flat.",
  "context": "Optional context"
}
```

#### Fact-Check URL
```
POST /api/fact-check/url
Content-Type: application/json
```

Request:
```json
{
  "url": "https://example.com/article"
}
```

#### Fact-Check Image
```
POST /api/fact-check/image
Content-Type: multipart/form-data
```

Request: Form data with `file` field (image, max 10MB)

### Response Format (All Endpoints)

```json
{
  "rating": 8.5,
  "explanation": "Brief explanation of the rating",
  "confidence": 0.9,
  "analysis": "Detailed analysis of the content...",
  "correct_aspects": [
    "Verified claim 1",
    "Verified claim 2"
  ],
  "incorrect_aspects": [
    "Misleading claim 1"
  ],
  "sources": [
    {
      "title": "NASA Official Website",
      "url": "https://nasa.gov/...",
      "relevance": "Primary source for space information"
    }
  ],
  "timestamp": "2025-10-13T12:00:00.000000",
  "input_type": "text|url|image"
}
```

### API Testing

**Using curl:**
```bash
# Text fact-check
curl -X POST http://localhost:8000/api/fact-check/text \
  -H "Content-Type: application/json" \
  -d '{"text": "The Earth orbits the Sun."}'

# URL fact-check
curl -X POST http://localhost:8000/api/fact-check/url \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.nasa.gov"}'

# Image fact-check
curl -X POST http://localhost:8000/api/fact-check/image \
  -F "file=@/path/to/image.jpg"
```

**Using Python:**
```python
import requests

response = requests.post(
    "http://localhost:8000/api/fact-check/text",
    json={"text": "The Earth is flat."}
)
result = response.json()
print(f"Rating: {result['rating']}/10")
print(f"Confidence: {result['confidence']}")
```

## 🏗️ Architecture

### System Design

```
┌─────────────┐    HTTP    ┌──────────────┐    API    ┌─────────────┐
│   Next.js   │ ◄────────► │   FastAPI    │ ◄───────► │  Mistral AI │
│   Frontend  │            │   Backend    │           │     API     │
└─────────────┘            └──────────────┘           └─────────────┘
```

### Backend Architecture

**Modular Design with Separation of Concerns:**

- **`main.py`** - FastAPI routes, startup/shutdown, middleware
- **`config.py`** - Pydantic Settings for configuration validation
- **`models.py`** - Request/response Pydantic models
- **`services.py`** - Business logic:
  - `MistralService` - AI interactions
  - `URLFetcherService` - URL content fetching
  - `ImageProcessorService` - Image processing
- **`exceptions.py`** - Custom exception classes with proper HTTP codes

**Key Patterns:**
- Dependency Injection for services
- Async/await for non-blocking I/O
- Lifespan events for startup/shutdown
- Global exception handlers
- Structured logging

### Frontend Architecture

**Component-Based Design:**

- **`app/page.tsx`** - Main page with state management
- **`components/FactChecker.tsx`** - Input handling (text/URL/image)
- **`components/FactCard.tsx`** - Results display
- **`lib/api.ts`** - API client with axios
- **`types/index.ts`** - TypeScript interfaces

**Key Features:**
- React hooks for state management
- Client-side components (`'use client'`)
- Type-safe API calls
- Error boundaries
- Loading states

### Data Flow

1. User inputs content via `FactChecker` component
2. Frontend validates and sends to backend API
3. Backend processes, calls Mistral AI
4. Mistral AI analyzes and returns structured JSON
5. Backend validates response with Pydantic
6. Frontend displays in `FactCard` component

## 🎯 Best Practices

### Code Quality

**Backend:**
- ✅ Full type hints throughout
- ✅ Comprehensive docstrings
- ✅ PEP 8 style guide
- ✅ Modular, DRY code
- ✅ Clear separation of concerns

**Frontend:**
- ✅ TypeScript strict mode
- ✅ Component-based architecture
- ✅ Props typing with interfaces
- ✅ ESLint rules
- ✅ Consistent naming conventions

### Error Handling

- ✅ Custom exception classes
- ✅ Proper HTTP status codes
- ✅ User-friendly error messages
- ✅ Global exception handlers
- ✅ Try-catch blocks with logging

### Security

- ✅ Input validation (Pydantic)
- ✅ File size limits enforced
- ✅ Timeout protection on requests
- ✅ Environment variables for secrets
- ✅ CORS configuration
- ✅ No sensitive data in code

### Performance

- ✅ Async/await throughout
- ✅ Non-blocking I/O
- ✅ Connection pooling
- ✅ Content size limits
- ✅ Efficient data processing
- ✅ Lazy loading of services

### Monitoring & Logging

- ✅ Structured logging
- ✅ Request/response logging
- ✅ Error tracking
- ✅ Health check endpoints
- ✅ Performance metrics in logs

### Configuration

- ✅ Environment-based config
- ✅ Type-safe settings (Pydantic Settings)
- ✅ Sensible defaults
- ✅ Validation on startup
- ✅ Documented options

## 🧪 Testing

### Manual Testing

**Frontend:**
1. Open http://localhost:3000
2. Test each input type:
   - **Text**: "The Earth is flat"
   - **URL**: "https://www.nasa.gov"
   - **Image**: Upload screenshot with text
3. Verify results display correctly
4. Test share functionality
5. Test responsive design (mobile/tablet/desktop)

**Backend:**
```bash
# Health check
curl http://localhost:8000/health

# Test text endpoint
curl -X POST http://localhost:8000/api/fact-check/text \
  -H "Content-Type: application/json" \
  -d '{"text": "Water boils at 100°C at sea level."}'

# Check API docs
open http://localhost:8000/docs
```

### Type Checking

**Frontend:**
```bash
cd frontend
npm run type-check
```

**Backend:**
```bash
cd backend
mypy main.py  # (if mypy installed)
```

## 🐛 Troubleshooting

### Backend Issues

**"MISTRAL_API_KEY environment variable is required"**
```bash
cd backend
echo "MISTRAL_API_KEY=your_key_here" > .env
```

**"Port already in use"**
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use different port
PORT=8001 python main.py
```

**"Module not found" errors**
```bash
pip install -r requirements.txt
# Make sure pydantic-settings is installed
pip install pydantic-settings
```

### Frontend Issues

**"Module not found: Can't resolve 'tailwindcss'"**
```bash
cd frontend
rm -rf .next node_modules package-lock.json
npm install
npm run dev
```

**"Connection refused" when calling API**
- Ensure backend is running on port 8000
- Check `.env.local` for correct API URL
- Verify CORS settings in backend

**Build errors**
```bash
# Clean build
rm -rf .next
npm run build
```

### General Issues

**Disk space errors**
```bash
# Clean npm cache
npm cache clean --force

# Clean Python cache
find . -type d -name "__pycache__" -exec rm -r {} +
```

**API returns errors**
- Check backend logs for details
- Verify Mistral AI API key is valid
- Check API rate limits
- Ensure proper JSON format in requests

## 🎨 Mistral Design System

The application follows Mistral AI's design guidelines:

### Colors
```css
--mistral-orange: #FF7000    /* Primary */
--mistral-dark: #0F0F0F      /* Background */
--mistral-gray: #1A1A1A      /* Surface */
--mistral-light-gray: #2A2A2A /* Borders */
--mistral-text: #E5E5E5      /* Text */
--mistral-accent: #FF8533    /* Hover states */
```

### Typography
- Font: Inter (Google Fonts)
- Weights: 300, 400, 500, 600, 700, 800

### Components
- Rounded corners (12-24px)
- Smooth transitions (0.3s ease)
- Orange accent highlights
- Dark theme throughout
- Subtle shadows and gradients

## 📦 Dependencies

### Backend
```
fastapi==0.115.0              # Web framework
uvicorn[standard]==0.30.6     # ASGI server
mistralai==1.2.0              # Mistral AI SDK
pydantic==2.9.2               # Data validation
pydantic-settings==2.5.2      # Config management
httpx==0.27.2                 # Async HTTP client
python-multipart==0.0.9       # File upload support
python-dotenv==1.0.1          # Environment variables
```

### Frontend
```
next: 14.2.18                 # React framework
react: 18.3.1                 # UI library
typescript: 5                 # Type safety
tailwindcss: 3.4.1            # Styling
axios: 1.7.7                  # HTTP client
lucide-react: 0.451.0         # Icons
```

## 🔄 Development Workflow

1. **Make changes** to code
2. **Server auto-reloads** (in dev mode)
3. **Test via UI** or `/docs`
4. **Check logs** for errors
5. **Type check** before committing
6. **Commit** with clear messages

## 📈 Future Enhancements

- [ ] User authentication
- [ ] Save fact-check history
- [ ] Export results as PDF
- [ ] Batch processing
- [ ] Rate limiting
- [ ] Caching (Redis)
- [ ] Database integration
- [ ] WebSocket for real-time updates
- [ ] Docker containerization
- [ ] CI/CD pipeline
- [ ] Monitoring (Prometheus/Grafana)
- [ ] Browser extension

## 📄 License

This project is created for the Mistral AI interview process.

## 👤 Author

Built with ❤️ for Mistral AI

## 🙏 Acknowledgments

- **Mistral AI** - Powerful language models
- **Next.js** - Amazing React framework
- **FastAPI** - Modern Python web framework
- **Tailwind CSS** - Utility-first CSS

---

<div align="center">

**Made with Mistral AI** • **Built for Excellence**

🚀 Ready for Production • ✨ Clean Code • 📚 Well Documented

</div>
