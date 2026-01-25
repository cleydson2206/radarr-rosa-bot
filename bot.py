import telebot
from datetime import datetime
import pytz

# ===============================
# TOKEN DO BOT (JÁ CONFIGURADO)
# ===============================
TOKEN = "8316037466:AAFin8vm0gZ-3GtysKHIg2kSSNp2znHPAUE"
bot = telebot.TeleBot(TOKEN)

TZ_BR = pytz.timezone("America/Sao_Paulo")

# ===============================
# FUNÇÕES AUXILIARES
# ===============================
def f(n):
    return f"{n:02d}"

def normalizar(h, m):
    while m >= 60:
        m -= 60
        h += 1
    while m < 0:
        m += 60
        h -= 1
    if h >= 24:
        h %= 24
    if h < 0:
        h += 24
    return h, m

# ===============================
# COMANDO /start
# ===============================
@bot.message_handler(commands=["start"])
def start(msg):
    bot.reply_to(
        msg,
        "🎯 *Radar Rosa Bot ATIVO*\n\n"
        "Use o comando:\n"
        "`/rosa 2152`\n\n"
        "Formato: HHMM\n"
        "Exemplo: `/rosa 2106`",
        parse_mode="Markdown"
    )

# ===============================
# COMANDO /rosa
# ===============================
@bot.message_handler(commands=["rosa"])
def rosa(msg):
    try:
        texto = msg.text.split()
        if len(texto) != 2 or len(texto[1]) != 4:
            raise ValueError

        hora = int(texto[1][:2])
        minuto = int(texto[1][2:])

        dezena = minuto // 10
        unidade = minuto % 10

        n1 = dezena + unidade
        n2 = dezena * unidade
        n3 = minuto // 2

        h1, m1 = normalizar(hora, minuto + n1)
        h2, m2 = normalizar(hora, minuto + n2)
        h3, m3 = normalizar(hora, minuto + n3)

        resposta = (
            "🌹 *RADAR ROSA – ZONAS QUENTES*\n\n"
            f"⏰ Rosa base: `{f(hora)}:{f(minuto)}`\n\n"
            "🎯 *Alvos calculados:*\n"
            f"🎯 `{f(h1)}:{f(m1)}`\n"
            f"🎯 `{f(h2)}:{f(m2)}`\n"
            f"🎯 `{f(h3)}:{f(m3)}`\n\n"
            "_Horário padrão de Brasília_"
        )

        bot.reply_to(msg, resposta, parse_mode="Markdown")

    except:
        bot.reply_to(
            msg,
            "❌ Formato inválido.\n\n"
            "Use assim:\n"
            "`/rosa 2152`",
            parse_mode="Markdown"
        )

# ===============================
# LOOP PRINCIPAL
# ===============================
print("🤖 Radar Rosa Bot iniciado...")
bot.infinity_polling()
