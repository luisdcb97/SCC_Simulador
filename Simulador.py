#!/usr/bin/env python3
# encoding: utf-8

import rand_generator
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

    def __init__(self, nome: str = "SimuladorX", debug: bool = False, registrar: bool = True, aleatorio: bool = False,
                 gui_stream: list = None):
        self.nome = nome

        self.debug = debug
        self.registrar = registrar  # Atrasa bastante o acesso ao programa
        self.seed_aleatoria = aleatorio

        # Representa o sitio onde são adicionados os prints caso queiramos imprimir num GUI e não na consola
        self.gui_stream = gui_stream

        if gui_stream is not None:
            self.debug = False

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
            Peca.Peca(0, 1 * 1000000, 1, 5, Aleatorio.exp_neg, "A", 0.05, seed_aleatoria=self.seed_aleatoria),
            Peca.Peca(1, 2 * 1000000, 2, 1.33, Aleatorio.exp_neg, "B", 0.05, seed_aleatoria=self.seed_aleatoria)]

        # Numero de pecas vendidas
        self.pecas_vendidas = [0 for i in range(self.numero_pecas)]
        self.pecas_criadas = [0 for i in range(self.numero_pecas)]

        # Custo inicial de quaisquer alteracoes
        self.divida = 0

        if self.registrar:
            self.registo = Registrador.comeca_registo()
            Registrador.regista(self.registo, str(self))
        else:
            self.registo = None

    def __str__(self):
        string = ""
        string += "Simulador \"" + self.nome + "\":\n"

        if self.debug:
            string += "\tModo Debug\n"
        if self.registrar:
            string += "\tA registar valores em " + Registrador.diretorio_registos + " -> " + self.registo.name + "\n"
        if self.seed_aleatoria:
            string += "\tA usar seeds aleatorias\n"

        string += "\n\tHorario de funcionamento: " + str(self.horas) + " "
        if self.horas == 1:
            string += "hora "
        else:
            string += "horas "
        string += "por dia durante " + str(self.dias) + " "
        if self.dias == 1:
            string += "dia"
        else:
            string += "dias"

        string += "\n\tTipos de Pecas:\n"
        for peca in self.tipo_pecas:
            string += altera_string(str(peca), "\t", "\t\t") + "\n"

        string += "\n\tServicos:\n"
        for i in range(len(self.tipo_pecas)):
            string += "\t\tPeca " + str(self.tipo_pecas[i].nome) + ":\n"
            for j in range(len(self.matriz_servicos[i])):
                string += altera_string(str(self.matriz_servicos[i][j]), "\t", "\t\t\t") + "\n"

        return string

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
            rand_generator.randst(self.tipo_pecas[i].semente, self.tipo_pecas[i].stream,
                                  self.tipo_pecas[i].seed_aleatoria)

        dias_executados = 0

        if self.registrar:
            Registrador.regista(self.registo,
                                "\n______________________Inicio da Simulacao_____________________________\n")

        while dias_executados < self.dias:
            self.executa_dia(dias_executados)
            print("Dia executado: " + str(dias_executados + 1))
            dias_executados += 1

        strings = self.relat()
        if self.gui_stream is None:
            for linha in strings:
                print(linha)
        else:
            self.gui_stream.extend(strings)

        if self.registrar:
            for l in strings:
                Registrador.regista(self.registo, l)
            if self.gui_stream is not None:
                self.gui_stream.append("\nDados de registo salvos em " + Registrador.diretorio_registos + " -> " + self.registo.name)
            print("\nDados de registo salvos em " + Registrador.diretorio_registos + " -> " + self.registo.name)

    def executa_dia(self, dias_executados: int):
        temp_string = "\n\n||||||||||||||||||||\n\n"
        temp_string += "->\tDia " + str(dias_executados + 1) + ":"
        temp_string += "\n\n||||||||||||||||||||\n"
        if self.debug:
            if self.gui_stream is None:
                print(temp_string)
            else:
                self.gui_stream.append(temp_string)
        if self.registrar:
            Registrador.regista(self.registo, temp_string)

        while self.tempo < (self.horas * 60 * (dias_executados + 1)):
            linhas = self.lista.lista_to_string()
            for l in linhas:
                if self.debug:
                    if self.gui_stream is None:
                        print(l)
                    else:
                        self.gui_stream.append(l)
                if self.registrar:
                    Registrador.regista(self.registo, l)
            evento = self.lista.retira_evento()
            self.tempo = evento.instante
            self.act_stats()
            evento.executa()

    def act_stats(self):
        """M�todo que actualiza os valores estat�sticos do simulador"""
        atualizados = []
        for i in range(self.numero_pecas):
            for j in range(len(self.matriz_servicos[i])):
                if self.matriz_servicos[i][j] not in atualizados:
                    self.matriz_servicos[i][j].act_stats()
                    atualizados.append(self.matriz_servicos[i][j])

    def relat(self):
        """M�todo que apresenta os resultados de simula��o finais"""
        strings = []
        for i in range(self.numero_pecas):
            strings.append("\n\n|----------------- Estatisticas da Peca " + str(
                self.tipo_pecas[i]) + " ------------------------|")
            for j in range(len(self.matriz_servicos[i])):
                strings.append("\n\n------------ Resultados " + str(
                    self.matriz_servicos[i][j]) + "---------------\n\n")
                relat_servico = self.matriz_servicos[i][j].relat()
                for string in relat_servico:
                    strings.append(string)

        strings.append("\n\n-----Resultados------------\n\n")

        lucro_total = 0
        for i in range(self.numero_pecas):
            strings.append("Peca " + str(self.tipo_pecas[i]) + ":")
            strings.append("\tPreco por Peca: " + str(self.tipo_pecas[i].custo) + " euros")
            strings.append("\tPecas Criadas: " + str(self.pecas_criadas[i]))
            strings.append("\tPecas Vendidadas: " + str(self.pecas_vendidas[i]))
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

    def altera_tempo_chegada(self, indice: int, media: float):
        self.tipo_pecas[indice].altera_media(media)

    def altera_horas(self, horas: int):
        self.horas = horas

    def altera_dias(self, dias: int):
        self.dias = dias

    def altera_registrar(self, altera: bool):
        if not self.registo and altera:
            self.registo = Registrador.comeca_registo()

    def restora_simulador(self):
        self.tempo = 0
        self.lista = Lista.Lista(self)
        self.pecas_vendidas = [0 for i in range(self.numero_pecas)]
        self.pecas_criadas = [0 for i in range(self.numero_pecas)]
        for serv in self.servicos:
            serv.restora_servico()

        if self.registrar:
            self.registo = Registrador.comeca_registo()
            Registrador.regista(self.registo, str(self))
        else:
            self.registo = None


def altera_string(string: str, prefixo: str, adiciona: str) -> str:
    nova = ""
    (antes, sep, depois) = string.partition(prefixo)
    while sep != "":
        nova += (adiciona + antes + sep)
        (antes, sep, depois) = depois.partition(prefixo)
    nova += adiciona + antes
    return nova


if __name__ == "__main__":
    sim = Simulador(registrar=True)
    # sim.altera_dias(20)
    # sim.altera_horas(8)
    print(str(sim))
    sim.executa()
