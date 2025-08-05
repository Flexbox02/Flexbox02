import os
import json
from typing import Dict, Optional

class GUIConfig:
    """Configuración para la aplicación GUI"""
    
    CONFIG_FILE = "snipe_it_config.json"
    
    def __init__(self):
        self.config_path = os.path.join(os.path.expanduser("~"), self.CONFIG_FILE)
        self._config = self._load_config()
    
    def _load_config(self) -> Dict:
        """Cargar configuración desde archivo"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return {}
    
    def save_config(self, snipe_url: str, api_token: str) -> bool:
        """Guardar configuración en archivo"""
        try:
            self._config = {
                'snipe_url': snipe_url.rstrip('/'),
                'api_token': api_token,
                'last_updated': str(os.path.getmtime(__file__))
            }
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=2)
            return True
        except IOError:
            return False
    
    def get_snipe_url(self) -> Optional[str]:
        """Obtener URL de Snipe IT"""
        return self._config.get('snipe_url')
    
    def get_api_token(self) -> Optional[str]:
        """Obtener API Token"""
        return self._config.get('api_token')
    
    def is_configured(self) -> bool:
        """Verificar si la aplicación está configurada"""
        return bool(self.get_snipe_url() and self.get_api_token())
    
    def clear_config(self) -> bool:
        """Limpiar configuración"""
        try:
            if os.path.exists(self.config_path):
                os.remove(self.config_path)
            self._config = {}
            return True
        except IOError:
            return False