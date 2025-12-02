import sys
import os
from tkinter import Tk, messagebox

# Intentar importar los módulos necesarios
try:
    from game_ui import EnglishGame
    import vocabulary
    from data_manager import DataManager
    
    def main():
        """Función principal que inicia la aplicación"""
        try:
            # Crear ventana principal
            root = Tk()
            
            # Configurar ventana
            root.title("English Learning Game")
            root.geometry("900x700")
            root.configure(bg='#2C3E50')
            
            # Intentar cargar el icono si existe
            try:
                if os.path.exists("icon.ico"):
                    root.iconbitmap("icon.ico")
            except:
                pass
            
            # Inicializar gestor de datos
            data_manager = DataManager()
            
            # Crear e iniciar la aplicación
            app = EnglishGame(root, data_manager)
            
            # Iniciar bucle principal
            root.mainloop()
            
        except Exception as e:
            # Mostrar mensaje de error en caso de fallo
            error_msg = f"Error al iniciar la aplicación:\n{str(e)}"
            print(error_msg)
            messagebox.showerror("Error", error_msg)
    
    if __name__ == "__main__":
        main()
        
except ImportError as e:
    print(f"Error de importación: {e}")
    print("Asegúrate de que todos los archivos del proyecto están en la misma carpeta.")
    input("Presiona Enter para salir...")