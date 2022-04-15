# Este é um chatBot de Versiculos biblicos.
import os
import telebot
from telebot import types
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

import Tools.tools
import config

from Biblia.biblia import Biblia
from datetime import datetime

bot = telebot.TeleBot(os.environ['CHAVE_API'])
print("ChatBot Iniciado")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Oi Amigo")

    keyboard = [[InlineKeyboardButton("Option 1", callback_data='1'),
                 InlineKeyboardButton("Option 2", callback_data='2')],
                [InlineKeyboardButton("Option 3", callback_data='3')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    button1 = types.KeyboardButton('/va')
    button2 = types.KeyboardButton('/v')
    #keyboard1 = ReplyKeyboardMarkup(resize_keyboard=True).add(button1).add(button2)
    keyboard2 = ReplyKeyboardMarkup(resize_keyboard=True).row(button1, button2)

    bot.send_message(message.chat.id, "Escolha uma Opção:", reply_markup=keyboard2)


# Solicitar Versiculo Aleatorio
@bot.message_handler(commands=["va", "Va", "vA", "VA"])
def verciculoAleatorio(mensagem):
    try:
        biblia = Biblia()
        biblia.versiculoAleatorio()
        bot.send_message(mensagem.chat.id, biblia.texto)
    except Exception as e:
        Tools.tools.enviarErroAdmin(bot, mensagem, e)


@bot.message_handler(commands=["vaa"])
def verciculoAleatorio(mensagem):
    try:
        biblia = Biblia()
        biblia.versiculoAleatorioAudio()
        bot.send_message(mensagem.chat.id, biblia.texto)
    except Exception as e:
        bot.send_message(mensagem.chat.id, "Algo deu Errado!")
        bot.send_message(os.environ['MY_ID'], str(mensagem.chat.first_name) + "🚨 Filipe Algo deu Errado! Veja: \n" + "📅 " + str(datetime.now().strftime("%d/%m/%y %H:%M:%S")) + "\n🤦 "  + str(e))
        print(mensagem)




@bot.message_handler(commands=["v", "V"])
def verciculo(mensagem):
    print(mensagem.text)
    if mensagem.text == "/v":
        texto = "<b>😓 - Endereço do texto não foi informado!</b>\n" \
                "⚠ - A busca pode ser feita de diversas maneiras:\n \n" \
                "<b>Capítulo Inteiro:</b> \n    ➡Livro.Capitulo\n" \
                "<b>Versículo Especifico:</b> \n    ➡Livro.Capitulo.Versiculo\n" \
                "<b>Intervalos Entre os Textos:</b> \n  ➡Livro.Capitulo.VersiculoInicial.VersiculoFinal\n" \
                "\n<b>Exemplo: /v jo.3.16</b>\n\n" \
                "⚠ - Ficar atento a Colocar um . (PONTO) entre os elementos do endereço"
        bot.send_message(mensagem.chat.id, texto, parse_mode="HTML")
    else:
        try:
            biblia = Biblia(mensagem.text)
            biblia.versiculo()
            bot.send_message(mensagem.chat.id, biblia.texto)
        except Exception as e:
            bot.send_message(mensagem.chat.id, "Algo deu Errado!")
            bot.send_message(os.environ['MY_ID'], str(mensagem.chat.first_name) + "🚨 Filipe Algo deu Errado! Veja: \n" + "📅 " + str(datetime.now().strftime("%d/%m/%y %H:%M:%S")) + "\n🤦 " + str(e))
            print(mensagem)

    if config.devAtivo == True:
        @bot.message_handler(func=lambda message: True)
        def echo_message(message):
            bot.reply_to(message, "ChatBot Rodando em Modo de Desenvolvimento!\nO Desenvolvedor Está Realizando Atualizações!\n SISTEMA INSTAVEL")

bot.polling()
