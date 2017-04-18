#!/usr/bin/env python
# encoding: utf-8

import Peca
import Aleatorio
import Simulador
import Servico


class Evento:
    """
    Classe abstrata da qual sao derivadas todos os eventos
    """

    def __init__(self, inst: float, sim: Simulador.Simulador, servico, peca: Peca.Peca):
        self.instante = inst  # Instante a que o evento ocorre
        self.simulador = sim
        self.servico = servico
        self.peca = peca

    def __lt__(self, outro):
        """
        Determina se um evento e menor que outro usando o seu instante de ocurrencia
        """
        return self.instante < outro.instante


class Chegada(Evento):
    """
    Representa a chegada de uma Peca a um Servico
    """

    def __init__(self, inst: float, sim: Simulador.Simulador, servico, peca: Peca.Peca):
        super().__init__(inst, sim, servico, peca)

    def executa(self):
        self.servico.inserePeca(self.peca)
        if self.servico == self.simulador.perfuracao_A:
            self.simulador.insereEvento(
                Chegada(self.simulador.tempo + Aleatorio.exp_neg(self.simulador.media_chegada_A), self.simulador,
                        self.servico, Peca.PecaA()))
        elif self.servico == self.simulador.perfuracao_B:
            self.simulador.insereEvento(
                Chegada(self.simulador.tempo + Aleatorio.exp_neg(self.simulador.media_chegada_B), self.simulador,
                        self.servico, Peca.PecaB()))


class Saida(Evento):
    """
    Representa a saida de uma Peca a um Servico, i.e., a libertacao do Servico
    """

    def __init__(self, inst: float, sim: Simulador.Simulador, servico: Servico.Servico, peca: Peca.Peca):
        super().__init__(inst, sim, servico, peca)

    def executa(self):
        self.servico.retiraPeca()
        # se peca for do tipo A
        if self.servico == self.simulador.perfuracao_A:
            self.simulador.insereEvento(
                Chegada(self.simulador.tempo, self.simulador, self.simulador.polimento_A, self.peca))
        elif self.servico == self.simulador.polimento_A:
            self.simulador.insereEvento(
                Chegada(self.simulador.tempo, self.simulador, self.simulador.envernizamento, self.peca))

        if self.servico == self.simulador.perfuracao_B:
            self.simulador.insereEvento(
                Chegada(self.simulador.tempo, self.simulador, self.simulador.polimento_B, self.peca))
        elif self.servico == self.simulador.polimento_B:
            self.simulador.insereEvento(
                Chegada(self.simulador.tempo, self.simulador, self.simulador.envernizamento, self.peca))
