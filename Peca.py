#!/usr/bin/env python3
# encoding: utf-8


class Peca:
    """
    Classe que representa uma peca
    """

    def __init__(self, tipo: int, nome: str = "", custo: float = 0):
        self.tipo = tipo
        self.nome = nome
        self.custo = custo

    def __str__(self):
        return self.nome
