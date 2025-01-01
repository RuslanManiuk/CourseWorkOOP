
#include <vector>
#include <algorithm>
#include <random>
#include <ctime>
#include <climits>

extern "C" {
    // Constants for player pieces
    const int EMPTY = 0;
    const int PLAYER = 1;
    const int AI = 2;
    
    // Difficulty levels
    enum Difficulty {
        EASY = 0,
        MEDIUM = 1,
        HARD = 2
    };

    class ConnectFourAI {
    private:
        int rows;
        int cols;
        std::vector<std::vector<int>> board;
        std::mt19937 rng;

        int evaluateWindow(const std::vector<int>& window, int piece) {
            int score = 0;
            int oppPiece = (piece == PLAYER) ? AI : PLAYER;

            if (std::count(window.begin(), window.end(), piece) == 4)
                score += 100;
            else if (std::count(window.begin(), window.end(), piece) == 3 
                     && std::count(window.begin(), window.end(), EMPTY) == 1)
                score += 5;
            else if (std::count(window.begin(), window.end(), piece) == 2 
                     && std::count(window.begin(), window.end(), EMPTY) == 2)
                score += 2;

            if (std::count(window.begin(), window.end(), oppPiece) == 3 
                && std::count(window.begin(), window.end(), EMPTY) == 1)
                score -= 4;

            return score;
        }

        int scorePosition(const std::vector<std::vector<int>>& board, int piece) {
            int score = 0;

            // Score center column
            std::vector<int> centerColumn;
            int centerCol = cols / 2;
            for (int r = 0; r < rows; r++) {
                centerColumn.push_back(board[r][centerCol]);
            }
            score += std::count(centerColumn.begin(), centerColumn.end(), piece) * 3;

            // Horizontal
            for (int r = 0; r < rows; r++) {
                for (int c = 0; c < cols - 3; c++) {
                    std::vector<int> window = {
                        board[r][c], board[r][c+1], 
                        board[r][c+2], board[r][c+3]
                    };
                    score += evaluateWindow(window, piece);
                }
            }

            // Vertical
            for (int c = 0; c < cols; c++) {
                for (int r = 0; r < rows - 3; r++) {
                    std::vector<int> window = {
                        board[r][c], board[r+1][c],
                        board[r+2][c], board[r+3][c]
                    };
                    score += evaluateWindow(window, piece);
                }
            }

            // Diagonal
            for (int r = 0; r < rows - 3; r++) {
                for (int c = 0; c < cols - 3; c++) {
                    std::vector<int> window1 = {
                        board[r][c], board[r+1][c+1],
                        board[r+2][c+2], board[r+3][c+3]
                    };
                    score += evaluateWindow(window1, piece);

                    std::vector<int> window2 = {
                        board[r+3][c], board[r+2][c+1],
                        board[r+1][c+2], board[r][c+3]
                    };
                    score += evaluateWindow(window2, piece);
                }
            }

            return score;
        }

        int minimax(std::vector<std::vector<int>>& board, int depth, int alpha, int beta, bool maximizingPlayer) {
            std::vector<int> validMoves = getValidMoves(board);
            bool isTerminal = isWinner(board, PLAYER) || isWinner(board, AI) || 
                            validMoves.empty() || depth == 0;

            if (isTerminal) {
                if (isWinner(board, AI))
                    return 100000;
                else if (isWinner(board, PLAYER))
                    return -100000;
                else if (validMoves.empty())
                    return 0;
                else
                    return scorePosition(board, AI);
            }

            if (maximizingPlayer) {
                int maxEval = INT_MIN;
                for (int col : validMoves) {
                    int row = getNextOpenRow(board, col);
                    if (row != -1) {
                        board[row][col] = AI;
                        int eval = minimax(board, depth - 1, alpha, beta, false);
                        board[row][col] = EMPTY;
                        maxEval = std::max(maxEval, eval);
                        alpha = std::max(alpha, eval);
                        if (beta <= alpha)
                            break;
                    }
                }
                return maxEval;
            } else {
                int minEval = INT_MAX;
                for (int col : validMoves) {
                    int row = getNextOpenRow(board, col);
                    if (row != -1) {
                        board[row][col] = PLAYER;
                        int eval = minimax(board, depth - 1, alpha, beta, true);
                        board[row][col] = EMPTY;
                        minEval = std::min(minEval, eval);
                        beta = std::min(beta, eval);
                        if (beta <= alpha)
                            break;
                    }
                }
                return minEval;
            }
        }

    public:
        ConnectFourAI(int r, int c) : rows(r), cols(c) {
            board = std::vector<std::vector<int>>(rows, std::vector<int>(cols, EMPTY));
            rng.seed(std::time(0));
        }

        std::vector<int> getValidMoves(const std::vector<std::vector<int>>& board) {
            std::vector<int> validMoves;
            for (int c = 0; c < cols; c++) {
                if (board[0][c] == EMPTY) {
                    validMoves.push_back(c);
                }
            }
            return validMoves;
        }

        int getNextOpenRow(const std::vector<std::vector<int>>& board, int col) {
            for (int r = rows - 1; r >= 0; r--) {
                if (board[r][col] == EMPTY) {
                    return r;
                }
            }
            return -1;
        }

        bool isWinner(const std::vector<std::vector<int>>& board, int piece) {
            // Horizontal
            for (int r = 0; r < rows; r++) {
                for (int c = 0; c < cols - 3; c++) {
                    if (board[r][c] == piece && 
                        board[r][c+1] == piece &&
                        board[r][c+2] == piece && 
                        board[r][c+3] == piece) {
                        return true;
                    }
                }
            }

            // Vertical
            for (int c = 0; c < cols; c++) {
                for (int r = 0; r < rows - 3; r++) {
                    if (board[r][c] == piece && 
                        board[r+1][c] == piece &&
                        board[r+2][c] == piece && 
                        board[r+3][c] == piece) {
                        return true;
                    }
                }
            }

            // Diagonal (positive slope)
            for (int r = 0; r < rows - 3; r++) {
                for (int c = 0; c < cols - 3; c++) {
                    if (board[r][c] == piece && 
                        board[r+1][c+1] == piece &&
                        board[r+2][c+2] == piece && 
                        board[r+3][c+3] == piece) {
                        return true;
                    }
                }
            }

            // Diagonal (negative slope)
            for (int r = 3; r < rows; r++) {
                for (int c = 0; c < cols - 3; c++) {
                    if (board[r][c] == piece && 
                        board[r-1][c+1] == piece &&
                        board[r-2][c+2] == piece && 
                        board[r-3][c+3] == piece) {
                        return true;
                    }
                }
            }

            return false;
        }

        int getBestMove(const std::vector<std::vector<int>>& currentBoard, int difficulty) {
            board = currentBoard;
            std::vector<int> validMoves = getValidMoves(board);
            
            if (validMoves.empty()) {
                return -1;
            }

            // Easy difficulty: random move
            if (difficulty == EASY) {
                std::uniform_int_distribution<int> dist(0, validMoves.size() - 1);
                return validMoves[dist(rng)];
            }

            // Medium and Hard difficulties use minimax with different depths
            int bestScore = INT_MIN;
            int bestMove = validMoves[0];
            int depth = (difficulty == MEDIUM) ? 4 : 6;

            for (int col : validMoves) {
                int row = getNextOpenRow(board, col);
                if (row != -1) {
                    board[row][col] = AI;
                    int score = minimax(board, depth, INT_MIN, INT_MAX, false);
                    board[row][col] = EMPTY;

                    if (score > bestScore) {
                        bestScore = score;
                        bestMove = col;
                    }
                }
            }

            return bestMove;
        }
    };

    // Interface functions for Python
    ConnectFourAI* createAI(int rows, int cols) {
        return new ConnectFourAI(rows, cols);
    }

    void destroyAI(ConnectFourAI* ai) {
        delete ai;
    }

    int getAIMove(ConnectFourAI* ai, int* board, int rows, int cols, int difficulty) {
        std::vector<std::vector<int>> boardVec(rows, std::vector<int>(cols));
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                boardVec[r][c] = board[r * cols + c];
            }
        }
        return ai->getBestMove(boardVec, difficulty);
    }
}