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

    def __init__(self, nome: str = "SimuladorX"):
        self.nome = nome

        # Numero de pecas diferentes
        self.numero_pecas = 2

        # Media das distribuicoes de chegada das pecas
        self.media_chegada_pecas = [5, 1.33]

        # Numero de clientes a ser atendidos
        self.n_clientes = 100

        # Relogio do simulador - Sempre inicializado a 0
        self.tempo = 0

        # Tempo de funcionamento da simulacao
        #       Horas de producao por dia
        self.horas = 0.5  # TODO valor temporario para diminuir o tempo de teste voltar a por a 8 no fim
        #       Dias da simulacao
        self.dias = 3

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

        dias_executados = 0
        while dias_executados < self.dias:
            temp_string = "\n\n||||||||||||||||||||\n\n"
            temp_string += "->\tDia " + str(dias_executados + 1) + ":"
            temp_string += "\n\n||||||||||||||||||||\n"
            if self.debug:
                print(temp_string)
            while self.tempo < (self.horas * 60 * (dias_executados + 1)):
                linhas = self.lista.lista_to_string()
                for l in linhas:
                    if self.debug:
                        print(l)
                evento = self.lista.retira_evento()
                self.tempo = evento.instante
                self.act_stats()
                evento.executa()
            strings = self.relat(dias_executados)
            for linha in strings:
                print(linha)

            # input("\n\nPressione Enter para Continuar\n\n")
            dias_executados += 1
    def act_stats(self):
        """M�todo que actualiza os valores estat�sticos do simulador"""
        atualizados = []
        for i in range(self.numero_pecas):
            for j in range(len(self.matriz_servicos[i])):
                if self.matriz_servicos[i][j] not in atualizados:
                    self.matriz_servicos[i][j].act_stats()
                    atualizados.append(self.matriz_servicos[i][j])

    def relat(self, dia: int):
        """M�todo que apresenta os resultados de simula��o finais"""
        strings = []
        for i in range(self.numero_pecas):
            strings.append("\n\n|----------------- Estatisticas do dia " + str(dia + 1) + " da Peca " + str(
                self.tipo_pecas[i]) + " ------------------------|")
            for j in range(len(self.matriz_servicos[i])):
                strings.append("\n\n------------ Resultados dia " + str(dia + 1) + " " + str(
                    self.matriz_servicos[i][j]) + "---------------\n\n")
                relat_servico = self.matriz_servicos[i][j].relat()
                for string in relat_servico:
                    strings.append(string)
        return strings

sim = Simulador()
sim.executa()
