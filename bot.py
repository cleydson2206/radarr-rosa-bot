import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta

# ================= CONFIGURAÇÕES =================
TOKEN = "8316037466:AAFin8vm0gZ-3GtysKHIg2kSSNp2znHPAUE"

# ID DO GRUPO (CORRETO -100...)
GROUP_ID = -1003690946411

LINK_APOSTA_MAX = "https://apostamax.com"
LINK_TIP_MINER = "https://tipminer.com"

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# ================= FUNÇÕES =================
def somar_minutos(hora_base, minutos):
    h, m = map(int, hora_base.split(":"))
    novo = datetime.now().replace(hour=h, minute=m) + timedelta(minutes=minutos)
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

def enviar_sinal_grupo(hora_rosa):
    zonas = calcular_zonas(hora_rosa)
    agora = datetime.now().strftime("%H:%M")

    mensagem = (
        "🌹 <b>ROSA 10x+ DETECTADO</b>\n\n"
        f"⏰ <b>Horário da rosa:</b> {hora_rosa}\n"
        "ENTRAR NO MINUTO"
        
        "1 MINUTO ANTES E 1 MINUTOS DEPOIS"
        "🎯 <b>ZONAS QUENTES:</b>\n"
        f"🎯 {zonas[0]}\n"
        f"🎯 {zonas[1]}\n"
        f"🎯 {zonas[2]}\n\n"
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
        "Formato: HHMM",
    )

@bot.message_handler(commands=["rosa"])
def rosa_manual(msg):
    try:
        hora = msg.text.split()[1]
        if len(hora) != 4:
            raise ValueError
        hora_formatada = f"{hora[:2]}:{hora[2:]}"
        enviar_sinal_grupo(hora_formatada)
        bot.reply_to(msg, "✅ Sinal enviado no grupo com sucesso.")
    except:
        bot.reply_to(msg, "❌ Use corretamente:\n/rosa 1852")

@bot.message_handler(commands=["teste"])
def teste(msg):
    agora = datetime.now().strftime("%H:%M")
    enviar_sinal_grupo(agora)
    bot.reply_to(msg, "🧪 Teste enviado no grupo.")

# ================= START BOT =================
print("🤖 Radar Rosa Bot ONLINE")
bot.infinity_polling()
