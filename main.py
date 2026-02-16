import os
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

from document_generator import DocumentGenerator
from node_fetcher import fetch_project_context, build_headers

load_dotenv()

APP_TITLE = "NEXA Documentation Generation Agent"
APP_VERSION = "1.0.0"

# API key auth (service-to-service)
API_KEY_HEADER = os.getenv("DOC_AGENT_API_KEY_HEADER", "X-API-Key")
API_KEY = os.getenv("DOC_AGENT_API_KEY", "")


def _get_header(headers: Dict[str, str], name: str) -> Optional[str]:
    """Case-insensitive header lookup"""
    for k, v in headers.items():
        if k.lower() == name.lower():
            return v
    return None


def _require_api_key(raw_headers: Dict[str, str]):
    """Validate API key for service-to-service authentication"""
    if not API_KEY:
        return  # Allow local/dev usage
    incoming = _get_header(raw_headers, API_KEY_HEADER)
    if not incoming or incoming != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing agent API key")


class CustomSection(BaseModel):
    """User-defined custom section"""
    title: str
    description: Optional[str] = None


class SelectedSection(BaseModel):
    """Section selected by user"""
    id: str = Field(..., description="Section ID (e.g., '1.1', '2.3')")
    title: str = Field(..., description="Section title")


class GenerateDocumentRequest(BaseModel):
    """Request model for document generation"""
    documentType: str = Field(..., description="Type of document to generate (SRS, SPRINT_REPORT, etc.)")
    projectId: str = Field(..., description="Project ID to gather context from")
    sprintId: Optional[str] = Field(None, description="Sprint ID (for sprint-specific documents)")
    userRequirements: Optional[str] = Field(None, description="User's specific requirements and focus areas")
    selectedSections: List[SelectedSection] = Field(default_factory=list, description="Sections selected by user")
    customSections: List[CustomSection] = Field(default_factory=list, description="Custom sections to include")
    additionalNotes: Optional[str] = Field(None, description="Additional instructions for the AI")
    includeDataSummary: bool = Field(True, description="Include project data summary in document")


class GenerateDocumentResponse(BaseModel):
    """Response model for document generation"""
    success: bool
    document: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class ListDocumentTypesResponse(BaseModel):
    """Response model for listing available document types"""
    success: bool
    documentTypes: List[Dict[str, Any]]
    categories: List[str]


app = FastAPI(
    title=APP_TITLE,
    version=APP_VERSION,
    description="AI-powered professional documentation generation agent using Gemini API"
)

# Initialize document generator
generator = DocumentGenerator()


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "ok": True,
        "service": APP_TITLE,
        "version": APP_VERSION
    }


@app.get("/ready")
async def ready():
    """Readiness probe endpoint"""
    return {
        "ok": True,
        "ready": True,
        "gemini_configured": bool(os.getenv("GEMINI_API_KEY"))
    }


@app.get("/api/documentation/types", response_model=ListDocumentTypesResponse)
async def list_document_types(request: Request):
    """
    List all available document types with their structures
    """
    raw_headers = {k: v for k, v in request.headers.items()}
    _require_api_key(raw_headers)
    
    try:
        document_types = generator.get_document_types()
        categories = generator.get_categories()
        
        return {
            "success": True,
            "documentTypes": document_types,
            "categories": categories
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list document types: {str(e)}")


@app.get("/api/documentation/types/{document_type}/structure")
async def get_document_structure(document_type: str, request: Request):
    """
    Get the complete section structure for a specific document type
    Returns detailed sections with descriptions for user selection
    """
    raw_headers = {k: v for k, v in request.headers.items()}
    _require_api_key(raw_headers)
    
    print(f"\n[STRUCTURE] Request for document type: {document_type}")
    print(f"[STRUCTURE] Uppercased: {document_type.upper()}")
    
    try:
        structure = generator.get_document_structure(document_type.upper())
        print(f"[STRUCTURE] Generator returned: {structure is not None}")
        
        if not structure:
            print(f"[ERROR] Document type '{document_type.upper()}' not found in DOCUMENT_TYPES")
            print(f"[DEBUG] Available types: {list(generator.get_document_types())}")
            raise HTTPException(status_code=404, detail=f"Document type '{document_type}' not found")
        
        print(f"[SUCCESS] Returning structure with {len(structure.get('structure', []))} sections")
        
        return {
            "success": True,
            "documentType": document_type.upper(),
            "structure": structure
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Exception in get_document_structure: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get structure: {str(e)}")


@app.post("/api/documentation/generate", response_model=GenerateDocumentResponse)
async def generate_document(req: GenerateDocumentRequest, request: Request):
    """
    Generate a professional document using AI
    
    This endpoint:
    1. Fetches project context from Node backend
    2. Builds intelligent prompt with document structure
    3. Calls Gemini API to generate professional content
    4. Returns structured markdown document
    """
    raw_headers = {k: v for k, v in request.headers.items()}
    _require_api_key(raw_headers)
    
    print(f"\n{'='*60}")
    print(f"[REQUEST] New document generation request")
    print(f"[REQUEST] Document Type: {req.documentType}")
    print(f"[REQUEST] Project ID: {req.projectId}")
    print(f"[REQUEST] Sprint ID: {req.sprintId}")
    print(f"[REQUEST] Headers received: {list(raw_headers.keys())}")
    print(f"{'='*60}\n")
    
    try:
        # Build headers for Node backend calls
        headers = build_headers(raw_headers)
        
        # Fetch project context from Node backend
        print(f"[FETCH] Fetching project context for projectId={req.projectId}")
        project_context = await fetch_project_context(
            project_id=req.projectId,
            sprint_id=req.sprintId,
            headers=headers
        )
        
        print(f"[SUCCESS] Fetched context: {len(project_context.get('tasks', []))} tasks, {len(project_context.get('sprints', []))} sprints")
        
        # Prepare selected sections
        selected_sections = [
            {
                "id": section.id,
                "title": section.title
            }
            for section in req.selectedSections
        ]
        
        # Prepare custom sections
        custom_sections = [
            {
                "title": section.title,
                "description": section.description
            }
            for section in req.customSections
        ]
        
        # Generate document using Gemini
        print(f"[AI] Generating {req.documentType} document...")
        if selected_sections:
            print(f"[AI] User selected {len(selected_sections)} specific sections")
        
        result = await generator.generate_document(
            document_type=req.documentType,
            project_context=project_context,
            user_requirements=req.userRequirements,
            selected_sections=selected_sections,
            custom_sections=custom_sections,
            additional_notes=req.additionalNotes,
            include_data_summary=req.includeDataSummary
        )
        
        if not result.get("success"):
            raise HTTPException(
                status_code=500,
                detail=result.get("error", "Document generation failed")
            )
        
        print(f"[SUCCESS] Document generated successfully: {result['document']['wordCount']} words")
        
        return {
            "success": True,
            "document": result["document"],
            "metadata": result["metadata"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Error generating document: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Document generation failed: {str(e)}"
        )


@app.get("/api/documentation/structure/{document_type}")
async def get_document_structure(document_type: str, request: Request):
    """
    Get the structure/template for a specific document type
    """
    raw_headers = {k: v for k, v in request.headers.items()}
    _require_api_key(raw_headers)
    
    try:
        structure = generator.get_document_structure(document_type)
        
        if not structure:
            raise HTTPException(
                status_code=404,
                detail=f"Document type '{document_type}' not found"
            )
        
        return {
            "success": True,
            "documentType": document_type,
            "structure": structure
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get document structure: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", "8003"))
    print(f"[START] Starting {APP_TITLE} on port {port}")
    print(f"[CONFIG] Gemini API configured: {bool(os.getenv('GEMINI_API_KEY'))}")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
