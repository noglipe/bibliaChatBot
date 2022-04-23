import os
import telebot
import Tools.tools
from Biblia.biblia import Biblia
from meulog.meulog import Log

log = Log()
bot = telebot.TeleBot(os.environ['CHAVE_API'])
log.inf("Start ChatBot")


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """
    /Start
    :param message:
    :return:
    """
    bot.reply_to(message, f'Olá {message.chat.first_name}')
    log.setId(message.chat.id)
    log.inf("Bem vindo Acionado!")
    texto = "<b>Bem Vindo a Biblia Chat Bot</b>\n" \
            "⚠ - Voce pode buscar versículos de diversas maneiras:\n \n" \
            "<b>Capítulo Inteiro:</b> \n    ➡Livro.Capitulo\n" \
            "<b>Versículo Especifico:</b> \n    ➡Livro.Capitulo.Versiculo\n" \
            "<b>Intervalos Entre os Textos:</b> \n    ➡Livro.Capitulo.VersiculoInicial.VersiculoFinal\n" \
            "\n<b>Exemplo: /v jo.3.16</b>\n\n" \
            "⚠ O .(PONTO) entre os elementos do endereço é obrigatório"
    bot.send_message(message.chat.id, texto, parse_mode="html")
    texto = "Você também pode obter Versículos Aleatórios em texto\n" \
            "<b>\Va</b> - Versículos Aleatório em Texto\n"
    bot.send_message(message.chat.id, texto, parse_mode="html")


@bot.message_handler(commands=["va", "Va", "vA", "VA"])
@log.tente
def versiculo_aleatorio(mensagem):
    log.inf("Solicitando Versículo Aleatório")
    biblia = Biblia(mensagem.chat.id)
    biblia.versiculoAleatorio()
    bot.send_message(mensagem.chat.id, biblia.texto())
    log.inf("Versículo Enviado")


@bot.message_handler(commands=["v", "V"])
def verciculo(mensagem):
    log.inf("Versículo Solicitado")
    if mensagem.text == "/v":
        texto = "<b>😓 - Endereço do texto não foi informado!</b>\n" \
                "⚠ - A busca pode ser feita de diversas maneiras:\n \n" \
                "<b>Capítulo Inteiro:</b> \n    ➡Livro.Capitulo\n" \
                "<b>Versículo Especifico:</b> \n    ➡Livro.Capitulo.Versiculo\n" \
                "<b>Intervalos Entre os Textos:</b> \n  ➡Livro.Capitulo.VersiculoInicial.VersiculoFinal\n" \
                "\n<b>Exemplo: /v jo.3.16</b>\n\n" \
                "⚠ - Ficar atento a Colocar um . (PONTO) entre os elementos do endereço"
        bot.send_message(mensagem.chat.id, texto, parse_mode="HTML")
        log.inf("Solicitação não Validada")
    else:
        try:
            log.inf("Solicitação de Versículo Validada")
            biblia = Biblia(mensagem.chat.id, mensagem.text)
            biblia.versiculo()
            bot.send_message(mensagem.chat.id, biblia.texto())
            log.inf("Versículo Enviado!")
        except Exception as e:
            Tools.tools.enviarErroAdmin(bot, mensagem, e, "verciculo")
            log.erro('verciculo', e)


bot.polling()
