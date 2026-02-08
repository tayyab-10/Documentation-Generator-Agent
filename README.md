# NEXA Documentation Generation Agent

AI-powered professional documentation generation agent using Google's Gemini API.

## Features

- **8 Professional Document Types**: SRS, Sprint Reports, Architecture Docs, User Manuals, API Docs, Test Plans, Project Charters, Design Documents
- **Industry Standards**: Follows IEEE, arc42, and Agile best practices
- **Context-Aware**: Uses actual project data from NEXA backend
- **High Accuracy**: Data-driven generation with no hallucinations
- **Flexible**: Supports custom sections and user requirements
- **Professional**: Technical writing quality output

## Document Types Supported

1. **SRS (Software Requirements Specification)** - IEEE 830-1998 compliant
2. **Sprint Report** - Comprehensive agile sprint summary
3. **Software Architecture Document** - arc42 framework based
4. **User Manual** - End-user documentation
5. **API Documentation** - REST API reference
6. **Test Plan** - QA testing strategy
7. **Project Charter** - Project authorization document
8. **Design Document** - Technical design specifications

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Create `.env` file:

```bash
cp .env.example .env
```

Edit `.env` and add your configuration:

```env
GEMINI_API_KEY=your_gemini_api_key_here
DOC_AGENT_GEMINI_MODEL=gemini-2.0-flash-exp
NODE_BASE_URL=https://nexa-au2s.onrender.com/api
DOC_AGENT_API_KEY=optional_service_key
PORT=8003
```

### 3. Run Locally

```bash
python main.py
```

Or with uvicorn:

```bash
uvicorn main:app --host 0.0.0.0 --port 8003 --reload
```

## API Endpoints

### Health Check
```
GET /health
GET /ready
```

### List Document Types
```
GET /api/documentation/types
```

Response:
```json
{
  "success": true,
  "documentTypes": [...],
  "categories": ["Requirements", "Agile", "Architecture", ...]
}
```

### Get Document Structure
```
GET /api/documentation/structure/{document_type}
```

### Generate Document
```
POST /api/documentation/generate
```

Request:
```json
{
  "documentType": "SPRINT_REPORT",
  "projectId": "507f1f77bcf86cd799439011",
  "sprintId": "507f1f77bcf86cd799439012",
  "userRequirements": "Focus on team performance and blockers",
  "customSections": [
    {
      "title": "Stakeholder Feedback",
      "description": "Include feedback from stakeholders"
    }
  ],
  "additionalNotes": "Make it executive-friendly",
  "includeDataSummary": true
}
```

Response:
```json
{
  "success": true,
  "document": {
    "title": "Sprint Report",
    "content": "# Sprint Report\n\n## Executive Summary...",
    "sections": [...],
    "wordCount": 2500,
    "documentType": "Sprint Report",
    "category": "Agile"
  },
  "metadata": {
    "documentType": "SPRINT_REPORT",
    "generatedAt": "2026-02-07T...",
    "model": "gemini-2.0-flash-exp",
    "projectId": "...",
    "sprintId": "..."
  }
}
```

## Deployment

### Render.com

1. Create new Web Service
2. Connect your repository
3. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Environment Variables**: Add GEMINI_API_KEY, NODE_BASE_URL, etc.

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8003

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8003"]
```

## Architecture

```
Node Backend (Request)
    ↓
Documentation Agent (FastAPI)
    ↓
1. Fetch project context from Node API
   - Project info, tasks, sprints, team
    ↓
2. Build intelligent prompt
   - Document structure template
   - Project data injection
   - User requirements
    ↓
3. Call Gemini API
   - Generate professional content
    ↓
4. Parse and structure output
   - Extract sections
   - Format markdown
    ↓
5. Return to Node Backend
   - Structured document
   - Metadata
```

## Quality Guarantees

- ✅ **Accurate**: Only uses real project data
- ✅ **Professional**: Industry-standard formats
- ✅ **Comprehensive**: Deep project context
- ✅ **Flexible**: Custom sections supported
- ✅ **Fast**: Async operations with httpx
- ✅ **Reliable**: Error handling and retries

## File Structure

```
Documentation Generation Agent/
├── main.py                     # FastAPI app and endpoints
├── document_generator.py       # Gemini-powered generation logic
├── document_templates.py       # Document structures and templates
├── node_fetcher.py            # Node backend integration
├── requirements.txt           # Python dependencies
├── .env.example              # Environment template
├── .env                      # Environment config (gitignored)
├── .gitignore               # Git ignore file
└── README.md                # This file
```

## Example Usage

### Generate Sprint Report

```bash
curl -X POST http://localhost:8003/api/documentation/generate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "documentType": "SPRINT_REPORT",
    "projectId": "507f1f77bcf86cd799439011",
    "sprintId": "507f1f77bcf86cd799439012",
    "userRequirements": "Focus on blockers and team performance"
  }'
```

### Generate SRS

```bash
curl -X POST http://localhost:8003/api/documentation/generate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "documentType": "SRS",
    "projectId": "507f1f77bcf86cd799439011",
    "userRequirements": "Include all functional and non-functional requirements"
  }'
```

## License

Part of NEXA Project Management System

## Support

For issues or questions, contact the NEXA development team.
# Documentation-Generator-Agent
