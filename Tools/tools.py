import os
from datetime import datetime
import pyttsx3


def time():
    return str(datetime.now().strftime("%d/%m/%y;%H:%M:%S"))


def enviarErroAdmin(bot, mensagem, e, em):
    bot.send_message(mensagem.chat.id, "Algo deu Errado!\nDev já foi acionado")
    bot.send_message(os.environ['MY_ID'],
                     str(mensagem.chat.first_name) + "🚨 Filipe Algo deu Errado! Veja: \n" + "📅 " + str(
                         datetime.now().strftime("%d/%m/%y %H:%M:%S")) + "\n🤦 " + str(e) + "\n Erro em: " + em)



def converterTexto(texto, idChat):
    """
     Retorna Caminho do Arquivo de audio ou erro!
    :param texto:
    :return:
    """
    t = texto[3:]
    print(f'{time()}-{idChat} - Converter: {t}')
    f_path = f'mp3s\{idChat}-c.mp3'

    engine = pyttsx3.init()
    engine.save_to_file(t, f_path)
    engine.runAndWait()

    while not (os.path.exists(f_path)):
        print(f'{time()}-{idChat} - Arquivo de Audio Sendo Gerado')

    print(f'{time()}-{idChat} - Arquivo Salvo')
    return f_path
