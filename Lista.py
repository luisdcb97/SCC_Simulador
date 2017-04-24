#!/usr/bin/env python3
# encoding: utf-8


class Lista:
    """
    Classe que contem os eventos do simulador a serem executados ordenados crescentemente pelo instante a serem executados
    """

    def __init__(self, sim):
        self.simulador = sim  # Simulador a que pertence a lista de eventos
        self.lista = []

    def insere_evento(self, evento):
        # Insere o evento no fim da lista e reordena-a
        self.lista.append(evento)
        self.lista.sort()

    def retira_evento(self):
        return self.lista.pop(0)

    def imprime_lista(self):
        """
        Imprime todos os eventos na lista
        """
        print("\n\n" + str(self.simulador.tempo) + ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n")
        for eve in self.lista:
            print(eve)
        print("\n\n<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")

    def lista_to_string(self):
        strings = []
        strings.append("\n\n" + str(self.simulador.tempo) + ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n")
        for eve in self.lista:
            strings.append(str(eve))
        strings.append("\n\n<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")
        return strings
