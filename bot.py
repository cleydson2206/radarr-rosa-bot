import telebot
from datetime import datetime, timedelta
import pytz

# =========================
# CONFIGURAÇÕES
# =========================
TOKEN = "8316037466:AAFin8vm0gZ-3GtysKHIg2kSSNp2znHPAUE"
CHAT_ID = -1001234567890  # 👈 TROQUE PELO ID DO SEU GRUPO
TZ = pytz.timezone("America/Sao_Paulo")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# =========================
# FUNÇÕES
# =========================
def calcular_zonas(hora_str):
    base = datetime.strptime(hora_str, "%H:%M")
    zonas = [
        base + timedelta(minutes=7),
        base + timedelta(minutes=10),
        base + timedelta(minutes=26),
    ]
    return [z.strftime("%H:%M") for z in zonas]

# =========================
# COMANDO PARA ROSA
# =========================
@bot.message_handler(func=lambda m: True)
def receber_hora(msg):
    texto = msg.text.strip()

    # aceita apenas formato HH:MM
    if len(texto) == 5 and texto[2] == ":":
        try:
            datetime.strptime(texto, "%H:%M")
        except:
            return

        zonas = calcular_zonas(texto)

        mensagem = (
            "🌹 <b>ROSA 10x+ DETECTADO</b>\n\n"
            f"⏰ Horário base: <b>{texto}</b>\n\n"
            "🎯 <b>ZONAS QUENTES:</b>\n"
            f"🎯 {zonas[0]}\n"
            f"🎯 {zonas[1]}\n"
            f"🎯 {zonas[2]}\n\n"
            "⏱️ Horário de Brasília"
        )

        bot.send_message(CHAT_ID, mensagem)

# =========================
# LOOP
# =========================
print("🤖 Radar Rosa Bot pronto para receber horários")
bot.infinity_polling()
