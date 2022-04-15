import requests
import pyttsx3

#Estou utilizando a abibliadigital.com.br para retornar os versiculos
class Biblia():
    __idioma = 'pt'
    __versao = 'nvi'
    __urlBase = 'https://www.abibliadigital.com.br/api/verses/'
    __versiculoInicial = ''
    __versiculoFinal =''
    __livro = ""
    __capitulo = ""
    texto = ''

    def __init__(self, endereco=""):
        print(endereco)
        try:
            listEndereco = endereco[3:].lower().split(".")
            if len(listEndereco) == 1:
                self.texto = "🛑 - Endereço incompleto!"
            if len(listEndereco) > 1:
                if len(listEndereco) > 2:
                    if len(listEndereco) > 3:
                        self.__versiculoFinal = listEndereco[3]
                    self.__versiculoInicial = listEndereco[2]
                self.__livro = listEndereco[0]
                self.__capitulo = listEndereco[1]
        except:
            pass

    def versiculo2Aleatorio(self):
        url = f'{self.__urlBase}{self.__versao}/{self.__idioma}/random'
        requisicao = requests.get(url)
        if requisicao.status_code ==200:
            js = requisicao.json()
            self.texto = f'{js["text"]} {js["book"]["name"]}: {js["chapter"]}:{js["number"]}'
        else:
            self.texto = "Algo deu Errado!"

    def versiculo(self):
        if self.__capitulo != "" and self.__livro != "":
            url = f'{self.__urlBase}{self.__versao}/{self.__livro}/{self.__capitulo}'

            if self.__versiculoInicial != "" and self.__versiculoFinal == "":
                url = f'{self.__urlBase}{self.__versao}/{self.__livro}/{self.__capitulo}/{self.__versiculoInicial}'

            requisicao = requests.get(url)
            if requisicao.status_code ==200:
                js = requisicao.json()
                endVerso = ""
                if self.__versiculoFinal != "":
                    endVerso = f'{self.__versiculoInicial}-{self.__versiculoFinal}'
                    for verso in js["verses"]:
                        if (int(verso["number"]) >= int(self.__versiculoInicial)) and (
                                int(verso["number"]) <= int(self.__versiculoFinal)):
                            self.texto = self.texto + " " + verso["text"]

                else:
                    if self.__versiculoInicial == "":
                        for verso in js["verses"]:
                                self.texto = self.texto + " " + verso["text"]
                    else:
                        self.texto = js["text"]
                        endVerso = self.__versiculoInicial

                self.texto = f'{self.texto} - {js["book"]["name"]:} {self.__capitulo}:{endVerso}'
            else:
                self.texto = "Algo deu Errado!"

            if len(self.texto) > 4096:
                self.texto = "Tamanho do texto não suportado"

        else:
            self.texto = "Endereço Incorreto!"

    def versiculoAleatorioAudio(self):
        self.versiculoAleatorio()
        engine = pyttsx3.init()
        engine.save_to_file(self.texto, 'test.mp3')
