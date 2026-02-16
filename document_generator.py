"""
Gemini-Powered Documentation Generator
Generates professional, accurate software documentation using Google's Gemini AI
"""

import os
import re
from typing import Any, Dict, List, Optional
import google.generativeai as genai
from document_templates import get_document_structure, get_document_types, get_categories


class DocumentGenerator:
    """
    Professional documentation generator using Gemini AI
    """
    
    def __init__(self):
        # Configure Gemini API (do it here, not at module level)
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("[ERROR] GEMINI_API_KEY not found in environment!")
            print(f"[DEBUG] Current working directory: {os.getcwd()}")
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        print(f"[DEBUG] GEMINI_API_KEY found: {api_key[:10]}...")
        genai.configure(api_key=api_key)
        
        # Use same model format as other agents: models/gemini-2.0-flash
        self.model_name = os.getenv("DOC_AGENT_GEMINI_MODEL", "models/gemini-2.0-flash")
        self.model = genai.GenerativeModel(self.model_name)
        print(f"[DOC] DocumentGenerator initialized with model: {self.model_name}")
    
    def get_document_types(self) -> List[Dict[str, Any]]:
        """Get all available document types"""
        return get_document_types()
    
    def get_categories(self) -> List[str]:
        """Get document categories"""
        return get_categories()
    
    def get_document_structure(self, document_type: str) -> Optional[Dict[str, Any]]:
        """Get structure for a specific document type"""
        doc = get_document_structure(document_type)
        if not doc:
            return None
        
        # Return full document info including structure
        return {
            "name": doc.get("name"),
            "description": doc.get("description"),
            "category": doc.get("category"),
            "structure": doc.get("structure", [])
        }
    
    async def generate_document(
        self,
        document_type: str,
        project_context: Dict[str, Any],
        user_requirements: Optional[str] = None,
        selected_sections: Optional[List[Dict[str, str]]] = None,
        custom_sections: Optional[List[Dict[str, str]]] = None,
        additional_notes: Optional[str] = None,
        include_data_summary: bool = True
    ) -> Dict[str, Any]:
        """
        Generate professional document using Gemini AI
        
        Args:
            document_type: Type of document (SRS, SPRINT_REPORT, etc.)
            project_context: Complete project data from Node backend
            user_requirements: User's specific requirements
            selected_sections: Specific sections selected by user to include
            custom_sections: User-defined custom sections
            additional_notes: Additional instructions
            include_data_summary: Include project data summary
            
        Returns:
            Dictionary with success status, document content, and metadata
        """
        try:
            # Get document structure
            doc_structure = get_document_structure(document_type)
            if not doc_structure:
                return {
                    "success": False,
                    "error": f"Unknown document type: {document_type}"
                }
            
            # Build comprehensive prompt
            prompt = self._build_prompt(
                document_type=document_type,
                doc_structure=doc_structure,
                project_context=project_context,
                user_requirements=user_requirements,
                selected_sections=selected_sections or [],
                custom_sections=custom_sections or [],
                additional_notes=additional_notes,
                include_data_summary=include_data_summary
            )
            
            # Generate content using Gemini
            print(f"[AI] Calling Gemini API to generate {doc_structure['name']}...")
            response = self.model.generate_content(prompt)
            generated_text = response.text
            
            # Parse and structure the document
            document = self._parse_document(generated_text, doc_structure)
            
            print(f"[SUCCESS] Document generated: {document['wordCount']} words")
            
            return {
                "success": True,
                "document": document,
                "metadata": {
                    "documentType": document_type,
                    "generatedAt": project_context.get("metadata", {}).get("fetchedAt"),
                    "model": self.model_name,
                    "projectId": project_context.get("project", {}).get("id"),
                    "sprintId": project_context.get("sprintDetail", {}).get("_id") if project_context.get("sprintDetail") else None,
                }
            }
            
        except Exception as e:
            print(f"[ERROR] Error generating document: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _build_prompt(
        self,
        document_type: str,
        doc_structure: Dict[str, Any],
        project_context: Dict[str, Any],
        user_requirements: Optional[str],
        selected_sections: List[Dict[str, str]],
        custom_sections: List[Dict[str, str]],
        additional_notes: Optional[str],
        include_data_summary: bool
    ) -> str:
        """Build comprehensive prompt for Gemini"""
        
        prompt = f"""You are a world-class professional technical writer and software documentation expert with deep expertise in industry standards (IEEE 830-1998, ISO, arc42, Agile best practices). Generate a comprehensive, accurate, and professional {doc_structure['name']}.

**CRITICAL WRITING GUIDELINES:**
1. **PROFESSIONAL TONE**: Write in a clear, authoritative, yet accessible manner similar to official IEEE or ISO documentation
2. **PROPER FORMATTING**: Use proper markdown formatting:
   - Use # for main headings (# 1. Introduction)
   - Use ## for subsections (## 1.1 Purpose)
   - Use ### for sub-subsections if needed
   - Include section numbering (1.1, 1.2, 2.1, etc.)
3. **COMPREHENSIVE CONTENT**: Write detailed paragraphs (minimum 3-5 sentences per subsection)
4. **STRUCTURED DATA**: Use bullet points for lists, tables for structured data, code blocks for technical specs
5. **SPECIFIC DETAILS**: Include concrete numbers, dates, names, and technical specifications from the project context
6. **HUMANIZED WRITING**: Write naturally, avoiding robotic or template-like language while maintaining professionalism
7. **ACCURACY**: Base ALL content on actual project data provided. Mark missing information as "[To be determined]"
8. **CONSISTENCY**: Maintain consistent terminology, style, and formatting throughout

**QUALITY REQUIREMENTS:**
- Follow {doc_structure['description']} standards meticulously
- Be specific and avoid vague statements
- Include actionable recommendations where relevant
- Write for both technical and non-technical stakeholders
- Ensure content is thorough and publication-ready

---

## DOCUMENT TYPE: {doc_structure['name']}
**Category:** {doc_structure['category']}
**Description:** {doc_structure['description']}

---

## DOCUMENT STRUCTURE TO GENERATE:

"""
        
        # If user selected specific sections, only show those
        if selected_sections:
            selected_ids = {sec['id'] for sec in selected_sections}
            prompt += "\n**GENERATE ONLY THE FOLLOWING SECTIONS (user-selected):**\n\n"
            
            for section in doc_structure.get("structure", []):
                section_subs = []
                for sub in section.get("subsections", []):
                    if sub['id'] in selected_ids:
                        section_subs.append(sub)
                
                if section_subs:
                    prompt += f"### Section {section['section']}: {section['title']}\n"
                    for sub in section_subs:
                        prompt += f"- **{sub['id']} {sub['title']}** - {sub.get('description', '')}\n"
                    prompt += "\n"
            
            prompt += "\n⚠️ **IMPORTANT**: Generate ONLY the sections listed above. Do NOT include any other sections.\n\n"
        else:
            # Show all sections
            for section in doc_structure.get("structure", []):
                prompt += f"\n### Section {section['section']}: {section['title']}\n"
                prompt += f"*{section.get('description', '')}*\n\n"
                for sub in section.get("subsections", []):
                    required_tag = "**[REQUIRED]**" if sub.get("required") else "[OPTIONAL]"
                    prompt += f"- **{sub['id']} {sub['title']}** {required_tag}\n"
                    if sub.get('description'):
                        prompt += f"  _{sub['description']}_\n"
        
        prompt += "\n---\n\n## PROJECT CONTEXT AND DATA:\n\n"
        
        # Add project information
        project = project_context.get("project", {})
        if project:
            prompt += f"### Project Information:\n"
            prompt += f"- **Project Name:** {project.get('name', 'N/A')}\n"
            prompt += f"- **Description:** {project.get('description', 'N/A')}\n"
            prompt += f"- **Created:** {project.get('createdAt', 'N/A')}\n\n"
        
        # Add task information
        tasks_data = project_context.get("tasks", {})
        if tasks_data and include_data_summary:
            stats = tasks_data.get("stats", {})
            prompt += f"### Tasks Overview:\n"
            prompt += f"- **Total Tasks:** {stats.get('total', 0)}\n"
            prompt += f"- **Completion Rate:** {stats.get('completionRate', 0):.1f}%\n"
            prompt += f"- **Status Distribution:** {stats.get('byStatus', {})}\n"
            prompt += f"- **Priority Distribution:** {stats.get('byPriority', {})}\n"
            prompt += f"- **Total Estimated Hours:** {stats.get('totalEstimatedHours', 0)}\n\n"
            
            # Add key tasks
            tasks = tasks_data.get("items", [])[:15]
            if tasks:
                prompt += "**Key Tasks:**\n"
                for idx, task in enumerate(tasks, 1):
                    prompt += f"{idx}. **{task.get('title', 'N/A')}** [{task.get('status', 'N/A')}] - {task.get('priority', 'medium')} priority, {task.get('estimatedHours', 0)}hrs\n"
                prompt += "\n"
        
        # Add sprint information
        sprints_data = project_context.get("sprints", {})
        if sprints_data and include_data_summary:
            stats = sprints_data.get("stats", {})
            prompt += f"### Sprint Information:\n"
            prompt += f"- **Total Sprints:** {stats.get('total', 0)}\n"
            prompt += f"- **Completed:** {stats.get('completed', 0)}\n"
            prompt += f"- **Active:** {stats.get('active', 0)}\n"
            prompt += f"- **Average Velocity:** {stats.get('avgVelocity', 0):.1f}\n"
            prompt += f"- **Average Capacity:** {stats.get('avgCapacity', 0):.1f} hours\n\n"
            
            # Add latest sprint details
            latest = sprints_data.get("latest")
            if latest:
                prompt += f"**Latest Sprint:**\n"
                prompt += f"- Sprint ID: {latest.get('sprintId', latest.get('_id', 'N/A'))}\n"
                prompt += f"- Summary: {latest.get('summary', 'N/A')}\n"
                prompt += f"- Status: {latest.get('status', 'N/A')}\n"
                prompt += f"- Duration: {latest.get('startDate', 'N/A')} to {latest.get('endDate', 'N/A')}\n"
                goals = latest.get('goals', [])
                prompt += f"- Goals: {', '.join(goals) if goals else 'N/A'}\n"
                prompt += f"- Total Effort: {latest.get('totalEffort', 0)} hours\n"
                prompt += f"- Predicted Velocity: {latest.get('predictedVelocity', 0)}\n\n"
        
        # Add specific sprint detail if provided
        sprint_detail = project_context.get("sprintDetail")
        if sprint_detail and document_type == "SPRINT_REPORT":
            prompt += f"### DETAILED SPRINT DATA (For Sprint Report):\n\n"
            prompt += f"**Sprint:** {sprint_detail.get('sprintId', 'N/A')}\n"
            prompt += f"**Summary:** {sprint_detail.get('summary', 'N/A')}\n"
            prompt += f"**Status:** {sprint_detail.get('status', 'N/A')}\n"
            prompt += f"**Period:** {sprint_detail.get('startDate', 'N/A')} to {sprint_detail.get('endDate', 'N/A')}\n\n"
            
            # Sprint goals
            goals = sprint_detail.get('goals', [])
            if goals:
                prompt += f"**Sprint Goals:**\n"
                for idx, goal in enumerate(goals, 1):
                    prompt += f"{idx}. {goal}\n"
                prompt += "\n"
            
            # Capacity and workload
            capacity = sprint_detail.get('capacity', {})
            if capacity:
                prompt += f"**Capacity:**\n"
                prompt += f"- Total Capacity: {capacity.get('totalCapacityHours', 0)} hours\n"
                member_caps = capacity.get('memberCapacities', [])
                if member_caps:
                    prompt += f"- Team Members: {len(member_caps)}\n\n"
            
            # Risk analysis
            risk = sprint_detail.get('riskAnalysis', {})
            if risk:
                prompt += f"**Risk Analysis:**\n"
                prompt += f"- Delay Risk: {risk.get('delayRiskPercent', 0)}%\n"
                prompt += f"- Overloaded Members: {', '.join(risk.get('overloadedMembers', [])) or 'None'}\n"
                prompt += f"- Critical Dependencies: {', '.join(risk.get('criticalDependencies', [])) or 'None'}\n\n"
            
            # Selected and deferred tasks
            selected = sprint_detail.get('selectedTasks', [])
            deferred = sprint_detail.get('deferredTasks', [])
            prompt += f"**Tasks:**\n"
            prompt += f"- Selected: {len(selected)} tasks\n"
            prompt += f"- Deferred: {len(deferred)} tasks\n\n"
            
            # Blocker health
            blocker_score = sprint_detail.get('blockerHealthScore')
            if blocker_score is not None:
                prompt += f"**Blocker Health:**\n"
                prompt += f"- Health Score: {blocker_score}\n"
                prompt += f"- Status: {sprint_detail.get('blockerStatus', 'N/A')}\n\n"
        
        # Add team information
        members_data = project_context.get("members", {})
        if members_data and include_data_summary:
            stats = members_data.get("stats", {})
            prompt += f"### Team Information:\n"
            prompt += f"- **Total Members:** {stats.get('total', 0)}\n"
            prompt += f"- **Role Distribution:** {stats.get('byRole', {})}\n\n"
            
            # List team members
            members = members_data.get("items", [])[:10]
            if members:
                prompt += "**Team Members:**\n"
                for member in members:
                    member_info = member.get('memberId', {})
                    if isinstance(member_info, dict):
                        name = member_info.get('name', 'N/A')
                    else:
                        name = 'N/A'
                    role = member.get('role', 'Member')
                    prompt += f"- {name} ({role})\n"
                prompt += "\n"
        
        # Add blockers information
        blockers_data = project_context.get("blockers", {})
        if blockers_data and blockers_data.get("total", 0) > 0:
            prompt += f"### Current Blockers:\n"
            prompt += f"- **Total Active Blockers:** {blockers_data.get('total', 0)}\n"
            blockers = blockers_data.get("items", [])[:10]
            if blockers:
                prompt += "\n**Active Blockers:**\n"
                for blocker in blockers:
                    prompt += f"- [{blocker.get('severity', 'Medium')}] {blocker.get('reason', 'N/A')}\n"
                prompt += "\n"
        
        # Add recent activity
        activity_data = project_context.get("activity", {})
        if activity_data and include_data_summary:
            recent = activity_data.get("recent", [])[:10]
            if recent:
                prompt += f"### Recent Activity:\n"
                for activity in recent:
                    user_info = activity.get('user', {})
                    user_name = user_info.get('name', 'Unknown') if isinstance(user_info, dict) else 'Unknown'
                    action = activity.get('action', 'N/A')
                    entity_type = activity.get('entityType', 'N/A')
                    prompt += f"- {user_name} {action} {entity_type}\n"
                prompt += "\n"
        
        # Add user requirements
        if user_requirements:
            prompt += f"\n---\n\n## USER REQUIREMENTS AND FOCUS AREAS:\n\n{user_requirements}\n\n"
        
        # Add custom sections
        if custom_sections:
            prompt += f"\n---\n\n## CUSTOM SECTIONS REQUESTED BY USER:\n\n"
            for idx, section in enumerate(custom_sections, 1):
                prompt += f"{idx}. **{section.get('title', 'N/A')}**\n"
                if section.get('description'):
                    prompt += f"   Description: {section['description']}\n"
            prompt += "\n"
        
        # Add additional notes
        if additional_notes:
            prompt += f"\n---\n\n## ADDITIONAL INSTRUCTIONS FROM USER:\n\n{additional_notes}\n\n"
        
        # Add output format instructions
        prompt += """
---

## OUTPUT FORMAT REQUIREMENTS:

Generate the complete document in **professional Markdown format** following these rules:

1. **Structure**: Follow the required structure exactly, using proper heading levels (##, ###, ####)
2. **Formatting**: Use appropriate markdown formatting:
   - **Bold** for emphasis
   - *Italic* for definitions
   - `Code blocks` for technical terms
   - Tables for structured data
   - Bullet points and numbered lists for clarity
3. **Tone**: Professional, clear, and appropriate for the document type
4. **Completeness**: Fill ALL required sections with actual project data
5. **Accuracy**: Only use information from the project context provided
6. **Missing Data**: If data is unavailable for a section, write "[To be determined - requires stakeholder input]" or similar
7. **Professional Standards**: Follow industry best practices for this document type
8. **No Preamble**: Start directly with the document title and content

**BEGIN GENERATING THE PROFESSIONAL DOCUMENT NOW:**

"""
        
        return prompt
    
    def _parse_document(
        self,
        generated_text: str,
        doc_structure: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Parse generated markdown into structured format
        """
        # Clean up markdown code blocks if present
        cleaned = generated_text.strip()
        cleaned = re.sub(r'^```markdown?\s*\n', '', cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r'\n```\s*$', '', cleaned)
        
        # Extract sections
        sections = self._extract_sections(cleaned)
        
        # Count words
        word_count = len(cleaned.split())
        
        # Extract title (first H1 or H2)
        title_match = re.search(r'^#\s+(.+)$', cleaned, re.MULTILINE)
        title = title_match.group(1) if title_match else doc_structure['name']
        
        return {
            "title": title,
            "content": cleaned,
            "sections": sections,
            "wordCount": word_count,
            "documentType": doc_structure['name'],
            "category": doc_structure['category'],
        }
    
    def _extract_sections(self, markdown: str) -> List[Dict[str, Any]]:
        """Extract sections from markdown document"""
        sections = []
        lines = markdown.split('\n')
        current_section = None
        current_content = []
        
        for line in lines:
            # Check for headings (## or ###)
            heading_match = re.match(r'^(#{1,6})\s+(.+)$', line)
            
            if heading_match:
                # Save previous section
                if current_section:
                    current_section['content'] = '\n'.join(current_content).strip()
                    sections.append(current_section)
                
                # Start new section
                level = len(heading_match.group(1))
                title = heading_match.group(2)
                current_section = {
                    "level": level,
                    "title": title,
                    "content": ""
                }
                current_content = []
            elif current_section:
                current_content.append(line)
        
        # Save last section
        if current_section:
            current_section['content'] = '\n'.join(current_content).strip()
            sections.append(current_section)
        
        return sections
