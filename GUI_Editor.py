#!/usr/bin/env python3
# encoding: utf-8

from tkinter import *
from tkinter import messagebox
import Simulador

largura_minima_janela = 600
altura_minima_janela = 400


class GUIEditor:
    def __init__(self, simulador, janela_principal=None, dicionario_estados: dict = None):
        self.raiz = Toplevel()
        self.raiz.wm_minsize(largura_minima_janela, altura_minima_janela)

        if janela_principal is not None:
            self.janela_principal = janela_principal
            self.dicionario_estados = dicionario_estados
            self.raiz.wm_protocol('WM_DELETE_WINDOW', self.sai_editor)

        self.simulador = simulador

        self.nav_bar = Frame(self.raiz)
        self.botao_tab_pecas = Button(self.nav_bar, text="Peças")
        self.botao_tab_servicos = Button(self.nav_bar, text="Servicos")

        self.botao_tab_pecas.bind("<Button-1>", self.muda_tab)
        self.botao_tab_servicos.bind("<Button-1>", self.muda_tab)

        # region Frame Pecas

        self.frame_edicao_pecas = Frame(self.raiz)

        self.labelframe_pecas = [LabelFrame(self.frame_edicao_pecas, text="Peça " + str(i)) for i in
                                 range(self.simulador.numero_pecas)]

        self.label_nome_pecas = [Label(self.labelframe_pecas[i], padx=25, text=str(self.simulador.tipo_pecas[i].nome))
                                 for i in
                                 range(self.simulador.numero_pecas)]

        self.label_frame_media_pecas = [LabelFrame(self.labelframe_pecas[i], text="Media") for i in
                                        range(self.simulador.numero_pecas)]

        self.entry_media_pecas = [Entry(self.label_frame_media_pecas[i], ) for i in
                                  range(self.simulador.numero_pecas)]

        for ind in range(len(self.entry_media_pecas)):
            self.entry_media_pecas[ind].bind("<FocusIn>", self.altera_foco_escrita)
            self.entry_media_pecas[ind].bind("<FocusOut>", self.altera_foco_escrita)
            self.entry_media_pecas[ind].bind("<Return>", self.insere_media_peca)
            self.entry_media_pecas[ind].insert(0, self.simulador.tipo_pecas[ind].media)

        self.label_frame_custo_pecas = [LabelFrame(self.labelframe_pecas[i], text="Custo") for i in
                                        range(self.simulador.numero_pecas)]

        self.entry_custo_pecas = [Entry(self.label_frame_custo_pecas[i], ) for i in
                                  range(self.simulador.numero_pecas)]

        for ind in range(len(self.entry_media_pecas)):
            self.entry_custo_pecas[ind].bind("<FocusIn>", self.altera_foco_escrita)
            self.entry_custo_pecas[ind].bind("<FocusOut>", self.altera_foco_escrita)
            self.entry_custo_pecas[ind].bind("<Return>", self.insere_custo_peca)
            self.entry_custo_pecas[ind].insert(0, self.simulador.tipo_pecas[ind].custo)

        for i in range(len(self.labelframe_pecas)):
            self.labelframe_pecas[i].grid(row=i)
            self.label_nome_pecas[i].grid(column=0, row=0)
            self.label_frame_media_pecas[i].grid(column=1, row=0)
            self.entry_media_pecas[i].pack()
            self.label_frame_custo_pecas[i].grid(column=2, row=0)
            self.entry_custo_pecas[i].pack()

        # endregion

        # region Servicos

        self.frame_edicao_servicos = Frame(self.raiz)

        self.labelframe_servicos = [LabelFrame(self.frame_edicao_servicos, text="Serviço " + str(i)) for i in
                                    range(len(self.simulador.servicos))]

        self.label_nome_servicos = [
            Label(self.labelframe_servicos[i], padx=25, text=str(self.simulador.servicos[i].nome)) for i in
            range(len(self.simulador.servicos))]

        self.label_frame_media_servicos = [LabelFrame(self.labelframe_servicos[i], text="Media") for i in
                                           range(len(self.simulador.servicos))]

        self.entry_media_servicos = [Entry(self.label_frame_media_servicos[i]) for i in
                                     range(len(self.simulador.servicos))]

        for ind in range(len(self.entry_media_servicos)):
            self.entry_media_servicos[ind].bind("<FocusIn>", self.altera_foco_escrita)
            self.entry_media_servicos[ind].bind("<FocusOut>", self.altera_foco_escrita)
            self.entry_media_servicos[ind].bind("<Return>", self.insere_media_servico)
            self.entry_media_servicos[ind].insert(0, self.simulador.servicos[ind].media)

        self.label_frame_desvio_servicos = [LabelFrame(self.labelframe_servicos[i], text="Desvio") for i in
                                            range(len(self.simulador.servicos))]

        self.entry_desvio_servicos = [Entry(self.label_frame_desvio_servicos[i]) for i in
                                      range(len(self.simulador.servicos))]

        for ind in range(len(self.entry_desvio_servicos)):
            self.entry_desvio_servicos[ind].bind("<FocusIn>", self.altera_foco_escrita)
            self.entry_desvio_servicos[ind].bind("<FocusOut>", self.altera_foco_escrita)
            self.entry_desvio_servicos[ind].bind("<Return>", self.insere_desvio_servico)
            self.entry_desvio_servicos[ind].insert(0, self.simulador.servicos[ind].desvio)

        self.label_frame_maquinas_servicos = [LabelFrame(self.labelframe_servicos[i], text="Maquinas") for i in
                                              range(len(self.simulador.servicos))]

        self.spinbox_maquinas_servico = [
            Spinbox(self.label_frame_maquinas_servicos[i], from_=1, to=100) for i in
            range(len(self.simulador.servicos))]

        for ind in range(len(self.spinbox_maquinas_servico)):
            self.spinbox_maquinas_servico[ind].bind("<Leave>", self.insere_maquinas_servico)
            self.spinbox_maquinas_servico[ind].delete(0, END)
            self.spinbox_maquinas_servico[ind].insert(0, self.simulador.servicos[ind].numero_maquinas)
            self.spinbox_maquinas_servico[ind].config(state="readonly")

        for i in range(len(self.labelframe_servicos)):
            self.labelframe_servicos[i].grid(row=i, sticky=W)
            self.label_nome_servicos[i].grid(column=0, row=0)
            self.label_frame_media_servicos[i].grid(column=1, row=0)
            self.entry_media_servicos[i].pack()
            self.label_frame_desvio_servicos[i].grid(column=2, row=0)
            self.entry_desvio_servicos[i].pack()
            self.label_frame_maquinas_servicos[i].grid(column=3, row=0)
            self.spinbox_maquinas_servico[i].pack()

        # endregion

        self.nav_bar.pack(side=TOP, fill=BOTH)
        self.botao_tab_pecas.grid(column=1, row=0)
        self.botao_tab_servicos.grid(column=2, row=0)

        self.tooltips = dict()
        self.tooltips[self.botao_tab_pecas] = ToolTip(self.botao_tab_pecas,
                                                      "Abre a tab de edição das Peças do Simulador")
        self.tooltips[self.botao_tab_servicos] = ToolTip(self.botao_tab_servicos,
                                                      "Abre a tab de edição dos Serviços do Simulador")

        self.frame_edicao_pecas.pack(side=BOTTOM, fill=BOTH, expand=True)

    def sai_editor(self):

        if not messagebox.askokcancel("Sair", "Deseja mesmo Sair?"):
            return

        for chave, valor, in self.dicionario_estados.items():
            chave.config(state=valor)

        self.janela_principal.botao_cria.config(state=NORMAL)
        self.janela_principal.botao_cria_c1.config(state=NORMAL)
        self.janela_principal.botao_cria_c2.config(state=NORMAL)
        self.janela_principal.botao_abre_editor.config(state=NORMAL)
        self.janela_principal.check_seed_aleatoria.config(state=NORMAL)
        self.janela_principal.check_registrar.config(state=NORMAL)

        self.janela_principal.adiciona_texto(self.janela_principal.consola,
                                             str(self.simulador) + "\nSimulador alterado!!!")

        self.raiz.destroy()

    def mostra(self):
        self.raiz.update()
        self.centra_janela(self.raiz)
        self.raiz.mainloop()

    def muda_tab(self, evento):
        widget = evento.widget
        frame_atual = self.raiz.slaves()[1]
        if widget == self.botao_tab_pecas and frame_atual != self.frame_edicao_pecas:
            frame_atual.pack_forget()
            self.frame_edicao_pecas.pack(side=BOTTOM, fill=BOTH, expand=True)
        if widget == self.botao_tab_servicos and frame_atual != self.frame_edicao_servicos:
            frame_atual.pack_forget()
            self.frame_edicao_servicos.pack(side=BOTTOM, fill=BOTH, expand=True)

    def entry_flash_errado(self, widget: Widget):
        cor_original = widget.cget("bg")
        tempo = 250
        for i in range(1, 10, 2):
            widget.after(i * tempo, lambda: widget.config(bg="red"))
            widget.after((i + 1) * tempo, lambda: widget.config(bg=cor_original))

    def entry_flash_certo(self, widget: Widget):
        cor_original = widget.cget("bg")
        tempo = 150
        for i in range(1, 10, 2):
            widget.after(i * tempo, lambda: widget.config(bg="green"))
            widget.after((i + 1) * tempo, lambda: widget.config(bg=cor_original))

    def altera_foco_escrita(self, evento):
        widget = evento.widget
        if int(evento.type) == 9:
            widget.config(bg="blue", fg="white")
        elif int(evento.type) == 10:
            widget.config(bg="white", fg="black")

    def insere_inteiro(self, evento):
        widget = evento.widget
        try:
            valor = int(widget.get())
        except ValueError:
            self.entry_flash_errado(widget)
            widget.delete("0", END)
            return False
        return valor

    def insere_float(self, evento):
        widget = evento.widget
        try:
            valor = float(widget.get())
        except ValueError:
            self.entry_flash_errado(widget)
            widget.delete("0", END)
            return False
        return valor

    def insere_media_peca(self, evento):
        valor = self.insere_float(evento)
        if valor is False:
            return
        widget = evento.widget
        if valor <= 0:
            self.entry_flash_errado(widget)
        else:
            self.entry_flash_certo(widget)
            indice = 0
            for i in range(len(self.entry_media_pecas)):
                if self.entry_media_pecas[i] == widget:
                    indice = i
                    break
            self.simulador.altera_tempo_chegada(indice, valor)

    def insere_custo_peca(self, evento):
        valor = self.insere_float(evento)
        if valor is False:
            return
        widget = evento.widget
        if valor <= 0:
            self.entry_flash_errado(widget)
        else:
            self.entry_flash_certo(widget)
            indice = 0
            for i in range(len(self.entry_custo_pecas)):
                if self.entry_custo_pecas[i] == widget:
                    indice = i
                    break
            self.simulador.altera_custo_peca(indice, valor)

    def insere_media_servico(self, evento):
        valor = self.insere_float(evento)
        if valor is False:
            return
        widget = evento.widget
        if valor <= 0:
            self.entry_flash_errado(widget)
        else:
            self.entry_flash_certo(widget)
            indice = 0
            for i in range(len(self.entry_media_servicos)):
                if self.entry_media_servicos[i] == widget:
                    indice = i
                    break
            self.simulador.altera_tempo_servico(indice, valor, self.simulador.servicos[indice].desvio)

    def insere_desvio_servico(self, evento):
        valor = self.insere_float(evento)
        if valor is False:
            return
        widget = evento.widget
        if valor <= 0:
            self.entry_flash_errado(widget)
        else:
            self.entry_flash_certo(widget)
            indice = 0
            for i in range(len(self.entry_media_servicos)):
                if self.entry_desvio_servicos[i] == widget:
                    indice = i
                    break
            self.simulador.altera_tempo_servico(indice, self.simulador.servicos[indice].media, valor)

    def insere_maquinas_servico(self, evento):
        valor = self.insere_inteiro(evento)
        if valor is False:
            return
        widget = evento.widget
        if valor <= 0:
            self.entry_flash_errado(widget)
        else:
            parent_name = widget.winfo_parent()
            parent = widget.nametowidget(parent_name)
            self.entry_flash_certo(parent)
            indice = 0
            for i in range(len(self.spinbox_maquinas_servico)):
                if self.spinbox_maquinas_servico[i] == widget:
                    indice = i
                    break
            self.simulador.altera_maquinas_servico(indice, valor)

    @staticmethod
    def centra_janela(janela):
        largura_ecra = janela.winfo_screenwidth()
        altura_ecra = janela.winfo_screenheight()

        largura_janela = janela.winfo_width()
        altura_janela = janela.winfo_height()

        x = int((largura_ecra - largura_janela) / 2)
        y = int((altura_ecra - altura_janela) / 2)

        janela.geometry("{}x{}+{}+{}".format(largura_janela, altura_janela, x, y))


class ToolTip:
    def __init__(self, widget: Widget, texto: str, tempo: int = 1000):
        self.widget = widget
        self.tempo = tempo
        self.texto = texto
        self.agendado = False
        self.id_criacao = None
        self.posicao = {"x": 0, "y": 0}
        self.janela = None
        self.widget.bind("<Enter>", self.entrar)
        self.widget.bind("<Leave>", self.sair)

    def sair(self, evento=None):
        self.desagendar()
        self.esconder()

    def entrar(self, evento=None):
        self.id_criacao = self.widget.after(1000, self.criar_janela)

    def criar_janela(self):
        x = self.widget.winfo_rootx() + self.widget.winfo_width() + 1
        y = self.widget.winfo_rooty()
        self.janela = Toplevel(self.widget)
        self.janela.wm_overrideredirect(True)
        self.janela.geometry("+%d+%d" % (x, y))
        self.mostra_conteudo()

    def mostra_conteudo(self):
        label = Label(self.janela, text=self.texto, background="#000000",
                      foreground="#ffffff", wraplength=int(self.widget.winfo_screenwidth()*0.2), relief=SOLID, borderwidth=1)
        label.pack()

    def desagendar(self):
        self.widget.after_cancel(self.id_criacao)
        self.id_criacao = None

    def esconder(self):
        janela = self.janela
        self.janela = None
        if janela:
            janela.destroy()


if __name__ == "__main__":
    sim = Simulador.Simulador()
    print(sim)
    app = GUIEditor(sim)
    app.mostra()
    print(sim)
