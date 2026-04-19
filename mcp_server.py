"""
MCP Server for NEXA Documentation Generation Agent.

Exposes document generation capabilities as MCP tools via FastMCP (Streamable HTTP
transport). Mounted on the existing FastAPI app under /mcp — all original REST
endpoints remain completely intact.
"""

from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
load_dotenv()

from mcp.server.fastmcp import FastMCP

# Import core generator class directly (avoids circular import with main.py)
from document_generator import DocumentGenerator

mcp = FastMCP(
    "nexa-documentation-generator",
    instructions=(
        "Generates professional project documentation (SRS, Sprint Report, Architecture Doc, "
        "User Manual, API Documentation, Test Plan, Project Charter, Design Document, "
        "Technical Specification) using AI and real project data from MongoDB. "
        "Call list_document_types first to discover available types, "
        "get_document_structure to let users choose sections, "
        "then generate_document to produce the final Markdown document."
    ),
)

# Shared generator instance (same class used by REST handlers)
_generator = DocumentGenerator()


@mcp.tool()
def list_document_types() -> Dict[str, Any]:
    """
    List all available document types with their names, categories and descriptions.

    Returns documentTypes (list of {id, name, description, category}) and
    categories (list of category strings).
    """
    return {
        "success": True,
        "documentTypes": _generator.get_document_types(),
        "categories": _generator.get_categories(),
    }


@mcp.tool()
def get_document_structure(document_type: str) -> Dict[str, Any]:
    """
    Get the complete section structure for a specific document type so that
    the user can select which sections to include.

    document_type must be one of: SRS, SPRINT_REPORT, ARCHITECTURE_DOC,
    USER_MANUAL, API_DOCUMENTATION, TEST_PLAN, PROJECT_CHARTER,
    DESIGN_DOCUMENT, TECHNICAL_SPEC.

    Returns structure object with sections, subsections, descriptions,
    required/selectable flags.
    """
    structure = _generator.get_document_structure(document_type.upper())
    if not structure:
        return {
            "success": False,
            "error": f"Document type '{document_type.upper()}' not found. "
                     "Call list_document_types() to see available types.",
        }
    return {"success": True, "documentType": document_type.upper(), "structure": structure}


@mcp.tool()
async def generate_document(
    document_type: str,
    project_id: str,
    auth_token: str,
    sprint_id: Optional[str] = None,
    user_requirements: Optional[str] = None,
    selected_sections: Optional[List[Dict[str, str]]] = None,
    custom_sections: Optional[List[Dict[str, str]]] = None,
    additional_notes: Optional[str] = None,
    include_data_summary: bool = True,
) -> Dict[str, Any]:
    """
    Generate a professional document using AI from live project data.

    document_type: e.g. SRS, SPRINT_REPORT, ARCHITECTURE_DOC.
    project_id: MongoDB project _id to pull tasks, sprints, team, blockers from.
    auth_token: Bearer token (with or without 'Bearer ' prefix) for Node API auth.
    sprint_id: Required only for SPRINT_REPORT. Accepts string ID like 'SPRINT-202602021520'.
    user_requirements: Free-text focus areas (e.g. 'Focus on authentication and security').
    selected_sections: List of {id, title} dicts. Only these sections are generated.
                       Leave empty to generate all sections for the document type.
    custom_sections: Additional user-defined sections as {title, description} dicts.
    additional_notes: Extra instructions for the AI writer.
    include_data_summary: Whether to include a project data statistics box in output.

    Returns: success, document {title, content (Markdown), wordCount, sections},
             metadata {generatedAt, model, documentType, projectId}.
    """
    from node_fetcher import build_headers, fetch_project_context

    # Build auth headers for Node backend
    token = auth_token.strip()
    if not token.startswith("Bearer "):
        token = f"Bearer {token}"
    raw_headers: Dict[str, str] = {"authorization": token}
    headers = build_headers(raw_headers)

    # Fetch live project context from Node backend
    project_context = await fetch_project_context(
        project_id=project_id,
        sprint_id=sprint_id,
        headers=headers,
    )

    # Generate document via Gemini
    result = await _generator.generate_document(
        document_type=document_type,
        project_context=project_context,
        user_requirements=user_requirements,
        selected_sections=selected_sections or [],
        custom_sections=custom_sections or [],
        additional_notes=additional_notes,
        include_data_summary=include_data_summary,
    )

    if not result.get("success"):
        return {
            "success": False,
            "error": result.get("error", "Document generation failed"),
        }

    return {
        "success": True,
        "document": result["document"],
        "metadata": result.get("metadata", {}),
    }
