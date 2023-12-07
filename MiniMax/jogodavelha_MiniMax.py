import tkinter as tk
from tkinter import messagebox
import time
import random

def iniciar_tabuleiro():
    return [[' ' for _ in range(3)] for _ in range(3)]

def imprimir_tabuleiro(tabuleiro):
    for linha in tabuleiro:
        print("|" + "|".join(linha) + "|")
    print()

def vencedor(tabuleiro, jogador):
    for i in range(3):
        if all([celula == jogador for celula in tabuleiro[i]]) or all([tabuleiro[j][i] == jogador for j in range(3)]):
            return True

    if all([tabuleiro[i][i] == jogador for i in range(3)]) or all([tabuleiro[i][2 - i] == jogador for i in range(3)]):
        return True

    return False

def verificar_tabuleiro_cheio(tabuleiro):
    return all(all(celula != ' ' for celula in linha) for linha in tabuleiro)

def algoritmo_minimax(tabuleiro, profundidade, maximizando, contador_geracoes):
    contador_geracoes[0] += 1

    if vencedor(tabuleiro, 'O'):
        return 1, contador_geracoes
    if vencedor(tabuleiro, 'X'):
        return -1, contador_geracoes
    if verificar_tabuleiro_cheio(tabuleiro):
        return 0, contador_geracoes

    if maximizando:
        melhor_pontuacao = float('-inf')
        for i in range(3):
            for j in range(3):
                if tabuleiro[i][j] == ' ':
                    tabuleiro[i][j] = 'O'
                    pontuacao, _ = algoritmo_minimax(tabuleiro, profundidade + 1, False, contador_geracoes)
                    tabuleiro[i][j] = ' '
                    melhor_pontuacao = max(pontuacao, melhor_pontuacao)
        return melhor_pontuacao, contador_geracoes
    else:
        melhor_pontuacao = float('inf')
        for i in range(3):
            for j in range(3):
                if tabuleiro[i][j] == ' ':
                    tabuleiro[i][j] = 'X'
                    pontuacao, _ = algoritmo_minimax(tabuleiro, profundidade + 1, True, contador_geracoes)
                    tabuleiro[i][j] = ' '
                    melhor_pontuacao = min(pontuacao, melhor_pontuacao)
        return melhor_pontuacao, contador_geracoes

def calcular_melhor_jogada(tabuleiro):
    melhor_pontuacao = float('-inf')
    movimentos_possiveis = []
    contador_geracoes = [0]

    tempo_inicial = time.time()

    for i in range(3):
        for j in range(3):
            if tabuleiro[i][j] == ' ':
                tabuleiro[i][j] = 'O'
                pontuacao, _ = algoritmo_minimax(tabuleiro, 0, False, contador_geracoes)
                tabuleiro[i][j] = ' '

                if pontuacao > melhor_pontuacao:
                    melhor_pontuacao = pontuacao
                    movimentos_possiveis = [(i, j)]
                elif pontuacao == melhor_pontuacao:
                    movimentos_possiveis.append((i, j))

    tempo_final = time.time()

    tempo_execucao = tempo_final - tempo_inicial

    movimento = random.choice(movimentos_possiveis) if movimentos_possiveis else (0, 0)
    return movimento, tempo_execucao, contador_geracoes[0]

def main():
    tabuleiro = iniciar_tabuleiro()
    modo_jogo = input("Escolha o modo de jogo (1: Jogador X IA, 2: IA X IA): ")

    if modo_jogo == '1':
        jogador_atual = 'X' if random.random() < 0.5 else 'O'
    else:
        jogador_atual = 'O'

    while True:
        imprimir_tabuleiro(tabuleiro)
        if modo_jogo == '1' and jogador_atual == 'X':
            linha = int(input("Insira a linha (0-2): "))
            coluna = int(input("Insira a coluna (0-2): "))
            if tabuleiro[linha][coluna] == ' ':
                tabuleiro[linha][coluna] = 'X'
                if vencedor(tabuleiro, 'X'):
                    print("X (Jogador) venceu!")
                    break
                jogador_atual = 'O'
        else:
            print(f"Turno da IA ({jogador_atual})")
            movimento, tempo_execucao, geracoes = calcular_melhor_jogada(tabuleiro)
            print(f"IA ({jogador_atual}) demorou {tempo_execucao:.4f} segundos e {geracoes} gerações para decidir.")
            tabuleiro[movimento[0]][movimento[1]] = jogador_atual
            if vencedor(tabuleiro, jogador_atual):
                imprimir_tabuleiro(tabuleiro)
                print(f"{jogador_atual} (IA) venceu!")
                break
            jogador_atual = 'X' if jogador_atual == 'O' else 'O'

        if verificar_tabuleiro_cheio(tabuleiro):
            imprimir_tabuleiro(tabuleiro)
            print("Empate!")
            break

class TicTacToeApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Jogo da Velha - Minimax")
        self.tabuleiro = self.iniciar_tabuleiro()
        self.modo_jogo = None
        self.jogador_atual = None
        self.botoes_tabuleiro = [[None for _ in range(3)] for _ in range(3)]
        self.informacao_jogo = tk.StringVar()
        self.historico_jogadas_ia = []
        self.criar_interface()

    def iniciar_tabuleiro(self):
        return [[' ' for _ in range(3)] for _ in range(3)]

    def criar_interface(self):
        frame_selecao = tk.Frame(self.master)
        frame_selecao.pack()

        tk.Label(frame_selecao, text="Escolha o modo de jogo:").pack()

        frame_botoes = tk.Frame(frame_selecao)
        frame_botoes.pack()
        tk.Button(frame_botoes, text="Jogador x IA", command=lambda: self.iniciar_jogo('1')).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botoes, text="IA x IA", command=lambda: self.iniciar_jogo('2')).pack(side=tk.LEFT, padx=5)

        self.label_informacao = tk.Label(frame_selecao, textvariable=self.informacao_jogo)
        self.label_informacao.pack()

        frame_tabuleiro = tk.Frame(self.master)
        frame_tabuleiro.pack()

        for i in range(3):
            for j in range(3):
                botao = tk.Button(frame_tabuleiro, text=' ', width=10, height=3, command=lambda row=i, col=j: self.jogada_jogador(row, col))
                botao.grid(row=i, column=j)
                self.botoes_tabuleiro[i][j] = botao

        tk.Label(self.master, text="").pack()

        self.texto_historico = tk.Text(self.master, height=20, width=70)
        self.texto_historico.pack()

    def iniciar_jogo(self, modo):
        self.modo_jogo = modo
        self.jogador_atual = 'X' if random.random() < 0.5 else 'O'
        self.tabuleiro = self.iniciar_tabuleiro()
        self.historico_jogadas_ia.clear()
        self.atualizar_tabuleiro()
        self.atualizar_historico_interface()
        self.jogar()

    def jogar(self):
        if self.modo_jogo == '1':
            if self.jogador_atual == 'X':
                self.habilitar_tabuleiro()
            else:
                self.jogada_ia()
                if not self.vencedor('X') and not self.vencedor('O') and self.verificar_tabuleiro_cheio():
                    resultado = "Empate!"
                    self.historico_jogadas_ia.append('\n' + resultado)
                    self.atualizar_historico_interface()
        elif self.modo_jogo == '2':
            self.jogada_ia()

    def jogada_jogador(self, row, col):
        if self.modo_jogo == '1' and self.jogador_atual == 'X' and self.tabuleiro[row][col] == ' ':
            self.tabuleiro[row][col] = 'X'
            self.atualizar_tabuleiro()
            if self.vencedor('X'):
                resultado = "O Jogador venceu!"
                self.historico_jogadas_ia.append('\n' + resultado)
                self.atualizar_historico_interface()
            else:
                self.jogador_atual = 'O'
                self.jogar()

    def jogada_ia(self):
        if not (self.vencedor('X') or self.vencedor('O') or self.verificar_tabuleiro_cheio()):
            tempo_inicio = time.time()
            movimento, tempo_execucao, geracoes = calcular_melhor_jogada(self.tabuleiro)
            self.tabuleiro[movimento[0]][movimento[1]] = self.jogador_atual
            self.atualizar_tabuleiro()
            tempo_execucao = time.time() - tempo_inicio

            detalhes_jogada = f"IA ({self.jogador_atual}) jogou em ({movimento[0]}, {movimento[1]}), tempo: {tempo_execucao:.4f} s, iterações: {geracoes}"
            self.historico_jogadas_ia.append(detalhes_jogada)

            if self.vencedor(self.jogador_atual):
                resultado = f"IA ({self.jogador_atual}) ganhou!"
                self.historico_jogadas_ia.append('\n' + resultado)
                self.atualizar_historico_interface()
            elif self.verificar_tabuleiro_cheio():
                resultado = "Empate!"
                self.historico_jogadas_ia.append('\n' + resultado)
                self.atualizar_historico_interface()
            else:
                self.jogador_atual = 'X' if self.jogador_atual == 'O' else 'O'
                if self.modo_jogo == '2':
                    self.jogar()
        else:
            self.atualizar_historico_interface()

    def atualizar_tabuleiro(self):
        for i in range(3):
            for j in range(3):
                self.botoes_tabuleiro[i][j]['text'] = self.tabuleiro[i][j]
                if self.modo_jogo == '1' and self.tabuleiro[i][j] == ' ':
                    self.botoes_tabuleiro[i][j]['state'] = tk.NORMAL
                else:
                    self.botoes_tabuleiro[i][j]['state'] = tk.DISABLED

    def atualizar_historico_interface(self):
        self.texto_historico.delete('1.0', tk.END)
        for jogada in self.historico_jogadas_ia:
            self.texto_historico.insert(tk.END, jogada + '\n')

    def habilitar_tabuleiro(self):
        for i in range(3):
            for j in range(3):
                if self.tabuleiro[i][j] == ' ':
                    self.botoes_tabuleiro[i][j]['state'] = tk.NORMAL

    def vencedor(self, jogador):
        for linha in self.tabuleiro:
            if all([celula == jogador for celula in linha]):
                return True

        for coluna in range(3):
            if all([self.tabuleiro[linha][coluna] == jogador for linha in range(3)]):
                return True

        if all([self.tabuleiro[i][i] == jogador for i in range(3)]) or all([self.tabuleiro[i][2 - i] == jogador for i in range(3)]):
            return True
        return False

    def verificar_tabuleiro_cheio(self):
        return all(all(celula != ' ' for celula in linha) for linha in self.tabuleiro)

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeApp(root)
    root.mainloop()