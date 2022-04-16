import os
import telebot
from telebot import types
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
import Tools.tools
import Tools.img_to_texto
from Config import config

from Biblia.biblia import Biblia
from meulog.meulog import Log

log = Log('log')

bot = telebot.TeleBot(os.environ['CHAVE_API'])
log.msg("Start ChatBot")


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """
    /Start
    :param message:
    :return:
    """
    bot.reply_to(message, f'Olá {message.chat.first_name}')
    log.setId((message.chat.id))
    log.msg("Bem vindo Acionado!")
    texto = "<b>Bem Vindo a Biblia Chat Bot</b>\n" \
            "⚠ - Voce pode buscar versículos de diversas maneiras:\n \n" \
            "<b>Capítulo Inteiro:</b> \n    ➡Livro.Capitulo\n" \
            "<b>Versículo Especifico:</b> \n    ➡Livro.Capitulo.Versiculo\n" \
            "<b>Intervalos Entre os Textos:</b> \n    ➡Livro.Capitulo.VersiculoInicial.VersiculoFinal\n" \
            "\n<b>Exemplo: /v jo.3.16</b>\n\n" \
            "⚠ O .(PONTO) entre os elementos do endereço é obrigatório"
    bot.send_message(message.chat.id, texto, parse_mode="html")
    texto = "Você também pode obter Versículos Aleatórios em texto e em áudio\n" \
            "<b>\Va</b> - Versículos Aleatório em Texto\n" \
            "<b>\Vaa</b> - Versículos Aleatório em Áudio\n"
    bot.send_message(message.chat.id, texto, parse_mode="html")


@bot.message_handler(commands=["va", "Va", "vA", "VA"])
def verciculoAleatorio(mensagem):
    log.msg("Solicitando Versículo Aleatório")
    try:
        biblia = Biblia(mensagem.chat.id)
        biblia.versiculoAleatorio()
        bot.send_message(mensagem.chat.id, biblia.texto())
        log.msg("Versículo Enviado")
    except Exception as e:
        Tools.tools.enviarErroAdmin(bot, mensagem, e, 'verciculoAleatorio')
        log.erro('verciculoAleatorio', e)



@bot.message_handler(commands=["aa"])
def verciculoAleatorioAudio(mensagem):
    log.msg("Versículo em Audio Solicitado")
    try:
        biblia = Biblia(mensagem.chat.id)
        f_patch = biblia.converterAudioESalvar(mensagem.chat.id)
        # bot.send_message(mensagem.chat.id, biblia.texto())
        file = open(f_patch, 'rb')
        bot.send_audio(mensagem.chat.id, file)
        log.msg("Versículo em Audio Enviado")
        file.close()
        if os.path.exists(f_patch):
            os.remove(f_patch)
            log.msg("Arquivo de Audio Excluído so Servidor")
    except Exception as e:
        Tools.tools.enviarErroAdmin(bot, mensagem, e, 'verciculoAleatorioAudio')
        log.erro('verciculoAleatorioAudio', e)


@bot.message_handler(commands=["v", "V"])
def verciculo(mensagem):
    log.msg("Versículo Solicitado")
    if mensagem.text == "/v":
        texto = "<b>😓 - Endereço do texto não foi informado!</b>\n" \
                "⚠ - A busca pode ser feita de diversas maneiras:\n \n" \
                "<b>Capítulo Inteiro:</b> \n    ➡Livro.Capitulo\n" \
                "<b>Versículo Especifico:</b> \n    ➡Livro.Capitulo.Versiculo\n" \
                "<b>Intervalos Entre os Textos:</b> \n  ➡Livro.Capitulo.VersiculoInicial.VersiculoFinal\n" \
                "\n<b>Exemplo: /v jo.3.16</b>\n\n" \
                "⚠ - Ficar atento a Colocar um . (PONTO) entre os elementos do endereço"
        bot.send_message(mensagem.chat.id, texto, parse_mode="HTML")
        log.msg("Solicitação não Validada")
    else:
        try:
            log.msg("Solicitação de Versículo Validada")
            biblia = Biblia(mensagem.chat.id, mensagem.text)
            biblia.versiculo()
            bot.send_message(mensagem.chat.id, biblia.texto())
            log.msg("Versículo Enviado!")
        except Exception as e:
            Tools.tools.enviarErroAdmin(bot, mensagem, e, "verciculo")
            log.erro('verciculo', e)


@bot.message_handler(commands=["c", "C"])
def converterAudio(mensagem):
    log.msg("Conversor de Audio Solicitado!")
    try:
        f_patch = Tools.tools.converterTexto(mensagem.text, mensagem.chat.id)
        file = open(f_patch, 'rb')
        bot.send_audio(mensagem.chat.id, file)
        log.msg("Audio Enviado!")

        file.close()

        if os.path.exists(f_patch):
            os.remove(f_patch)
            log.msg("Arquivo Removido do Servidor!")
    except Exception as e:
        Tools.tools.enviarErroAdmin(bot, mensagem, e, "converterAudio")
        log.erro('converterAudio', e)

"""
@bot.message_handler(content_types= ["photo"])
def fotoPtexto(mensagem):
    print(f'{Tools.tools.time()}-{mensagem.chat.id} - Imagem Recebida!')

    file_path = bot.get_file(mensagem.photo[-1].file_id).file_path
    file = bot.download_file(file_path)

    with open(f'img/{mensagem.chat.id}.jpg', 'wb') as new_file:
        new_file.write(file)
        print(f'{Tools.tools.time()}-{mensagem.chat.id} - Imagem Salva!')

    #bot.send_photo(mensagem.chat.id, file)
    #print(f'{Tools.tools.time()}-{mensagem.chat.id} - Imagem Reenviada!')

    bot.send_message(mensagem.chat.id, Tools.img_to_texto.converter(mensagem.chat.id))
"""

@bot.message_handler(func=lambda mensagem: True)
def responderTudo(mensagem):
    if config.devAtivo == True:
        log.msg("Modo Desenvolvedor!")
        print("Já Acabou?")
        bot.reply_to(mensagem, "ChatBot Rodando em Modo de Desenvolvimento!\nSISTEMA INSTAVEL")


bot.polling()
