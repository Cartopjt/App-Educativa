import json
import os
import random
from datetime import datetime
from .vocabulary import vocabulary_data

class Game:
    
    def __init__(self, base_dir=None):
        self.vocabulary = vocabulary_data
        self.score = 0
        self.level = 1
        self.current_category = None
        self.load_progress()
    
    def load_progress(self):
        try:
            if os.path.exists("data/progress.json"):
                with open("data/progress.json", "r") as f:
                    data = json.load(f)
                    self.score = data.get("score", 0)
                    self.level = data.get("level", 1)
        except:
            self.score = 0
            self.level = 1
    
    def save_progress(self):
        """Guarda el progreso"""
        os.makedirs("data", exist_ok=True)
        with open("data/progress.json", "w") as f:
            json.dump({
                "score": self.score,
                "level": self.level,
                "saved": datetime.now().isoformat()
            }, f, indent=2)
    
    def get_categories(self):
        return list(self.vocabulary.keys())
    
    def get_category_words(self, category):
        return self.vocabulary.get(category, {})
    
    def get_random_word(self, category=None):
        if category:
            words = self.vocabulary.get(category, {})
        else:
            # Juntar todas las palabras de todas las categorías
            words = {}
            for cat_words in self.vocabulary.values():
                words.update(cat_words)
        
        if not words:
            return None, None
        
        spanish_word = random.choice(list(words.keys()))
        english_word = words[spanish_word]
        
        return spanish_word, english_word
    
    def add_points(self, points):
        """Añade puntos"""
        self.score += points
        # Subir nivel cada 100 puntos
        if self.score >= self.level * 100:
            self.level += 1
        self.save_progress()
        return self.level
    
    def get_word_count(self):
        total = 0
        for category in self.vocabulary.values():
            total += len(category)
        return total