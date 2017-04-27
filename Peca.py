#!/usr/bin/env python3
# encoding: utf-8

import rand_generator

class Peca:
    """
    Classe que representa uma peca
    """

    def __init__(self, tipo: int, semente: int, stream: int, media: float, metodo=None, nome: str = "", custo: float = 0, seed_aleatoria: bool=False):
        self.tipo = tipo
        self.nome = nome
        self.custo = custo

        self.semente = semente
        self.stream = stream

        rand_generator.randst(semente, stream, seed_aleatoria)

        self.media = media
        self.metodo = metodo
        if self.metodo is None:
            self.chegada = self.media
        else:
            self.chegada = metodo(self.stream, self.media)

    def altera_media(self, media):
        self.media = media
        if self.metodo is None:
            self.chegada = self.media
        else:
            self.chegada = self.metodo(self.stream, self.media)

    def altera_metodo(self, metodo = None):
        self.metodo = metodo
        if self.metodo is None:
            self.chegada = self.media
        else:
            self.chegada = metodo(self.stream, self.media)

    def altera_aleatoriedade(self, altera: bool):
        rand_generator.randst(self.semente, self.stream, altera)

    def __str__(self):
        return self.nome
