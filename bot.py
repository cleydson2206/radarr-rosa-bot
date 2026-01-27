import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta
import pytz

# ================= CONFIG =================
TOKEN = "8316037466:AAFin8vm0gZ-3GtysKHIg2kSSNp2znHPAUE"
GROUP_ID = -1003690946411

LINK_APOSTA_MAX = "https://apostamax.com"
LINK_TIP_MINER = "https://tipminer.com"

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
TZ_BR = pytz.timezone("America/Sao_Paulo")

# ================= FUNÇÕES =================
def agora_br():
    return datetime.now(TZ_BR)

def somar(hora, minutos):
    h, m = map(int, hora.split(":"))
    base = agora_br().replace(hour=h, minute=m, second=0)
    return (base + timedelta(minutes=minutos)).strftime("%H:%M")

def zonas_quentes(hora):
    return [somar(hora, 7), somar(hora, 10), somar(hora, 26)]

def teclado(hora):
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("🚀 Abrir Aposta Max", url=LINK_APOSTA_MAX),
        InlineKeyboardButton("📊 Abrir Tip Miner", url=f"{LINK_TIP_MINER}?hora={hora}")
    )
    return kb

def enviar_sinal(hora):
    zonas = zonas_quentes(hora)
    msg = (
        "🌹 <b>ROSA 10x+ DETECTADO</b>\n\n"
        f"⏰ <b>Horário da rosa:</b> {hora}\n"
        "⚠️ <b>Entrar 1 min antes ou 1 min depois</b>\n\n"
        "🎯 <b>ZONAS QUENTES:</b>\n"
        f"🎯 {zonas[0]}\n"
        f"🎯 {zonas[1]}\n"
        f"🎯 {zonas[2]}\n\n"
        "🚀 <b>ENTRAR NO MINUTO</b>\n\n"
        f"🧠 Análise gerada: {agora_br().strftime('%H:%M')}\n"
        "🇧🇷 Horário de Brasília"
    )

    bot.send_message(GROUP_ID, msg, reply_markup=teclado(hora))

# ================= COMANDOS =================
@bot.message_handler(commands=["start"])
def start(msg):
    bot.reply_to(
        msg,
        "🤖 <b>Radar Rosa Bot ATIVO</b>\n\n"
        "🌹 /rosa HHMM\n"
        "♻️ /recuperacao\n\n"
        "🇧🇷 Horário de Brasília"
    )

@bot.message_handler(commands=["rosa"])
def rosa(msg):
    try:
        hora = msg.text.split()[1]
        hora = f"{hora[:2]}:{hora[2:]}"
        enviar_sinal(hora)
        bot.reply_to(msg, "✅ Sinal enviado no grupo.")
    except:
        bot.reply_to(msg, "❌ Use: /rosa 1852")

@bot.message_handler(commands=["recuperacao"])
def recuperacao(msg):
    bot.send_message(
        GROUP_ID,
        "♻️ <b>AVIATOR EM PADRÃO DE RECUPERAÇÃO</b>\n\n"
        "⚠️ Evite entradas forçadas\n"
        "🧠 Radar analisando o mercado\n\n"
        "🇧🇷 Horário de Brasília"
    )

print("🤖 BOT ONLINE")
bot.infinity_polling()
