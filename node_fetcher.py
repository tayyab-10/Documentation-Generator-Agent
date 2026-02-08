"""
Node Backend Fetcher
Fetches project context from Node.js backend for documentation generation
"""

import os
from typing import Dict, List, Optional, Any
import httpx

NODE_BASE_URL = os.getenv("NODE_BASE_URL", "http://localhost:5000/api")
REQUEST_TIMEOUT = 10.0


def build_headers(raw_headers: Dict[str, str]) -> Dict[str, str]:
    """
    Forward authentication headers from Node request to agent's outbound calls
    """
    headers = {"Content-Type": "application/json"}
    
    # Forward Authorization header (JWT token)
    auth = raw_headers.get("authorization") or raw_headers.get("Authorization")
    if auth:
        headers["Authorization"] = auth
    
    # Forward Cookie header (session)
    cookie = raw_headers.get("cookie") or raw_headers.get("Cookie")
    if cookie:
        headers["Cookie"] = cookie
    
    return headers


async def fetch_project_info(project_id: str, headers: Dict[str, str]) -> Dict[str, Any]:
    """Fetch basic project information"""
    url = f"{NODE_BASE_URL}/project/{project_id}"
    
    print(f"[DEBUG] fetch_project_info called")
    print(f"[DEBUG] NODE_BASE_URL: {NODE_BASE_URL}")
    print(f"[DEBUG] Project ID: {project_id}")
    print(f"[DEBUG] Full URL: {url}")
    print(f"[DEBUG] Headers: {headers}")
    
    try:
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            print(f"[DEBUG] Sending GET request to: {url}")
            response = await client.get(url, headers=headers)
            print(f"[DEBUG] Response status: {response.status_code}")
            print(f"[DEBUG] Response headers: {response.headers}")
            
            response.raise_for_status()
            data = response.json()
            print(f"[DEBUG] Response data: {data}")
            
            # Check if project data exists (your API returns {project: {...}, members: [...]})
            if "project" not in data:
                raise ValueError(f"Node API error: Project data not found in response")
            
            return data.get("project", {})
    except httpx.ConnectError as e:
        print(f"[ERROR] Connection failed to {url}: {str(e)}")
        print(f"[ERROR] Is your Node.js backend running on {NODE_BASE_URL}?")
        raise
    except httpx.TimeoutException as e:
        print(f"[ERROR] Request timeout to {url}: {str(e)}")
        raise
    except Exception as e:
        print(f"[ERROR] Unexpected error in fetch_project_info: {type(e).__name__}: {str(e)}")
        raise


async def fetch_tasks(project_id: str, headers: Dict[str, str]) -> List[Dict[str, Any]]:
    """Fetch all tasks for a project"""
    url = f"{NODE_BASE_URL}/tasks/{project_id}"
    
    print(f"[DEBUG] Fetching tasks from: {url}")
    
    try:
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            response = await client.get(url, headers=headers)
            print(f"[DEBUG] Tasks response status: {response.status_code}")
            response.raise_for_status()
            data = response.json()
            print(f"[DEBUG] Tasks count: {len(data.get('tasks', []))}")
            
            return data.get("tasks", [])
    except Exception as e:
        print(f"[ERROR] Failed to fetch tasks: {type(e).__name__}: {str(e)}")
        raise


async def fetch_sprints(project_id: str, headers: Dict[str, str]) -> List[Dict[str, Any]]:
    """Fetch all sprints for a project"""
    url = f"{NODE_BASE_URL}/sprint/{project_id}"
    
    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        return data.get("sprints", [])


async def fetch_sprint_by_id(sprint_id: str, headers: Dict[str, str]) -> Dict[str, Any]:
    """Fetch specific sprint by ID"""
    url = f"{NODE_BASE_URL}/sprint/sprint/{sprint_id}"
    
    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        # Check if sprint data exists (API may return {success: true, sprint: {...}} or just {sprint: {...}})
        if "sprint" not in data and "success" not in data:
            raise ValueError(f"Sprint not found: {sprint_id}")
        
        return data.get("sprint", {})


async def fetch_team_members(project_id: str, headers: Dict[str, str]) -> List[Dict[str, Any]]:
    """Fetch team members for a project"""
    url = f"{NODE_BASE_URL}/projectMember/{project_id}"
    
    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        return data.get("members", [])


async def fetch_activity_logs(
    project_id: str, 
    headers: Dict[str, str],
    limit: int = 100
) -> List[Dict[str, Any]]:
    """Fetch recent activity logs for a project"""
    url = f"{NODE_BASE_URL}/activity-logs"
    params = {"project": project_id, "limit": limit}
    
    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
        response = await client.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        return data.get("activityLogs", [])


async def fetch_blockers(project_id: str, headers: Dict[str, str]) -> List[Dict[str, Any]]:
    """Fetch active blockers for a project"""
    url = f"{NODE_BASE_URL}/blockers"
    params = {"projectId": project_id, "resolved": "false"}
    
    try:
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            return data.get("blockers", [])
    except Exception as e:
        print(f"[WARN] Failed to fetch blockers: {str(e)}")
        return []


async def fetch_project_context(
    project_id: str,
    sprint_id: Optional[str],
    headers: Dict[str, str]
) -> Dict[str, Any]:
    """
    Fetch comprehensive project context for documentation generation
    This is the main entry point that gathers all necessary data
    """
    print(f"[FETCH] Fetching context for projectId={project_id}, sprintId={sprint_id}")
    print(f"[DEBUG] NODE_BASE_URL configured as: {NODE_BASE_URL}")
    print(f"[DEBUG] Headers received: {list(headers.keys())}")
    
    try:
        # Fetch all data in parallel
        results = await httpx.AsyncClient(timeout=REQUEST_TIMEOUT * 2).aclose()
        
        # Fetch project info
        project = await fetch_project_info(project_id, headers)
        
        # Fetch tasks
        tasks = await fetch_tasks(project_id, headers)
        
        # Fetch sprints
        sprints = await fetch_sprints(project_id, headers)
        
        # Fetch team
        members = await fetch_team_members(project_id, headers)
        
        # Fetch activity logs
        activity = await fetch_activity_logs(project_id, headers, limit=100)
        
        # Fetch blockers
        blockers = await fetch_blockers(project_id, headers)
        
        # If sprint_id provided, fetch detailed sprint info
        sprint_detail = None
        if sprint_id:
            try:
                sprint_detail = await fetch_sprint_by_id(sprint_id, headers)
            except Exception as e:
                print(f"[WARN] Failed to fetch sprint detail: {str(e)}")
        
        # Calculate task statistics
        task_stats = calculate_task_stats(tasks)
        
        # Calculate sprint statistics
        sprint_stats = calculate_sprint_stats(sprints)
        
        # Calculate team statistics
        team_stats = calculate_team_stats(members)
        
        context = {
            "project": {
                "id": project.get("_id"),
                "name": project.get("name"),
                "description": project.get("description"),
                "createdAt": project.get("createdAt"),
                "owner": project.get("owner"),
            },
            "tasks": {
                "items": tasks[:50],  # Top 50 tasks
                "stats": task_stats,
            },
            "sprints": {
                "items": sprints[:10],  # Recent 10 sprints
                "stats": sprint_stats,
                "latest": sprints[0] if sprints else None,
            },
            "members": {
                "items": members,
                "stats": team_stats,
            },
            "activity": {
                "recent": activity[:30],  # Recent 30 activities
                "total": len(activity),
            },
            "blockers": {
                "items": blockers,
                "total": len(blockers),
            },
            "sprintDetail": sprint_detail,
            "metadata": {
                "fetchedAt": httpx.codes.OK,
                "projectId": project_id,
                "sprintId": sprint_id,
            }
        }
        
        print(f"[SUCCESS] Context fetched: {len(tasks)} tasks, {len(sprints)} sprints, {len(members)} members")
        
        return context
        
    except httpx.ConnectError as e:
        print(f"[ERROR] Connection Error - Cannot connect to Node backend")
        print(f"[ERROR] URL: {NODE_BASE_URL}")
        print(f"[ERROR] Error: {str(e)}")
        print(f"[ERROR] Please ensure your Node.js backend is running on port 5000")
        raise ValueError(f"Failed to connect to Node backend at {NODE_BASE_URL}. Is it running?")
    except httpx.HTTPError as e:
        print(f"[ERROR] HTTP error fetching context: {type(e).__name__}: {str(e)}")
        raise ValueError(f"Failed to fetch project context: {str(e)}")
    except Exception as e:
        print(f"[ERROR] Unexpected error fetching context: {type(e).__name__}: {str(e)}")
        import traceback
        print(f"[ERROR] Traceback: {traceback.format_exc()}")
        raise ValueError(f"Failed to fetch project context: {str(e)}")


def calculate_task_stats(tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate task statistics"""
    stats = {
        "total": len(tasks),
        "byStatus": {},
        "byPriority": {},
        "totalEstimatedHours": 0,
        "completionRate": 0,
    }
    
    for task in tasks:
        # Status distribution
        status = task.get("status", "Unassigned")
        stats["byStatus"][status] = stats["byStatus"].get(status, 0) + 1
        
        # Priority distribution
        priority = task.get("priority", "medium")
        stats["byPriority"][priority] = stats["byPriority"].get(priority, 0) + 1
        
        # Total hours
        stats["totalEstimatedHours"] += task.get("estimatedHours", 0)
    
    # Completion rate
    completed = stats["byStatus"].get("Done", 0)
    stats["completionRate"] = (completed / stats["total"] * 100) if stats["total"] > 0 else 0
    
    return stats


def calculate_sprint_stats(sprints: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate sprint statistics"""
    stats = {
        "total": len(sprints),
        "completed": 0,
        "active": 0,
        "planned": 0,
        "avgVelocity": 0,
        "avgCapacity": 0,
    }
    
    total_velocity = 0
    velocity_count = 0
    total_capacity = 0
    capacity_count = 0
    
    for sprint in sprints:
        status = sprint.get("status", "Planned")
        if status == "Completed":
            stats["completed"] += 1
        elif status == "Active":
            stats["active"] += 1
        else:
            stats["planned"] += 1
        
        # Velocity
        velocity = sprint.get("predictedVelocity") or sprint.get("velocity")
        if velocity:
            total_velocity += velocity
            velocity_count += 1
        
        # Capacity
        capacity_data = sprint.get("capacity", {})
        if isinstance(capacity_data, dict):
            total_cap = capacity_data.get("totalCapacityHours", 0)
            if total_cap:
                total_capacity += total_cap
                capacity_count += 1
    
    if velocity_count > 0:
        stats["avgVelocity"] = total_velocity / velocity_count
    
    if capacity_count > 0:
        stats["avgCapacity"] = total_capacity / capacity_count
    
    return stats


def calculate_team_stats(members: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate team statistics"""
    stats = {
        "total": len(members),
        "byRole": {},
    }
    
    for member in members:
        role = member.get("role", "Member")
        stats["byRole"][role] = stats["byRole"].get(role, 0) + 1
    
    return stats
