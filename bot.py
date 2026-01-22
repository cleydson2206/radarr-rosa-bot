import telebot
from datetime import datetime

TOKEN = "8316037466:AAGEGHmlUlL31TwcFOWCoTtxZcbT9dodx-Y"

bot = telebot.TeleBot(TOKEN)

def f(n):
    return f"{n:02d}"

def normalizar(h, m):
    while m >= 60:
        m -= 60
        h += 1
    if h >= 24:
        h %= 24
    return h, m

@bot.message_handler(commands=['start'])
def start(msg):
    bot.reply_to(
        msg,
        "🌹 *Radar Rosa Bot ativo*\n\n"
        "Use o comando:\n"
        "`/rosa 2152`\n\n"
        "Formato: HHMM\n"
        "Exemplo: /rosa 2152",
        parse_mode="Markdown"
    )

@bot.message_handler(commands=['rosa'])
def radar_rosa(msg):
    try:
        valor = msg.text.split()[1]
        if len(valor) != 4:
            raise ValueError

        h = int(valor[:2])
        m = int(valor[2:])

        d = m // 10
        u = m % 10

        n1 = d + u
        n2 = d * u
        n3 = m // 2

        r1 = normalizar(h, m + n1)
        r2 = normalizar(h, m + n2)
        r3 = normalizar(h, m + n3)

        resposta = (
            "🎯 *ZONAS QUENTES – RADAR ROSA*\n\n"
            f"⏱ {f(r1[0])}:{f(r1[1])}\n"
            f"⏱ {f(r2[0])}:{f(r2[1])}\n"
            f"⏱ {f(r3[0])}:{f(r3[1])}\n\n"
            "⚠️ Use leitura de sequência\n"
            "🌹 Caçador de Rosas"
        )

        bot.reply_to(msg, resposta, parse_mode="Markdown")

    except:
        bot.reply_to(
            msg,
            "❌ Use o formato correto:\n"
            "`/rosa 2152`",
            parse_mode="Markdown"
        )

bot.infinity_polling()
