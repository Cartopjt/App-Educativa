# core/progress_manager.py
import json
import os
from datetime import datetime

class ProgressManager:
    """Maneja el progreso del usuario"""
    
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.progress_file = os.path.join(data_dir, "progress.json")
        self.ensure_data_dir()
    
    def ensure_data_dir(self):
        """Asegura que el directorio de datos existe"""
        try:
            if not os.path.exists(self.data_dir):
                os.makedirs(self.data_dir)
        except Exception as e:
            print(f"Error al crear directorio de datos: {e}")
    
    def load_progress(self):
        """Carga el progreso guardado"""
        default_progress = {
            "score": 0,
            "level": 1,
            "games_played": 0,
            "words_learned": 0,
            "last_played": None
        }
        
        try:
            if os.path.exists(self.progress_file):
                with open(self.progress_file, 'r', encoding='utf-8') as f:
                    progress = json.load(f)
                    # Asegurar que todas las claves existan
                    for key, value in default_progress.items():
                        if key not in progress:
                            progress[key] = value
                    return progress
        except Exception as e:
            print(f"Error al cargar progreso: {e}")
        
        return default_progress
    
    def save_progress(self, progress_data):
        """Guarda el progreso"""
        try:
            # Cargar progreso existente para preservar datos no proporcionados
            existing_progress = self.load_progress()
            
            # Actualizar con nuevos datos
            existing_progress.update(progress_data)
            
            # Añadir fecha de guardado
            existing_progress['last_saved'] = datetime.now().isoformat()
            
            # Guardar en archivo
            with open(self.progress_file, 'w', encoding='utf-8') as f:
                json.dump(existing_progress, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Error al guardar progreso: {e}")
            return False
    
    def reset_progress(self):
        """Reinicia todo el progreso del usuario"""
        try:
            default_progress = {
                "score": 0,
                "level": 1,
                "games_played": 0,
                "words_learned": 0,
                "last_played": None,
                "reset_date": datetime.now().isoformat()
            }
            
            with open(self.progress_file, 'w', encoding='utf-8') as f:
                json.dump(default_progress, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Error al reiniciar progreso: {e}")
            return False