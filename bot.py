import os
import telebot
from datetime import datetime
import pytz
import time

# ===============================
# VARIÁVEIS DE AMBIENTE (RAILWAY)
# ===============================
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = int(os.getenv("GROUP_ID"))

if not BOT_TOKEN or not GROUP_ID:
    raise Exception("❌ BOT_TOKEN ou GROUP_ID não configurados no Railway")

# ===============================
# BOT
# ===============================
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")
TZ_BR = pytz.timezone("America/Sao_Paulo")

def agora_br():
    return datetime.now(TZ_BR).strftime("%H:%M")

# ===============================
# COMANDOS
# ===============================

@bot.message_handler(commands=["start"])
def start(msg):
    bot.send_message(
        msg.chat.id,
        "🤖 <b>Radar Rosa ATIVO</b>\n\n"
        "📌 Comandos disponíveis:\n"
        "🌹 <b>/rosa HHMM</b>\n"
        "♻️ <b>/recuperacao</b>\n"
        "⏰ Horário de Brasília"
    )

@bot.message_handler(commands=["rosa"])
def rosa(msg):
    try:
        hora = msg.text.split(" ")[1]
        bot.send_message(
            GROUP_ID,
            f"🌹 <b>ROSA CONFIRMADA</b>\n"
            f"⏰ Entrada: <b>{hora}</b>"
        )
    except:
        bot.reply_to(msg, "❌ Use: <b>/rosa HHMM</b>")

@bot.message_handler(commands=["recuperacao"])
def recuperacao(msg):
    bot.send_message(
        GROUP_ID,
        "♻️ <b>Modo recuperação ativado</b>"
    )

# ===============================
# LOOP PRINCIPAL (NÃO REMOVE)
# ===============================

print("🤖 Bot Telegram iniciado com sucesso")

while True:
    try:
        bot.infinity_polling(skip_pending=True, timeout=60)
    except Exception as e:
        print("⚠️ Erro no bot:", e)
        time.sleep(5)
