#!/usr/bin/env python3
# encoding: utf-8

import Evento
import Lista
import Servico
import Peca
import Registrador
import Aleatorio


class Simulador:
    """
    Representa o simulador com os dados iniciais pre-inseridos

    A unidade de tempo é o minuto
    """

    def __init__(self, nome: str = "SimuladorX", debug: bool = False, registrar: bool = True, aleatorio: bool = False):
        self.nome = nome

        self.debug = debug
        self.registrar = registrar  # Atrasa bastante o acesso ao programa
        self.seed_aleatoria = aleatorio

        # Numero de pecas diferentes
        self.numero_pecas = 2

        # Relogio do simulador - Sempre inicializado a 0
        self.tempo = 0

        # Tempo de funcionamento da simulacao
        #       Horas de producao por dia
        self.horas = 8
        #       Dias da simulacao
        self.dias = 20

        # Servicos - pode haver mais que um
        self.matriz_servicos = [[] for i in range(self.numero_pecas)]
        #   ---> Servicos Peca B
        self.matriz_servicos[0].append(Servico.Servico(self, 2, 0.7, 10 * 1111111, 10, nome="Perfuracao_A"))
        self.matriz_servicos[0].append(Servico.Servico(self, 4, 1.2, 11 * 1111111, 11, nome="Polimento_A"))
        #   ---> Servicos Peca B
        self.matriz_servicos[1].append(Servico.Servico(self, 0.75, 0.3, 12 * 1111111, 12, nome="Perfuracao_B"))
        self.matriz_servicos[1].append(Servico.Servico(self, 3, 1, 13 * 1111111, 13, maquinas=2, nome="Polimento_B"))
        #   ---> Servicos Comuns
        servico = Servico.Servico(self, 1.4, 0.3, 14 * 1111111, 14, maquinas=2, nome="Envernizamento_Comum")
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
        self.tipo_pecas = [
            Peca.Peca(0, 0 * 1000000, 0, 5, Aleatorio.exp_neg, "A", 0.05, seed_aleatoria=self.seed_aleatoria),
            Peca.Peca(1, 1 * 1000000, 1, 1.33, Aleatorio.exp_neg, "B", 0.05, seed_aleatoria=self.seed_aleatoria)]

        # Numero de pecas vendidas
        self.pecas_vendidas = [0 for i in range(self.numero_pecas)]

        # Custo inicial de quaisquer alteracoes
        self.divida = 0

        if self.registrar:
            self.registo = Registrador.comeca_registo()
            self.regista_servidor()

    def __str__(self):
        pass

    def insereEvento(self, evento):
        self.lista.insere_evento(evento)

    def altera_aleatoriedade(self, altera: bool):
        for serv in self.servicos:
            serv.altera_aleatoriedade(altera)
        for peca in self.tipo_pecas:
            peca.altera_aleatoriedade(altera)

    def executa(self):
        for i in range(self.numero_pecas):
            self.insereEvento(Evento.Chegada(self.tempo, self, self.matriz_servicos[i][0], self.tipo_pecas[i]))

        dias_executados = 0

        if self.registrar:
            Registrador.regista(self.registo,
                                "\n______________________Inicio da Simulacao_____________________________\n")

        while dias_executados < self.dias:
            self.executa_dia(dias_executados)
            if self.pausa:
                input("\n\nPressione Enter para Continuar\n\n")
            dias_executados += 1
        if self.registrar:
            print("\nDados de registo salvos em " + Registrador.diretorio_registos + " -> " + self.registo.name)

    def executa_dia(self, dias_executados: int):
        temp_string = "\n\n||||||||||||||||||||\n\n"
        temp_string += "->\tDia " + str(dias_executados + 1) + ":"
        temp_string += "\n\n||||||||||||||||||||\n"
        if self.debug:
            print(temp_string)
        if self.registrar:
            Registrador.regista(self.registo, temp_string)

        while self.tempo < (self.horas * 60 * (dias_executados + 1)):
            linhas = self.lista.lista_to_string()
            for l in linhas:
                if self.debug:
                    print(l)
                if self.registrar:
                    Registrador.regista(self.registo, l)
            evento = self.lista.retira_evento()
            self.tempo = evento.instante
            self.act_stats()
            evento.executa()
        strings = self.relat(dias_executados)
        for linha in strings:
            print(linha)

        if self.registrar:
            for l in strings:
                Registrador.regista(self.registo, l)

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

        strings.append("\n\n-----Resultados do dia " + str(dia + 1) + "------------\n\n")

        lucro_total = 0
        for i in range(self.numero_pecas):
            strings.append("Peca " + str(self.tipo_pecas[i]) + ":")
            strings.append("\tPreco por Peca: " + str(self.tipo_pecas[i].custo) + " euros")
            strings.append("\tPecas Vendidads: " + str(self.pecas_vendidas[i]))
            lucro = self.pecas_vendidas[i] * self.tipo_pecas[i].custo
            lucro_total += lucro
            strings.append("\tLucro total: " + "{:.2f}".format(lucro))
            strings.append(
                "\tLucro apos pagar divida: " + "{:.2f}".format(lucro - self.divida))

        strings.append("Lucro total producao: " + "{:.2f}".format(lucro_total))
        strings.append(
            "Lucro producao apos pagar divida: " + "{:.2f}".format(lucro_total - self.divida))
        return strings

    def regista_servidor(self):
        Registrador.regista(self.registo, "Simulador \"" + self.nome + "\":")

        string = "\tHorario de funcionamento: " + str(self.horas) + " "
        if self.horas == 1:
            string += "hora "
        else:
            string += "horas "
        string += "por dia durante " + str(self.dias) + " "
        if self.dias == 1:
            string += "dia"
        else:
            string += "dias"
        Registrador.regista(self.registo, string)

        string = "\tTipos de Pecas:\n"
        for peca in self.tipo_pecas:
            string += "\t\t" + str(peca) + "\n"
        Registrador.regista(self.registo, string)

        string = "\tServicos:\n"
        for i in range(len(self.tipo_pecas)):
            string += "\t\tPeca " + str(self.tipo_pecas[i].nome) + ":\n"
            for j in range(len(self.matriz_servicos[i])):
                string += "\t\t\t" + str(self.matriz_servicos[i][j]) + "\n"
        Registrador.regista(self.registo, string)

    def limpa_servicos(self):
        self.matriz_servicos = [[] for i in range(self.numero_pecas)]
        self.servicos = []

    def restora_lista_servicos(self):
        self.servicos = []
        for i in range(len(self.matriz_servicos)):
            for j in range(len(self.matriz_servicos[i])):
                if self.matriz_servicos[i][j] not in self.servicos:
                    self.servicos.append(self.matriz_servicos[i][j])

    def remove_servico(self, peca, indice):
        self.matriz_servicos[peca.tipo] = self.matriz_servicos[peca.tipo][:indice] + self.matriz_servicos[peca.tipo][
                                                                                     indice + 1:]

    def altera_maquinas_servico(self, indice: int, maquinas: int):
        self.servicos[indice].numero_maquinas = maquinas

    def altera_tempo_servico(self, indice: int, media: float, desvio: float):
        self.servicos[indice].media = media
        self.servicos[indice].desvio = desvio

    def restora_simulador(self):
        self.tempo = 0
        self.lista = Lista.Lista(self)
        self.pecas_vendidas = [0 for i in range(self.numero_pecas)]
        for serv in self.servicos:
            serv.espera = []
            serv.ocupadas = 0
            serv.temp_ultimo = self.tempo
            serv.soma_temp_espera = 0
            serv.soma_temp_servico = 0


if __name__ == "__main__":
    sim = Simulador()
    sim.executa()
    sim.restora_simulador()
    sim.executa()
