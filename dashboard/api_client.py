"""API client for communicating with FastAPI backend."""
import requests
from typing import Optional, Dict, Any, List

API_BASE_URL = "http://localhost:8000"


class APIClient:
    """Client for interacting with the Fitness Tracker API."""
    
    def __init__(self, token: Optional[str] = None):
        self.token = token
        self.base_url = API_BASE_URL
    
    def _headers(self) -> Dict[str, str]:
        """Get request headers with auth token if available."""
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Handle API response and errors."""
        if response.status_code >= 400:
            try:
                error = response.json()
                return {"error": True, "detail": error.get("detail", "Unknown error")}
            except:
                return {"error": True, "detail": response.text}
        return response.json()
    
    # Auth endpoints
    def register(self, username: str, email: str, password: str) -> Dict[str, Any]:
        """Register a new user."""
        response = requests.post(
            f"{self.base_url}/auth/register",
            json={"username": username, "email": email, "password": password}
        )
        return self._handle_response(response)
    
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """Login and get JWT token."""
        response = requests.post(
            f"{self.base_url}/auth/login",
            json={"username": username, "password": password}
        )
        if response.status_code == 200:
            return response.json()
        return self._handle_response(response)
    
    def get_current_user(self) -> Dict[str, Any]:
        """Get current user info."""
        response = requests.get(
            f"{self.base_url}/auth/me",
            headers=self._headers()
        )
        return self._handle_response(response)

    
    # Fitness records endpoints
    def get_fitness_records(
        self, 
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        workout_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get fitness records with optional filters."""
        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        if workout_type:
            params["workout_type"] = workout_type
        
        response = requests.get(
            f"{self.base_url}/fitness-records",
            headers=self._headers(),
            params=params
        )
        if response.status_code == 200:
            return response.json()
        return []
    
    def create_fitness_record(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new fitness record."""
        response = requests.post(
            f"{self.base_url}/fitness-records",
            headers=self._headers(),
            json=data
        )
        return self._handle_response(response)
    
    def delete_fitness_record(self, record_id: str) -> bool:
        """Delete a fitness record."""
        response = requests.delete(
            f"{self.base_url}/fitness-records/{record_id}",
            headers=self._headers()
        )
        return response.status_code == 204
    
    # Health metrics endpoints
    def get_health_metrics(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get health metrics with optional filters."""
        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        
        response = requests.get(
            f"{self.base_url}/health-metrics",
            headers=self._headers(),
            params=params
        )
        if response.status_code == 200:
            return response.json()
        return []
    
    def create_health_metric(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new health metric."""
        response = requests.post(
            f"{self.base_url}/health-metrics",
            headers=self._headers(),
            json=data
        )
        return self._handle_response(response)
    
    def delete_health_metric(self, metric_id: str) -> bool:
        """Delete a health metric."""
        response = requests.delete(
            f"{self.base_url}/health-metrics/{metric_id}",
            headers=self._headers()
        )
        return response.status_code == 204
