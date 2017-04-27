#!/usr/bin/env python3
# encoding: utf-8

import Peca
import Aleatorio


class Evento:
    """
    Classe abstrata da qual sao derivadas todos os eventos
    """

    def __init__(self, inst: float, sim, servico, peca):
        self.instante = inst  # Instante a que o evento ocorre
        self.simulador = sim
        self.servico = servico
        self.peca = peca

    def __lt__(self, outro):
        """
        Determina se um evento e menor que outro usando o seu instante de ocurrencia
        """
        return self.instante < outro.instante

    def __str__(self):
        return "T: " + str(self.instante) + "\t" + self.__class__.__name__ + " da peca " + str(self.peca) \
               + " do servico " + str(self.servico)


class Chegada(Evento):
    """
    Representa a chegada de uma Peca a um Servico
    """

    def __init__(self, inst: float, sim, servico, peca):
        super().__init__(inst, sim, servico, peca)

    def executa(self):
        self.servico.inserePeca(self.peca)
        indice = self.peca.tipo
        self.simulador.pecas_criadas[indice] += 1
        if self.servico == self.simulador.matriz_servicos[indice][0]:
            tempo_extra = self.peca.get_chegada()
            self.simulador.insereEvento(Chegada(self.simulador.tempo + tempo_extra, self.simulador, self.servico,
                                                Peca.Peca(self.peca.tipo, self.peca.semente, self.peca.stream,
                                                          self.peca.media, nome=self.peca.nome, custo=self.peca.custo)))


class Saida(Evento):
    """
    Representa a saida de uma Peca a um Servico, i.e., a libertacao do Servico
    """

    def __init__(self, inst: float, sim, servico, peca):
        super().__init__(inst, sim, servico, peca)

    def executa(self):
        self.servico.retiraPeca()
        indice_peca = self.peca.tipo
        indice_servico = 0
        for i in range(len(self.simulador.matriz_servicos[indice_peca])):
            if self.simulador.matriz_servicos[indice_peca][i] == self.servico:
                indice_servico = i
        if indice_servico + 1 < len(self.simulador.matriz_servicos[indice_peca]):
            self.simulador.matriz_servicos[indice_peca][indice_servico + 1].inserePeca(self.peca)
        else:
            self.simulador.pecas_vendidas[indice_peca] += 1
