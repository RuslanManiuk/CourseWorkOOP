
class Config:
    # Клас для зберігання налаштувань гри
    FULLSCREEN = False
    RESOLUTION = (800, 600)
    VOLUME = 0.0
    MUSIC_ENABLED = True

    @classmethod
    def save_to_file(cls):
        """Зберігає налаштування в текстовий файл"""
        with open('game_settings.txt', 'w', encoding='utf-8') as f:
            f.write(f'FULLSCREEN={cls.FULLSCREEN}\n')
            f.write(f'RESOLUTION={cls.RESOLUTION[0]},{cls.RESOLUTION[1]}\n')
            f.write(f'VOLUME={cls.VOLUME}\n')
            f.write(f'MUSIC_ENABLED={cls.MUSIC_ENABLED}\n')

    @classmethod
    def load_from_file(cls):
        """Завантажує налаштування з текстового файлу"""
        try:
            with open('game_settings.txt', 'r', encoding='utf-8') as f:
                for line in f:
                    key, value = line.strip().split('=')
                    if key == 'FULLSCREEN':
                        cls.FULLSCREEN = value.lower() == 'true'
                    elif key == 'RESOLUTION':
                        width, height = map(int, value.split(','))
                        cls.RESOLUTION = (width, height)
                    elif key == 'VOLUME':
                        cls.VOLUME = float(value)
                    elif key == 'MUSIC_ENABLED':
                        cls.MUSIC_ENABLED = value.lower() == 'true'
        except FileNotFoundError:
            # Якщо файл не знайдено, використовуємо значення за замовчуванням
            pass