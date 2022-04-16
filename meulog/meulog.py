import meulog.tools


class Log:
    """
    Class log para registrar e exibir os erros
    """

    __texto: ''

    def __init__(self, arquivo, id=""):
        """
        :param id: Identificador
        :type id: str
        :param arquivo: Local do arquivo que será salvo
        """
        self.__arquivo = arquivo
        self.__id = id

    def __registrar(self, texto):
        """
        Salvar no arquivo de log o Erro
        :param texto:
        :return:
        """
        texto = texto.replace('-', ';')
        self.__f = open('log', 'a', encoding="utf-8")
        self.__f.writelines(texto)
        self.__f.close()

    def setId(self, id):
        self.__id = id

    def erro(self, localErro, em):
        """
        Recebe um identificador, Local do Erro e Erro a ser Exibido e Registrada
        :param localErro: Onde Ocorreu o Erro
        :type localErro: str
        :param em: Erro retornado pelo Try
        """
        texto = f'E-{meulog.tools.dataHora()}-{self.__id}-{localErro}-{str(em)}\n'
        print(texto)
        self.__registrar(texto)

    def msg(self, msg):
        """
        Recebe um identificador e a mensagem a ser Exibida e Registrada
        :param id: Identificador
        :type id: str
        :param msg: Mensagem a ser Registrada
        :type msg: str
        """
        texto = f'M-{meulog.tools.dataHora()}-{self.__id}-{msg}'
        print(texto)
        self.__registrar(texto+"\n")
