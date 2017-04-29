#!/usr/bin/env python3
# encoding: utf-8

import rand_generator


class Peca:
    """
    Classe que representa uma peca
    """

    def __init__(self, tipo: int, semente: int, stream: int, media: float, metodo=None, nome: str = "",
                 custo: float = 0, seed_aleatoria: bool = False):
        self.tipo = tipo
        self.nome = nome
        self.custo = custo

        self.semente = semente
        self.stream = stream

        self.media = media
        self.metodo = metodo
        self.seed_aleatoria = seed_aleatoria

    def get_chegada(self):
        if self.metodo is None:
            return self.media
        else:
            return self.metodo(self.stream, self.media)

    def altera_media(self, media):
        self.media = media

    def altera_metodo(self, metodo=None):
        self.metodo = metodo

    def altera_aleatoriedade(self, altera: bool):
        rand_generator.randst(self.semente, self.stream, altera)
        self.seed_aleatoria = altera

    def __str__(self):
        string = self.nome + "\n"
        string += "\t-> Custo: " + str(self.custo) + "\n"
        string += "\t-> Media Chegada: " + str(self.media) + "\n"
        if self.metodo:
            string += "\t-> Metodo Chegada: " + str(self.metodo.__name__) + "\n"

        string += "\t-> Stream: " + str(self.stream) + "\n"
        string += "\t-> Semente: " + str(self.semente)
        if self.seed_aleatoria:
            string += "\t[Aleatoria]"
        string += "\n"
        return string
