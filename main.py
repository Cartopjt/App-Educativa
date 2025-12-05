import sys
import os

def setup_paths():
    if getattr(sys, 'frozen', False):
        base_dir = sys._MEIPASS
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Añadir rutas
    sys.path.insert(0, base_dir)
    
    # Verificar carpetas existentes
    for folder in ['core', 'utils', 'ui']:
        folder_path = os.path.join(base_dir, folder)
        if os.path.exists(folder_path):
            sys.path.insert(0, folder_path)
    
    return base_dir

def main():
    """Función principal"""
    try:
        base_dir = setup_paths()
        print("🌟 Iniciando Aventura de Inglés...")
        
        from core.game import Game
        from ui.app import EnglishApp  
        
        game = Game()
        app = EnglishApp(game)
        
        app.run()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        
        if not getattr(sys, 'frozen', False):
            input("\nPresiona Enter para salir...")
        sys.exit(1)

if __name__ == "__main__":
    main()
