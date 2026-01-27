import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
import pytz

# ================= CONFIG =================
TOKEN = "8316037466:AAFin8vm0gZ-3GtysKHIg2kSSNp2znHPAUE"
GROUP_ID = -1003690946411  # ID do grupo (NÃO APAGAR)
TZ_BR = pytz.timezone("America/Sao_Paulo")

LINK_APOSTA_MAX = "https://apostamax.com"
LINK_TIP_MINER = "https://tipminer.com"

# ==========================================
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

def agora_br():
    return datetime.now(TZ_BR).strftime("%H:%M")

# ================= COMANDOS =================
@bot.message_handler(commands=["start"])
def start(msg):
    texto = (
        "🤖 <b>Radar Rosa Bot ATIVO</b>\n\n"
        "Comandos disponíveis:\n"
        "🌹 <b>/rosa HHMM</b>\n"
        "♻️ <b>/recuperacao</b>\n\n"
        "🕒 Horário de Brasília"
    )
    bot.send_message(msg.chat.id, texto)

@bot.message_handler(commands=["rosa"])
def rosa(msg):
    try:
        hora = msg.text.split(" ")[1]
        texto = (
            f"🌹 <b>ROSA CONFIRMADA</b>\n\n"
            f"⏰ Horário: <b>{hora}</b>\n"
            f"🎯 Entrada curta\n\n"
            f"🔗 TipMiner: {LINK_TIP_MINER}\n"
            f"💰 Aposte: {LINK_APOSTA_MAX}"
        )
        bot.send_message(GROUP_ID, texto)
    except:
        bot.reply_to(msg, "❌ Use: /rosa HHMM")

@bot.message_handler(commands=["recuperacao"])
def recuperacao(msg):
    texto = (
        "♻️ <b>RECUPERAÇÃO ATIVA</b>\n\n"
        "📊 Gestão aplicada\n"
        "⏳ Aguardando próxima oportunidade"
    )
    bot.send_message(GROUP_ID, texto)

# ================= START BOT =================
print("🤖 BOT ONLINE")
bot.infinity_polling(skip_pending=True)
