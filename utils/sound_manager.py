# utils/sound_manager.py - GESTOR DE SONIDOS
import pygame
import os
from .paths import PathManager

class SoundManager:
    """Gestiona los efectos de sonido de la aplicación"""
    
    def __init__(self, enabled=True):
        self.enabled = enabled
        self.sounds = {}
        
        if enabled:
            try:
                pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
                self.load_default_sounds()
            except Exception as e:
                print(f"⚠️ No se pudieron inicializar los sonidos: {e}")
                self.enabled = False
    
    def load_default_sounds(self):
        """Carga sonidos por defecto o crea fallbacks"""
        sound_files = {
            'click': 'click.mp3',
            'correct': 'correct.mp3',
            'incorrect': 'error.mp3',
            'level_up': 'level_up.mp3'
        }
        
        for name, filename in sound_files.items():
            sound_path = PathManager.get_resource_path(f"assets/sounds/{filename}")
            
            if os.path.exists(sound_path):
                try:
                    self.sounds[name] = pygame.mixer.Sound(sound_path)
                except Exception:
                    print(f"⚠️ No se pudo cargar el sonido: {filename}")
                    self.create_fallback_sound(name)
            else:
                print(f"📁 Sonido no encontrado: {filename}")
                self.create_fallback_sound(name)
    
    def create_fallback_sound(self, name):
        """Crea un sonido simple como fallback"""
        try:
            # Crear un sonido simple con pygame
            import numpy as np
            
            if name == 'correct':
                frequency = 800
                duration = 300
            elif name == 'incorrect':
                frequency = 400
                duration = 400
            elif name == 'level_up':
                frequency = 1000
                duration = 500
            else:  # click
                frequency = 600
                duration = 100
            
            # Crear onda senoidal simple
            sample_rate = 22050
            frames = int(duration * sample_rate / 1000)
            arr = np.array([4096 * np.sin(2 * np.pi * frequency * x / sample_rate) 
                           for x in range(frames)]).astype(np.int16)
            arr = np.repeat(arr.reshape(frames, 1), 2, axis=1)
            
            sound = pygame.sndarray.make_sound(arr)
            self.sounds[name] = sound
            
        except Exception:
            self.sounds[name] = None
    
    def play(self, sound_name, volume=0.7):
        """Reproduce un efecto de sonido"""
        if not self.enabled or sound_name not in self.sounds:
            return
        
        try:
            sound = self.sounds[sound_name]
            if sound:
                sound.set_volume(volume)
                sound.play()
        except Exception:
            pass  # Silenciar errores de sonido
    
    def stop_all(self):
        """Detiene todos los sonidos"""
        if self.enabled:
            pygame.mixer.stop()