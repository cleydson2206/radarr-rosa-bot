import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta
import pytz

# ================= CONFIGURAÇÕES =================

TOKEN = "8316037466:AAFin8vm0gZ-3GtysKHIg2kSSNp2znHPAUE"

GROUP_ID = -1003690946411

LINK_APOSTA_MAX = "https://apostamax.bet.br/games/spribe/aviator"
LINK_TIP_MINER = "https://tipminer.com"

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

TZ_BR = pytz.timezone("America/Sao_Paulo")

# ================= FUNÇÕES =================

def agora_brasilia():
    return datetime.now(TZ_BR)

def formatar_hora(dt):
    return dt.strftime("%H:%M")

def somar_minutos(hora_base, minutos):
    h, m = map(int, hora_base.split(":"))
    base = agora_brasilia().replace(hour=h, minute=m, second=0)
    novo = base + timedelta(minutes=minutos)
    return formatar_hora(novo)

def calcular_zonas(hora_rosa):
    return [
        somar_minutos(hora_rosa, 7),
        somar_minutos(hora_rosa, 10),
        somar_minutos(hora_rosa, 26),
    ]

def teclado(hora):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("🚀 Abrir Aposta Max", url=LINK_APOSTA_MAX),
        InlineKeyboardButton(
            "📊 Abrir Tip Miner",
            url=f"{LINK_TIP_MINER}?hora={hora}"
        )
    )
    return markup

def enviar_sinal_grupo(hora_rosa):
    zonas = calcular_zonas(hora_rosa)
    horario_analise = formatar_hora(agora_brasilia())

    mensagem = (
        "🌹 <b>ROSA 10x+ DETECTADO</b>\n\n"
        f"⏰ <b>Horário da rosa:</b> {hora_rosa}\n\n"
        "⚠️ <b>ENTRAR 1 MINUTO ANTES</b>\n"
        "⚠️ <b>OU 1 MINUTO DEPOIS</b>\n\n"
        "🎯 <b>ZONAS QUENTES:</b>\n"
        f"🎯 {zonas[0]}\n"
        f"🎯 {zonas[1]}\n"
        f"🎯 {zonas[2]}\n\n"
        "🚀 <b>ENTRAR NO MINUTO</b>\n\n"
        f"🧠 <b>Análise gerada:</b> {horario_analise}\n"
        "🇧🇷 Horário de Brasília"
    )

    bot.send_message(
        chat_id=GROUP_ID,
        text=mensagem,
        reply_markup=teclado(hora_rosa)
    )

# ================= COMANDOS =================

@bot.message_handler(commands=["start"])
def start(msg):
    bot.reply_to(
        msg,
        "🤖 <b>Radar Rosa Bot ATIVO</b>\n\n"
        "Use o comando:\n"
        "<code>/rosa 1852</code>\n\n"
        "Formato: HHMM\n"
        "📡 Leitura automática do Tip Miner ativa",
    )

@bot.message_handler(commands=["rosa"])
def rosa_manual(msg):
    try:
        hora = msg.text.split()[1]
        if len(hora) != 4 or not hora.isdigit():
            raise ValueError

        hora_formatada = f"{hora[:2]}:{hora[2:]}"
        enviar_sinal_grupo(hora_formatada)

        bot.reply_to(msg, "✅ Sinal enviado no grupo.")
    except:
        bot.reply_to(
            msg,
            "❌ Use corretamente:\n<code>/rosa 1852</code>"
        )

@bot.message_handler(commands=["teste"])
def teste(msg):
    agora = formatar_hora(agora_brasilia())
    enviar_sinal_grupo(agora)
    bot.reply_to(msg, "🧪 Teste enviado no grupo.")

# ================= START =================

print("🤖 Radar Rosa Bot ONLINE — Horário Brasília")
bot.infinity_polling(skip_pending=True)
