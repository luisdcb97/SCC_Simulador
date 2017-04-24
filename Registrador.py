#!/usr/bin/env python3
# encoding: utf-8

import sys
import datetime
import os

diretorio_registos = os.getcwd() + "\Registos"


def novo_diretorio():
    if not os.path.isdir(diretorio_registos):
        os.mkdir(diretorio_registos)


def comeca_registo(nome: str = None):
    data = datetime.datetime.today()

    if os.getcwd() != diretorio_registos:
        novo_diretorio()
        os.chdir(diretorio_registos)

    nome_ficheiro = "Registo - "
    if nome is None:
        nome_ficheiro += "_".join(
            (str(data.year), str(data.month), str(data.day), "-".join((str(data.hour), str(data.minute)))))
    else:
        nome_ficheiro += nome
    nome_ficheiro += ".txt"

    ficheiro = open(nome_ficheiro, "a")
    ficheiro.write("------------------- Registo ")
    if nome is None:
        ficheiro.write("_".join(
            (str(data.year), str(data.month), str(data.day), ":".join((str(data.hour), str(data.minute))))))
    else:
        ficheiro.write("\"" + nome + "\"")

    ficheiro.write("--------------------\n\n")
    # Fazer flush de um ficheiro esvazia o buffer criado pelo programa para ele, i.e. realiza uma
    # system call para os dados serem guardados, no entanto podem existir tambem buffers no sistema operativo, ou seja,
    # os dados podem não ser escritos para disco imediatamente mas para uma memoria temporaria, e.g. RAM
    # Para esvaziar o buffer do SO importar o modulo "os" e usar a funcao fsync
    ficheiro.flush()

    return ficheiro


def regista(ficheiro, linha: str):
    ficheiro.write(linha + "\n")
    ficheiro.flush()


def fecha_registo(ficheiro):
    ficheiro.close()
