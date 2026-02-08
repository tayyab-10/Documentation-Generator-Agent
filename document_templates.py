"""
Document Templates and Structures
Defines professional document types based on industry standards
"""

DOCUMENT_TYPES = {
    "SRS": {
        "name": "Software Requirements Specification (SRS)",
        "description": "IEEE 830-1998 compliant requirements specification",
        "category": "Requirements",
        "icon": "FileText",
        "structure": [
            {
                "section": "1",
                "title": "Introduction",
                "subsections": [
                    {"id": "1.1", "title": "Purpose", "required": True},
                    {"id": "1.2", "title": "Scope", "required": True},
                    {"id": "1.3", "title": "Definitions, Acronyms, and Abbreviations", "required": True},
                    {"id": "1.4", "title": "References", "required": False},
                    {"id": "1.5", "title": "Overview", "required": True},
                ]
            },
            {
                "section": "2",
                "title": "Overall Description",
                "subsections": [
                    {"id": "2.1", "title": "Product Perspective", "required": True},
                    {"id": "2.2", "title": "Product Functions", "required": True},
                    {"id": "2.3", "title": "User Characteristics", "required": True},
                    {"id": "2.4", "title": "Constraints", "required": True},
                    {"id": "2.5", "title": "Assumptions and Dependencies", "required": True},
                ]
            },
            {
                "section": "3",
                "title": "Specific Requirements",
                "subsections": [
                    {"id": "3.1", "title": "Functional Requirements", "required": True},
                    {"id": "3.2", "title": "Interface Requirements", "required": True},
                    {"id": "3.3", "title": "Performance Requirements", "required": True},
                    {"id": "3.4", "title": "Design Constraints", "required": False},
                    {"id": "3.5", "title": "Quality Attributes", "required": True},
                    {"id": "3.6", "title": "Other Requirements", "required": False},
                ]
            },
            {
                "section": "Appendix",
                "title": "Appendices",
                "subsections": [
                    {"id": "A", "title": "Data Flow Diagrams", "required": False},
                    {"id": "B", "title": "Use Case Diagrams", "required": False},
                ]
            }
        ]
    },
    
    "SPRINT_REPORT": {
        "name": "Sprint Report",
        "description": "Comprehensive agile sprint summary and metrics",
        "category": "Agile",
        "icon": "Calendar",
        "structure": [
            {
                "section": "1",
                "title": "Executive Summary",
                "subsections": [
                    {"id": "1.1", "title": "Sprint Overview", "required": True},
                    {"id": "1.2", "title": "Sprint Goals Achievement", "required": True},
                    {"id": "1.3", "title": "Overall Status", "required": True},
                ]
            },
            {
                "section": "2",
                "title": "Sprint Metrics",
                "subsections": [
                    {"id": "2.1", "title": "Velocity and Capacity", "required": True},
                    {"id": "2.2", "title": "Burndown Analysis", "required": True},
                    {"id": "2.3", "title": "Task Completion Rate", "required": True},
                    {"id": "2.4", "title": "Story Points Delivered", "required": True},
                ]
            },
            {
                "section": "3",
                "title": "Work Completed",
                "subsections": [
                    {"id": "3.1", "title": "Completed Tasks", "required": True},
                    {"id": "3.2", "title": "Key Achievements", "required": True},
                    {"id": "3.3", "title": "Business Value Delivered", "required": True},
                ]
            },
            {
                "section": "4",
                "title": "Challenges and Blockers",
                "subsections": [
                    {"id": "4.1", "title": "Blockers Encountered", "required": True},
                    {"id": "4.2", "title": "Unfinished Work", "required": True},
                    {"id": "4.3", "title": "Risk Mitigation Actions", "required": False},
                ]
            },
            {
                "section": "5",
                "title": "Team Insights",
                "subsections": [
                    {"id": "5.1", "title": "Team Performance", "required": True},
                    {"id": "5.2", "title": "Workload Distribution", "required": True},
                    {"id": "5.3", "title": "Process Improvements", "required": True},
                ]
            },
            {
                "section": "6",
                "title": "Next Steps",
                "subsections": [
                    {"id": "6.1", "title": "Upcoming Sprint Goals", "required": True},
                    {"id": "6.2", "title": "Action Items", "required": True},
                    {"id": "6.3", "title": "Recommendations", "required": True},
                ]
            }
        ]
    },
    
    "ARCHITECTURE_DOC": {
        "name": "Software Architecture Document",
        "description": "arc42-based architecture documentation",
        "category": "Architecture",
        "icon": "Layers",
        "structure": [
            {
                "section": "1",
                "title": "Introduction and Goals",
                "subsections": [
                    {"id": "1.1", "title": "Requirements Overview", "required": True},
                    {"id": "1.2", "title": "Quality Goals", "required": True},
                    {"id": "1.3", "title": "Stakeholders", "required": True},
                ]
            },
            {
                "section": "2",
                "title": "Architecture Constraints",
                "subsections": [
                    {"id": "2.1", "title": "Technical Constraints", "required": True},
                    {"id": "2.2", "title": "Organizational Constraints", "required": False},
                ]
            },
            {
                "section": "3",
                "title": "System Scope and Context",
                "subsections": [
                    {"id": "3.1", "title": "Business Context", "required": True},
                    {"id": "3.2", "title": "Technical Context", "required": True},
                ]
            },
            {
                "section": "4",
                "title": "Solution Strategy",
                "subsections": [
                    {"id": "4.1", "title": "Technology Decisions", "required": True},
                    {"id": "4.2", "title": "System Decomposition", "required": True},
                ]
            },
            {
                "section": "5",
                "title": "Building Block View",
                "subsections": [
                    {"id": "5.1", "title": "System Overview", "required": True},
                    {"id": "5.2", "title": "Component Architecture", "required": True},
                ]
            },
            {
                "section": "6",
                "title": "Runtime View",
                "subsections": [
                    {"id": "6.1", "title": "Key Scenarios", "required": True},
                    {"id": "6.2", "title": "Component Interactions", "required": True},
                ]
            },
            {
                "section": "7",
                "title": "Deployment View",
                "subsections": [
                    {"id": "7.1", "title": "Infrastructure Overview", "required": True},
                    {"id": "7.2", "title": "Deployment Architecture", "required": True},
                ]
            },
            {
                "section": "8",
                "title": "Crosscutting Concepts",
                "subsections": [
                    {"id": "8.1", "title": "Security Concepts", "required": True},
                    {"id": "8.2", "title": "Error Handling Strategy", "required": True},
                ]
            },
            {
                "section": "9",
                "title": "Architecture Decisions",
                "subsections": [
                    {"id": "9.1", "title": "Key Decisions and Rationale", "required": True},
                ]
            },
            {
                "section": "10",
                "title": "Quality Requirements",
                "subsections": [
                    {"id": "10.1", "title": "Performance Requirements", "required": True},
                    {"id": "10.2", "title": "Security Requirements", "required": True},
                ]
            },
            {
                "section": "11",
                "title": "Risks and Technical Debt",
                "subsections": [
                    {"id": "11.1", "title": "Known Risks", "required": True},
                    {"id": "11.2", "title": "Technical Debt Items", "required": False},
                ]
            },
            {
                "section": "12",
                "title": "Glossary",
                "subsections": [
                    {"id": "12.1", "title": "Terms and Definitions", "required": True},
                ]
            }
        ]
    },
    
    "USER_MANUAL": {
        "name": "User Manual",
        "description": "End-user documentation and guides",
        "category": "User Documentation",
        "icon": "BookOpen",
        "structure": [
            {
                "section": "1",
                "title": "Introduction",
                "subsections": [
                    {"id": "1.1", "title": "About This Manual", "required": True},
                    {"id": "1.2", "title": "Intended Audience", "required": True},
                    {"id": "1.3", "title": "System Requirements", "required": True},
                ]
            },
            {
                "section": "2",
                "title": "Getting Started",
                "subsections": [
                    {"id": "2.1", "title": "Installation", "required": True},
                    {"id": "2.2", "title": "First-Time Setup", "required": True},
                    {"id": "2.3", "title": "Quick Start Guide", "required": True},
                ]
            },
            {
                "section": "3",
                "title": "Features and Functionality",
                "subsections": [
                    {"id": "3.1", "title": "Core Features", "required": True},
                    {"id": "3.2", "title": "Advanced Features", "required": False},
                ]
            },
            {
                "section": "4",
                "title": "Step-by-Step Guides",
                "subsections": [
                    {"id": "4.1", "title": "Common Tasks and Workflows", "required": True},
                ]
            },
            {
                "section": "5",
                "title": "Troubleshooting",
                "subsections": [
                    {"id": "5.1", "title": "Common Issues and Solutions", "required": True},
                    {"id": "5.2", "title": "Error Messages", "required": True},
                    {"id": "5.3", "title": "Support Contact Information", "required": True},
                ]
            }
        ]
    },
    
    "API_DOCUMENTATION": {
        "name": "API Documentation",
        "description": "REST API reference and integration guide",
        "category": "Technical",
        "icon": "Code",
        "structure": [
            {
                "section": "1",
                "title": "Overview",
                "subsections": [
                    {"id": "1.1", "title": "Introduction", "required": True},
                    {"id": "1.2", "title": "Base URL and Versioning", "required": True},
                    {"id": "1.3", "title": "Authentication", "required": True},
                ]
            },
            {
                "section": "2",
                "title": "Getting Started",
                "subsections": [
                    {"id": "2.1", "title": "Quick Start Guide", "required": True},
                    {"id": "2.2", "title": "API Keys and Authorization", "required": True},
                    {"id": "2.3", "title": "Rate Limiting", "required": True},
                ]
            },
            {
                "section": "3",
                "title": "API Reference",
                "subsections": [
                    {"id": "3.1", "title": "Endpoints", "required": True},
                    {"id": "3.2", "title": "Request/Response Format", "required": True},
                    {"id": "3.3", "title": "Data Models", "required": True},
                ]
            },
            {
                "section": "4",
                "title": "Error Handling",
                "subsections": [
                    {"id": "4.1", "title": "Error Codes and Messages", "required": True},
                ]
            },
            {
                "section": "5",
                "title": "Code Examples",
                "subsections": [
                    {"id": "5.1", "title": "Sample Requests", "required": True},
                    {"id": "5.2", "title": "Integration Examples", "required": False},
                ]
            }
        ]
    },
    
    "TEST_PLAN": {
        "name": "Test Plan Document",
        "description": "Comprehensive testing strategy and test cases",
        "category": "Quality Assurance",
        "icon": "CheckCircle",
        "structure": [
            {
                "section": "1",
                "title": "Introduction",
                "subsections": [
                    {"id": "1.1", "title": "Purpose and Scope", "required": True},
                    {"id": "1.2", "title": "Test Objectives", "required": True},
                ]
            },
            {
                "section": "2",
                "title": "Test Strategy",
                "subsections": [
                    {"id": "2.1", "title": "Test Approach", "required": True},
                    {"id": "2.2", "title": "Test Levels", "required": True},
                    {"id": "2.3", "title": "Test Types", "required": True},
                ]
            },
            {
                "section": "3",
                "title": "Test Environment",
                "subsections": [
                    {"id": "3.1", "title": "Requirements", "required": True},
                    {"id": "3.2", "title": "Test Tools", "required": True},
                ]
            },
            {
                "section": "4",
                "title": "Test Cases",
                "subsections": [
                    {"id": "4.1", "title": "Functional Test Cases", "required": True},
                    {"id": "4.2", "title": "Non-Functional Test Cases", "required": True},
                ]
            },
            {
                "section": "5",
                "title": "Test Schedule and Deliverables",
                "subsections": [
                    {"id": "5.1", "title": "Test Timeline", "required": True},
                    {"id": "5.2", "title": "Test Reports", "required": True},
                ]
            }
        ]
    },
    
    "PROJECT_CHARTER": {
        "name": "Project Charter",
        "description": "Project authorization and high-level plan",
        "category": "Project Management",
        "icon": "Flag",
        "structure": [
            {
                "section": "1",
                "title": "Project Overview",
                "subsections": [
                    {"id": "1.1", "title": "Project Purpose", "required": True},
                    {"id": "1.2", "title": "Project Description", "required": True},
                    {"id": "1.3", "title": "Business Case", "required": True},
                ]
            },
            {
                "section": "2",
                "title": "Project Scope",
                "subsections": [
                    {"id": "2.1", "title": "Objectives and Deliverables", "required": True},
                    {"id": "2.2", "title": "Success Criteria", "required": True},
                    {"id": "2.3", "title": "Out of Scope", "required": True},
                ]
            },
            {
                "section": "3",
                "title": "Stakeholders",
                "subsections": [
                    {"id": "3.1", "title": "Project Sponsor", "required": True},
                    {"id": "3.2", "title": "Project Team", "required": True},
                    {"id": "3.3", "title": "Key Stakeholders", "required": True},
                ]
            },
            {
                "section": "4",
                "title": "Project Timeline and Budget",
                "subsections": [
                    {"id": "4.1", "title": "Key Milestones", "required": True},
                    {"id": "4.2", "title": "Resource Requirements", "required": True},
                ]
            },
            {
                "section": "5",
                "title": "Risks and Assumptions",
                "subsections": [
                    {"id": "5.1", "title": "High-Level Risks", "required": True},
                    {"id": "5.2", "title": "Key Assumptions", "required": True},
                ]
            }
        ]
    },
    
    "DESIGN_DOCUMENT": {
        "name": "Design Document",
        "description": "Detailed technical design specifications",
        "category": "Design",
        "icon": "Layout",
        "structure": [
            {
                "section": "1",
                "title": "Introduction",
                "subsections": [
                    {"id": "1.1", "title": "Purpose and Scope", "required": True},
                    {"id": "1.2", "title": "Design Goals", "required": True},
                ]
            },
            {
                "section": "2",
                "title": "System Overview",
                "subsections": [
                    {"id": "2.1", "title": "System Architecture", "required": True},
                    {"id": "2.2", "title": "Component Overview", "required": True},
                ]
            },
            {
                "section": "3",
                "title": "Detailed Design",
                "subsections": [
                    {"id": "3.1", "title": "Data Model", "required": True},
                    {"id": "3.2", "title": "Component Interactions", "required": True},
                ]
            },
            {
                "section": "4",
                "title": "Interface Design",
                "subsections": [
                    {"id": "4.1", "title": "User Interface", "required": True},
                    {"id": "4.2", "title": "API Interfaces", "required": True},
                ]
            },
            {
                "section": "5",
                "title": "Database Design",
                "subsections": [
                    {"id": "5.1", "title": "Schema Design", "required": True},
                    {"id": "5.2", "title": "Data Dictionary", "required": True},
                ]
            },
            {
                "section": "6",
                "title": "Security Design",
                "subsections": [
                    {"id": "6.1", "title": "Authentication and Authorization", "required": True},
                    {"id": "6.2", "title": "Data Protection", "required": True},
                ]
            }
        ]
    },
    
    "TECHNICAL_SPEC": {
        "name": "Technical Specification",
        "description": "Detailed technical implementation specification",
        "category": "Technical",
        "icon": "FileCode",
        "structure": [
            {
                "section": "1",
                "title": "Overview",
                "subsections": [
                    {"id": "1.1", "title": "Technical Summary", "required": True},
                    {"id": "1.2", "title": "Technology Stack", "required": True},
                ]
            },
            {
                "section": "2",
                "title": "System Components",
                "subsections": [
                    {"id": "2.1", "title": "Backend Services", "required": True},
                    {"id": "2.2", "title": "Frontend Components", "required": True},
                    {"id": "2.3", "title": "Database Design", "required": True},
                ]
            },
            {
                "section": "3",
                "title": "Implementation Details",
                "subsections": [
                    {"id": "3.1", "title": "Core Algorithms", "required": True},
                    {"id": "3.2", "title": "Data Flow", "required": True},
                ]
            },
            {
                "section": "4",
                "title": "Integration Points",
                "subsections": [
                    {"id": "4.1", "title": "External APIs", "required": True},
                    {"id": "4.2", "title": "Third-Party Services", "required": False},
                ]
            },
            {
                "section": "5",
                "title": "Deployment and Operations",
                "subsections": [
                    {"id": "5.1", "title": "Deployment Architecture", "required": True},
                    {"id": "5.2", "title": "Monitoring and Logging", "required": True},
                ]
            }
        ]
    }
}


def get_document_types():
    """Get list of all available document types"""
    return [
        {
            "id": key,
            **value
        }
        for key, value in DOCUMENT_TYPES.items()
    ]


def get_document_structure(document_type: str):
    """Get structure for a specific document type"""
    return DOCUMENT_TYPES.get(document_type)


def get_categories():
    """Get unique categories for filtering"""
    categories = set()
    for doc in DOCUMENT_TYPES.values():
        categories.add(doc["category"])
    return sorted(list(categories))
