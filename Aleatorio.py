#!/usr/bin/env python3
# encoding: utf-8

import rand_generator
import math


def exp_neg(stream: int, media: float = 1):
    """
    Retorna um valor aleatorio seguindo uma distribuicao exponencial de media "media"

    :param media: Media da exponencial
    :type media: float
    :return: Valor resultante da exponencial
    :rtype: float
    """
    return -media * math.log(rand_generator.rand(stream))


def gerador_dist_normal(stream: int, media: float, desvio: float):
    while True:
        v1 = 2 * rand_generator.rand(stream) - 1
        v2 = 2 * rand_generator.rand(stream) - 1

        w = math.pow(v1, 2) + math.pow(v2, 2)
        # Se w for maior que 1 ou menor ou igual a 0 refaz os valores
        if w > 0 and not w > 1:
            break

    # w esta entre 0 e 1, exclusive no 0
    y1 = v1 * math.sqrt((-2 * math.log(w) / w))
    y2 = v2 * math.sqrt((-2 * math.log(w) / w))

    X1 = media + y1 * desvio
    X2 = media + y2 * desvio

    # Apenas fornecemos os valores se forem maiores que 0

    if X1 > 0:
        yield X1

    if X2 > 0:
        yield X2
