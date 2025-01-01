import pygame
import os
import sys

from Menu.main_Menu import MainMenu
from Menu.game_Menu import GameMenu
from Menu.settings_Menu import SettingsMenu
from Menu.one_on_one_Menu import OneOnOneMenu
from Menu.game_bot_Menu import BotGameMenu
from Game.One_on_One_Game import OneOnOneGame
from Game.with_bot_Game import GameWithAI
from Configuration.class_Config import Config
from Music_Manager.music_Manager import MusicManager

class StateManager:
    def __init__(self, screen):
        self.screen = screen
        self.state = "MAIN_MENU"

        # Перевірка, що pygame.mixer ініціалізовано
        if not pygame.mixer.get_init():
            pygame.mixer.init()
            print("Mixer ініціалізовано")

        # Завантаження збережених налаштувань
        Config.load_from_file()

        # Застосування відеоналаштувань
        if Config.FULLSCREEN:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(Config.RESOLUTION)

        # Ініціалізація музики з правильним шляхом
        print("Створення MusicManager")
        self.music_manager = MusicManager()

        # Формування правильного шляху до файлу музики
        music_file = "2-cherry-cute-bgm-271158.mp3"
        music_path = os.path.join("Sounds", music_file)

        print(f"Спроба завантажити музику за шляхом: {music_path}")

        if self.music_manager.load_track(music_path):
            print("Трек успішно завантажено")
            self.music_manager.set_volume(Config.VOLUME)
            if Config.MUSIC_ENABLED:
                print("Спроба відтворення музики при запуску")
                self.music_manager.play_music()
        else:
            print(f"Не вдалося завантажити музику за шляхом: {music_path}")

    def run(self):
        while True:
            if self.state == "MAIN_MENU":
                selected_option = MainMenu(self.screen).display()
                if selected_option == "Грати":
                    self.state = "GAME_MENU"
                elif selected_option == "Налаштування":
                    settings_menu = SettingsMenu(self.screen, self.music_manager)
                    selected_option = settings_menu.display()
                    if selected_option == "Повернутися":
                        self.state = "MAIN_MENU"
                elif selected_option == "Вихід":
                    pygame.quit()
                    sys.exit()

            elif self.state == "GAME_MENU":
                selected_option = GameMenu(self.screen).display()
                if selected_option == "З комп'ютером":
                    self.state = "BOT_GAME_MENU"
                elif selected_option == "1 на 1":
                    self.state = "ONE_ON_ONE_MENU"
                elif selected_option == "Повернутися":
                    self.state = "MAIN_MENU"

            elif self.state == "BOT_GAME_MENU":
                with_bot_menu = BotGameMenu(self.screen)
                selected_option = with_bot_menu.run()
                if selected_option == "back":
                    self.state = "GAME_MENU"
                elif selected_option:
                    difficulty, rows, cols = selected_option
                    game = GameWithAI(self.screen, rows, cols, difficulty.upper())
                    game.play()

            elif self.state == "ONE_ON_ONE_MENU":
                one_on_one_menu = OneOnOneMenu(self.screen)
                selected_option = one_on_one_menu.run()
                if selected_option == "back":
                    self.state = "GAME_MENU"
                elif selected_option[0] == "start_game":
                    rows, cols = selected_option[1], selected_option[2]
                    game = OneOnOneGame(self.screen, rows, cols)
                    game.play()