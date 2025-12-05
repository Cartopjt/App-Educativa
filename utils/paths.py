import sys
import os

class PathManager:
    """Gestiona las rutas de archivos para funcionar en .exe y desarrollo"""
    
    @staticmethod
    def get_base_path():
        """Obtiene el directorio base de la aplicación"""
        if getattr(sys, 'frozen', False):
            # Ejecutable empaquetado (.exe)
            return sys._MEIPASS
        else:
            # Desarrollo normal
            return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    @staticmethod
    def get_resource_path(relative_path):
        """Obtiene la ruta absoluta a un recurso"""
        try:
            # Para PyInstaller
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        return os.path.join(base_path, relative_path)
    
    @staticmethod
    def get_data_path(filename):
        """Obtiene la ruta para archivos de datos (se guardan en AppData)"""
        if getattr(sys, 'frozen', False):
            # En .exe, guardar en AppData
            app_name = "EnglishAdventure"
            if os.name == 'nt':  # Windows
                import ctypes.wintypes
                CSIDL_APPDATA = 26
                path_buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
                ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_APPDATA, None, 0, path_buf)
                appdata_dir = path_buf.value
                data_dir = os.path.join(appdata_dir, app_name)
            else:  # Linux/Mac
                home_dir = os.path.expanduser("~")
                data_dir = os.path.join(home_dir, f".{app_name.lower()}")
        else:
            # En desarrollo, usar carpeta local
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            data_dir = os.path.join(base_dir, "data")
        
        # Crear directorio si no existe
        os.makedirs(data_dir, exist_ok=True)
        
        return os.path.join(data_dir, filename)