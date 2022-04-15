import os
from datetime import datetime


def enviarErroAdmin(bot, mensagem, e):
    bot.send_message(mensagem.chat.id, "Algo deu Errado!")
    bot.send_message(os.environ['MY_ID'],
                     str(mensagem.chat.first_name) + "🚨 Filipe Algo deu Errado! Veja: \n" + "📅 " + str(
                         datetime.now().strftime("%d/%m/%y %H:%M:%S")) + "\n🤦 " + str(e))
    print(mensagem)