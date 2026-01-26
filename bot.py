import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta
import pytz

# ================= CONFIGURAÇÕES =================
TOKEN = "8316037466:AAFin8vm0gZ-3GtysKHIg2kSSNp2znHPAUE"

GROUP_ID = -1003690946411

LINK_APOSTA_MAX = "https://apostamax.com"
LINK_TIP_MINER = "https://tipminer.com"

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# Timezone Brasil
TZ_BR = pytz.timezone("America/Sao_Paulo")

# ================= FUNÇÕES =================
def agora_brasilia():
    return datetime.now(TZ_BR)

def somar_minutos(hora_base, minutos):
    h, m = map(int, hora_base.split(":"))
    base = agora_brasilia().replace(hour=h, minute=m, second=0)
    novo = base + timedelta(minutes=minutos)
    return novo.strftime("%H:%M")

def calcular_zonas(hora_rosa):
    return [
        somar_minutos(hora_rosa, 7),
        somar_minutos(hora_rosa, 10),
        somar_minutos(hora_rosa, 26)
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

# ================= MENSAGENS =================
def enviar_sinal_grupo(hora_rosa):
    zonas = calcular_zonas(hora_rosa)
    horario_analise = agora_brasilia().strftime("%H:%M")

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
        f"🧠 Análise gerada: {horario_analise}\n"
        "🇧🇷 Horário de Brasília"
    )

    bot.send_message(
        chat_id=GROUP_ID,
        text=mensagem,
        reply_markup=teclado(hora_rosa)
    )

def enviar_recuperacao():
    horario = agora_brasilia().strftime("%H:%M")

    mensagem = (
        "♻️ <b>PADRÃO DE RECUPERAÇÃO IDENTIFICADO</b>\n\n"
        "📉 O Aviator passou por sequência de baixas\n"
        "📈 Histórico indica <b>fase de recuperação</b>\n\n"
        "⚠️ Evite entradas antecipadas\n"
        "🎯 Priorize entradas estratégicas\n"
        "🚀 Busque alvos controlados (2.00x+)\n\n"
        f"🕒 Monitoramento ativo às {horario}\n"
        "🇧🇷 Horário de Brasília"
    )

    bot.send_message(
        chat_id=GROUP_ID,
        text=mensagem,
        reply_markup=teclado(horario)
    )

# ================= COMANDOS =================
@bot.message_handler(commands=["start"])
def start(msg):
    bot.reply_to(
        msg,
        "🤖 <b>Radar Rosa Bot ATIVO</b>\n\n"
        "Comandos disponíveis:\n\n"
        "🌹 <code>/rosa 1852</code>\n"
        "♻️ <code>/recuperacao</code>\n\n"
        "Formato do horário: HHMM\n"
        "🇧🇷 Horário de Brasília"
    )

@bot.message_handler(commands=["rosa"])
def rosa_manual(msg):
    try:
        hora = msg.text.split()[1]
        if len(hora) != 4:
            raise ValueError

        hora_formatada = f"{hora[:2]}:{hora[2:]}"
        enviar_sinal_grupo(hora_formatada)

        bot.reply_to(msg, "✅ Sinal enviado no grupo.")
    except:
        bot.reply_to(msg, "❌ Use corretamente:\n/rosa 1852")

@bot.message_handler(commands=["recuperacao"])
def recuperacao(msg):
    enviar_recuperacao()
    bot.reply_to(msg, "♻️ Aviso de recuperação enviado no grupo.")

# ================= START =================
print("🤖 Radar Rosa Bot ONLINE - Horário Brasília")
bot.infinity_polling()
