from datetime import datetime


def dataHora():
    """
    :return: Retorna a Data e Hora Formatada
    """
    dh = str(datetime.now().strftime("%d/%m/%y %H:%M:%S"))
    dh.replace(' ', '-')
    return str(dh)
