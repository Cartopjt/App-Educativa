import json
import os
from datetime import datetime

class DataManager:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.progress_file = os.path.join(data_dir, "progress.json")
        self.stats_file = os.path.join(data_dir, "stats.json")
        
        self.ensure_data_dir()
    
    def ensure_data_dir(self):
        try:
            if not os.path.exists(self.data_dir):
                os.makedirs(self.data_dir)
        except Exception as e:
            print(f"Error al crear directorio de datos: {e}")
    
    def load_progress(self):
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
                    for key, value in default_progress.items():
                        if key not in progress:
                            progress[key] = value
                    return progress
        except Exception as e:
            print(f"Error al cargar progreso: {e}")
        
        return default_progress
    
    def save_progress(self, progress_data):
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
    
    def update_stats(self, game_type, correct_answers, total_questions):
        # Actualiza las estadísticas del usuario
        try:
            # Cargar estadísticas existentes
            stats = self.load_stats()
            
            # Actualizar estadísticas generales
            stats['total_games'] = stats.get('total_games', 0) + 1
            stats['total_questions'] = stats.get('total_questions', 0) + total_questions
            stats['total_correct'] = stats.get('total_correct', 0) + correct_answers
            
            # Actualizar estadísticas por tipo de juego
            if game_type not in stats['games']:
                stats['games'][game_type] = {
                    'played': 0,
                    'questions': 0,
                    'correct': 0
                }
            
            stats['games'][game_type]['played'] += 1
            stats['games'][game_type]['questions'] += total_questions
            stats['games'][game_type]['correct'] += correct_answers
            
            # Calcular porcentajes
            if stats['total_questions'] > 0:
                stats['overall_accuracy'] = (stats['total_correct'] / stats['total_questions']) * 100
            
            # Guardar estadísticas actualizadas
            self.save_stats(stats)
            
            return True
        except Exception as e:
            print(f"Error al actualizar estadísticas: {e}")
            return False
    
    def load_stats(self):
        default_stats = {
            "total_games": 0,
            "total_questions": 0,
            "total_correct": 0,
            "overall_accuracy": 0,
            "games": {},
            "first_play": datetime.now().isoformat(),
            "last_play": None
        }
        
        try:
            if os.path.exists(self.stats_file):
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    stats = json.load(f)
                    # Asegurar que todas las claves existan
                    for key, value in default_stats.items():
                        if key not in stats:
                            stats[key] = value
                    return stats
        except Exception as e:
            print(f"Error al cargar estadísticas: {e}")
        
        return default_stats
    
    def save_stats(self, stats_data):
        try:
            # Actualizar fecha de última jugada
            stats_data['last_play'] = datetime.now().isoformat()
            
            # Guardar en archivo
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(stats_data, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Error al guardar estadísticas: {e}")
            return False
    
    def get_achievements(self):
        progress = self.load_progress()
        stats = self.load_stats()
        
        achievements = []
        
        # Logros basados en puntuación
        if progress['score'] >= 100:
            achievements.append("Primeros 100 puntos")
        if progress['score'] >= 500:
            achievements.append("500 puntos")
        if progress['score'] >= 1000:
            achievements.append("Maestro del inglés (1000 puntos)")
        
        # Logros basados en nivel
        if progress['level'] >= 5:
            achievements.append("Nivel 5 alcanzado")
        if progress['level'] >= 10:
            achievements.append("Nivel 10 alcanzado")
        
        # Logros basados en juegos jugados
        if stats.get('total_games', 0) >= 10:
            achievements.append("10 juegos completados")
        if stats.get('total_games', 0) >= 50:
            achievements.append("50 juegos completados")
        
        # Logros basados en precisión
        if stats.get('overall_accuracy', 0) >= 80:
            achievements.append("Precisión del 80%")
        if stats.get('overall_accuracy', 0) >= 95:
            achievements.append("Precisión experta (95%)")
        
        return achievements
    
    def reset_progress(self):
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