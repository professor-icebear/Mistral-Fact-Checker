# Mistral Fact Checker

<div align="center">

![Mistral AI](https://img.shields.io/badge/Powered%20by-Mistral%20AI-FF7000?style=for-the-badge)
![Next.js](https://img.shields.io/badge/Next.js-14-black?style=for-the-badge&logo=next.js)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi)
![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?style=for-the-badge&logo=typescript)
![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python)

**AI-Powered Fact Checking Application**

[Live Demo](https://fanciful-jelly-4022e8.netlify.app/) • [API Docs](http://localhost:8000/docs)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [AI Integration](#-ai-integration)
- [Features](#-features)
- [Quick Start](#-quick-start)
- [API Documentation](#-api-documentation)
- [Architecture](#-architecture)
- [Testing](#-testing)
- [Troubleshooting](#-troubleshooting)

## 🎯 Overview

Production-ready fact-checking application leveraging Mistral AI's language models to verify information from text, URLs, and images. Built for the **Mistral AI Software Engineer internship**, demonstrating full-stack development skills, AI integration expertise, and production best practices.

**Key Highlights:**
- ✅ Clean, modular architecture with separation of concerns
- ✅ Production-ready error handling and type safety
- ✅ Advanced AI integration with structured prompts and source validation
- ✅ Beautiful UI following Mistral design system

## 🤖 AI Integration

### Mistral Models Used

**Text & URL Analysis:** `mistral-large-latest`
- Best-in-class reasoning and comprehensive fact-checking
- Structured output with JSON mode for reliable parsing

**Image Analysis:** `pixtral-large-latest`
- Multimodal vision model for OCR and visual content understanding
- Processes images up to 10MB

### Prompt Engineering Strategy

The application uses **structured prompting** with explicit instructions for consistent, high-quality outputs:

```python
# Example prompt structure (services.py)
system_prompt = """You are a fact-checking expert. Analyze content and return structured JSON."""

user_prompt = f"""
Fact-check the following: {content}

Provide:
1. Rating (0-10): Accuracy score
2. Confidence (0.0-1.0): Your certainty level
3. Analysis: Detailed reasoning
4. Correct/Incorrect aspects: Specific claims with verification
5. Sources: Credible references with URLs
"""
```

### Key Implementation Details

**Temperature Control:** Set to `0.3` for consistent, factual outputs (configurable via `MISTRAL_TEMPERATURE`)

**Response Validation:** Uses Pydantic models to ensure Mistral returns properly structured JSON:
```python
class FactCheckResult(BaseModel):
    rating: float  # 0-10 scale
    confidence: float  # 0.0-1.0
    analysis: str
    correct_aspects: List[str]
    incorrect_aspects: List[str]
    sources: List[Source]  # title, url, relevance
```

**Source Generation:** LLM identifies relevant authoritative sources based on content domain (scientific claims → academic journals, news → reputable outlets)

**Multi-Input Processing:**
- **Text:** Direct LLM analysis with context awareness
- **URLs:** Fetches content via `httpx`, extracts text, then analyzes
- **Images:** Converts to base64, sends to Pixtral with vision-specific prompts

### Output Scoring System

The rating (0-10) is derived from:
- **Factual accuracy:** Cross-referenced against LLM's knowledge base
- **Source credibility:** Quality and recency of supporting evidence
- **Claim specificity:** Verifiable vs. subjective statements

Confidence score reflects the model's certainty based on available information and claim complexity.

## ✨ Features

**Core Functionality:**
- 📝 Text, 🔗 URL, and 🖼️ Image fact-checking with comprehensive reports
- 📊 Structured results: rating, confidence, analysis, sources
- 📤 Share functionality and responsive design

**Technical:**
- 🎨 Mistral design system, 🔐 password protection, 🔒 full type safety
- 🛡️ Robust error handling, ⚙️ environment-based config
- 🚀 Async/await, connection pooling, production-ready

## 🚀 Quick Start

### Prerequisites
- Node.js 18+, Python 3.9+
- Mistral AI API key from [console.mistral.ai](https://console.mistral.ai/)

### Setup & Run

```bash
# Backend
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
echo "MISTRAL_API_KEY=your_key_here" > .env
python main.py  # Runs on http://localhost:8000

# Frontend (new terminal)
cd frontend
npm install
echo "NEXT_PUBLIC_APP_PASSWORD=demo123" > .env.local
npm run dev  # Runs on http://localhost:3000
```

**🌐 Live Demo:** [https://fanciful-jelly-4022e8.netlify.app/](https://fanciful-jelly-4022e8.netlify.app/)

### Tech Stack
- **Frontend:** Next.js 14, TypeScript, Tailwind CSS, Axios
- **Backend:** FastAPI, Mistral AI SDK, Pydantic, httpx
- **Architecture:** Modular design, dependency injection, async/await

## 📁 Project Structure

```
backend/
├── main.py         # FastAPI routes, startup/shutdown
├── config.py       # Pydantic settings & validation
├── models.py       # Request/response schemas
├── services.py     # Mistral AI, URL fetching, image processing
└── exceptions.py   # Custom exceptions

frontend/
├── app/page.tsx              # Main UI with state management
├── components/
│   ├── FactChecker.tsx       # Input forms (text/url/image)
│   ├── FactCard.tsx          # Results display
│   └── PasswordGate.tsx      # Auth component
├── lib/api.ts                # API client
└── types/index.ts            # TypeScript interfaces
```

<details>
<summary><b>⚙️ Configuration Options</b></summary>

**Backend `.env`:**
```bash
MISTRAL_API_KEY=required
MISTRAL_TEXT_MODEL=mistral-large-latest
MISTRAL_VISION_MODEL=pixtral-large-latest
MISTRAL_TEMPERATURE=0.3
MAX_IMAGE_SIZE_MB=10
```

**Frontend `.env.local`:**
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_PASSWORD=your_password
```
</details>

## 📚 API Documentation

**Interactive Docs:** `http://localhost:8000/docs`

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/api/fact-check/text` | Fact-check text input |
| `POST` | `/api/fact-check/url` | Fact-check URL content |
| `POST` | `/api/fact-check/image` | Fact-check image (multipart/form-data) |

### Response Format

```json
{
  "rating": 8.5,              // 0-10 accuracy score
  "confidence": 0.9,          // 0.0-1.0 certainty
  "explanation": "Brief summary",
  "analysis": "Detailed reasoning",
  "correct_aspects": ["Verified claim 1", "..."],
  "incorrect_aspects": ["Misleading claim 1"],
  "sources": [
    {"title": "NASA", "url": "https://...", "relevance": "Primary source"}
  ],
  "timestamp": "2025-10-13T12:00:00",
  "input_type": "text|url|image"
}
```

<details>
<summary><b>Example Usage</b></summary>

```bash
# Text
curl -X POST http://localhost:8000/api/fact-check/text \
  -H "Content-Type: application/json" \
  -d '{"text": "Water boils at 100°C at sea level."}'

# URL
curl -X POST http://localhost:8000/api/fact-check/url \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.nasa.gov"}'

# Image
curl -X POST http://localhost:8000/api/fact-check/image \
  -F "file=@image.jpg"
```
</details>

## 🏗️ Architecture

```
┌─────────────┐          ┌──────────────┐          ┌─────────────┐
│   Next.js   │  ◄────►  │   FastAPI    │  ◄────►  │  Mistral AI │
│   Frontend  │   HTTP   │   Backend    │   API    │   (LLM)     │
└─────────────┘          └──────────────┘          └─────────────┘
```

### Backend: Modular Design
- **`main.py`** - FastAPI routes, lifespan events, global exception handlers
- **`services.py`** - `MistralService`, `URLFetcherService`, `ImageProcessorService`
- **`models.py`** - Pydantic request/response validation
- **`config.py`** - Type-safe settings with Pydantic Settings
- **`exceptions.py`** - Custom exceptions with HTTP codes

**Patterns:** Dependency injection, async/await, structured logging

### Frontend: Component-Based
- **`page.tsx`** - State management (useState, error handling)
- **`FactChecker.tsx`** - Input forms with validation
- **`FactCard.tsx`** - Results display with responsive design
- **`api.ts`** - Axios client with error handling

**Patterns:** React hooks, TypeScript strict mode, type-safe API calls

## 🎯 Best Practices Implemented

**Security:** Input validation (Pydantic), file size limits, timeouts, env secrets, CORS  
**Performance:** Async/await, non-blocking I/O, connection pooling  
**Code Quality:** Full type hints, modular architecture, PEP 8, ESLint  
**Error Handling:** Custom exceptions, proper HTTP codes, global handlers  
**Monitoring:** Structured logging, health checks, request/response tracking

## 🧪 Testing

### Run Tests
```bash
cd backend
source venv/bin/activate
pytest test_main.py -v
```

**Coverage:** Health checks, text/URL/image fact-checking, response validation, error handling  
**Note:** Tests use mocked Mistral AI service (no API calls)

### Quick Manual Test
```bash
# Backend health
curl http://localhost:8000/health

# Test fact-checking
curl -X POST http://localhost:8000/api/fact-check/text \
  -H "Content-Type: application/json" \
  -d '{"text": "The Earth orbits the Sun."}'

# Frontend: Open http://localhost:3000
# Try text, URL (nasa.gov), and image inputs
```

## 🐛 Troubleshooting

<details>
<summary><b>Common Issues</b></summary>

**Backend**
```bash
# Missing API key
echo "MISTRAL_API_KEY=your_key" > backend/.env

# Port already in use
lsof -ti:8000 | xargs kill -9

# Module not found
pip install -r requirements.txt
```

**Frontend**
```bash
# Connection refused
# → Ensure backend is running on port 8000
# → Check NEXT_PUBLIC_API_URL in .env.local

# Build errors
rm -rf .next node_modules && npm install
```

**API Errors**
- Check backend logs for details
- Verify Mistral API key is valid
- Ensure proper JSON format in requests
</details>

---

## 📄 License

Created for the Mistral AI interview process.

## 🔗 Resources

- **Mistral AI Documentation:** [docs.mistral.ai](https://docs.mistral.ai)
- **FastAPI Docs:** [fastapi.tiangolo.com](https://fastapi.tiangolo.com)
- **Next.js Docs:** [nextjs.org/docs](https://nextjs.org/docs)
