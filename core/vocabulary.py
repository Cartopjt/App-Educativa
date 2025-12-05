# Diccionario completo de vocabulario español-inglés
vocabulary_data = {
    "Saludos": {
        "hola": "hello",
        "adiós": "goodbye",
        "buenos días": "good morning",
        "buenas tardes": "good afternoon",
        "buenas noches": "good night",
        "por favor": "please",
        "gracias": "thank you",
        "de nada": "you're welcome",
        "lo siento": "I'm sorry",
        "¿cómo estás?": "how are you?",
        "bien": "good",
        "mal": "bad",
        "regular": "okay",
        "¿y tú?": "and you?",
        "mucho gusto": "nice to meet you"
    },
    "Frutas": {
        "manzana": "apple",
        "plátano": "banana",
        "naranja": "orange",
        "uva": "grape",
        "fresa": "strawberry",
        "sandía": "watermelon",
        "piña": "pineapple",
        "mango": "mango",
        "pera": "pear",
        "melón": "melon",
        "cereza": "cherry",
        "limón": "lemon",
        "kiwi": "kiwi",
        "papaya": "papaya",
        "coco": "coconut"
    },
    "Animales": {
        "perro": "dog",
        "gato": "cat",
        "pájaro": "bird",
        "pez": "fish",
        "caballo": "horse",
        "vaca": "cow",
        "elefante": "elephant",
        "león": "lion",
        "tigre": "tiger",
        "oso": "bear",
        "mono": "monkey",
        "serpiente": "snake",
        "conejo": "rabbit",
        "ratón": "mouse",
        "tortuga": "turtle"
    },
    "Familia": {
        "madre": "mother",
        "padre": "father",
        "hermano": "brother",
        "hermana": "sister",
        "abuelo": "grandfather",
        "abuela": "grandmother",
        "tío": "uncle",
        "tía": "aunt",
        "primo": "cousin",
        "prima": "cousin",
        "hijo": "son",
        "hija": "daughter",
        "esposo": "husband",
        "esposa": "wife",
        "sobrino": "nephew",
        "sobrina": "niece"
    },
    "Colores": {
        "rojo": "red",
        "azul": "blue",
        "verde": "green",
        "amarillo": "yellow",
        "naranja": "orange",
        "morado": "purple",
        "rosa": "pink",
        "blanco": "white",
        "negro": "black",
        "gris": "gray",
        "marrón": "brown",
        "celeste": "light blue",
        "dorado": "gold",
        "plateado": "silver"
    },
    "Números": {
        "uno": "one",
        "dos": "two",
        "tres": "three",
        "cuatro": "four",
        "cinco": "five",
        "seis": "six",
        "siete": "seven",
        "ocho": "eight",
        "nueve": "nine",
        "diez": "ten",
        "once": "eleven",
        "doce": "twelve",
        "trece": "thirteen",
        "catorce": "fourteen",
        "quince": "fifteen",
        "veinte": "twenty",
        "cincuenta": "fifty",
        "cien": "one hundred"
    }
}

def get_categories():
    """Devuelve la lista de categorías disponibles"""
    return list(vocabulary_data.keys())

def get_words_by_category(category):
    """Devuelve las palabras de una categoría específica"""
    return vocabulary_data.get(category, {})

def get_random_word(category=None):
    """Devuelve una palabra aleatoria, opcionalmente de una categoría específica"""
    import random
    
    if category:
        words = vocabulary_data.get(category, {})
    else:
        # Juntar todas las palabras de todas las categorías
        words = {}
        for cat_words in vocabulary_data.values():
            words.update(cat_words)
    
    if not words:
        return None, None
    
    spanish_word = random.choice(list(words.keys()))
    english_word = words[spanish_word]
    
    return spanish_word, english_word

def get_word_count():
    """Devuelve el número total de palabras en el vocabulario"""
    total = 0
    for category in vocabulary_data.values():
        total += len(category)
    return total
