import time
import random

def init_board():
    return [[' ' for _ in range(3)] for _ in range(3)]

def print_board(board):
    for row in board:
        print("|" + "|".join(row) + "|")
    print()

def is_winner(board, player):
    for row in board:
        if all([cell == player for cell in row]):
            return True
    for col in range(3):
        if all([board[row][col] == player for row in range(3)]):
            return True
    if all([board[i][i] == player for i in range(3)]) or all([board[i][2 - i] == player for i in range(3)]):
        return True
    return False

def is_board_full(board):
    return all(all(cell != ' ' for cell in row) for row in board)

def minimax(board, depth, is_maximizing, generation_count):
    generation_count[0] += 1 

    if is_winner(board, 'O'):
        return 1, generation_count
    if is_winner(board, 'X'):
        return -1, generation_count
    if is_board_full(board):
        return 0, generation_count

    if is_maximizing:
        best_score = float('-inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    score, _ = minimax(board, depth + 1, False, generation_count)
                    board[i][j] = ' '
                    best_score = max(score, best_score)
        return best_score, generation_count
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    score, _ = minimax(board, depth + 1, True, generation_count)
                    board[i][j] = ' '
                    best_score = min(score, best_score)
        return best_score, generation_count

def best_move(board):
    best_score = float('-inf')
    possible_moves = []
    generation_count = [0]

    start_time = time.time()

    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'O'
                score, _ = minimax(board, 0, False, generation_count)
                board[i][j] = ' '
                if score > best_score:
                    best_score = score
                    possible_moves = [(i, j)]
                elif score == best_score:
                    possible_moves.append((i, j))

    end_time = time.time() 

    execution_time = end_time - start_time

    move = random.choice(possible_moves) if possible_moves else (0, 0)
    return move, execution_time, generation_count[0]

def main():
    board = init_board()
    game_mode = input("Escolha o modo de jogo (1: Jogador X IA, 2 IA X IA): ")

    if game_mode == '1':
        current_player = 'X' if random.random() < 0.5 else 'O'
    else:
        current_player = 'O'

    while True:
        print_board(board)
        if game_mode == '1' and current_player == 'X':
            row = int(input("Insira a linha (0-2): "))
            col = int(input("Insira a coluna (0-2): "))
            if board[row][col] == ' ':
                board[row][col] = 'X'
                if is_winner(board, 'X'):
                    print("X (Jogador) venceu!")
                    break
                current_player = 'O'
        else:
            print(f"Turno da IA ({current_player})")
            move, execution_time, generations = best_move(board)
            print(f"IA ({current_player}) demorou {execution_time:.4f} segundos e {generations} gerações para decidir.")
            board[move[0]][move[1]] = current_player
            if is_winner(board, current_player):
                print_board(board)
                print(f"{current_player} (IA) venceu!")
                break
            current_player = 'X' if current_player == 'O' else 'O'
        
        if is_board_full(board):
            print_board(board)
            print("Empate!")
            break

main()