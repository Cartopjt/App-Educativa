import tkinter as tk
from tkinter import ttk, messagebox, font
import random
import json
from datetime import datetime

class EnglishGame:
    
    def __init__(self, root, data_manager):
        self.root = root
        self.data_manager = data_manager
        self.vocabulary = self.load_vocabulary()
        
        # Configuración de colores
        self.colors = {
            'bg_primary': '#2C3E50',
            'bg_secondary': '#34495E',
            'accent': '#1ABC9C',
            'accent_dark': '#16A085',
            'text': '#ECF0F1',
            'correct': '#2ECC71',
            'incorrect': '#E74C3C',
            'button': '#3498DB',
            'button_hover': '#2980B9'
        }
        
        # Estado del juego
        self.current_category = None
        self.current_mode = None
        self.current_question = 0
        self.total_questions = 10
        self.correct_answers = 0
        self.current_score = 0
        self.current_level = 1
        
        # Configurar fuente
        self.title_font = font.Font(family='Helvetica', size=24, weight='bold')
        self.heading_font = font.Font(family='Helvetica', size=18, weight='bold')
        self.normal_font = font.Font(family='Helvetica', size=12)
        self.button_font = font.Font(family='Helvetica', size=14, weight='bold')
        
        # Cargar progreso del usuario
        self.load_progress()
        
        # Configurar interfaz
        self.setup_ui()
        
        # Mostrar pantalla de inicio
        self.show_main_menu()
    
    def load_vocabulary(self):
        """Carga el vocabulario desde el módulo de vocabulario"""
        try:
            # Intentar importar dinámicamente
            import vocabulary
            return vocabulary.vocabulary_data
        except ImportError:
            # Vocabulario por defecto si falla la importación
            return {
                "Saludos": {
                    "hola": "hello",
                    "adiós": "goodbye",
                    "buenos días": "good morning",
                    "buenas tardes": "good afternoon",
                    "buenas noches": "good night",
                    "por favor": "please",
                    "gracias": "thank you",
                    "de nada": "you're welcome"
                },
                "Frutas": {
                    "manzana": "apple",
                    "plátano": "banana",
                    "naranja": "orange",
                    "uva": "grape",
                    "fresa": "strawberry",
                    "sandía": "watermelon",
                    "piña": "pineapple",
                    "mango": "mango"
                },
                "Animales": {
                    "perro": "dog",
                    "gato": "cat",
                    "pájaro": "bird",
                    "pez": "fish",
                    "caballo": "horse",
                    "vaca": "cow",
                    "elefante": "elephant",
                    "león": "lion"
                },
                "Familia": {
                    "madre": "mother",
                    "padre": "father",
                    "hermano": "brother",
                    "hermana": "sister",
                    "abuelo": "grandfather",
                    "abuela": "grandmother",
                    "tío": "uncle",
                    "tía": "aunt"
                }
            }
    
    def setup_ui(self):
        """Configura los elementos básicos de la interfaz"""
        # Frame principal
        self.main_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame para el contenido
        self.content_frame = tk.Frame(self.main_frame, bg=self.colors['bg_primary'])
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Frame para la barra superior (puntaje y nivel)
        self.top_bar_frame = tk.Frame(self.main_frame, bg=self.colors['bg_secondary'], height=50)
        self.top_bar_frame.pack(fill=tk.X, padx=10, pady=5)
        self.top_bar_frame.pack_propagate(False)
        
        # Etiquetas para puntaje y nivel
        self.score_label = tk.Label(self.top_bar_frame, 
                                   text=f"Puntos: {self.current_score}", 
                                   bg=self.colors['bg_secondary'],
                                   fg=self.colors['text'],
                                   font=self.button_font)
        self.score_label.pack(side=tk.LEFT, padx=20)
        
        self.level_label = tk.Label(self.top_bar_frame, 
                                   text=f"Nivel: {self.current_level}", 
                                   bg=self.colors['bg_secondary'],
                                   fg=self.colors['text'],
                                   font=self.button_font)
        self.level_label.pack(side=tk.RIGHT, padx=20)
        
        # Botón de volver al menú
        self.back_button = tk.Button(self.top_bar_frame,
                                    text="← Menú Principal",
                                    command=self.show_main_menu,
                                    bg=self.colors['button'],
                                    fg=self.colors['text'],
                                    font=self.normal_font,
                                    padx=10,
                                    pady=5,
                                    cursor="hand2")
        self.back_button.pack(side=tk.LEFT, padx=20)
        self.back_button.pack_forget()  # Ocultar inicialmente
    
    def clear_content_frame(self):
        """Limpia el frame de contenido"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_main_menu(self):
        """Muestra el menú principal del juego"""
        self.clear_content_frame()
        self.current_mode = None
        self.hide_back_button()
        
        # Título
        title_label = tk.Label(self.content_frame,
                              text="English Learning Game",
                              font=self.title_font,
                              bg=self.colors['bg_primary'],
                              fg=self.colors['accent'])
        title_label.pack(pady=(0, 30))
        
        # Subtítulo
        subtitle_label = tk.Label(self.content_frame,
                                 text="Aprende inglés básico de forma divertida",
                                 font=self.normal_font,
                                 bg=self.colors['bg_primary'],
                                 fg=self.colors['text'])
        subtitle_label.pack(pady=(0, 40))
        
        # Frame para botones principales
        buttons_frame = tk.Frame(self.content_frame, bg=self.colors['bg_primary'])
        buttons_frame.pack(pady=20)
        
        # Botones de categorías
        categories_label = tk.Label(buttons_frame,
                                   text="Selecciona una categoría:",
                                   font=self.heading_font,
                                   bg=self.colors['bg_primary'],
                                   fg=self.colors['text'])
        categories_label.pack(pady=(0, 15))
        
        categories = list(self.vocabulary.keys())
        for i in range(0, len(categories), 2):
            row_frame = tk.Frame(buttons_frame, bg=self.colors['bg_primary'])
            row_frame.pack(pady=5)
            
            for j in range(2):
                if i + j < len(categories):
                    category = categories[i + j]
                    btn = tk.Button(row_frame,
                                   text=category,
                                   font=self.button_font,
                                   bg=self.colors['button'],
                                   fg=self.colors['text'],
                                   padx=30,
                                   pady=15,
                                   width=15,
                                   cursor="hand2",
                                   command=lambda cat=category: self.select_category(cat))
                    btn.pack(side=tk.LEFT, padx=10)
        
        # Modo de práctica libre
        practice_label = tk.Label(buttons_frame,
                                 text="Modo de práctica libre:",
                                 font=self.heading_font,
                                 bg=self.colors['bg_primary'],
                                 fg=self.colors['text'])
        practice_label.pack(pady=(30, 15))
        
        practice_frame = tk.Frame(buttons_frame, bg=self.colors['bg_primary'])
        practice_frame.pack()
        
        # Botones para modos de juego
        modes = [
            ("Flashcards", self.start_flashcards),
            ("Quiz", self.start_quiz),
            ("Traducción", self.start_translation_game)
        ]
        
        for mode_name, mode_command in modes:
            btn = tk.Button(practice_frame,
                           text=mode_name,
                           font=self.button_font,
                           bg=self.colors['accent'],
                           fg=self.colors['text'],
                           padx=30,
                           pady=15,
                           width=15,
                           cursor="hand2",
                           command=mode_command)
            btn.pack(side=tk.LEFT, padx=10, pady=5)
    
    def select_category(self, category):
        """Muestra los modos de juego para una categoría específica"""
        self.clear_content_frame()
        self.current_category = category
        self.show_back_button()
        
        # Título de categoría
        title_label = tk.Label(self.content_frame,
                              text=f"Categoría: {category}",
                              font=self.title_font,
                              bg=self.colors['bg_primary'],
                              fg=self.colors['accent'])
        title_label.pack(pady=(0, 30))
        
        # Información de la categoría
        word_count = len(self.vocabulary[category])
        info_label = tk.Label(self.content_frame,
                             text=f"{word_count} palabras para aprender",
                             font=self.normal_font,
                             bg=self.colors['bg_primary'],
                             fg=self.colors['text'])
        info_label.pack(pady=(0, 40))
        
        # Frame para botones de modos
        modes_frame = tk.Frame(self.content_frame, bg=self.colors['bg_primary'])
        modes_frame.pack(pady=20)
        
        modes_label = tk.Label(modes_frame,
                              text="Selecciona un modo de juego:",
                              font=self.heading_font,
                              bg=self.colors['bg_primary'],
                              fg=self.colors['text'])
        modes_label.pack(pady=(0, 20))
        
        # Botones para modos de juego
        modes = [
            ("Flashcards", self.start_flashcards, "Tarjetas para memorizar"),
            ("Quiz", self.start_quiz, "Preguntas de opción múltiple"),
            ("Traducción", self.start_translation_game, "Juego de traducción")
        ]
        
        for mode_name, mode_command, mode_desc in modes:
            mode_frame = tk.Frame(modes_frame, bg=self.colors['bg_primary'])
            mode_frame.pack(pady=10)
            
            btn = tk.Button(mode_frame,
                           text=mode_name,
                           font=self.button_font,
                           bg=self.colors['button'],
                           fg=self.colors['text'],
                           padx=30,
                           pady=10,
                           width=20,
                           cursor="hand2",
                           command=mode_command)
            btn.pack(side=tk.LEFT, padx=5)
            
            desc_label = tk.Label(mode_frame,
                                 text=mode_desc,
                                 font=self.normal_font,
                                 bg=self.colors['bg_primary'],
                                 fg=self.colors['text'])
            desc_label.pack(side=tk.LEFT, padx=10)
    
    def start_flashcards(self):
        """Inicia el modo de juego Flashcards"""
        self.clear_content_frame()
        self.current_mode = "flashcards"
        self.show_back_button()
        
        if not self.current_category:
            # Modo libre - seleccionar categoría aleatoria
            categories = list(self.vocabulary.keys())
            self.current_category = random.choice(categories)
        
        # Obtener palabras de la categoría
        words = list(self.vocabulary[self.current_category].items())
        random.shuffle(words)
        
        if not words:
            messagebox.showinfo("Sin palabras", "No hay palabras en esta categoría.")
            return
        
        self.flashcards_words = words
        self.current_flashcard = 0
        
        # Mostrar primera flashcard
        self.show_flashcard()
    
    def show_flashcard(self):
        """Muestra una flashcard individual"""
        # Limpiar frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        if self.current_flashcard >= len(self.flashcards_words):
            # Fin de las flashcards
            self.show_flashcards_results()
            return
        
        # Obtener palabra actual
        spanish_word, english_word = self.flashcards_words[self.current_flashcard]
        
        # Título
        title_label = tk.Label(self.content_frame,
                              text="Flashcards",
                              font=self.title_font,
                              bg=self.colors['bg_primary'],
                              fg=self.colors['accent'])
        title_label.pack(pady=(0, 20))
        
        # Progreso
        progress_label = tk.Label(self.content_frame,
                                 text=f"Tarjeta {self.current_flashcard + 1} de {len(self.flashcards_words)}",
                                 font=self.normal_font,
                                 bg=self.colors['bg_primary'],
                                 fg=self.colors['text'])
        progress_label.pack(pady=(0, 30))
        
        # Flashcard (simulada con un frame)
        flashcard_frame = tk.Frame(self.content_frame,
                                  bg=self.colors['bg_secondary'],
                                  relief=tk.RAISED,
                                  borderwidth=3)
        flashcard_frame.pack(pady=20, padx=50, fill=tk.BOTH, expand=True)
        
        # Palabra en español (siempre visible)
        spanish_label = tk.Label(flashcard_frame,
                                text=spanish_word,
                                font=font.Font(family='Helvetica', size=32, weight='bold'),
                                bg=self.colors['bg_secondary'],
                                fg=self.colors['text'])
        spanish_label.pack(pady=50)
        
        # Separador
        separator = tk.Frame(flashcard_frame,
                            height=2,
                            bg=self.colors['accent'])
        separator.pack(fill=tk.X, padx=20, pady=10)
        
        # Palabra en inglés (inicialmente oculta)
        self.english_label = tk.Label(flashcard_frame,
                                     text="???",
                                     font=font.Font(family='Helvetica', size=32),
                                     bg=self.colors['bg_secondary'],
                                     fg=self.colors['accent'])
        self.english_label.pack(pady=50)
        
        # Frame para botones
        buttons_frame = tk.Frame(self.content_frame, bg=self.colors['bg_primary'])
        buttons_frame.pack(pady=30)
        
        # Botón para mostrar traducción
        show_btn = tk.Button(buttons_frame,
                            text="Mostrar Traducción",
                            font=self.button_font,
                            bg=self.colors['accent'],
                            fg=self.colors['text'],
                            padx=20,
                            pady=10,
                            cursor="hand2",
                            command=lambda: self.reveal_translation(english_word))
        show_btn.pack(side=tk.LEFT, padx=10)
        
        # Botón para siguiente tarjeta
        next_btn = tk.Button(buttons_frame,
                            text="Siguiente",
                            font=self.button_font,
                            bg=self.colors['button'],
                            fg=self.colors['text'],
                            padx=20,
                            pady=10,
                            cursor="hand2",
                            command=self.next_flashcard)
        next_btn.pack(side=tk.LEFT, padx=10)
        
        # Botón para terminar
        finish_btn = tk.Button(buttons_frame,
                              text="Terminar",
                              font=self.button_font,
                              bg=self.colors['incorrect'],
                              fg=self.colors['text'],
                              padx=20,
                              pady=10,
                              cursor="hand2",
                              command=self.show_flashcards_results)
        finish_btn.pack(side=tk.LEFT, padx=10)
    
    def reveal_translation(self, english_word):
        """Revela la traducción en la flashcard"""
        self.english_label.config(text=english_word, fg=self.colors['text'])
    
    def next_flashcard(self):
        """Pasa a la siguiente flashcard"""
        self.current_flashcard += 1
        self.show_flashcard()
    
    def show_flashcards_results(self):
        """Muestra los resultados del modo flashcards"""
        self.clear_content_frame()
        
        title_label = tk.Label(self.content_frame,
                              text="Flashcards Completadas",
                              font=self.title_font,
                              bg=self.colors['bg_primary'],
                              fg=self.colors['accent'])
        title_label.pack(pady=(0, 30))
        
        # Calcular puntos ganados
        words_learned = min(self.current_flashcard, len(self.flashcards_words))
        points_earned = words_learned * 5
        
        # Actualizar puntaje
        self.current_score += points_earned
        self.update_score()
        
        # Mostrar resultados
        results_text = f"""
        Has revisado {self.current_flashcard} palabras.
        
        Puntos ganados: +{points_earned}
        Puntuación total: {self.current_score}
        
        ¡Buen trabajo! Continúa practicando.
        """
        
        results_label = tk.Label(self.content_frame,
                                text=results_text,
                                font=self.normal_font,
                                bg=self.colors['bg_primary'],
                                fg=self.colors['text'],
                                justify=tk.LEFT)
        results_label.pack(pady=20)
        
        # Botones de acción
        buttons_frame = tk.Frame(self.content_frame, bg=self.colors['bg_primary'])
        buttons_frame.pack(pady=30)
        
        restart_btn = tk.Button(buttons_frame,
                               text="Repetir Flashcards",
                               font=self.button_font,
                               bg=self.colors['button'],
                               fg=self.colors['text'],
                               padx=20,
                               pady=10,
                               cursor="hand2",
                               command=self.start_flashcards)
        restart_btn.pack(side=tk.LEFT, padx=10)
        
        menu_btn = tk.Button(buttons_frame,
                            text="Volver al Menú",
                            font=self.button_font,
                            bg=self.colors['accent'],
                            fg=self.colors['text'],
                            padx=20,
                            pady=10,
                            cursor="hand2",
                            command=self.show_main_menu)
        menu_btn.pack(side=tk.LEFT, padx=10)
    
    def start_quiz(self):
        """Inicia el modo de juego Quiz"""
        self.clear_content_frame()
        self.current_mode = "quiz"
        self.show_back_button()
        
        # Configurar el quiz
        self.current_question = 0
        self.correct_answers = 0
        
        # Preparar preguntas
        self.questions = self.prepare_quiz_questions()
        self.total_questions = len(self.questions)
        
        if self.total_questions == 0:
            messagebox.showinfo("Sin preguntas", "No hay suficientes palabras para crear un quiz.")
            return
        
        # Mostrar primera pregunta
        self.show_quiz_question()
    
    def prepare_quiz_questions(self):
        """Prepara las preguntas para el quiz"""
        questions = []
        
        # Determinar categorías a usar
        if self.current_category:
            categories = [self.current_category]
        else:
            # Modo libre: usar todas las categorías
            categories = list(self.vocabulary.keys())
        
        # Crear preguntas
        for category in categories:
            words = list(self.vocabulary[category].items())
            
            for spanish_word, correct_answer in words:
                # Crear opciones incorrectas
                all_english_words = []
                for cat in categories:
                    all_english_words.extend(self.vocabulary[cat].values())
                
                # Eliminar la respuesta correcta y obtener opciones únicas
                all_english_words = list(set(all_english_words))
                if correct_answer in all_english_words:
                    all_english_words.remove(correct_answer)
                
                # Seleccionar 3 opciones incorrectas aleatorias
                if len(all_english_words) >= 3:
                    wrong_answers = random.sample(all_english_words, 3)
                else:
                    wrong_answers = all_english_words
                
                # Crear lista de opciones
                options = wrong_answers + [correct_answer]
                random.shuffle(options)
                
                # Añadir pregunta
                questions.append({
                    'category': category,
                    'spanish': spanish_word,
                    'correct': correct_answer,
                    'options': options
                })
        
        # Limitar a 10 preguntas máximo
        random.shuffle(questions)
        return questions[:10]
    
    def show_quiz_question(self):
        """Muestra una pregunta del quiz"""
        # Limpiar frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        if self.current_question >= self.total_questions:
            # Fin del quiz
            self.show_quiz_results()
            return
        
        # Obtener pregunta actual
        question = self.questions[self.current_question]
        
        # Título
        title_label = tk.Label(self.content_frame,
                              text="Quiz de Inglés",
                              font=self.title_font,
                              bg=self.colors['bg_primary'],
                              fg=self.colors['accent'])
        title_label.pack(pady=(0, 10))
        
        # Categoría y progreso
        progress_label = tk.Label(self.content_frame,
                                 text=f"Categoría: {question['category']} | Pregunta {self.current_question + 1} de {self.total_questions}",
                                 font=self.normal_font,
                                 bg=self.colors['bg_primary'],
                                 fg=self.colors['text'])
        progress_label.pack(pady=(0, 30))
        
        # Pregunta
        question_frame = tk.Frame(self.content_frame,
                                 bg=self.colors['bg_secondary'],
                                 relief=tk.RAISED,
                                 borderwidth=2)
        question_frame.pack(pady=20, padx=50, fill=tk.BOTH, expand=True)
        
        question_label = tk.Label(question_frame,
                                 text=f"¿Cómo se dice '{question['spanish']}' en inglés?",
                                 font=font.Font(family='Helvetica', size=20),
                                 bg=self.colors['bg_secondary'],
                                 fg=self.colors['text'],
                                 wraplength=600)
        question_label.pack(pady=40)
        
        # Frame para opciones
        options_frame = tk.Frame(self.content_frame, bg=self.colors['bg_primary'])
        options_frame.pack(pady=20)
        
        # Crear botones para cada opción
        for i, option in enumerate(question['options']):
            btn = tk.Button(options_frame,
                           text=option,
                           font=self.button_font,
                           bg=self.colors['button'],
                           fg=self.colors['text'],
                           padx=30,
                           pady=15,
                           width=20,
                           cursor="hand2",
                           command=lambda opt=option, q=question: self.check_quiz_answer(opt, q['correct']))
            btn.pack(pady=5)
    
    def check_quiz_answer(self, selected_option, correct_answer):
        """Verifica la respuesta del quiz"""
        if selected_option == correct_answer:
            # Respuesta correcta
            self.correct_answers += 1
            self.show_feedback("¡Correcto!", True)
        else:
            # Respuesta incorrecta
            self.show_feedback(f"Incorrecto. La respuesta correcta es: {correct_answer}", False)
        
        # Pasar a la siguiente pregunta después de un breve retraso
        self.root.after(1500, self.next_quiz_question)
    
    def show_feedback(self, message, is_correct):
        """Muestra retroalimentación visual"""
        # Crear ventana emergente
        feedback_window = tk.Toplevel(self.root)
        feedback_window.title("Resultado")
        feedback_window.geometry("400x200")
        feedback_window.configure(bg=self.colors['bg_primary'])
        feedback_window.transient(self.root)
        feedback_window.grab_set()
        
        # Centrar ventana
        feedback_window.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (feedback_window.winfo_width() // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (feedback_window.winfo_height() // 2)
        feedback_window.geometry(f"+{x}+{y}")
        
        # Color según resultado
        bg_color = self.colors['correct'] if is_correct else self.colors['incorrect']
        
        # Mensaje
        msg_label = tk.Label(feedback_window,
                            text=message,
                            font=self.heading_font,
                            bg=bg_color,
                            fg=self.colors['text'],
                            wraplength=350)
        msg_label.pack(pady=50, padx=20, fill=tk.BOTH, expand=True)
        
        # Cerrar automáticamente después de 1.5 segundos
        feedback_window.after(1500, feedback_window.destroy)
    
    def next_quiz_question(self):
        """Pasa a la siguiente pregunta del quiz"""
        self.current_question += 1
        self.show_quiz_question()
    
    def show_quiz_results(self):
        """Muestra los resultados del quiz"""
        self.clear_content_frame()
        
        title_label = tk.Label(self.content_frame,
                              text="Quiz Completado",
                              font=self.title_font,
                              bg=self.colors['bg_primary'],
                              fg=self.colors['accent'])
        title_label.pack(pady=(0, 30))
        
        # Calcular porcentaje y puntos
        percentage = (self.correct_answers / self.total_questions) * 100
        points_earned = self.correct_answers * 10
        
        # Actualizar puntaje
        self.current_score += points_earned
        self.update_score()
        
        # Verificar si sube de nivel
        level_up = False
        if self.current_score >= self.current_level * 100:
            self.current_level += 1
            level_up = True
        
        # Mostrar resultados
        results_text = f"""
        Resultados del Quiz:
        
        Preguntas: {self.total_questions}
        Correctas: {self.correct_answers}
        Porcentaje: {percentage:.1f}%
        
        Puntos ganados: +{points_earned}
        Puntuación total: {self.current_score}
        Nivel actual: {self.current_level}
        """
        
        if level_up:
            results_text += f"\n\n¡FELICIDADES! ¡Has subido al nivel {self.current_level}!"
        
        results_label = tk.Label(self.content_frame,
                                text=results_text,
                                font=self.normal_font,
                                bg=self.colors['bg_primary'],
                                fg=self.colors['text'],
                                justify=tk.LEFT)
        results_label.pack(pady=20)
        
        # Botones de acción
        buttons_frame = tk.Frame(self.content_frame, bg=self.colors['bg_primary'])
        buttons_frame.pack(pady=30)
        
        restart_btn = tk.Button(buttons_frame,
                               text="Jugar otro Quiz",
                               font=self.button_font,
                               bg=self.colors['button'],
                               fg=self.colors['text'],
                               padx=20,
                               pady=10,
                               cursor="hand2",
                               command=self.start_quiz)
        restart_btn.pack(side=tk.LEFT, padx=10)
        
        menu_btn = tk.Button(buttons_frame,
                            text="Volver al Menú",
                            font=self.button_font,
                            bg=self.colors['accent'],
                            fg=self.colors['text'],
                            padx=20,
                            pady=10,
                            cursor="hand2",
                            command=self.show_main_menu)
        menu_btn.pack(side=tk.LEFT, padx=10)
        
        # Guardar progreso
        self.save_progress()
    
    def start_translation_game(self):
        """Inicia el juego de traducción"""
        self.clear_content_frame()
        self.current_mode = "translation"
        self.show_back_button()
        
        # Configurar el juego
        self.current_question = 0
        self.correct_answers = 0
        
        # Preparar palabras
        self.translation_words = self.prepare_translation_words()
        self.total_questions = len(self.translation_words)
        
        if self.total_questions == 0:
            messagebox.showinfo("Sin palabras", "No hay suficientes palabras para el juego.")
            return
        
        # Mostrar primera palabra
        self.show_translation_word()
    
    def prepare_translation_words(self):
        """Prepara las palabras para el juego de traducción"""
        words = []
        
        # Determinar categorías a usar
        if self.current_category:
            categories = [self.current_category]
        else:
            # Modo libre: usar todas las categorías
            categories = list(self.vocabulary.keys())
        
        # Recoger palabras
        for category in categories:
            for spanish, english in self.vocabulary[category].items():
                words.append({
                    'category': category,
                    'spanish': spanish,
                    'english': english
                })
        
        # Limitar a 10 palabras máximo
        random.shuffle(words)
        return words[:10]
    
    def show_translation_word(self):
        """Muestra una palabra para traducir"""
        # Limpiar frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        if self.current_question >= self.total_questions:
            # Fin del juego
            self.show_translation_results()
            return
        
        # Obtener palabra actual
        word = self.translation_words[self.current_question]
        
        # Título
        title_label = tk.Label(self.content_frame,
                              text="Juego de Traducción",
                              font=self.title_font,
                              bg=self.colors['bg_primary'],
                              fg=self.colors['accent'])
        title_label.pack(pady=(0, 10))
        
        # Categoría y progreso
        progress_label = tk.Label(self.content_frame,
                                 text=f"Categoría: {word['category']} | Palabra {self.current_question + 1} de {self.total_questions}",
                                 font=self.normal_font,
                                 bg=self.colors['bg_primary'],
                                 fg=self.colors['text'])
        progress_label.pack(pady=(0, 30))
        
        # Palabra a traducir
        word_frame = tk.Frame(self.content_frame,
                             bg=self.colors['bg_secondary'],
                             relief=tk.RAISED,
                             borderwidth=2)
        word_frame.pack(pady=20, padx=50, fill=tk.BOTH, expand=True)
        
        word_label = tk.Label(word_frame,
                             text=f"Traduce al inglés:\n\n'{word['spanish']}'",
                             font=font.Font(family='Helvetica', size=24),
                             bg=self.colors['bg_secondary'],
                             fg=self.colors['text'])
        word_label.pack(pady=40)
        
        # Entrada de texto para la traducción
        input_frame = tk.Frame(self.content_frame, bg=self.colors['bg_primary'])
        input_frame.pack(pady=20)
        
        self.answer_var = tk.StringVar()
        
        answer_entry = tk.Entry(input_frame,
                               textvariable=self.answer_var,
                               font=font.Font(family='Helvetica', size=16),
                               width=30)
        answer_entry.pack(pady=10)
        answer_entry.focus()
        
        # Botón para verificar
        check_btn = tk.Button(input_frame,
                             text="Verificar",
                             font=self.button_font,
                             bg=self.colors['accent'],
                             fg=self.colors['text'],
                             padx=30,
                             pady=10,
                             cursor="hand2",
                             command=lambda: self.check_translation(self.answer_var.get(), word['english']))
        check_btn.pack(pady=10)
        
        # Permitir verificar con Enter
        answer_entry.bind('<Return>', lambda e: check_btn.invoke())
    
    def check_translation(self, user_answer, correct_answer):
        """Verifica la traducción del usuario"""
        # Normalizar respuestas (minúsculas, sin espacios extras)
        user_answer_clean = user_answer.strip().lower()
        correct_answer_clean = correct_answer.lower()
        
        if user_answer_clean == correct_answer_clean:
            # Respuesta correcta
            self.correct_answers += 1
            self.show_translation_feedback("¡Correcto!", True, correct_answer_clean)
        else:
            # Respuesta incorrecta
            self.show_translation_feedback(f"Incorrecto. La respuesta es: {correct_answer}", False, correct_answer_clean)
        
        # Pasar a la siguiente palabra después de un retraso
        self.root.after(2000, self.next_translation_word)
    
    def show_translation_feedback(self, message, is_correct, correct_answer):
        """Muestra retroalimentación para el juego de traducción"""
        feedback_window = tk.Toplevel(self.root)
        feedback_window.title("Resultado")
        feedback_window.geometry("500x250")
        feedback_window.configure(bg=self.colors['bg_primary'])
        feedback_window.transient(self.root)
        feedback_window.grab_set()
        
        # Centrar ventana
        feedback_window.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (feedback_window.winfo_width() // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (feedback_window.winfo_height() // 2)
        feedback_window.geometry(f"+{x}+{y}")
        
        # Color según resultado
        bg_color = self.colors['correct'] if is_correct else self.colors['incorrect']
        
        # Contenido
        content_frame = tk.Frame(feedback_window, bg=bg_color)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Mensaje
        msg_label = tk.Label(content_frame,
                            text=message,
                            font=self.heading_font,
                            bg=bg_color,
                            fg=self.colors['text'],
                            wraplength=450)
        msg_label.pack(pady=10)
        
        # Pronunciación (si es correcto)
        if is_correct:
            pronunciation_label = tk.Label(content_frame,
                                          text=f"Pronunciación: /{self.get_pronunciation_guide(correct_answer)}/",
                                          font=self.normal_font,
                                          bg=bg_color,
                                          fg=self.colors['text'])
            pronunciation_label.pack(pady=10)
        
        # Cerrar automáticamente después de 2 segundos
        feedback_window.after(2000, feedback_window.destroy)
    
    def get_pronunciation_guide(self, word):
        """Proporciona una guía de pronunciación simple (simulada)"""
        # Esta es una guía de pronunciación muy básica
        pronunciation_guide = {
            "hello": "je-lou",
            "goodbye": "gud-bai",
            "apple": "a-pul",
            "banana": "ba-na-na",
            "dog": "dog",
            "cat": "cat",
            "mother": "ma-der",
            "father": "fa-der"
        }
        
        return pronunciation_guide.get(word.lower(), word.lower())
    
    def next_translation_word(self):
        """Pasa a la siguiente palabra del juego de traducción"""
        self.current_question += 1
        self.show_translation_word()
    
    def show_translation_results(self):
        """Muestra los resultados del juego de traducción"""
        self.clear_content_frame()
        
        title_label = tk.Label(self.content_frame,
                              text="Juego de Traducción Completado",
                              font=self.title_font,
                              bg=self.colors['bg_primary'],
                              fg=self.colors['accent'])
        title_label.pack(pady=(0, 30))
        
        # Calcular puntos
        points_earned = self.correct_answers * 15  # Más puntos por traducción
        
        # Actualizar puntaje
        self.current_score += points_earned
        self.update_score()
        
        # Verificar si sube de nivel
        level_up = False
        if self.current_score >= self.current_level * 100:
            self.current_level += 1
            level_up = True
        
        # Mostrar resultados
        results_text = f"""
        Resultados del Juego de Traducción:
        
        Palabras: {self.total_questions}
        Traducciones correctas: {self.correct_answers}
        
        Puntos ganados: +{points_earned}
        Puntuación total: {self.current_score}
        Nivel actual: {self.current_level}
        """
        
        if level_up:
            results_text += f"\n\n¡FELICIDADES! ¡Has subido al nivel {self.current_level}!"
        
        results_label = tk.Label(self.content_frame,
                                text=results_text,
                                font=self.normal_font,
                                bg=self.colors['bg_primary'],
                                fg=self.colors['text'],
                                justify=tk.LEFT)
        results_label.pack(pady=20)
        
        # Botones de acción
        buttons_frame = tk.Frame(self.content_frame, bg=self.colors['bg_primary'])
        buttons_frame.pack(pady=30)
        
        restart_btn = tk.Button(buttons_frame,
                               text="Jugar otra vez",
                               font=self.button_font,
                               bg=self.colors['button'],
                               fg=self.colors['text'],
                               padx=20,
                               pady=10,
                               cursor="hand2",
                               command=self.start_translation_game)
        restart_btn.pack(side=tk.LEFT, padx=10)
        
        menu_btn = tk.Button(buttons_frame,
                            text="Volver al Menú",
                            font=self.button_font,
                            bg=self.colors['accent'],
                            fg=self.colors['text'],
                            padx=20,
                            pady=10,
                            cursor="hand2",
                            command=self.show_main_menu)
        menu_btn.pack(side=tk.LEFT, padx=10)
        
        # Guardar progreso
        self.save_progress()
    
    def show_back_button(self):
        """Muestra el botón para volver al menú principal"""
        self.back_button.pack(side=tk.LEFT, padx=20)
    
    def hide_back_button(self):
        """Oculta el botón para volver al menú principal"""
        self.back_button.pack_forget()
    
    def update_score(self):
        """Actualiza la etiqueta del puntaje"""
        self.score_label.config(text=f"Puntos: {self.current_score}")
        self.level_label.config(text=f"Nivel: {self.current_level}")
    
    def load_progress(self):
        """Carga el progreso del usuario"""
        try:
            progress = self.data_manager.load_progress()
            self.current_score = progress.get('score', 0)
            self.current_level = progress.get('level', 1)
        except Exception as e:
            print(f"Error al cargar progreso: {e}")
            # Usar valores por defecto
            self.current_score = 0
            self.current_level = 1
    
    def save_progress(self):
        """Guarda el progreso del usuario"""
        try:
            progress = {
                'score': self.current_score,
                'level': self.current_level,
                'last_saved': datetime.now().isoformat()
            }
            self.data_manager.save_progress(progress)
        except Exception as e:
            print(f"Error al guardar progreso: {e}")