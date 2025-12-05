import tkinter as tk
from tkinter import ttk, messagebox, font, simpledialog
import random
import json
from datetime import datetime
import pygame
import os

from core.vocabulary import vocabulary_data
from core.quiz_generator import QuizGenerator
from utils.sound_manager import SoundManager

class EnglishApp:
    def __init__(self, game):
        self.game = game
        self.vocabulary = vocabulary_data
        self.quiz_generator = QuizGenerator(vocabulary_data)
        self.player_name = "Explorador"
        
        # Cargar nombre guardado si existe
        self.load_player_name()
        
        # Configuración de colores
        self.colors = {
            'bg_primary': '#E6F3FF',
            'bg_secondary': '#FFE6F2',
            'bg_gradient_start': '#FFE6E6',
            'bg_gradient_end': '#E6F3FF',
            'accent': '#FF6B8B',
            'accent_dark': '#FF4D6D',
            'text': '#333366',
            'correct': '#4CD964',
            'incorrect': '#FF3B30',
            'button': '#5AC8FA',
            'button_hover': '#34AADC',
            'highlight': '#FFD166',
            'card_bg': '#FFFFFF',
            'shadow': '#E0E0E0',
            'shadow_dark': '#B0B0B0',
            'transparent_gray': '#F5F5F5'
        }
        
        # Estado del juego
        self.current_category = None
        self.current_mode = None
        self.current_question = 0
        self.total_questions = 10
        self.correct_answers = 0
        self.quiz_questions = []
        self.current_score = self.game.score
        self.current_level = self.game.level
        
        # Variables para juego de traducción
        self.translation_words = []
        self.current_translation_index = 0
        self.translation_score = 0
        
        # Configurar ventana
        self.root = tk.Tk()
        self.setup_fonts()
        self.setup_window()
        
        # Configurar sonidos
        try:
            self.sound_manager = SoundManager(enabled=True)
        except:
            self.sound_manager = None
            print("⚠️ Sonidos desactivados")
        
        # Mostrar pantalla de inicio
        self.show_main_menu()
    
    def load_player_name(self):
        """Carga el nombre del jugador desde archivo"""
        try:
            if os.path.exists("data/player.json"):
                with open("data/player.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.player_name = data.get("name", "Explorador")
        except:
            self.player_name = "Explorador"
    
    def save_player_name(self):
        """Guarda el nombre del jugador"""
        try:
            os.makedirs("data", exist_ok=True)
            with open("data/player.json", "w", encoding="utf-8") as f:
                json.dump({"name": self.player_name}, f, indent=2, ensure_ascii=False)
        except:
            pass
    
    def change_player_name(self):
        """Permite al jugador cambiar su nombre"""
        new_name = simpledialog.askstring(
            "Cambiar Nombre",
            "Ingresa tu nuevo nombre:",
            initialvalue=self.player_name,
            parent=self.root
        )
        
        if new_name and new_name.strip():
            self.player_name = new_name.strip()
            self.save_player_name()
            messagebox.showinfo("¡Listo!", f"Ahora te llamas: {self.player_name}")
            self.show_main_menu()
    
    def setup_fonts(self):
        """Configura las fuentes"""
        self.title_font = font.Font(family='Comic Sans MS', size=28, weight='bold')
        self.heading_font = font.Font(family='Comic Sans MS', size=20, weight='bold')
        self.normal_font = font.Font(family='Comic Sans MS', size=12)
        self.button_font = font.Font(family='Comic Sans MS', size=14, weight='bold')
        self.game_font = font.Font(family='Comic Sans MS', size=16)
    
    def setup_window(self):
        """Configura la ventana principal con tamaño adaptable"""
        self.root.title("✨ Aventura de Inglés para Niños ✨")
        
        # Obtener tamaño de pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Tamaño adaptable (80% de pantalla máximo)
        window_width = min(1000, int(screen_width * 0.8))
        window_height = min(700, int(screen_height * 0.8))
        
        # Centrar ventana
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.minsize(800, 600)
        self.root.configure(bg=self.colors['bg_primary'])
        
        # Configurar grid para que sea responsive
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Frame principal con grid
        self.main_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Barra superior
        self.setup_top_bar()
        
        # Frame para contenido principal con scroll
        self.setup_content_frame()
    
    def setup_content_frame(self):
        """Configura el frame de contenido con scroll"""
        # Frame contenedor
        self.content_container = tk.Frame(self.main_frame, bg=self.colors['bg_primary'])
        self.content_container.grid(row=1, column=0, sticky="nsew", pady=(10, 0))
        self.content_container.grid_rowconfigure(0, weight=1)
        self.content_container.grid_columnconfigure(0, weight=1)
        
        # Canvas para scroll
        self.canvas = tk.Canvas(self.content_container, bg=self.colors['card_bg'], 
                               highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.content_container, orient="vertical", 
                                 command=self.canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Configurar canvas
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Frame interno dentro del canvas
        self.content_frame = tk.Frame(self.canvas, bg=self.colors['card_bg'])
        self.canvas_window = self.canvas.create_window((0, 0), window=self.content_frame, 
                                                      anchor="nw", tags="self.content_frame")
        
        # Configurar scroll
        self.content_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        
        # Bind eventos de mouse para scroll
        self.content_frame.bind("<Enter>", self.bind_mousewheel)
        self.content_frame.bind("<Leave>", self.unbind_mousewheel)
    
    def on_frame_configure(self, event):
        """Actualiza scrollregion cuando cambia el frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def on_canvas_configure(self, event):
        """Ajusta el tamaño del frame interno cuando cambia el canvas"""
        self.canvas.itemconfig(self.canvas_window, width=event.width)
    
    def bind_mousewheel(self, event):
        """Habilita scroll con mousewheel"""
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
    
    def unbind_mousewheel(self, event):
        """Deshabilita scroll con mousewheel"""
        self.canvas.unbind_all("<MouseWheel>")
    
    def on_mousewheel(self, event):
        """Maneja scroll con mousewheel"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def setup_top_bar(self):
        """Configura la barra superior mejorada"""
        top_bar = tk.Frame(self.main_frame, bg=self.colors['bg_secondary'], 
                          height=70, relief='flat')
        top_bar.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        top_bar.grid_columnconfigure(1, weight=1)
        top_bar.pack_propagate(False)
        
        # Logo izquierdo
        logo_frame = tk.Frame(top_bar, bg=self.colors['bg_secondary'])
        logo_frame.pack(side=tk.LEFT, padx=20)
        
        tk.Label(logo_frame, text="📚✨", font=font.Font(size=24),
                bg=self.colors['bg_secondary'], fg=self.colors['accent']).pack(side=tk.LEFT)
        
        tk.Label(logo_frame, text="EDULINGO", 
                font=font.Font(family='Comic Sans MS', size=16, weight='bold'),
                bg=self.colors['bg_secondary'], fg=self.colors['text']).pack(side=tk.LEFT, padx=5)
        
        # Centro: Información del jugador
        center_frame = tk.Frame(top_bar, bg=self.colors['bg_secondary'])
        center_frame.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=20)
        
        # Nombre del jugador con botón para cambiar
        name_frame = tk.Frame(center_frame, bg=self.colors['bg_secondary'])
        name_frame.pack(pady=5)
        
        tk.Label(name_frame, text=f"👤 {self.player_name}", 
                font=self.normal_font,
                bg=self.colors['bg_secondary'], 
                fg=self.colors['text']).pack(side=tk.LEFT)
        
        change_name_btn = tk.Button(name_frame, text="✏️", 
                                   font=font.Font(size=10),
                                   bg=self.colors['button'],
                                   fg='white',
                                   padx=5,
                                   pady=2,
                                   cursor="hand2",
                                   command=self.change_player_name)
        change_name_btn.pack(side=tk.LEFT, padx=(10, 0))
        
        # Puntaje y nivel
        stats_frame = tk.Frame(center_frame, bg=self.colors['bg_secondary'])
        stats_frame.pack()
        
        self.score_label = tk.Label(stats_frame, 
                                   text=f"🏆 {self.current_score} Puntos",
                                   font=self.normal_font,
                                   bg=self.colors['bg_secondary'],
                                   fg=self.colors['text'])
        self.score_label.pack(side=tk.LEFT, padx=10)
        
        self.level_label = tk.Label(stats_frame,
                                   text=f"⭐ Nivel {self.current_level}",
                                   font=self.normal_font,
                                   bg=self.colors['bg_secondary'],
                                   fg=self.colors['text'])
        self.level_label.pack(side=tk.LEFT, padx=10)
        
        # Botón de menú derecho
        self.back_button = tk.Button(top_bar,
                                    text="🏠 Menú Principal",
                                    font=self.button_font,
                                    bg=self.colors['button'],
                                    fg='white',
                                    padx=15,
                                    pady=8,
                                    cursor="hand2",
                                    command=self.show_main_menu)
        self.back_button.pack(side=tk.RIGHT, padx=20)
        self.back_button.pack_forget()
    
    def show_main_menu(self):
        """Muestra el menú principal mejorado"""
        self.clear_content_frame()
        self.current_mode = None
        self.hide_back_button()
        
        # Contenedor principal con padding
        main_container = tk.Frame(self.content_frame, bg=self.colors['card_bg'])
        main_container.pack(expand=True, fill=tk.BOTH, padx=30, pady=30)
        
        # Bienvenida personalizada
        welcome_frame = tk.Frame(main_container, bg=self.colors['card_bg'])
        welcome_frame.pack(pady=(0, 30))
        
        welcome_text = f"¡Hola, {self.player_name}!"
        tk.Label(welcome_frame, text=welcome_text,
                font=self.title_font,
                bg=self.colors['card_bg'],
                fg=self.colors['accent']).pack()
        
        tk.Label(welcome_frame, text="¡Aprende inglés divirtiéndote!",
                font=self.normal_font,
                bg=self.colors['card_bg'],
                fg=self.colors['text']).pack(pady=10)
        
        # Tarjeta de estadísticas
        stats_card = tk.Frame(main_container, bg=self.colors['bg_secondary'],
                            relief='ridge', bd=2)
        stats_card.pack(pady=20, padx=50, fill=tk.X)
        
        stats_content = tk.Frame(stats_card, bg=self.colors['bg_secondary'], pady=15)
        stats_content.pack()
        
        stats_grid = tk.Frame(stats_content, bg=self.colors['bg_secondary'])
        stats_grid.pack()
        
        # Estadísticas en grid 2x2
        stats_data = [
            ("📊 Palabras Totales", str(sum(len(cat) for cat in self.vocabulary.values()))),
            ("🎮 Categorías", str(len(self.vocabulary))),
            ("🏆 Tu Puntaje", str(self.current_score)),
            ("⭐ Tu Nivel", str(self.current_level))
        ]
        
        for i, (label, value) in enumerate(stats_data):
            frame = tk.Frame(stats_grid, bg=self.colors['bg_secondary'])
            frame.grid(row=i//2, column=i%2, padx=30, pady=10)
            
            tk.Label(frame, text=label, font=self.normal_font,
                    bg=self.colors['bg_secondary'], fg=self.colors['text']).pack()
            tk.Label(frame, text=value, font=self.heading_font,
                    bg=self.colors['bg_secondary'], fg=self.colors['accent']).pack()
        
        # Categorías con scroll horizontal
        categories_section = tk.Frame(main_container, bg=self.colors['card_bg'])
        categories_section.pack(pady=30, fill=tk.X)
        
        tk.Label(categories_section, text="🎯 ELIGE UNA CATEGORÍA 🎯",
                font=self.heading_font,
                bg=self.colors['card_bg'],
                fg=self.colors['accent']).pack(pady=(0, 20))
        
        # Frame con scroll horizontal para categorías
        cat_container = tk.Frame(categories_section, bg=self.colors['card_bg'])
        cat_container.pack(fill=tk.X)
        
        # Canvas para scroll horizontal
        cat_canvas = tk.Canvas(cat_container, height=120, bg=self.colors['card_bg'],
                              highlightthickness=0)
        cat_canvas.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        cat_scrollbar = ttk.Scrollbar(cat_container, orient="horizontal",
                                     command=cat_canvas.xview)
        cat_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        cat_canvas.configure(xscrollcommand=cat_scrollbar.set)
        
        cat_inner_frame = tk.Frame(cat_canvas, bg=self.colors['card_bg'])
        cat_canvas.create_window((0, 0), window=cat_inner_frame, anchor="nw")
        
        # Emojis para categorías
        category_emojis = {
            "Saludos": "👋", "Frutas": "🍎", "Animales": "🐶",
            "Familia": "👨‍👩‍👧‍👦", "Colores": "🎨", "Números": "🔢"
        }
        
        for i, category in enumerate(self.vocabulary.keys()):
            emoji = category_emojis.get(category, "📚")
            btn = tk.Button(cat_inner_frame,
                          text=f"{emoji}\n{category}",
                          font=self.button_font,
                          bg=self.colors['button'],
                          fg='white',
                          width=15,
                          height=3,
                          padx=10,
                          pady=5,
                          cursor="hand2",
                          command=lambda cat=category: self.select_category(cat))
            btn.grid(row=0, column=i, padx=10, pady=5)
        
        cat_inner_frame.update_idletasks()
        cat_canvas.configure(scrollregion=cat_canvas.bbox("all"))
        
        # Modos de juego en grid
        modes_section = tk.Frame(main_container, bg=self.colors['card_bg'])
        modes_section.pack(pady=30, fill=tk.BOTH, expand=True)
        
        tk.Label(modes_section, text="🎮 MODOS DE JUEGO 🎮",
                font=self.heading_font,
                bg=self.colors['card_bg'],
                fg=self.colors['accent']).pack(pady=(0, 20))
        
        # Grid 2x2 para modos
        modes_frame = tk.Frame(modes_section, bg=self.colors['card_bg'])
        modes_frame.pack()
        
        modes = [
            ("📚 Flashcards", self.start_flashcards, "Aprende con tarjetas interactivas"),
            ("❓ Quiz", self.show_quiz_selection, "Pon a prueba tus conocimientos"),
            ("🔤 Traducción", self.show_translation_selection, "Practica traduciendo palabras"),
            ("🏆 Estadísticas", self.show_stats, "Ver tu progreso detallado")
        ]
        
        for i, (title, command, desc) in enumerate(modes):
            row = i // 2
            col = i % 2
            
            mode_frame = tk.Frame(modes_frame, bg=self.colors['card_bg'])
            mode_frame.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
            
            btn = tk.Button(mode_frame,
                          text=title,
                          font=self.button_font,
                          bg=self.colors['accent'],
                          fg='white',
                          width=20,
                          height=2,
                          padx=10,
                          pady=5,
                          cursor="hand2",
                          command=command)
            btn.pack(pady=(0, 10))
            
            tk.Label(mode_frame, text=desc,
                    font=self.normal_font,
                    bg=self.colors['card_bg'],
                    fg=self.colors['text'],
                    wraplength=200,
                    justify=tk.CENTER).pack()
    
    # ==============================
    # MODO QUIZ - COMPLETO
    # ==============================
    
    def show_quiz_selection(self):
        """Muestra selección de categoría para quiz"""
        self.clear_content_frame()
        self.show_back_button()
        self.current_mode = "quiz"
        
        container = tk.Frame(self.content_frame, bg=self.colors['card_bg'])
        container.pack(expand=True, fill=tk.BOTH, padx=30, pady=30)
        
        tk.Label(container, text="🎯 SELECCIONA MODO QUIZ",
                font=self.title_font,
                bg=self.colors['card_bg'],
                fg=self.colors['accent']).pack(pady=(0, 30))
        
        # Opciones de quiz
        options_frame = tk.Frame(container, bg=self.colors['card_bg'])
        options_frame.pack(expand=True)
        
        quiz_options = [
            ("📚 Por Categoría", self.show_quiz_category_selection, 
             "Elige una categoría específica para el quiz"),
            ("🔀 Aleatorio", lambda: self.start_quiz(category=None),
             "Preguntas de todas las categorías"),
            ("🏆 Desafío", lambda: self.start_quiz(category=None, num_questions=20),
             "20 preguntas difíciles")
        ]
        
        for i, (title, command, desc) in enumerate(quiz_options):
            option_frame = tk.Frame(options_frame, bg=self.colors['card_bg'])
            option_frame.pack(pady=20, padx=50, fill=tk.X)
            
            btn = tk.Button(option_frame, text=title,
                          font=self.button_font,
                          bg=self.colors['button'],
                          fg='white',
                          width=25,
                          height=2,
                          padx=10,
                          pady=5,
                          cursor="hand2",
                          command=command)
            btn.pack(pady=(0, 10))
            
            tk.Label(option_frame, text=desc,
                    font=self.normal_font,
                    bg=self.colors['card_bg'],
                    fg=self.colors['text'],
                    wraplength=300,
                    justify=tk.CENTER).pack()
    
    def show_quiz_category_selection(self):
        """Muestra selección de categoría para quiz"""
        self.clear_content_frame()
        
        container = tk.Frame(self.content_frame, bg=self.colors['card_bg'])
        container.pack(expand=True, fill=tk.BOTH, padx=30, pady=30)
        
        tk.Label(container, text="📚 ELIGE UNA CATEGORÍA PARA EL QUIZ",
                font=self.title_font,
                bg=self.colors['card_bg'],
                fg=self.colors['accent']).pack(pady=(0, 30))
        
        # Grid de categorías
        categories_frame = tk.Frame(container, bg=self.colors['card_bg'])
        categories_frame.pack(expand=True)
        
        categories = list(self.vocabulary.keys())
        for i, category in enumerate(categories):
            btn = tk.Button(categories_frame,
                          text=f"📚 {category}",
                          font=self.button_font,
                          bg=self.colors['button'],
                          fg='white',
                          width=20,
                          height=2,
                          cursor="hand2",
                          command=lambda cat=category: self.start_quiz(category=cat))
            btn.grid(row=i//2, column=i%2, padx=15, pady=10)
        
        tk.Button(container, text="🔙 Volver",
                 font=self.button_font,
                 bg=self.colors['accent'],
                 fg='white',
                 padx=30,
                 pady=10,
                 cursor="hand2",
                 command=self.show_quiz_selection).pack(pady=20)
    
    def start_quiz(self, category=None, num_questions=10):
        """Inicia el juego de quiz"""
        self.clear_content_frame()
        self.show_back_button()
        
        # Generar preguntas
        self.quiz_questions = self.quiz_generator.generate_multiple_choice(
            category=category, 
            num_questions=num_questions
        )
        
        if not self.quiz_questions:
            messagebox.showinfo("Sin palabras", "No hay suficientes palabras para el quiz.")
            self.show_quiz_selection()
            return
        
        # Inicializar estado del quiz
        self.current_question = 0
        self.total_questions = len(self.quiz_questions)
        self.correct_answers = 0
        self.selected_answer = None
        
        # Mostrar primera pregunta
        self.show_quiz_question()
    
    def show_quiz_question(self):
        """Muestra una pregunta del quiz"""
        self.clear_content_frame()
        
        if self.current_question >= len(self.quiz_questions):
            self.show_quiz_results()
            return
        
        question = self.quiz_questions[self.current_question]
        
        container = tk.Frame(self.content_frame, bg=self.colors['card_bg'])
        container.pack(expand=True, fill=tk.BOTH, padx=30, pady=30)
        
        # Información del quiz
        info_frame = tk.Frame(container, bg=self.colors['card_bg'])
        info_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(info_frame, 
                text=f"📚 {question['category']}",
                font=self.heading_font,
                bg=self.colors['card_bg'],
                fg=self.colors['accent']).pack(side=tk.LEFT)
        
        tk.Label(info_frame,
                text=f"Pregunta {self.current_question + 1} de {self.total_questions}",
                font=self.normal_font,
                bg=self.colors['card_bg'],
                fg=self.colors['text']).pack(side=tk.RIGHT)
        
        # Pregunta
        question_frame = tk.Frame(container, bg=self.colors['bg_secondary'],
                                 relief='ridge', bd=3, padx=30, pady=30)
        question_frame.pack(fill=tk.X, pady=20)
        
        tk.Label(question_frame, text="¿Cómo se dice en inglés?",
                font=self.game_font,
                bg=self.colors['bg_secondary'],
                fg=self.colors['text']).pack()
        
        tk.Label(question_frame, text=f"\"{question['spanish']}\"",
                font=('Comic Sans MS', 36, 'bold'),
                bg=self.colors['bg_secondary'],
                fg=self.colors['accent']).pack(pady=20)
        
        # Opciones de respuesta
        options_frame = tk.Frame(container, bg=self.colors['card_bg'])
        options_frame.pack(pady=30)
        
        self.option_buttons = []
        for i, option in enumerate(question['options']):
            btn = tk.Button(options_frame,
                          text=f"{chr(65+i)}) {option}",
                          font=self.button_font,
                          bg=self.colors['button'],
                          fg='white',
                          width=30,
                          height=2,
                          padx=10,
                          pady=5,
                          cursor="hand2",
                          command=lambda opt=option: self.check_quiz_answer(opt, question['correct']))
            btn.pack(pady=10)
            self.option_buttons.append(btn)
        
        # Botón para saltar pregunta
        tk.Button(container, text="⏭️ Saltar Pregunta",
                 font=self.button_font,
                 bg=self.colors['shadow'],
                 fg='white',
                 padx=20,
                 pady=10,
                 cursor="hand2",
                 command=self.next_quiz_question).pack(pady=20)
    
    def check_quiz_answer(self, selected, correct):
        """Verifica la respuesta del quiz"""
        # Deshabilitar todos los botones
        for btn in self.option_buttons:
            btn.config(state=tk.DISABLED)
        
        # Encontrar el botón seleccionado
        for btn in self.option_buttons:
            if btn.cget('text').endswith(selected):
                if selected == correct:
                    # Respuesta correcta
                    btn.config(bg=self.colors['correct'], fg='white')
                    if self.sound_manager:
                        self.sound_manager.play('correct')
                    self.correct_answers += 1
                    # Añadir puntos inmediatamente
                    self.current_score += 10
                    self.update_score()
                else:
                    # Respuesta incorrecta
                    btn.config(bg=self.colors['incorrect'], fg='white')
                    if self.sound_manager:
                        self.sound_manager.play('incorrect')
                    # Resaltar la correcta
                    for btn2 in self.option_buttons:
                        if btn2.cget('text').endswith(correct):
                            btn2.config(bg=self.colors['correct'], fg='white')
        
        # Botón para continuar
        container = self.content_frame.winfo_children()[0]
        tk.Button(container, text="➡️ Siguiente Pregunta",
                 font=self.button_font,
                 bg=self.colors['accent'],
                 fg='white',
                 padx=20,
                 pady=10,
                 cursor="hand2",
                 command=self.next_quiz_question).pack(pady=20)
    
    def next_quiz_question(self):
        """Pasa a la siguiente pregunta del quiz"""
        if self.sound_manager:
            self.sound_manager.play('click')
        
        self.current_question += 1
        self.show_quiz_question()
    
    def show_quiz_results(self):
        """Muestra resultados del quiz"""
        if self.sound_manager:
            if self.correct_answers == self.total_questions:
                self.sound_manager.play('level_up')
            elif self.correct_answers >= self.total_questions / 2:
                self.sound_manager.play('correct')
            else:
                self.sound_manager.play('incorrect')
        
        # Calcular puntaje final
        accuracy = (self.correct_answers / self.total_questions) * 100
        points_earned = self.correct_answers * 10
        self.current_score += points_earned
        self.update_score()
        
        self.clear_content_frame()
        container = tk.Frame(self.content_frame, bg=self.colors['card_bg'])
        container.pack(expand=True, fill=tk.BOTH, padx=30, pady=30)
        
        # Determinar mensaje según puntaje
        if accuracy == 100:
            emoji = "🎖️"
            title = "¡PERFECTO!"
            message = "¡Excelente trabajo! ¡Eres un genio del inglés!"
        elif accuracy >= 80:
            emoji = "🎉"
            title = "¡FELICIDADES!"
            message = "¡Muy bien! Vas por buen camino."
        elif accuracy >= 60:
            emoji = "👍"
            title = "¡BIEN HECHO!"
            message = "¡Buen trabajo! Sigue practicando."
        else:
            emoji = "💪"
            title = "¡SIGUE INTENTANDO!"
            message = "La práctica hace al maestro. ¡No te rindas!"
        
        tk.Label(container, text=f"{emoji} {title}",
                font=self.title_font,
                bg=self.colors['card_bg'],
                fg=self.colors['accent']).pack(pady=(0, 30))
        
        result_text = f"""
        📊 RESULTADOS DEL QUIZ
        
        ✅ Respuestas correctas: {self.correct_answers}/{self.total_questions}
        📈 Precisión: {accuracy:.1f}%
        ✨ Puntos ganados: +{points_earned}
        🏆 Puntuación total: {self.current_score}
        
        {message}
        """
        
        tk.Label(container, text=result_text,
                font=self.game_font,
                bg=self.colors['card_bg'],
                fg=self.colors['text'],
                justify=tk.CENTER).pack(expand=True)
        
        btn_frame = tk.Frame(container, bg=self.colors['card_bg'])
        btn_frame.pack(pady=30)
        
        tk.Button(btn_frame, text="🔄 Jugar Otra Vez",
                 font=self.button_font,
                 bg=self.colors['button'],
                 fg='white',
                 padx=20,
                 pady=10,
                 cursor="hand2",
                 command=self.show_quiz_selection).pack(side=tk.LEFT, padx=10)
        
        tk.Button(btn_frame, text="🏠 Menú Principal",
                 font=self.button_font,
                 bg=self.colors['accent'],
                 fg='white',
                 padx=20,
                 pady=10,
                 cursor="hand2",
                 command=self.show_main_menu).pack(side=tk.LEFT, padx=10)
        
        # Guardar progreso
        self.save_progress()
    
    # ==============================
    # MODO TRADUCCIÓN - COMPLETO
    # ==============================
    
    def show_translation_selection(self):
        """Muestra selección de categoría para traducción"""
        self.clear_content_frame()
        self.show_back_button()
        self.current_mode = "translation"
        
        container = tk.Frame(self.content_frame, bg=self.colors['card_bg'])
        container.pack(expand=True, fill=tk.BOTH, padx=30, pady=30)
        
        tk.Label(container, text="🔤 JUEGO DE TRADUCCIÓN",
                font=self.title_font,
                bg=self.colors['card_bg'],
                fg=self.colors['accent']).pack(pady=(0, 30))
        
        # Opciones de traducción
        options_frame = tk.Frame(container, bg=self.colors['card_bg'])
        options_frame.pack(expand=True)
        
        translation_options = [
            ("📚 Por Categoría", self.show_translation_category_selection,
             "Traduce palabras de una categoría específica"),
            ("🔀 Aleatorio", lambda: self.start_translation_game(category=None),
             "Palabras de todas las categorías"),
            ("🏆 Desafío Largo", lambda: self.start_translation_game(category=None, num_words=20),
             "20 palabras para traducir")
        ]
        
        for i, (title, command, desc) in enumerate(translation_options):
            option_frame = tk.Frame(options_frame, bg=self.colors['card_bg'])
            option_frame.pack(pady=20, padx=50, fill=tk.X)
            
            btn = tk.Button(option_frame, text=title,
                          font=self.button_font,
                          bg=self.colors['button'],
                          fg='white',
                          width=25,
                          height=2,
                          padx=10,
                          pady=5,
                          cursor="hand2",
                          command=command)
            btn.pack(pady=(0, 10))
            
            tk.Label(option_frame, text=desc,
                    font=self.normal_font,
                    bg=self.colors['card_bg'],
                    fg=self.colors['text'],
                    wraplength=300,
                    justify=tk.CENTER).pack()
    
    def show_translation_category_selection(self):
        """Muestra selección de categoría para traducción"""
        self.clear_content_frame()
        
        container = tk.Frame(self.content_frame, bg=self.colors['card_bg'])
        container.pack(expand=True, fill=tk.BOTH, padx=30, pady=30)
        
        tk.Label(container, text="📚 ELIGE UNA CATEGORÍA",
                font=self.title_font,
                bg=self.colors['card_bg'],
                fg=self.colors['accent']).pack(pady=(0, 30))
        
        # Grid de categorías
        categories_frame = tk.Frame(container, bg=self.colors['card_bg'])
        categories_frame.pack(expand=True)
        
        categories = list(self.vocabulary.keys())
        for i, category in enumerate(categories):
            btn = tk.Button(categories_frame,
                          text=f"📚 {category}",
                          font=self.button_font,
                          bg=self.colors['button'],
                          fg='white',
                          width=20,
                          height=2,
                          cursor="hand2",
                          command=lambda cat=category: self.start_translation_game(category=cat))
            btn.grid(row=i//2, column=i%2, padx=15, pady=10)
        
        tk.Button(container, text="🔙 Volver",
                 font=self.button_font,
                 bg=self.colors['accent'],
                 fg='white',
                 padx=30,
                 pady=10,
                 cursor="hand2",
                 command=self.show_translation_selection).pack(pady=20)
    
    def start_translation_game(self, category=None, num_words=10):
        """Inicia el juego de traducción"""
        self.clear_content_frame()
        self.show_back_button()
        
        # Obtener palabras
        if category:
            # Palabras de una categoría específica
            category_words = self.vocabulary.get(category, {})
            words_list = [{"spanish": esp, "english": eng, "category": category} 
                         for esp, eng in category_words.items()]
        else:
            # Todas las palabras mezcladas
            words_list = []
            for cat, words in self.vocabulary.items():
                for esp, eng in words.items():
                    words_list.append({"spanish": esp, "english": eng, "category": cat})
        
        if not words_list:
            messagebox.showinfo("Sin palabras", "No hay palabras para traducir.")
            self.show_translation_selection()
            return
        
        # Mezclar y seleccionar palabras
        random.shuffle(words_list)
        self.translation_words = words_list[:num_words]
        self.current_translation_index = 0
        self.translation_score = 0
        
        # Mostrar primera palabra
        self.show_translation_word()
    
    def show_translation_word(self):
        """Muestra una palabra para traducir"""
        self.clear_content_frame()
        
        if self.current_translation_index >= len(self.translation_words):
            self.show_translation_results()
            return
        
        word_data = self.translation_words[self.current_translation_index]
        
        container = tk.Frame(self.content_frame, bg=self.colors['card_bg'])
        container.pack(expand=True, fill=tk.BOTH, padx=30, pady=30)
        
        # Información
        info_frame = tk.Frame(container, bg=self.colors['card_bg'])
        info_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(info_frame, 
                text=f"📚 {word_data['category']}",
                font=self.heading_font,
                bg=self.colors['card_bg'],
                fg=self.colors['accent']).pack(side=tk.LEFT)
        
        tk.Label(info_frame,
                text=f"Palabra {self.current_translation_index + 1} de {len(self.translation_words)}",
                font=self.normal_font,
                bg=self.colors['card_bg'],
                fg=self.colors['text']).pack(side=tk.RIGHT)
        
        # Palabra a traducir
        word_frame = tk.Frame(container, bg=self.colors['bg_secondary'],
                             relief='ridge', bd=3, padx=30, pady=30)
        word_frame.pack(fill=tk.X, pady=20)
        
        tk.Label(word_frame, text="Traduce al inglés:",
                font=self.game_font,
                bg=self.colors['bg_secondary'],
                fg=self.colors['text']).pack()
        
        tk.Label(word_frame, text=f"\"{word_data['spanish']}\"",
                font=('Comic Sans MS', 36, 'bold'),
                bg=self.colors['bg_secondary'],
                fg=self.colors['accent']).pack(pady=20)
        
        # Entrada de traducción
        input_frame = tk.Frame(container, bg=self.colors['card_bg'])
        input_frame.pack(pady=30)
        
        tk.Label(input_frame, text="Tu respuesta:",
                font=self.game_font,
                bg=self.colors['card_bg'],
                fg=self.colors['text']).pack(pady=(0, 10))
        
        self.translation_entry = tk.Entry(input_frame,
                                        font=('Comic Sans MS', 18),
                                        width=30,
                                        bd=2,
                                        relief='ridge',
                                        justify='center')
        self.translation_entry.pack(pady=10)
        self.translation_entry.focus()
        
        # Bind Enter key para enviar respuesta
        self.translation_entry.bind('<Return>', 
                                  lambda e: self.check_translation(word_data['english']))
        
        # Botones
        btn_frame = tk.Frame(container, bg=self.colors['card_bg'])
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="✅ Verificar",
                 font=self.button_font,
                 bg=self.colors['button'],
                 fg='white',
                 padx=20,
                 pady=10,
                 cursor="hand2",
                 command=lambda: self.check_translation(word_data['english'])).pack(side=tk.LEFT, padx=10)
        
        tk.Button(btn_frame, text="⏭️ Saltar",
                 font=self.button_font,
                 bg=self.colors['shadow'],
                 fg='white',
                 padx=20,
                 pady=10,
                 cursor="hand2",
                 command=self.next_translation_word).pack(side=tk.LEFT, padx=10)
        
        tk.Button(btn_frame, text="💡 Pista",
                 font=self.button_font,
                 bg=self.colors['highlight'],
                 fg=self.colors['text'],
                 padx=20,
                 pady=10,
                 cursor="hand2",
                 command=lambda: self.show_hint(word_data['english'])).pack(side=tk.LEFT, padx=10)
    
    def check_translation(self, correct_answer):
        """Verifica la traducción del usuario"""
        user_answer = self.translation_entry.get().strip().lower()
        correct_answer_lower = correct_answer.lower()
        
        # Verificar respuesta
        is_correct = (user_answer == correct_answer_lower)
        
        # Mostrar feedback
        feedback_frame = tk.Frame(self.content_frame.winfo_children()[0], 
                                 bg=self.colors['card_bg'])
        feedback_frame.pack(pady=20)
        
        if is_correct:
            tk.Label(feedback_frame, text="✅ ¡CORRECTO!",
                    font=self.heading_font,
                    bg=self.colors['card_bg'],
                    fg=self.colors['correct']).pack()
            self.translation_score += 1
            if self.sound_manager:
                self.sound_manager.play('correct')
        else:
            tk.Label(feedback_frame, text="❌ ¡INCORRECTO!",
                    font=self.heading_font,
                    bg=self.colors['card_bg'],
                    fg=self.colors['incorrect']).pack()
            tk.Label(feedback_frame, text=f"La respuesta correcta es: \"{correct_answer}\"",
                    font=self.game_font,
                    bg=self.colors['card_bg'],
                    fg=self.colors['text']).pack(pady=10)
            if self.sound_manager:
                self.sound_manager.play('incorrect')
        
        # Deshabilitar entrada
        self.translation_entry.config(state=tk.DISABLED)
        
        # Botón para continuar
        tk.Button(feedback_frame, text="➡️ Siguiente Palabra",
                 font=self.button_font,
                 bg=self.colors['accent'],
                 fg='white',
                 padx=20,
                 pady=10,
                 cursor="hand2",
                 command=self.next_translation_word).pack(pady=20)
    
    def show_hint(self, correct_answer):
        """Muestra una pista para la palabra"""
        hint = ""
        for i, char in enumerate(correct_answer):
            if i == 0:
                hint += char.upper()
            elif i < len(correct_answer) - 1 and random.random() > 0.5:
                hint += char
            else:
                hint += "_"
        
        messagebox.showinfo("💡 Pista", 
                          f"Pista: {hint}\n\nLa palabra tiene {len(correct_answer)} letras.")
    
    def next_translation_word(self):
        """Pasa a la siguiente palabra"""
        if self.sound_manager:
            self.sound_manager.play('click')
        
        self.current_translation_index += 1
        self.show_translation_word()
    
    def show_translation_results(self):
        """Muestra resultados del juego de traducción"""
        # Calcular puntaje final
        accuracy = (self.translation_score / len(self.translation_words)) * 100
        points_earned = self.translation_score * 15  # Más puntos por traducción
        self.current_score += points_earned
        self.update_score()
        
        if self.sound_manager:
            if accuracy == 100:
                self.sound_manager.play('level_up')
            elif accuracy >= 70:
                self.sound_manager.play('correct')
        
        self.clear_content_frame()
        container = tk.Frame(self.content_frame, bg=self.colors['card_bg'])
        container.pack(expand=True, fill=tk.BOTH, padx=30, pady=30)
        
        # Determinar mensaje según puntaje
        if accuracy == 100:
            emoji = "🏆"
            title = "¡TRADUCTOR EXPERTO!"
            message = "¡Perfecto! Traduces como un nativo."
        elif accuracy >= 80:
            emoji = "🎯"
            title = "¡EXCELENTE!"
            message = "¡Muy buen trabajo! Casi perfecto."
        elif accuracy >= 60:
            emoji = "✨"
            title = "¡BIEN HECHO!"
            message = "¡Buen progreso! Sigue practicando."
        else:
            emoji = "📚"
            title = "¡A SEGUIR ESTUDIANDO!"
            message = "Cada error es una oportunidad para aprender."
        
        tk.Label(container, text=f"{emoji} {title}",
                font=self.title_font,
                bg=self.colors['card_bg'],
                fg=self.colors['accent']).pack(pady=(0, 30))
        
        result_text = f"""
        🔤 RESULTADOS DE TRADUCCIÓN
        
        ✅ Traducciones correctas: {self.translation_score}/{len(self.translation_words)}
        📈 Precisión: {accuracy:.1f}%
        ✨ Puntos ganados: +{points_earned}
        🏆 Puntuación total: {self.current_score}
        
        {message}
        
        💡 Consejo: Intenta usar las palabras nuevas en oraciones.
        """
        
        tk.Label(container, text=result_text,
                font=self.game_font,
                bg=self.colors['card_bg'],
                fg=self.colors['text'],
                justify=tk.CENTER).pack(expand=True)
        
        btn_frame = tk.Frame(container, bg=self.colors['card_bg'])
        btn_frame.pack(pady=30)
        
        tk.Button(btn_frame, text="🔄 Jugar Otra Vez",
                 font=self.button_font,
                 bg=self.colors['button'],
                 fg='white',
                 padx=20,
                 pady=10,
                 cursor="hand2",
                 command=self.show_translation_selection).pack(side=tk.LEFT, padx=10)
        
        tk.Button(btn_frame, text="🏠 Menú Principal",
                 font=self.button_font,
                 bg=self.colors['accent'],
                 fg='white',
                 padx=20,
                 pady=10,
                 cursor="hand2",
                 command=self.show_main_menu).pack(side=tk.LEFT, padx=10)
        
        # Guardar progreso
        self.save_progress()
    
    # ==============================
    # FUNCIONES COMUNES (sin cambios)
    # ==============================
    
    def show_stats(self):
        """Muestra estadísticas detalladas"""
        self.clear_content_frame()
        self.show_back_button()
        
        container = tk.Frame(self.content_frame, bg=self.colors['card_bg'])
        container.pack(expand=True, fill=tk.BOTH, padx=30, pady=30)
        
        tk.Label(container, text="📊 TUS ESTADÍSTICAS",
                font=self.title_font,
                bg=self.colors['card_bg'],
                fg=self.colors['accent']).pack(pady=(0, 30))
        
        stats_text = f"""
        👤 Jugador: {self.player_name}
        
        🏆 Puntuación total: {self.current_score}
        ⭐ Nivel actual: {self.current_level}
        
        📚 Palabras aprendidas: {self.current_score // 10}
        🎮 Partidas jugadas: {self.current_level - 1}
        
        ¡Sigue así! Cada palabra que aprendes te acerca más a ser un experto.
        """
        
        tk.Label(container, text=stats_text,
                font=self.game_font,
                bg=self.colors['card_bg'],
                fg=self.colors['text'],
                justify=tk.LEFT).pack(expand=True)
        
        tk.Button(container, text="⬅️ Volver",
                 font=self.button_font,
                 bg=self.colors['button'],
                 fg='white',
                 padx=30,
                 pady=10,
                 cursor="hand2",
                 command=self.show_main_menu).pack(pady=30)
    
    def start_flashcards(self):
        """Inicia flashcards"""
        self.clear_content_frame()
        self.current_mode = "flashcards"
        self.show_back_button()
        
        if hasattr(self, 'sound_manager') and self.sound_manager:
            self.sound_manager.play('click')
        
        # Si no hay categoría, mostrar selección
        if not self.current_category:
            self.show_category_selection()
            return
        
        self.start_flashcards_game()
    
    def show_category_selection(self):
        """Muestra selección de categoría para flashcards"""
        container = tk.Frame(self.content_frame, bg=self.colors['card_bg'])
        container.pack(expand=True, fill=tk.BOTH, padx=30, pady=30)
        
        tk.Label(container, text="📚 ELIGE UNA CATEGORÍA PARA FLASHCARDS",
                font=self.title_font,
                bg=self.colors['card_bg'],
                fg=self.colors['accent']).pack(pady=(0, 30))
        
        # Grid de categorías
        categories_frame = tk.Frame(container, bg=self.colors['card_bg'])
        categories_frame.pack(expand=True)
        
        categories = list(self.vocabulary.keys())
        for i, category in enumerate(categories):
            btn = tk.Button(categories_frame,
                          text=f"📚 {category}",
                          font=self.button_font,
                          bg=self.colors['button'],
                          fg='white',
                          width=20,
                          height=2,
                          cursor="hand2",
                          command=lambda cat=category: self.select_category_for_flashcards(cat))
            btn.grid(row=i//2, column=i%2, padx=15, pady=10)
        
        tk.Button(container, text="🔀 Categoría Aleatoria",
                 font=self.button_font,
                 bg=self.colors['accent'],
                 fg='white',
                 padx=30,
                 pady=10,
                 cursor="hand2",
                 command=lambda: self.select_category_for_flashcards(random.choice(categories))
                 ).pack(pady=20)
    
    def select_category_for_flashcards(self, category):
        """Selecciona categoría y comienza flashcards"""
        self.current_category = category
        self.start_flashcards_game()
    
    def start_flashcards_game(self):
        """Inicia el juego de flashcards"""
        words = list(self.vocabulary[self.current_category].items())
        random.shuffle(words)
        
        if not words:
            messagebox.showinfo("Sin palabras", "No hay palabras en esta categoría.")
            self.show_main_menu()
            return
        
        self.flashcards_words = words
        self.current_flashcard = 0
        self.show_flashcard()
    
    def show_flashcard(self):
        """Muestra una flashcard"""
        self.clear_content_frame()
        
        if self.current_flashcard >= len(self.flashcards_words):
            self.show_flashcards_results()
            return
        
        spanish, english = self.flashcards_words[self.current_flashcard]
        
        container = tk.Frame(self.content_frame, bg=self.colors['card_bg'])
        container.pack(expand=True, fill=tk.BOTH, padx=30, pady=30)
        
        # Información
        info_frame = tk.Frame(container, bg=self.colors['card_bg'])
        info_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(info_frame, 
                text=f"📚 {self.current_category}",
                font=self.heading_font,
                bg=self.colors['card_bg'],
                fg=self.colors['accent']).pack(side=tk.LEFT)
        
        tk.Label(info_frame,
                text=f"Tarjeta {self.current_flashcard + 1} de {len(self.flashcards_words)}",
                font=self.normal_font,
                bg=self.colors['card_bg'],
                fg=self.colors['text']).pack(side=tk.RIGHT)
        
        # Flashcard
        flashcard = tk.Frame(container, bg=self.colors['bg_secondary'],
                            relief='ridge', bd=3)
        flashcard.pack(expand=True, fill=tk.BOTH, padx=50, pady=20)
        
        # Palabra en español
        tk.Label(flashcard, text=spanish,
                font=('Comic Sans MS', 48, 'bold'),
                bg=self.colors['bg_secondary'],
                fg=self.colors['accent']).pack(expand=True)
        
        # Separador
        tk.Frame(flashcard, height=2, bg=self.colors['accent']).pack(fill=tk.X, padx=50, pady=20)
        
        # Palabra en inglés (inicialmente oculta)
        self.english_label = tk.Label(flashcard, text="???",
                                     font=('Comic Sans MS', 48),
                                     bg=self.colors['bg_secondary'],
                                     fg=self.colors['shadow'])
        self.english_label.pack(expand=True)
        
        # Botones
        btn_frame = tk.Frame(container, bg=self.colors['card_bg'])
        btn_frame.pack(pady=30)
        
        tk.Button(btn_frame, text="👁️ Mostrar Respuesta",
                 font=self.button_font,
                 bg=self.colors['button'],
                 fg='white',
                 padx=20,
                 pady=10,
                 cursor="hand2",
                 command=lambda: self.reveal_translation(english)).pack(side=tk.LEFT, padx=10)
        
        tk.Button(btn_frame, text="➡️ Siguiente",
                 font=self.button_font,
                 bg=self.colors['accent'],
                 fg='white',
                 padx=20,
                 pady=10,
                 cursor="hand2",
                 command=self.next_flashcard).pack(side=tk.LEFT, padx=10)
        
        tk.Button(btn_frame, text="🏁 Terminar",
                 font=self.button_font,
                 bg=self.colors['incorrect'],
                 fg='white',
                 padx=20,
                 pady=10,
                 cursor="hand2",
                 command=self.show_flashcards_results).pack(side=tk.LEFT, padx=10)
    
    def reveal_translation(self, english):
        """Revela la traducción"""
        if hasattr(self, 'sound_manager') and self.sound_manager:
            self.sound_manager.play('correct')
        
        self.english_label.config(text=english, fg=self.colors['correct'])
    
    def next_flashcard(self):
        """Siguiente flashcard"""
        if hasattr(self, 'sound_manager') and self.sound_manager:
            self.sound_manager.play('click')
        
        self.current_flashcard += 1
        self.show_flashcard()
    
    def show_flashcards_results(self):
        """Muestra resultados de flashcards"""
        if hasattr(self, 'sound_manager') and self.sound_manager:
            self.sound_manager.play('level_up')
        
        words_reviewed = min(self.current_flashcard, len(self.flashcards_words))
        points_earned = words_reviewed * 5
        self.current_score += points_earned
        self.update_score()
        
        self.clear_content_frame()
        container = tk.Frame(self.content_frame, bg=self.colors['card_bg'])
        container.pack(expand=True, fill=tk.BOTH, padx=30, pady=30)
        
        tk.Label(container, text="🎉 ¡FELICIDADES! 🎉",
                font=self.title_font,
                bg=self.colors['card_bg'],
                fg=self.colors['accent']).pack(pady=(0, 30))
        
        result_text = f"""
        📊 RESULTADOS
        
        📚 Categoría: {self.current_category}
        🔢 Palabras revisadas: {words_reviewed}
        ✨ Puntos ganados: +{points_earned}
        🏆 Puntuación total: {self.current_score}
        
        ¡Excelente trabajo! Sigue practicando.
        """
        
        tk.Label(container, text=result_text,
                font=self.game_font,
                bg=self.colors['card_bg'],
                fg=self.colors['text'],
                justify=tk.CENTER).pack(expand=True)
        
        btn_frame = tk.Frame(container, bg=self.colors['card_bg'])
        btn_frame.pack(pady=30)
        
        tk.Button(btn_frame, text="🔄 Repetir",
                 font=self.button_font,
                 bg=self.colors['button'],
                 fg='white',
                 padx=20,
                 pady=10,
                 cursor="hand2",
                 command=self.start_flashcards_game).pack(side=tk.LEFT, padx=10)
        
        tk.Button(btn_frame, text="🏠 Menú Principal",
                 font=self.button_font,
                 bg=self.colors['accent'],
                 fg='white',
                 padx=20,
                 pady=10,
                 cursor="hand2",
                 command=self.show_main_menu).pack(side=tk.LEFT, padx=10)
        
        # Guardar progreso
        self.save_progress()
    
    def select_category(self, category):
        """Selecciona una categoría para ver detalles"""
        self.current_category = category
        self.show_category_details()
    
    def show_category_details(self):
        """Muestra detalles de una categoría"""
        self.clear_content_frame()
        self.show_back_button()
        
        container = tk.Frame(self.content_frame, bg=self.colors['card_bg'])
        container.pack(expand=True, fill=tk.BOTH, padx=30, pady=30)
        
        # Título
        tk.Label(container, text=f"📚 {self.current_category.upper()}",
                font=self.title_font,
                bg=self.colors['card_bg'],
                fg=self.colors['accent']).pack(pady=(0, 20))
        
        # Información
        word_count = len(self.vocabulary[self.current_category])
        tk.Label(container, text=f"✨ {word_count} palabras para aprender ✨",
                font=self.heading_font,
                bg=self.colors['card_bg'],
                fg=self.colors['text']).pack(pady=(0, 30))
        
        # Lista de palabras
        words_frame = tk.Frame(container, bg=self.colors['card_bg'])
        words_frame.pack(expand=True, fill=tk.BOTH)
        
        # Canvas para scroll
        words_canvas = tk.Canvas(words_frame, bg=self.colors['card_bg'],
                                highlightthickness=0)
        words_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        words_scrollbar = ttk.Scrollbar(words_frame, orient="vertical",
                                       command=words_canvas.yview)
        words_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        words_canvas.configure(yscrollcommand=words_scrollbar.set)
        
        words_inner = tk.Frame(words_canvas, bg=self.colors['card_bg'])
        words_canvas.create_window((0, 0), window=words_inner, anchor="nw")
        
        # Mostrar palabras
        for spanish, english in self.vocabulary[self.current_category].items():
            word_card = tk.Frame(words_inner, bg=self.colors['bg_secondary'],
                                relief='ridge', bd=1)
            word_card.pack(fill=tk.X, pady=5, padx=10)
            
            tk.Label(word_card, text=f"🇪🇸 {spanish}",
                    font=self.game_font,
                    bg=self.colors['bg_secondary'],
                    fg=self.colors['accent']).pack(side=tk.LEFT, padx=20, pady=10)
            
            tk.Label(word_card, text="➡️",
                    font=self.game_font,
                    bg=self.colors['bg_secondary'],
                    fg=self.colors['text']).pack(side=tk.LEFT, padx=10)
            
            tk.Label(word_card, text=f"🇬🇧 {english}",
                    font=self.game_font,
                    bg=self.colors['bg_secondary'],
                    fg=self.colors['text']).pack(side=tk.LEFT, padx=20, pady=10)
        
        words_inner.update_idletasks()
        words_canvas.configure(scrollregion=words_canvas.bbox("all"))
        
        # Botones
        btn_frame = tk.Frame(container, bg=self.colors['card_bg'])
        btn_frame.pack(pady=30)
        
        tk.Button(btn_frame, text="🎴 Jugar Flashcards",
                 font=self.button_font,
                 bg=self.colors['accent'],
                 fg='white',
                 padx=20,
                 pady=10,
                 cursor="hand2",
                 command=self.start_flashcards).pack(side=tk.LEFT, padx=10)
        
        tk.Button(btn_frame, text="❓ Jugar Quiz",
                 font=self.button_font,
                 bg=self.colors['button'],
                 fg='white',
                 padx=20,
                 pady=10,
                 cursor="hand2",
                 command=lambda: self.start_quiz(category=self.current_category)).pack(side=tk.LEFT, padx=10)
        
        tk.Button(btn_frame, text="🔤 Jugar Traducción",
                 font=self.button_font,
                 bg=self.colors['highlight'],
                 fg=self.colors['text'],
                 padx=20,
                 pady=10,
                 cursor="hand2",
                 command=lambda: self.start_translation_game(category=self.current_category)).pack(side=tk.LEFT, padx=10)
        
        tk.Button(btn_frame, text="⬅️ Volver",
                 font=self.button_font,
                 bg=self.colors['shadow'],
                 fg='white',
                 padx=20,
                 pady=10,
                 cursor="hand2",
                 command=self.show_main_menu).pack(side=tk.LEFT, padx=10)
    
    def clear_content_frame(self):
        """Limpia el frame de contenido"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_back_button(self):
        """Muestra botón de volver"""
        if hasattr(self, 'back_button'):
            self.back_button.pack(side=tk.RIGHT)
    
    def hide_back_button(self):
        """Oculta botón de volver"""
        if hasattr(self, 'back_button'):
            self.back_button.pack_forget()
    
    def update_score(self):
        """Actualiza display de puntaje"""
        if hasattr(self, 'score_label'):
            self.score_label.config(text=f"🏆 {self.current_score} Puntos")
        
        # Subir nivel cada 100 puntos
        new_level = (self.current_score // 100) + 1
        if new_level > self.current_level:
            self.current_level = new_level
            if hasattr(self, 'sound_manager') and self.sound_manager:
                self.sound_manager.play('level_up')
        
        if hasattr(self, 'level_label'):
            self.level_label.config(text=f"⭐ Nivel {self.current_level}")
    
    def save_progress(self):
        """Guarda progreso"""
        try:
            self.game.score = self.current_score
            self.game.level = self.current_level
            self.game.save_progress()
        except Exception as e:
            print(f"Error guardando progreso: {e}")
    
    def run(self):
        """Inicia la aplicación"""
        self.root.mainloop()