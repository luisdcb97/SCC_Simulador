#!/usr/bin/env python3
# encoding: utf-8

import Evento
import Lista
import Servico
import Peca


class Simulador:
    """
    Representa o simulador com os dados iniciais pre-inseridos

    A unidade de tempo é o minuto
    """

    def __init__(self):
        # Numero de pecas diferentes
        self.numero_pecas = 2

        # Media das distribuicoes de chegada das pecas
        self.media_chegada_pecas = [5, 1.33]

        # Numero de clientes a ser atendidos
        self.n_clientes = 100

        # Relogio do simulador - Sempre inicializado a 0
        self.tempo = 0

        # Servicos - pode haver mais que um
        self.matriz_servicos = [[] for i in range(self.numero_pecas)]
        #   ---> Servicos Peca B
        self.matriz_servicos[0].append(Servico.Servico(self, 2, 0.7, nome="Perfuracao_A"))
        self.matriz_servicos[0].append(Servico.Servico(self, 4, 1.2, nome="Polimento_A"))
        #   ---> Servicos Peca B
        self.matriz_servicos[1].append(Servico.Servico(self, 0.75, 0.3, nome="Perfuracao_B"))
        self.matriz_servicos[1].append(Servico.Servico(self, 3, 1, maquinas=2, nome="Polimento_B"))
        #   ---> Servicos Comuns
        servico = Servico.Servico(self, 1.4, 0.3 / 60, nome="Envernizamento_Comum")
        self.matriz_servicos[0].append(servico)
        self.matriz_servicos[1].append(servico)

        self.servicos = []
        for i in range(len(self.matriz_servicos)):
            for j in range(len(self.matriz_servicos[i])):
                if self.matriz_servicos[i][j] not in self.servicos:
                    self.servicos.append(self.matriz_servicos[i][j])

        # Lista de eventos - onde são mantidos todos os eventos da simulacao - Apenas existe uma por simulador
        self.lista = Lista.Lista(self)

        # Tipos de Pecas vendidas
        self.tipo_pecas = [Peca.Peca(0, "A"), Peca.Peca(1, "B")]

        # Numero de pecas vendidas
        self.pecas_vendidas = [0 for i in range(self.numero_pecas)]

        # Custo construcao do simulador - unidade e o euro
        self.construcao = 50
        # Custo manutencao do simulador - unidade e o euro por dia
        self.manutencao = 1

        self.pausa = False
        self.debug = True

    def __str__(self):
        pass

    def insereEvento(self, evento):
        self.lista.insere_evento(evento)

    def executa(self):
        for i in range(self.numero_pecas):
            self.insereEvento(Evento.Chegada(self.tempo, self, self.matriz_servicos[i][0], self.tipo_pecas[i]))
        while self.servicos[2].atendidos < self.n_clientes:
            if self.debug:
                self.lista.imprime_lista()
            evento = self.lista.retira_evento()
            self.tempo = evento.instante
            self.act_stats()
            evento.executa()
        self.relat()

    def act_stats(self):
        """M�todo que actualiza os valores estat�sticos do simulador"""
        atualizados = []
        for i in range(self.numero_pecas):
            for j in range(len(self.matriz_servicos[i])):
                if self.matriz_servicos[i][j] not in atualizados:
                    self.matriz_servicos[i][j].act_stats()
                    atualizados.append(self.matriz_servicos[i][j])

    def relat(self):
        """M�todo que apresenta os resultados de simula��o finais"""
        for i in range(self.numero_pecas):
            print("\n\n|----------------- Estatisticas finais da Peca " + str(self.tipo_pecas[i]) + " ------------------------|")
            for j in range(len(self.matriz_servicos[i])):
                print("\n\n------------FINAL RESULTS " + str(self.matriz_servicos[i][j]) + "---------------\n\n")
                self.matriz_servicos[i][j].relat()

sim = Simulador()
sim.executa()