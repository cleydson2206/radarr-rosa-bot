import os
import telebot
from datetime import datetime
import pytz

# ===== CONFIG VIA VARIÁVEIS DE AMBIENTE =====
# Railway → Variáveis:
# BOT_TOKEN = token do bot
# GROUP_ID  = id do grupo (ex: -100xxxxxxxxxx)

TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = int(os.getenv("GROUP_ID"))

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

TZ_BR = pytz.timezone("America/Sao_Paulo")


def agora_br():
    return datetime.now(TZ_BR).strftime("%H:%M")


# ===== COMANDOS =====

@bot.message_handler(commands=["start"])
def start(msg):
    bot.send_message(
        msg.chat.id,
        "🤖 <b>Radar Rosa ATIVO</b>\n\n"
        "Comandos disponíveis:\n"
        "🌸 /rosa HH:MM\n"
        "♻️ /recuperacao\n"
        "⏰ Horário de Brasília"
    )


@bot.message_handler(commands=["rosa"])
def rosa(msg):
    try:
        hora = msg.text.split(" ")[1]
        bot.send_message(
            GROUP_ID,
            f"🌸 <b>ROSA CONFIRMADA</b>\n"
            f"⏰ Entrada: <b>{hora}</b>"
        )
    except:
        bot.reply_to(msg, "❌ Use: /rosa HH:MM")


@bot.message_handler(commands=["recuperacao"])
def recuperacao(msg):
    bot.send_message(
        GROUP_ID,
        "♻️ <b>Modo recuperação ativo</b>"
    )


print("🤖 Bot Telegram iniciado")
bot.infinity_polling(skip_pending=True)
