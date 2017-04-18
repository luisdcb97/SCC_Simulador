#!/usr/bin/env python
# encoding: utf-8
import Evento
import Lista
import Servico


class Simulador:
    """
    Representa o simulador com os dados iniciais pre-inseridos

    A unidade de tempo é o minuto
    """

    def __init__(self):
        # Media das distribuicoes de chegada das pecas
        self.media_chegada_A = 5
        self.media_chegada_B = 1.33

        # Numero de clientes a ser atendidos
        self.n_clientes = 100

        # Relogio do simulador - Sempre inicializado a 0
        self.tempo = 0

        # Servicos - pode haver mais que um
        #   ---> Servicos Peca A
        self.perfuracao_A = Servico.Servico(self, 2, 0.7, nome="Perfuracao_A")
        self.polimento_A = Servico.Servico(self, 4, 1.2, nome="Polimento_A")
        #   ---> Servicos Peca B
        self.perfuracao_B = Servico.Servico(self, 0.75, 0.3, nome="Perfuracao_B")
        self.polimento_B = Servico.Servico(self, 3, 1, maquinas=2, nome="Polimento_B")
        #   ---> Servicos Comuns
        self.envernizamento = Servico.Servico(self, 1.4, 0.3 / 60, nome="Perfuracao_A")

        # Lista de eventos - onde são mantidos todos os eventos da simulacao - Apenas existe uma por simulador
        self.lista = Lista.Lista(self)

        # Numero de pecas vendidas
        self.vendidas_A = 0
        self.vendidas_B = 0

        # Custo construcao do simulador - unidade e o euro
        self.construcao = 50
        # Custo manutencao do simulador - unidade e o euro por dia
        self.manutencao = 1

        self.pausa = False

        # TODO agendar a primeira chegada

    def __str__(self):
        pass

    def insereEvento(self, evento: Evento.Evento):
        self.lista.insere_evento(evento)
