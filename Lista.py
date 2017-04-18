#!/usr/bin/env python
# encoding: utf-8

import Evento
import Simulador


class Lista:
    """
    Classe que contem os eventos do simulador a serem executados ordenados crescentemente pelo instante a serem executados
    """

    def __init__(self, sim: Simulador.Simulador):
        self.simulador = sim  # Simulador a que pertence a lista de eventos
        self.lista = []

    def insere_evento(self, evento: Evento.Evento):
        # Insere o evento no fim da lista e reordena-a
        self.lista.append(evento)
        self.lista.sort()

    def retira_evento(self) -> Evento.Evento:
        return self.lista.pop(0)

    def imprime_lista(self):
        """
        Imprime todos os eventos na lista
        Evento --- Instante
        """
        pass
