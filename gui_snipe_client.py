import requests
from typing import Dict, List, Optional
from gui_config import GUIConfig

class GUISnipeITClient:
    """Cliente Snipe IT para la aplicación GUI"""
    
    def __init__(self, config: GUIConfig):
        self.config = config
        self.base_url = None
        self.headers = None
        self._update_config()
    
    def _update_config(self):
        """Actualizar configuración del cliente"""
        if self.config.is_configured():
            self.base_url = self.config.get_snipe_url().rstrip('/')
            self.headers = {
                'Authorization': f'Bearer {self.config.get_api_token()}',
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
    
    def test_connection(self) -> Dict:
        """Probar conexión con Snipe IT"""
        if not self.config.is_configured():
            return {
                'success': False,
                'error': 'Configuración no encontrada. Configure primero la URL y el token.'
            }
        
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/users/me",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'user': data,
                    'message': 'Conexión exitosa'
                }
            else:
                return {
                    'success': False,
                    'error': f'Error de autenticación: {response.status_code}'
                }
                
        except requests.exceptions.ConnectionError:
            return {
                'success': False,
                'error': 'No se pudo conectar al servidor Snipe IT. Verifique la URL.'
            }
        except requests.exceptions.Timeout:
            return {
                'success': False,
                'error': 'Tiempo de espera agotado. El servidor no responde.'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Error inesperado: {str(e)}'
            }
    
    def search_users(self, search_term: str) -> Dict:
        """Buscar usuarios por término"""
        if not self.config.is_configured():
            return {
                'success': False,
                'error': 'Configuración no encontrada'
            }
        
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/users",
                headers=self.headers,
                params={'search': search_term, 'limit': 50},
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'users': data.get('rows', []),
                    'total': data.get('total', 0)
                }
            else:
                return {
                    'success': False,
                    'error': f'Error en la búsqueda: {response.status_code}'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Error en la búsqueda: {str(e)}'
            }
    
    def get_user_by_email(self, email: str) -> Dict:
        """Obtener usuario por email"""
        search_result = self.search_users(email)
        
        if not search_result['success']:
            return search_result
        
        # Buscar usuario exacto por email
        for user in search_result['users']:
            if user.get('email', '').lower() == email.lower():
                return {
                    'success': True,
                    'user': user
                }
        
        return {
            'success': False,
            'error': f'Usuario con email {email} no encontrado'
        }
    
    def get_user_assets(self, user_id: int) -> Dict:
        """Obtener activos de un usuario"""
        if not self.config.is_configured():
            return {
                'success': False,
                'error': 'Configuración no encontrada'
            }
        
        try:
            # Assets (Hardware)
            assets_response = requests.get(
                f"{self.base_url}/api/v1/users/{user_id}/assets",
                headers=self.headers,
                timeout=15
            )
            
            # Accessories
            accessories_response = requests.get(
                f"{self.base_url}/api/v1/users/{user_id}/accessories",
                headers=self.headers,
                timeout=15
            )
            
            # Licenses
            licenses_response = requests.get(
                f"{self.base_url}/api/v1/users/{user_id}/licenses",
                headers=self.headers,
                timeout=15
            )
            
            assets = []
            accessories = []
            licenses = []
            
            if assets_response.status_code == 200:
                assets_data = assets_response.json()
                assets = assets_data.get('rows', [])
            
            if accessories_response.status_code == 200:
                accessories_data = accessories_response.json()
                accessories = accessories_data.get('rows', [])
            
            if licenses_response.status_code == 200:
                licenses_data = licenses_response.json()
                licenses = licenses_data.get('rows', [])
            
            return {
                'success': True,
                'assets': assets,
                'accessories': accessories,
                'licenses': licenses,
                'total_items': len(assets) + len(accessories) + len(licenses)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error obteniendo activos: {str(e)}'
            }
    
    def get_user_complete_data(self, email: str) -> Dict:
        """Obtener datos completos del usuario para el reporte"""
        # Obtener usuario
        user_result = self.get_user_by_email(email)
        if not user_result['success']:
            return user_result
        
        user = user_result['user']
        
        # Obtener activos del usuario
        assets_result = self.get_user_assets(user['id'])
        if not assets_result['success']:
            return assets_result
        
        # Combinar todos los activos en una sola lista para el PDF
        all_assets = []
        
        # Agregar hardware assets
        for asset in assets_result['assets']:
            asset['type'] = 'hardware'
            all_assets.append(asset)
        
        # Agregar accessories
        for accessory in assets_result['accessories']:
            accessory['type'] = 'accessory'
            all_assets.append(accessory)
        
        # Agregar licenses
        for license_item in assets_result['licenses']:
            license_item['type'] = 'license'
            all_assets.append(license_item)
        
        return {
            'success': True,
            'user': user,
            'assets': all_assets,
            'assets_breakdown': {
                'hardware': len(assets_result['assets']),
                'accessories': len(assets_result['accessories']),
                'licenses': len(assets_result['licenses'])
            }
        }