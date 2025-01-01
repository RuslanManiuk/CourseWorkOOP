import numpy as np
import ctypes

# Завантаження C++ бібліотеки
lib_path = "D:\\Курсова робота ООП\\CourseWorkOOP_CPP_Python\\Bot\\bot_library.dll"
connect_four_lib = ctypes.CDLL(str(lib_path))

# Константи
EMPTY = 0
PLAYER = 1
AI = 2

# Налаштування типів для функцій C++
connect_four_lib.createAI.argtypes = [ctypes.c_int32, ctypes.c_int32]
connect_four_lib.createAI.restype = ctypes.c_void_p

connect_four_lib.destroyAI.argtypes = [ctypes.c_void_p]
connect_four_lib.destroyAI.restype = None

connect_four_lib.getAIMove.argtypes = [
    ctypes.c_void_p,
    np.ctypeslib.ndpointer(dtype=np.int32, flags='C_CONTIGUOUS'),
    ctypes.c_int32,
    ctypes.c_int32,
    ctypes.c_int32
]
connect_four_lib.getAIMove.restype = ctypes.c_int32


def test_connect_four_ai():
    print("Запуск тестів для Connect Four AI...")

    # Створення екземпляру AI
    rows = ctypes.c_int32(6)
    cols = ctypes.c_int32(7)
    ai_ptr = connect_four_lib.createAI(rows, cols)

    def test_ai_move(board, difficulty, test_name):
        """Допоміжна функція для тестування ходу AI"""
        flat_board = np.ascontiguousarray(board.flatten(), dtype=np.int32)
        move = connect_four_lib.getAIMove(
            ai_ptr,
            flat_board,
            ctypes.c_int32(rows.value),
            ctypes.c_int32(cols.value),
            ctypes.c_int32(difficulty)
        )
        print(f"\n{test_name}")
        print(f"Дошка:")
        print(board)
        print(f"AI обрав стовпець: {move}")
        return move

    # ТЕСТИ ДЛЯ ЛЕГКОГО РІВНЯ (0)
    def test_easy_level():
        print("\n=== ТЕСТИ ЛЕГКОГО РІВНЯ ===")

        def test_easy_empty_board():
            print("\nТест 1.1 - Порожня дошка (Легкий рівень):")
            board = np.zeros((rows.value, cols.value), dtype=np.int32)
            move = test_ai_move(board, 0, "Тест порожньої дошки - легкий рівень")
            assert 0 <= move < cols.value, "Хід має бути в межах дошки"
            print("Очікувана поведінка: Випадковий стовпець")

        def test_easy_partially_filled():
            print("\nТест 1.2 - Частково заповнена дошка (Легкий рівень):")
            board = np.zeros((rows.value, cols.value), dtype=np.int32)
            board[5, 3] = PLAYER
            board[5, 4] = AI
            board[4, 3] = PLAYER
            move = test_ai_move(board, 0, "Тест частково заповненої дошки")
            assert 0 <= move < cols.value, "Хід має бути в межах дошки"
            print("Очікувана поведінка: Випадковий доступний стовпець")

        def test_easy_almost_full():
            print("\nТест 1.3 - Майже повна дошка (Легкий рівень):")
            board = np.ones((rows.value, cols.value), dtype=np.int32) * PLAYER
            board[0, 3] = EMPTY  # Залишаємо одну вільну позицію
            move = test_ai_move(board, 0, "Тест майже повної дошки")
            assert move == 3, "Має вибрати єдиний доступний стовпець"
            print("Очікувана поведінка: Випадковий доступний стовпець")

        def test_easy_full_board():
            print("\nТест 1.4 - Повна дошка (Легкий рівень):")
            board = np.ones((rows.value, cols.value), dtype=np.int32) * PLAYER
            move = test_ai_move(board, 0, "Тест повної дошки")
            assert move == -1, "При повній дошці має повертатися -1"
            print("Очікувана поведінка: Повернення -1")

        test_easy_empty_board()
        test_easy_partially_filled()
        test_easy_almost_full()
        test_easy_full_board()

    # ТЕСТИ ДЛЯ СЕРЕДНЬОГО РІВНЯ (1)
    def test_medium_level():
        print("\n=== ТЕСТИ СЕРЕДНЬОГО РІВНЯ ===")

        def test_medium_empty_board():
            print("\nТест 2.1 - Порожня дошка (Середній рівень):")
            board = np.zeros((rows.value, cols.value), dtype=np.int32)
            move = test_ai_move(board, 1, "Тест порожньої дошки - середній рівень")
            assert 0 <= move < cols.value, "Хід має бути в межах дошки"
            print("Очікувана поведінка: Випадковий стовпець з перевагою центру")

        def test_medium_partially_filled():
            print("\nТест 2.2 - Частково заповнена дошка (Середній рівень):")
            board = np.zeros((rows.value, cols.value), dtype=np.int32)
            board[5, 0:3] = PLAYER  # Три фішки гравця в ряд
            move = test_ai_move(board, 1, "Тест блокування")
            assert move == 3, "AI має заблокувати четверту позицію"
            print("Очікувана поведінка: Блокування простої загрози")

        def test_medium_offensive():
            print("\nТест 2.3 - Створення власної комбінації (Середній рівень):")
            board = np.zeros((rows.value, cols.value), dtype=np.int32)
            board[5, 1:3] = AI  # Дві фішки AI в ряд
            move = test_ai_move(board, 1, "Тест атаки")
            assert 0 <= move < cols.value, "Хід має бути в межах дошки"
            print("Очікувана поведінка: Спроба створити виграшну комбінацію")

        def test_medium_almost_full():
            print("\nТест 2.4 - Майже повна дошка (Середній рівень):")
            board = np.ones((rows.value, cols.value), dtype=np.int32) * PLAYER
            board[0:2, 3] = EMPTY  # Залишаємо дві вільні позиції в центрі
            move = test_ai_move(board, 1, "Тест стратегічного вибору")
            assert move == 3, "Має вибрати центральний стовпець"
            print("Очікувана поведінка: Вибір найбільш значущого ходу")

        def test_medium_full_board():
            print("\nТест 2.5 - Повна дошка (Середній рівень):")
            board = np.ones((rows.value, cols.value), dtype=np.int32) * PLAYER
            move = test_ai_move(board, 1, "Тест повної дошки")
            assert move == -1, "При повній дошці має повертатися -1"
            print("Очікувана поведінка: Повернення -1")

        test_medium_empty_board()
        test_medium_partially_filled()
        test_medium_offensive()
        test_medium_almost_full()
        test_medium_full_board()

    # ТЕСТИ ДЛЯ СКЛАДНОГО РІВНЯ (2)
    def test_hard_level():
        print("\n=== ТЕСТИ СКЛАДНОГО РІВНЯ ===")

        def test_hard_empty_board():
            print("\nТест 3.1 - Порожня дошка (Складний рівень):")
            board = np.zeros((rows.value, cols.value), dtype=np.int32)
            move = test_ai_move(board, 2, "Тест порожньої дошки - складний рівень")
            assert move == 3, "AI має вибрати центральний стовпець"
            print("Очікувана поведінка: Стратегічний початковий вибір (центр)")

        def test_hard_winning_move():
            print("\nТест 3.2 - Виграшна можливість (Складний рівень):")
            board = np.zeros((rows.value, cols.value), dtype=np.int32)
            board[5, 0:3] = AI  # Три фішки AI в ряд
            move = test_ai_move(board, 2, "Тест виграшного ходу")
            assert move == 3, "AI має зробити виграшний хід"
            print("Очікувана поведінка: Виграшний хід")

        def test_hard_blocking_fork():
            print("\nТест 3.3 - Блокування форку (Складний рівень):")
            board = np.zeros((rows.value, cols.value), dtype=np.int32)
            board[5, 2:4] = PLAYER
            board[4, 3] = PLAYER
            move = test_ai_move(board, 2, "Тест блокування форку")
            assert move in [1, 4], "AI має заблокувати потенційний форк"
            print("Очікувана поведінка: Стратегічне блокування")

        def test_hard_almost_full():
            print("\nТест 3.4 - Майже повна дошка (Складний рівень):")
            board = np.ones((rows.value, cols.value), dtype=np.int32) * PLAYER
            board[0:2, 3] = EMPTY
            board[0:2, 4] = EMPTY
            move = test_ai_move(board, 2, "Тест складної стратегії")
            assert move in [3, 4], "AI має вибрати оптимальний стовпець"
            print("Очікувана поведінка: Максимізація власної вигоди")

        def test_hard_full_board():
            print("\nТест 3.5 - Повна дошка (Складний рівень):")
            board = np.ones((rows.value, cols.value), dtype=np.int32) * PLAYER
            move = test_ai_move(board, 2, "Тест повної дошки")
            assert move == -1, "При повній дошці має повертатися -1"
            print("Очікувана поведінка: Повернення -1")

        test_hard_empty_board()
        test_hard_winning_move()
        test_hard_blocking_fork()
        test_hard_almost_full()
        test_hard_full_board()

    try:
        # Запуск всіх тестів
        test_easy_level()
        test_medium_level()
        test_hard_level()

        print("\nВсі тести успішно завершено!")

    except AssertionError as e:
        print(f"\nПомилка тесту: {e}")
    except Exception as e:
        print(f"\nНеочікувана помилка: {e}")
    finally:
        # Очищення пам'яті
        if ai_ptr:
            connect_four_lib.destroyAI(ctypes.c_void_p(ai_ptr))


if __name__ == "__main__":
    test_connect_four_ai()