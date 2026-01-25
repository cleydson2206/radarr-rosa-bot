import telebot
import time
import threading
import requests
from datetime import datetime, timedelta
import pytz

# =========================
# CONFIGURAÇÕES
# =========================
TOKEN = "8316037466:AAFin8vm0gZ-3GtysKHIg2kSSNp2znHPAUE"
CHAT_ID = -1001234567890  # 👈 TROQUE PELO ID DO SEU GRUPO
TIMEZONE = pytz.timezone("America/Sao_Paulo")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# =========================
# FUNÇÕES AUXILIARES
# =========================
def hora_br():
    return datetime.now(TIMEZONE)

def formatar_hora(dt):
    return dt.strftime("%H:%M")

def calcular_zonas(hora_base):
    base = datetime.strptime(hora_base, "%H:%M")
    zonas = [
        base + timedelta(minutes=7),
        base + timedelta(minutes=10),
        base + timedelta(minutes=26),
    ]
    return [z.strftime("%H:%M") for z in zonas]

# =========================
# COMANDO /start
# =========================
@bot.message_handler(commands=["start"])
def start(msg):
    bot.send_message(
        msg.chat.id,
        "🎯 <b>Radar Rosa Bot ATIVO</b>\n\n"
        "Use:\n"
        "<code>/rosa HHMM</code>\n\n"
        "Exemplo:\n"
        "<code>/rosa 2152</code>"
    )

# =========================
# COMANDO MANUAL /rosa
# =========================
@bot.message_handler(commands=["rosa"])
def rosa_manual(msg):
    try:
        hora = msg.text.split()[1]
        hora = f"{hora[:2]}:{hora[2:]}"
        zonas = calcular_zonas(hora)

        texto = (
            "🌹 <b>RADAR ROSA — ZONAS QUENTES</b>\n\n"
            f"⏰ Rosa base: <b>{hora}</b>\n\n"
            "🎯 <b>Alvos calculados:</b>\n"
            f"• {zonas[0]}\n"
            f"• {zonas[1]}\n"
            f"• {zonas[2]}\n\n"
            "🕒 Horário de Brasília"
        )

        bot.send_message(CHAT_ID, texto)

    except:
        bot.reply_to(msg, "❌ Use corretamente: /rosa HHMM\nEx: /rosa 2152")

# =========================
# 🔥 INTEGRAÇÃO TIP MINER
# =========================
def verificar_tip_miner():
    """
    AQUI você conecta a API / Webhook / Scraper do Tip Miner
    Sempre que detectar um ROSA 10x+, chame enviar_sinal()
    """

    while True:
        try:
            # 🔁 EXEMPLO (SIMULADO)
            # Substitua por API real do Tip Miner
            resposta = requests.get("https://exemplo-tipminer-api.com/rosa")

            if resposta.status_code == 200:
                dados = resposta.json()

                if dados.get("multiplicador", 0) >= 10:
                    hora_rosa = dados["hora"]  # Ex: "21:52"
                    enviar_sinal(hora_rosa)

        except:
            pass

        time.sleep(30)  # checa a cada 30s

# =========================
# ENVIO AUTOMÁTICO NO GRUPO
# =========================
def enviar_sinal(hora_rosa):
    zonas = calcular_zonas(hora_rosa)

    texto = (
        "🚨 <b>ROSA 10x+ DETECTADO (TIP MINER)</b>\n\n"
        f"🌹 Rosa: <b>{hora_rosa}</b>\n\n"
        "🔥 <b>ZONAS QUENTES:</b>\n"
        f"🎯 {zonas[0]}\n"
        f"🎯 {zonas[1]}\n"
        f"🎯 {zonas[2]}\n\n"
        "⏱️ Monitoramento automático"
    )

    bot.send_message(CHAT_ID, texto)

# =========================
# THREAD DO TIP MINER
# =========================
threading.Thread(target=verificar_tip_miner, daemon=True).start()

# =========================
# LOOP PRINCIPAL
# =========================
print("🤖 Radar Rosa Bot ONLINE")
bot.infinity_polling()
