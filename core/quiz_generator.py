import random

class QuizGenerator:
    
    def __init__(self, vocabulary):
        self.vocabulary = vocabulary
    
    def generate_multiple_choice(self, category=None, num_questions=10):
        """Genera preguntas de opción múltiple"""
        questions = []
        
        # Determinar categorías a usar
        if category:
            categories = [category]
        else:
            categories = list(self.vocabulary.keys())
        
        # Si no hay suficientes palabras, usar todas las categorías
        total_words = sum(len(self.vocabulary[cat]) for cat in categories)
        if total_words < num_questions:
            categories = list(self.vocabulary.keys())
        
        # Recolectar todas las palabras de las categorías seleccionadas
        all_words = []
        for cat in categories:
            for spanish, english in self.vocabulary[cat].items():
                all_words.append({
                    'category': cat,
                    'spanish': spanish,
                    'english': english
                })
        
        # Mezclar y seleccionar palabras
        random.shuffle(all_words)
        selected_words = all_words[:num_questions]
        
        # Crear preguntas
        all_english_words = [word['english'] for word in all_words]
        
        for word_data in selected_words:
            # Obtener todas las posibles respuestas incorrectas
            wrong_answers = [w for w in all_english_words if w != word_data['english']]
            
            # Seleccionar 3 opciones incorrectas aleatorias
            if len(wrong_answers) >= 3:
                selected_wrong = random.sample(wrong_answers, 3)
            else:
                selected_wrong = wrong_answers
            
            # Crear lista de opciones
            options = selected_wrong + [word_data['english']]
            random.shuffle(options)
            
            questions.append({
                'category': word_data['category'],
                'spanish': word_data['spanish'],
                'correct': word_data['english'],
                'options': options,
                'type': 'multiple_choice'
            })
        
        return questions