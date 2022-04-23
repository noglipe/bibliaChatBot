import meulog.tools


class Log:
    """
    Registrar e exibir os erros

    Methods:
        erro
        inf
        setArquivo
        setId
        tente
    """

    def __init__(self, path='log.csv', identificador='0'):
        """
        :param identificador: Caso queira registrar algum identificador
        :type identificador: str
        :param path: Local do arquivo que será salvo
        :type path: str
        """
        self.__path = path
        self.__id = identificador

    def __registrar(self, texto):
        """
        Salvar no arquivo de log
        :param texto:
        :return:
        """
        texto = texto.replace('-', ';')
        self.__f = open(self.__path, 'a', encoding="utf-8")
        self.__f.writelines(texto)
        self.__f.close()

    def erro(self, funcao_erro, em):
        """
        Exibir e Registrar erro
        :param funcao_erro: Onde Ocorreu o Erro
        :type funcao_erro: str
        :param em: Erro retornado pelo Try
        """
        texto = f'E-{meulog.tools.dataHora()}-{self.__id}-{funcao_erro}-{str(em)}'
        print(texto+'\n')
        self.__registrar(texto)

    def inf(self, msg):
        """
        Exibir e Registrar informação.
        :param msg: Mensagem a ser registrada.
        :type msg: str.
        """
        texto = f'M-{meulog.tools.dataHora()}-{self.__id}-{msg}'
        print(texto)
        self.__registrar(texto + '\n')

    def setArquivo(self, arquivo):
        """
        Altera o caminho do Arquivo
        """
        self.__path = arquivo

    def setId(self, identificador):
        self.__id = identificador

    def setFuncao(self, funcao):
        self.__funcao = funcao

    def tente(self, func):
        """

        :param func:
        :return:
        """

        def tentar(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except Exception as e:
                self.erro(func.__name__, e)

        return tentar
