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
    for linha in tabuleiro:
        if all([celula == jogador for celula in linha]):
            return True

    for coluna in range(3):
        if all([tabuleiro[linha][coluna] == jogador for linha in range(3)]):
            return True

    if all([tabuleiro[i][i] == jogador for i in range(3)]) or all([tabuleiro[i][2 - i] == jogador for i in range(3)]):
        return True
    return False

def tabuleiro_cheio(tabuleiro):
    return all(all(celula != ' ' for celula in linha) for linha in tabuleiro)

def avaliar_tabuleiro(tabuleiro):
    def pontuar_linha(linha):
        pontuacao = 0
        if linha.count('O') == 2 and linha.count(' ') == 1:
            pontuacao += 10
        if linha.count('X') == 2 and linha.count(' ') == 1:
            pontuacao -= 10
        return pontuacao

    pontuacao = 0
    for i in range(3):
        pontuacao += pontuar_linha([tabuleiro[i][j] for j in range(3)])
        pontuacao += pontuar_linha([tabuleiro[j][i] for j in range(3)])

    pontuacao += pontuar_linha([tabuleiro[i][i] for i in range(3)])
    pontuacao += pontuar_linha([tabuleiro[i][2 - i] for i in range(3)])

    return pontuacao

def melhor_movimento_hill_climbing(tabuleiro, contador_iteracoes):
    melhor_pontuacao = float('-inf')
    movimentos_possiveis = []

    for i in range(3):
        for j in range(3):
            if tabuleiro[i][j] == ' ':
                tabuleiro[i][j] = 'O'
                pontuacao = avaliar_tabuleiro(tabuleiro)
                contador_iteracoes[0] += 1
                tabuleiro[i][j] = ' '

                if pontuacao > melhor_pontuacao:
                    melhor_pontuacao = pontuacao
                    movimentos_possiveis = [(i, j)]
                elif pontuacao == melhor_pontuacao:
                    movimentos_possiveis.append((i, j))

    movimento = random.choice(movimentos_possiveis) if movimentos_possiveis else (0, 0)
    return movimento

def main():
    tabuleiro = iniciar_tabuleiro()
    modo_jogo = input("Escolha o modo de jogo (1: Jogador X IA, 2 IA X IA): ")

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
            tempo_inicio = time.time()
            contador_iteracoes = [0]
            movimento = melhor_movimento_hill_climbing(tabuleiro, contador_iteracoes)
            tempo_fim = time.time()
            tempo_execucao = tempo_fim - tempo_inicio
            print(f"IA ({jogador_atual}) demorou {tempo_execucao:.4f} segundos e {contador_iteracoes[0]} gerações para decidir.")
            tabuleiro[movimento[0]][movimento[1]] = jogador_atual

            if vencedor(tabuleiro, jogador_atual):
                imprimir_tabuleiro(tabuleiro)
                print(f"{jogador_atual} (IA) ganhou!")
                break
            jogador_atual = 'X' if jogador_atual == 'O' else 'O'

        if tabuleiro_cheio(tabuleiro):
            imprimir_tabuleiro(tabuleiro)
            print("Empate!")
            break

class TicTacToeApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Jogo da Velha - Subida da Encosta")
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
                if not self.vencedor('X') and not self.vencedor('O') and self.tabuleiro_cheio():
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
        if not (self.vencedor('X') or self.vencedor('O') or self.tabuleiro_cheio()):
            tempo_inicio = time.time()
            contador_iteracoes = [0]
            movimento = self.melhor_movimento_hill_climbing(contador_iteracoes)
            tempo_fim = time.time()
            self.tabuleiro[movimento[0]][movimento[1]] = self.jogador_atual
            self.atualizar_tabuleiro()
            tempo_execucao = tempo_fim - tempo_inicio

            detalhes_jogada = f"IA ({self.jogador_atual}) jogou em ({movimento[0]}, {movimento[1]}), tempo: {tempo_execucao:.4f} s, iterações: {contador_iteracoes[0]}"
            self.historico_jogadas_ia.append(detalhes_jogada)

            if self.vencedor(self.jogador_atual):
                resultado = f"IA ({self.jogador_atual}) ganhou!"
                self.historico_jogadas_ia.append('\n' + resultado)
                self.atualizar_historico_interface()
            elif self.tabuleiro_cheio():
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

    def limpar_tabuleiro(self):
        for i in range(3):
            for j in range(3):
                self.botoes_tabuleiro[i][j]['text'] = ' '
                self.botoes_tabuleiro[i][j]['state'] = tk.DISABLED
        self.modo_jogo = None
        self.informacao_jogo.set("")

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

    def tabuleiro_cheio(self):
        return all(all(celula != ' ' for celula in linha) for linha in self.tabuleiro)

    def avaliar_tabuleiro(self):
        def pontuar_linha(linha):
            pontuacao = 0
            if linha.count('O') == 2 and linha.count(' ') == 1:
                pontuacao += 10
            if linha.count('X') == 2 and linha.count(' ') == 1:
                pontuacao -= 10
            return pontuacao

        pontuacao = 0
        for i in range(3):
            pontuacao += pontuar_linha([self.tabuleiro[i][j] for j in range(3)])
            pontuacao += pontuar_linha([self.tabuleiro[j][i] for j in range(3)])

        pontuacao += pontuar_linha([self.tabuleiro[i][i] for i in range(3)])
        pontuacao += pontuar_linha([self.tabuleiro[i][2 - i] for i in range(3)])

        return pontuacao

    def melhor_movimento_hill_climbing(self, contador_iteracoes):
        melhor_pontuacao = float('-inf')
        movimentos_possiveis = []

        for i in range(3):
            for j in range(3):
                if self.tabuleiro[i][j] == ' ':
                    self.tabuleiro[i][j] = 'O'
                    pontuacao = self.avaliar_tabuleiro()
                    contador_iteracoes[0] += 1
                    self.tabuleiro[i][j] = ' '

                    if pontuacao > melhor_pontuacao:
                        melhor_pontuacao = pontuacao
                        movimentos_possiveis = [(i, j)]
                    elif pontuacao == melhor_pontuacao:
                        movimentos_possiveis.append((i, j))

        movimento = random.choice(movimentos_possiveis) if movimentos_possiveis else (0, 0)
        return movimento

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeApp(root)
    root.mainloop()