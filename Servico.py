#!/usr/bin/env python
# encoding: utf-8

import Evento
import Peca
import Simulador
import Aleatorio


class Servico:
    """
    Classe que representa um servico
    """

    def __init__(self, sim: Simulador.Simulador, media: float, desvio: float, maquinas: int = 1,
                 nome: str = "ServicoX"):
        self.espera = []
        self.simulador = sim
        self.ocupacao = [maquinas * False]  # representa o estado de ocupacao de cada maquina do Servico
        self.numero_maquinas = maquinas
        self.atendidos = 0
        self.temp_last = sim.tempo  # Tempo que passou desde o ultimo evento
        self.soma_temp_espera = 0
        self.soma_temp_servico = 0
        self.media = media
        self.desvio = desvio
        self.nome = nome

    def inserePeca(self, peca: Peca.Peca):
        """
        Metodo que insere peca no servico
        """

        for i in range(self.numero_maquinas):
            if not self.ocupacao[i]:  # Se servico livre,
                self.ocupacao[i] = True  # fica ocupado e
                # agenda saida do cliente c para daqui a self.simulator.media_serv instantes
                self.simulador.insereEvento(
                    Evento.Saida(self.simulador.tempo + Aleatorio.normal(self.media, self.desvio), self.simulador,
                                 self, peca))
                break
            else:
                self.espera.append(peca)

    def retiraPeca(self):
        """
        Metodo que retira cliente do servico
        """
        self.atendidos += 1
        if self.espera == []:  # Se a fila est� vazia,
            for i in range(self.numero_maquinas):
                if self.ocupacao[i]:
                    self.ocupacao[i] = False
                    break
        else:
            self.espera.pop(0)
            self.simulador.insereEvento(
                Evento.Saida(self.simulador.tempo + Aleatorio.normal(self.media, self.desvio), self.simulador,
                             self))
