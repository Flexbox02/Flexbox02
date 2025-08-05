import requests
from typing import Dict, List, Optional
from config import Config

class SnipeITClient:
    def __init__(self):
        self.base_url = Config.SNIPE_IT_URL.rstrip('/')
        self.headers = {
            'Authorization': f'Bearer {Config.SNIPE_IT_TOKEN}',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    
    def _make_request(self, endpoint: str, method: str = 'GET', params: Dict = None) -> Dict:
        """Make HTTP request to Snipe IT API"""
        url = f"{self.base_url}/api/v1/{endpoint}"
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error connecting to Snipe IT API: {str(e)}")
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user information by email"""
        try:
            response = self._make_request('users', params={'search': email})
            users = response.get('rows', [])
            
            for user in users:
                if user.get('email', '').lower() == email.lower():
                    return user
            
            return None
        except Exception as e:
            raise Exception(f"Error fetching user: {str(e)}")
    
    def get_user_assets(self, user_id: int) -> List[Dict]:
        """Get assets assigned to a user"""
        try:
            response = self._make_request(f'users/{user_id}/assets')
            return response.get('rows', [])
        except Exception as e:
            raise Exception(f"Error fetching user assets: {str(e)}")
    
    def get_asset_details(self, asset_id: int) -> Dict:
        """Get detailed information about an asset"""
        try:
            response = self._make_request(f'hardware/{asset_id}')
            return response
        except Exception as e:
            raise Exception(f"Error fetching asset details: {str(e)}")
    
    def get_user_complete_data(self, email: str) -> Dict:
        """Get complete user data including assets"""
        user = self.get_user_by_email(email)
        if not user:
            raise Exception(f"User with email {email} not found")
        
        # Get user assets
        assets = self.get_user_assets(user['id'])
        
        # Get detailed asset information
        detailed_assets = []
        for asset in assets:
            try:
                asset_detail = self.get_asset_details(asset['id'])
                detailed_assets.append(asset_detail)
            except Exception as e:
                print(f"Warning: Could not fetch details for asset {asset['id']}: {e}")
                detailed_assets.append(asset)
        
        return {
            'user': user,
            'assets': detailed_assets
        }