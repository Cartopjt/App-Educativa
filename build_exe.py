import PyInstaller.__main__
import os
import shutil
import sys

def clean_build_folders():
    """Limpia carpetas de builds anteriores"""
    folders = ['build', 'dist']
    for folder in folders:
        if os.path.exists(folder):
            print(f"🧹 Limpiando carpeta: {folder}")
            shutil.rmtree(folder)

def build_executable():
    """Construye el ejecutable con PyInstaller"""
    
    # Configuración para PyInstaller
    args = [
        'main.py',  # Archivo principal
        '--name=EnglishAdventure',  # Nombre del ejecutable
        '--onefile',  # Un solo archivo .exe
        '--windowed',  # Sin consola (ocultar terminal)
        '--clean',  # Limpiar builds anteriores
        '--noconfirm',  # No preguntar confirmación
        
        # Icono de la aplicación
        '--icon=assets/icon/icon.ico',
        
        # Incluir recursos
        '--add-data=assets;assets',
        '--add-data=core;core',
        '--add-data=ui;ui',
        '--add-data=utils;utils',
        
        # Excluir módulos innecesarios (reduce tamaño)
        '--exclude-module=matplotlib',
        '--exclude-module=scipy',
        '--exclude-module=numpy',
        
        # Optimizaciones
        '--optimize=2',
    ]
    
    # Para Windows específicamente
    if sys.platform == 'win32':
        args.extend([
            '--uac-admin',  # No pedir admin por defecto
        ])
    
    print("🚀 Construyendo ejecutable...")
    print(f"📋 Argumentos: {' '.join(args)}")
    
    try:
        PyInstaller.__main__.run(args)
        print("✅ ¡Ejecutable creado exitosamente!")
        print("📁 El archivo se encuentra en: dist/EnglishAdventure.exe")
        
        # Copiar recursos adicionales si es necesario
        if os.path.exists('data'):
            print("📋 Copiando datos de usuario...")
            if not os.path.exists('dist/data'):
                shutil.copytree('data', 'dist/data')
        
    except Exception as e:
        print(f"❌ Error al crear el ejecutable: {e}")
        return False
    
    return True

def create_portable_version():
    print("🎒 Creando versión portable...")
    
    portable_dir = "EnglishAdventure_Portable"
    
    if os.path.exists(portable_dir):
        shutil.rmtree(portable_dir)
    
    # Crear estructura
    os.makedirs(portable_dir)
    
    # Copiar ejecutable
    if os.path.exists("dist/EnglishAdventure.exe"):
        shutil.copy2("dist/EnglishAdventure.exe", 
                    os.path.join(portable_dir, "EnglishAdventure.exe"))
    
    # Copiar assets si existen
    if os.path.exists("assets"):
        shutil.copytree("assets", os.path.join(portable_dir, "assets"))
    
    # Crear README portable
    readme_text = """# Aventura de Inglés - Versión Portable

¡Hola! Esta es la versión portable de Aventura de Inglés.

## 📋 Cómo usar:
1. Ejecuta "EnglishAdventure.exe"
2. ¡Aprende inglés divirtiéndote!

## 📁 Tus datos se guardarán en:
- Windows: AppData/Roaming/EnglishAdventure/
- Linux/Mac: ~/.englishadventure/

## 🚫 Sin instalación necesaria
Puedes copiar esta carpeta a cualquier lugar.

¡Disfruta aprendiendo!
"""
    
    with open(os.path.join(portable_dir, "README.txt"), "w", encoding="utf-8") as f:
        f.write(readme_text)
    
    print(f"✅ Versión portable creada en: {portable_dir}/")

def main():
    """Función principal del script de build"""
    print("=" * 50)
    print("🔧 CONSTRUCTOR DE EJECUTABLE - AVENTURA DE INGLÉS")
    print("=" * 50)
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists("main.py"):
        print("❌ Error: Debes ejecutar este script desde el directorio raíz del proyecto")
        print("   Directorio actual:", os.getcwd())
        return
    
    # Limpiar builds anteriores
    clean_build_folders()
    
    # Construir ejecutable
    if build_executable():
        # Crear versión portable opcional
        create = input("\n¿Crear versión portable también? (s/n): ").lower()
        if create == 's':
            create_portable_version()
        
        print("\n" + "=" * 50)
        print("🎉 ¡PROCESO COMPLETADO!")
        print("=" * 50)
        print("\n📋 Resumen:")
        print("  • Ejecutable: dist/EnglishAdventure.exe")
        print("  • Tamaño aproximado: 20-30 MB")
        print("  • Requisitos: Windows 7/8/10/11 (64-bit)")
        print("\n⚠️  Nota: El primer inicio puede ser lento")
        print("   debido a la extracción de archivos.")
        
    else:
        print("❌ Fallo en la construcción del ejecutable")

if __name__ == "__main__":
    main()