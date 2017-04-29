#!/usr/bin/env python3
# encoding: utf-8

import Evento
import Aleatorio
import rand_generator


class Servico:
    """
    Classe que representa um servico
    """

    def __init__(self, sim, media: float, desvio: float, semente: int, stream: int, maquinas: int = 1,
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

        self.semente = semente
        self.stream = stream
        self.gerador = None

        rand_generator.randst(semente, stream, sim.seed_aleatoria)

    def __str__(self):
        string = self.nome + "\n"
        string += "\t-> Media Chegada: " + str(self.media) + " minutos\n"
        string += "\t-> Desvio Chegada: " + str(self.desvio) + " minutos\n"
        string += "\t-> Numero Maquinas: " + str(self.numero_maquinas) + "\n"

        string += "\t-> Stream: " + str(self.stream) + "\n"
        string += "\t-> Semente: " + str(self.semente)
        if self.simulador.seed_aleatoria:
            string += "\t[Aleatoria]"
        string += "\n"
        return string

    def __repr__(self):
        return "Servico<" + self.nome + ", " + str(self.media) + ", " + str(self.desvio) + ", " \
               + str(self.numero_maquinas) + ">"

    def altera_aleatoriedade(self, altera: bool):
        rand_generator.randst(self.semente, self.stream, altera)

    def altera_maquinas(self, maquinas: int):
        self.numero_maquinas = maquinas

    def altera_tempo(self, media: float, desvio: float):
        self.media = media
        self.desvio = desvio

    def restora_servico(self):
        self.espera = []
        self.ocupadas = 0
        self.atendidos = 0
        self.temp_ultimo = self.simulador.tempo
        self.soma_temp_espera = 0
        self.soma_temp_servico = 0
        rand_generator.randst(self.semente, self.stream, self.simulador.seed_aleatoria)

    def get_tempo(self):
        # GENERATOR POWER
        tempo = None
        while tempo is None:
            try:
                tempo = next(self.gerador)
            except TypeError:
                self.gerador = Aleatorio.gerador_dist_normal(self.stream, self.media, self.desvio)
            except StopIteration:
                self.gerador = Aleatorio.gerador_dist_normal(self.stream, self.media, self.desvio)

        return tempo

    def inserePeca(self, peca):
        """
        Metodo que insere peca no servico
        """

        if self.ocupadas < self.numero_maquinas:
            self.ocupadas += 1
            self.simulador.insereEvento(
                Evento.Saida(self.simulador.tempo + self.get_tempo(), self.simulador,
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
                Evento.Saida(self.simulador.tempo + self.get_tempo(), self.simulador,
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

        strings = []
        strings.append("Tempo medio de espera - " + "{:.5f}".format(temp_med_fila))
        strings.append("Comp. medio da fila - " + "{:.5f}".format(comp_med_fila))
        strings.append("Utilizacao do servico - " + "{:.5f}".format(utilizacao_serv))
        strings.append("Tempo de simulacao - " + "{:.5f}".format(self.simulador.tempo))
        strings.append("Numero de clientes atendidos - " + str(self.atendidos))
        strings.append("Numero de clientes na fila - " + str(len(self.espera)))

        return strings
