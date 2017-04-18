#!/usr/bin/env python
# encoding: utf-8

import random
import math
import numpy


def exp_neg(media: float = 1) -> float:
    """
    Retorna um valor aleatorio seguindo uma distribuicao exponencial de media "media"

    :param media: Media da exponencial
    :type media: float
    :return: Valor resultante da exponencial
    :rtype: float
    """
    return -media * math.log(random.random())


def normal(media: float, desvio: float) -> float:
    """
    Retorna um valor aleatorio seguindo uma distribuicao normal de media "media" e desvio-padrao "desvio"

    :param media: Media da distribuicao normal
    :type media: float
    :param desvio: Desvio dadistribuicao normal
    :type desvio: float
    :return: Valor resultante da distribuicao normal
    :rtype: float
    """
    return numpy.random.normal(media, desvio)
