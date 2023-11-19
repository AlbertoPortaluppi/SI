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

def evaluate_board(board):
    def score_line(line):
        score = 0
        if line.count('O') == 2 and line.count(' ') == 1:
            score += 10
        if line.count('X') == 2 and line.count(' ') == 1:
            score -= 10
        return score

    score = 0
    for i in range(3):
        score += score_line([board[i][j] for j in range(3)]) 
        score += score_line([board[j][i] for j in range(3)]) 

    score += score_line([board[i][i] for i in range(3)])
    score += score_line([board[i][2 - i] for i in range(3)])

    return score

def hill_climbing_best_move(board, iteration_count):
    best_score = float('-inf')
    possible_moves = []

    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'O'
                score = evaluate_board(board)
                iteration_count[0] += 1 
                board[i][j] = ' '
                if score > best_score:
                    best_score = score
                    possible_moves = [(i, j)]
                elif score == best_score:
                    possible_moves.append((i, j))

    move = random.choice(possible_moves) if possible_moves else (0, 0)
    return move

def main_hill_climbing():
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
            start_time = time.time()
            iteration_count = [0]
            move = hill_climbing_best_move(board, iteration_count)
            end_time = time.time()
            execution_time = end_time - start_time
            print(f"IA ({current_player}) demorou {execution_time:.4f} segundos e {iteration_count[0]} gerações para decidir.")
            board[move[0]][move[1]] = current_player
            if is_winner(board, current_player):
                print_board(board)
                print(f"{current_player} (IA) ganhou!")
                break
            current_player = 'X' if current_player == 'O' else 'O'
        
        if is_board_full(board):
            print_board(board)
            print("Empate!")
            break

main_hill_climbing()