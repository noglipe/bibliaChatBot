import os

import requests
import pyttsx3
from datetime import datetime
from meulog.meulog import Log

def time():
    return str(datetime.now().strftime("%d/%m/%y %H:%M:%S"))

class Biblia:
    """
    Class par realizar consultas e retonar os texto solicitado da API da
    A Bíblia Digital - https://www.abibliadigital.com.br/api/verses/

    Methods:
        __init__
        converterEndereco
        construirTexto
        realizarConsulta
        versiculoAleatorio
        versiculo
        texto
        converterAudioESalvar

    """

    def converterEndereco(self, endereco):
        """
        Desmembra e texto em livro, capítulo e versículos
        :param endereco:
        :return:
        """

        list_endereco = endereco[3:].lower().split(".")
        self.__opcao = len(list_endereco)

        if self.__opcao == 1:
            self.__texto = "🛑 - Endereço incompleto!"

        if self.__opcao > 1:
            self.__livro = list_endereco[0]
            self.__capitulo = list_endereco[1]

        if self.__opcao > 2:
            self.__versiculos.append(list_endereco[2])

        if self.__opcao > 3:
            self.__versiculos.append(list_endereco[3])

    def __init__(self, idChat, endereco=""):
        """
        :param endereco: endereço do texto Bíblico
        :return :
        """
        print(f'{time()}-{idChat} - Instanciando Bíblia!')
        self.__idChat = idChat
        self.__endereco = endereco
        self.__opcao = 0
        self.__idioma = 'pt'
        self.__versao = 'nvi'
        self.__urlBase = 'https://www.abibliadigital.com.br/api/verses/'
        self.__versiculos = list()
        self.__livro = ""
        self.__capitulo = ""
        self.__texto = ''

        self.converterEndereco(endereco)

        self.__log = Log('log', self.__idChat)
        self.__log.setId(self.__idChat)

    def construirTexto(self, js):
        """
        Recebe o retorno da consulta e constrói o texto que será enviado ao usuário
        :param js:
        :return:
        """
        self.__log.msg("Obtendo Texto")
        self.__texto = ""

        if self.__opcao == 3 or self.__opcao == 1:  # Livro, Capítulo e Versículo
            self.__texto = f'{js["text"]} {js["book"]["name"]} - {js["chapter"]} : {js["number"]}.'
        else:

            if self.__opcao == 2:
                endereco = f'{js["book"]["name"]} : {self.__capitulo}'
                for verse in js["verses"]:
                    self.__texto = self.__texto + " " + verse["text"]
                self.__texto = self.__texto + " " + endereco

            if self.__opcao > 3:
                endereco = f'{js["book"]["name"]} : {self.__capitulo} : {self.__versiculos[0]} - {self.__versiculos[1]}'
                for verse in js["verses"]:
                    if int(verse["number"]) > int(self.__versiculos[0]) and int(verse["number"]) < int(
                            self.__versiculos[1]):
                        self.__texto = self.__texto + " " + verse["text"]
                self.__texto = self.__texto + " " + endereco

    def realizarConsulta(self, url_consulta):
        """
        Realiza a consulta na API caso haja erro salva uma mensagem de erro na variável texto
        :param url_consulta:
        :return:
        """
        self.__log.msg("Realizando Consulta na API")
        r = requests.get(url_consulta)

        if r.status_code == 200:
            self.construirTexto(r.json())
        else:
            self.__texto = "Algo deu Errado!"

    def versiculoAleatorio(self):
        """
        Preenche a variável texto com o retorno da busca por um versículo aleatório na API
        :return:
        """
        self.__log.msg("Preparando Consulta Aleatória")
        url_consulta = f'{self.__urlBase}{self.__versao}/{self.__idioma}/random'
        self.realizarConsulta(url_consulta)

    def versiculo(self):
        """
        Realiza a consulta paseado no endereço informado e armazena o resultado na variável texto
        :return:
        """
        self.__log.msg("Preparando Consulta de versículo")
        if self.__opcao == 3:
            url_consulta = f'{self.__urlBase}{self.__versao}/{self.__livro}/{self.__capitulo}/{self.__versiculos[0]}'
        else:
            url_consulta = f'{self.__urlBase}{self.__versao}/{self.__livro}/{self.__capitulo}'

        self.realizarConsulta(url_consulta)

    def texto(self):
        """
        Retorna o valor da variável texto caso ela tenha um tamanho menor que 4096
        A capacidade do Telergam é de 4096 caracteres
        :return:
        """
        self.__log.msg("Retorno do Texto")
        if len(self.__texto) > 4096:
            return "Tamano do Texto não Suportado pelo Telegram"
        return self.__texto

    def converterAudioESalvar(self, idChat):
        """
        Retorna Caminho do Arquivo de audio ou erro!
        :param idChat: Id do chat
        :return: str
        """
        self.__log.msg("Convertendo Texto em Audio")
        self.versiculoAleatorio()

        engine = pyttsx3.init()
        f_path = f'mp3s/{idChat}-v.mp3'
        engine.save_to_file(self.__texto, f_path)
        engine.runAndWait()

        while not (os.path.exists(f_path)):
            self.__log.msg("LooP Arquivo de Audio Sendo Gerad")

        self.__log.msg("Arquivo de Audio Salvo no Servidor")
        return f_path
