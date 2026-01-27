import telebot
from datetime import datetime
import pytz
import os

# ============== CONFIG ==============
TOKEN = os.getenv("8316037466:AAFin8vm0gZ-3GtysKHIg2kSSNp2znHPAUE")
GROUP_ID = int(os.getenv("-1003690946411"))

TZ_BR = pytz.timezone("America/Sao_Paulo")
bot = telebot.TeleBot(TOKEN)

# ============== FUNÇÕES ==============
def agora():
    return datetime.now(TZ_BR).strftime("%H:%M")

@bot.message_handler(commands=["rosa"])
def receber_rosa(msg):
    hora = msg.text.replace("/rosa", "").strip()

    mensagem = f"""
🌹 ROSA 10x+ DETECTADO

⏰ Horário da rosa: {hora}

⚠️ ENTRAR:
• 1 minuto antes
• ou 1 minuto depois

🔥 ZONAS QUENTES:
• {hora}

🔄 Leitura 100% automática do Tip Miner
⏱️ Horário de Brasília
"""

    bot.send_message(GROUP_ID, mensagem)

print("🤖 Bot iniciado")
bot.infinity_polling(skip_pending=True)
