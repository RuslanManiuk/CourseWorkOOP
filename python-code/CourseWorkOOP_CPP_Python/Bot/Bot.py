import ctypes
import numpy as np
import os

from enum import Enum

class Difficulty(Enum):
    EASY = 0
    MEDIUM = 1
    HARD = 2


class ConnectFourAI:
    def __init__(self, rows, cols):

        # Завантаження скомпільованої бібліотеки С++
        self.lib = ctypes.CDLL('Bot/bot_library.dll')

        # Визначення типів аргументів та результатів для ф-цій бібліотеки
        self.lib.createAI.argtypes = [ctypes.c_int, ctypes.c_int]
        self.lib.createAI.restype = ctypes.c_void_p

        self.lib.destroyAI.argtypes = [ctypes.c_void_p]

        self.lib.getAIMove.argtypes = [
            ctypes.c_void_p,
            np.ctypeslib.ndpointer(dtype=np.int32),
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int
        ]
        self.lib.getAIMove.restype = ctypes.c_int

        # Створення екземпляра AI
        self.ai = self.lib.createAI(rows, cols)
        self.rows = rows
        self.cols = cols

    def get_move(self, board, difficulty):
        """
        Отримати хід AI для поточного стану дошки

        :param board: Поточний стан дошки
        :param difficulty: Рівні складності
        :return: Стовпець для ходу AI
        """

        # Перетворення дошки в одновимірний масив
        board_array = np.array(board, dtype=np.int32)

        # Виклик ф-ції С++ для отримання ходу AI
        move = self.lib.getAIMove(
            self.ai,
            board_array,
            self.rows,
            self.cols,
            difficulty.value
        )
        return move

    def __del__(self):
        if hasattr(self, 'ai'):
            self.lib.destroyAI(self.ai)