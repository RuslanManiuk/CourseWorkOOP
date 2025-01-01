import pygame

class MusicManager:
    def __init__(self):
        # Ініціалізуємо mixer, якщо він ще не ініціалізований
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        self.is_playing = False
        self.current_track = None

    def load_track(self, track_name):
        """Завантажує трек, якщо він ще не завантажений"""
        try:
            if self.current_track != track_name:
                print(f"Завантаження треку: {track_name}")
                pygame.mixer.music.load(track_name)
                self.current_track = track_name
                return True
            return True
        except Exception as e:
            print(f"Помилка завантаження треку: {e}")
            return False

    def play_music(self):
        """Починає відтворення музики"""
        try:
            print("Спроба відтворення музики")
            pygame.mixer.music.play(-1)
            self.is_playing = True
            print("Музика почала грати")
        except Exception as e:
            print(f"Помилка відтворення музики: {e}")

    def pause_music(self):
        """Ставить музику на паузу"""
        try:
            pygame.mixer.music.pause()
            self.is_playing = False
            print("Музика на паузі")
        except Exception as e:
            print(f"Помилка паузи музики: {e}")

    def unpause_music(self):
        """Відновлює відтворення музики"""
        try:
            pygame.mixer.music.unpause()
            self.is_playing = True
            print("Музика відновлена")
        except Exception as e:
            print(f"Помилка відновлення музики: {e}")

    def set_volume(self, volume):
        """Встановлює гучність"""
        try:
            pygame.mixer.music.set_volume(volume)
            print(f"Гучність встановлена на {volume}")
        except Exception as e:
            print(f"Помилка встановлення гучності: {e}") 