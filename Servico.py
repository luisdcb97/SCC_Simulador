#!/usr/bin/env python3
# encoding: utf-8

import Evento
import Aleatorio


class Servico:
    """
    Classe que representa um servico
    """

    def __init__(self, sim, media: float, desvio: float, maquinas: int = 1,
                 nome: str = "ServicoX"):
        self.espera = []
        self.simulador = sim
        # Numero de maquinas do Servico ocupadas
        self.ocupadas = 0
        self.numero_maquinas = maquinas
        self.atendidos = 0
        # Tempo que passou desde o ultimo evento
        self.temp_ultimo = sim.tempo
        self.soma_temp_espera = 0
        self.soma_temp_servico = 0
        self.media = media
        self.desvio = desvio
        self.nome = nome

    def __str__(self):
        return self.nome

    def __repr__(self):
        return "Servico<" + self.nome + ", " + str(self.media) + ", " + str(self.desvio) + ", " \
               + str(self.numero_maquinas) + ">"

    def inserePeca(self, peca):
        """
        Metodo que insere peca no servico
        """

        if self.ocupadas < self.numero_maquinas:
            self.ocupadas += 1
            self.simulador.insereEvento(
                Evento.Saida(self.simulador.tempo + Aleatorio.normal(self.media, self.desvio), self.simulador,
                             self, peca))
        else:
            self.espera.append(peca)

    def retiraPeca(self):
        """
        Metodo que retira cliente do servico
        """
        self.atendidos += 1
        if self.espera == []:  # Se a fila est� vazia,
                self.ocupadas -= 1
        else:
            peca = self.espera.pop(0)
            self.simulador.insereEvento(
                Evento.Saida(self.simulador.tempo + Aleatorio.normal(self.media, self.desvio), self.simulador,
                             self, peca))

    def act_stats(self):
        """Metodo que calcula os valores estatisticos a cada iteracao/evento do simulador"""
        # Calcula tempo que passou desde o ultimo evento
        temp_desd_ult = self.simulador.tempo - self.temp_ultimo
        self.temp_ultimo = self.simulador.tempo
        # Contabiliza tempo de espera na fila
        # para todos os clientes que estiveram na fila durante o intervalo
        self.soma_temp_espera += len(self.espera) * temp_desd_ult
        # Contabiliza tempo de atendimento
        self.soma_temp_servico += self.ocupadas * temp_desd_ult

    def relat(self):
        """Metodo que calcula e imprime os valores finais estatisticos"""
        # Tempo m�dio de espera na fila
        temp_med_fila = self.soma_temp_espera / (self.atendidos + len(self.espera))
        # Comprimento m�dio da fila de espera
        # self.simulator.instant neste momento � o valor do tempo de simula��o,
        # uma vez que a simula��o come�ou em 0 e este m�todo s� � chamdo no fim da simula��o
        comp_med_fila = self.soma_temp_espera / self.simulador.tempo
        # Tempo m�dio de atendimento no servi�o
        utilizacao_serv = (self.soma_temp_servico / self.simulador.tempo) / self.numero_maquinas

        # Apresenta resultados
        print("Tempo medio de espera", temp_med_fila)
        print("Comp. medio da fila", comp_med_fila)
        print("Utilizacao do servico", utilizacao_serv)
        print("Tempo de simulacao", self.simulador.tempo)
        print("Numero de clientes atendidos", self.atendidos)
        print("Numero de clientes na fila", len(self.espera))
