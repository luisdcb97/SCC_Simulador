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

        self.botao_cria_c1 = Button(self.side_frame, text="Cria C1", bg="#3A3F42", fg="#2AAF51",
                                    font=("Arial", 18, "bold"),
                                    relief=RAISED, activebackground="#2AAF51", activeforeground="#3A3F42",
                                    command=self.cria_simulador_c1)

        self.botao_cria_c2 = Button(self.side_frame, text="Cria C2", bg="#3A3F42", fg="#2AAF51",
                                    font=("Arial", 18, "bold"),
                                    relief=RAISED, activebackground="#2AAF51", activeforeground="#3A3F42",
                                    command=self.cria_simulador_c2)

        self.debug = BooleanVar(master=self.side_frame, value=False)
        self.registrar = BooleanVar(master=self.side_frame, value=True)
        self.seed_aleatoria = BooleanVar(master=self.side_frame, value=False)

        self.check_debug = Checkbutton(self.side_frame, text="Debug", command=self.altera_debug, variable=self.debug,
                                       state=DISABLED
                                       )
        self.check_registrar = Checkbutton(self.side_frame, text="Registar", command=self.altera_registrar,
                                           variable=self.registrar)
        self.check_seed_aleatoria = Checkbutton(self.side_frame, text="Seed Aleatoria",
                                                command=self.altera_seed_aleatoria, variable=self.seed_aleatoria)

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
        self.botao_cria_c1.pack(side=TOP)
        self.botao_cria_c2.pack(side=TOP)
        self.check_debug.pack(side=BOTTOM)
        self.check_registrar.pack(side=BOTTOM)
        self.check_seed_aleatoria.pack(side=BOTTOM)

        self.simulador = None
        self.stream = []

    def cria_simulador(self):
        self.stream.clear()
        self.simulador = Simulador.Simulador(registrar=self.registrar.get(), debug=self.debug.get(),
                                             aleatorio=self.seed_aleatoria.get(), gui_stream=self.stream)
        self.adiciona_texto(self.consola, str(self.simulador) + "\nSimulador pronto a correr!!!")
        self.altera_estado_botao(self.botao_corre, NORMAL)
        self.altera_estado_botao(self.botao_restora, DISABLED)

    def cria_simulador_c1(self):
        self.stream.clear()
        self.simulador = Simulador.Simulador(registrar=self.registrar.get(), debug=self.debug.get(),
                                             aleatorio=self.seed_aleatoria.get(), gui_stream=self.stream)
        self.simulador.altera_maquinas_servico(4, 3)
        self.adiciona_texto(self.consola, str(self.simulador) + "\nSimulador pronto a correr!!!")
        self.altera_estado_botao(self.botao_corre, NORMAL)
        self.altera_estado_botao(self.botao_restora, DISABLED)

    def cria_simulador_c2(self):
        self.stream.clear()
        self.simulador = Simulador.Simulador(registrar=self.registrar.get(), debug=self.debug.get(),
                                             aleatorio=self.seed_aleatoria.get(), gui_stream=self.stream)
        self.simulador.altera_tempo_servico(4, 1.7, 1)
        self.adiciona_texto(self.consola, str(self.simulador) + "\nSimulador pronto a correr!!!")
        self.altera_estado_botao(self.botao_corre, NORMAL)
        self.altera_estado_botao(self.botao_restora, DISABLED)

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
        self.stream.clear()
        self.simulador.restora_simulador()
        self.consola.config(state=NORMAL)
        self.consola.delete(1.0, END)
        self.consola.config(state=DISABLED)
        self.adiciona_texto(self.consola, "Simulador reiniciado!!!")
        self.adiciona_texto(self.consola, "-" * 100)
        self.altera_estado_botao(self.botao_corre, NORMAL)
        self.altera_estado_botao(self.botao_restora, DISABLED)
        self.adiciona_texto(self.consola, str(self.simulador) + "\nSimulador pronto a correr!!!")

    def altera_debug(self):
        if self.simulador:
            self.simulador.debug = self.debug.get()
        self.adiciona_texto(self.consola, "Debug alterado para " + str(self.debug.get()))

    def altera_registrar(self):
        if self.simulador:
            self.simulador.registrar = self.registrar.get()
            self.simulador.altera_registrar(self.simulador.registrar)
        self.adiciona_texto(self.consola, "Registar alterado para " + str(self.registrar.get()))

    def altera_seed_aleatoria(self):
        if self.simulador:
            self.simulador.seed_aleatoria = self.seed_aleatoria.get()
            self.simulador.altera_aleatoriedade(self.simulador.seed_aleatoria)
        self.adiciona_texto(self.consola, "Aleatorio alterado para " + str(self.seed_aleatoria.get()))

    def mostra(self):
        self.raiz.update()
        self.centra_janela(self.raiz)
        self.adiciona_intro()
        self.raiz.mainloop()

    def adiciona_intro(self):
        self.consola.config(state=NORMAL)
        self.consola.insert(INSERT, "Bem-vindos ao Simulador \n")
        self.consola.insert(INSERT, "Primórdios de um Império Fabril\n\n")
        self.consola.insert(INSERT, "(C) Copyright 2017 Meme Industries All Rights Reserved\n\n")
        self.consola.tag_add("intro", "1.0", "5.0")
        self.consola.tag_config("intro", justify="center")
        self.consola.tag_add("nome_programa", "2.0", "3.0")
        self.consola.tag_config("nome_programa", font=("Arial", 16, "bold", "italic"), foreground="blue")
        self.consola.tag_add("copyright", "4.0", "5.0")
        self.consola.tag_config("copyright", foreground="#40c050")
        self.consola.config(state=DISABLED)
        self.consola.see(END)

    def altera_estado_botao(self, botao: Button, estado):
        if estado == NORMAL or estado == DISABLED:
            botao.config(state=estado)

    def altera_estado_check(self, botao: Checkbutton, estado):
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
