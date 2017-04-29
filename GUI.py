#!/usr/bin/env python3
# encoding: utf-8

from tkinter import *
import Simulador
import time

largura_minima_janela = 800
altura_minima_janela = 560


class GUI:
    def __init__(self):
        self.raiz = Tk()
        self.raiz.wm_title("Primórdios de um Império Fabril")
        self.raiz.iconbitmap("Icon.ico")
        self.dimensoes_minimas = {"largura": 800, "altura": 560}
        self.raiz.minsize(width=self.dimensoes_minimas["largura"], height=self.dimensoes_minimas["altura"])

        self.cursor_state = {"scrollY": "sb_v_double_arrow", "text_select": "xterm", "button_disabled": "X_cursor",
                             "scrollX": "sb_h_double_arrow", "button": "hand2", "text_console": "tcross"}

        self.side_frame = Frame(width=150, bg="#ffddee", relief=FLAT)
        self.top_frame = Frame(height=50, relief=FLAT)

        self.consola = Text(self.raiz, bg="#1b1a1f", fg="#3d8a2f", wrap=WORD, insertbackground="#5e202f",
                            relief=GROOVE, cursor=self.cursor_state["text_console"], font=("Arial", 14), state=DISABLED,
                            selectbackground="#7c8068")
        self.scroll_consola = Scrollbar(self.raiz, cursor=self.cursor_state["scrollY"])
        # Scrollbar passa a controlar o scroll do texto
        self.scroll_consola.config(command=self.consola.yview)
        # altera a posicao mostrada pelo scrollbar para indicar a posicao no texto
        self.consola.config(yscrollcommand=self.scroll_consola.set)

        self.botao_corre = Button(self.top_frame, text="Correr", bg="#3A3F42", fg="#2AAF51", font=("Arial", 18, "bold"),
                                  relief=RAISED, activebackground="#2AAF51", activeforeground="#3A3F42",
                                  command=self.corre_simulador, state=DISABLED)

        self.botao_restora = Button(self.top_frame, text="Restora", bg="#3A3F42", fg="#2AAF51",
                                    font=("Arial", 18, "bold"), state=DISABLED,
                                    relief=RAISED, activebackground="#2AAF51", activeforeground="#3A3F42",
                                    command=self.restora_simulador)

        self.botao_cria = Button(self.side_frame, text="Cria", bg="#3A3F42", fg="#2AAF51",
                                 font=("Arial", 18, "bold"),
                                 relief=RAISED, activebackground="#2AAF51", activeforeground="#3A3F42",
                                 command=self.cria_simulador)

        self.debug = F

        # Colocar os frames na aplicacao
        self.side_frame.pack(side=LEFT, fill=Y)
        self.top_frame.pack(side=TOP, fill=X)
        self.scroll_consola.pack(side=RIGHT, fill=Y)
        self.consola.pack(side=RIGHT, fill=BOTH)

        # Colocar cenas no frame de cima
        self.botao_corre.pack(side=LEFT)
        self.botao_restora.pack(side=LEFT)

        # Colocar cenas no frame da esquerda
        self.botao_cria.pack(side=TOP)

        self.simulador = None
        self.stream = []

    def cria_simulador(self):
        self.simulador = Simulador.Simulador(registrar=True, gui_stream=self.stream)
        self.adiciona_texto(self.consola, "\nSimulador criado")
        self.adiciona_texto(self.consola, str(self.simulador))

    def corre_simulador(self):
        if self.simulador is not None:
            self.simulador.executa()
            for linha in self.stream:
                self.adiciona_texto(self.consola, linha)
            self.adiciona_texto(self.consola, "\nSimulador correu!!!")
            self.altera_estado_botao(self.botao_corre, DISABLED)
            self.altera_estado_botao(self.botao_restora, NORMAL)
        else:
            self.adiciona_texto(self.consola, "\nSimulador nao correu!!!")

    def restora_simulador(self):
        self.consola.config(state=NORMAL)
        self.consola.delete(1.0, END)
        self.consola.config(state=DISABLED)
        self.adiciona_texto(self.consola, "Simulador reiniciado!!!")
        self.altera_estado_botao(self.botao_corre, NORMAL)
        self.altera_estado_botao(self.botao_restora, DISABLED)

    def mostra(self):
        self.raiz.update()
        self.centra_janela(self.raiz)

        for i in range(200):
            self.adiciona_texto(self.consola, ["linha numero ", i])

        self.raiz.mainloop()

    def altera_estado_botao(self, botao: Button, estado):
        if estado == NORMAL or estado == DISABLED:
            botao.config(state=estado)

    @staticmethod
    def centra_janela(janela: Tk):
        largura_ecra = janela.winfo_screenwidth()
        altura_ecra = janela.winfo_screenheight()

        largura_janela = janela.winfo_width()
        altura_janela = janela.winfo_height()

        x = int((largura_ecra - largura_janela) / 2)
        y = int((altura_ecra - altura_janela) / 2)

        janela.geometry("{}x{}+{}+{}".format(largura_janela, altura_janela, x, y))

    @staticmethod
    def adiciona_texto(contentor: Text, texto):
        adiciona = ""
        if type(texto) == StringVar:
            adiciona = texto.get() + "\n"
        elif type(texto) == str:
            adiciona = texto + "\n"
        elif type(texto) == list:
            for elem in texto:
                adiciona += str(elem) + "\n"
        contentor.config(state=NORMAL)
        contentor.insert(INSERT, adiciona)
        contentor.config(state=DISABLED)
        contentor.see(END)

    @staticmethod
    def alterar_tamanho_janela(janela: Tk, largura: int = 200, altura: int = 200):
        janela.geometry("{}x{}+{}+{}".format(largura, altura, 0, 0))


if __name__ == "__main__":
    app = GUI()
    app.mostra()
