import os
import time
import requests
from datetime import datetime
import pytz

# ===== CONFIG VIA VARIÁVEIS DE AMBIENTE =====
BOT_TOKEN = os.getenv("8316037466:AAFin8vm0gZ-3GtySKHIg2kSSNp2znHPAUE")
GROUP_ID = os.getenv("-1003690946411")

if not BOT_TOKEN or not GROUP_ID:
    raise Exception("BOT_TOKEN ou GROUP_ID não configurados no Railway")

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
TZ_BR = pytz.timezone("America/Sao_Paulo")

def agora_br():
    return datetime.now(TZ_BR).strftime("%H:%M")

def enviar_mensagem(texto):
    payload = {
        "chat_id": GROUP_ID,
        "text": texto,
        "parse_mode": "HTML"
    }
    requests.post(TELEGRAM_API, json=payload, timeout=10)

print("📡 Collector iniciado e rodando...")

# ===== LOOP PRINCIPAL =====
while True:
    try:
        # 🔴 AQUI entra sua lógica real depois
        # Por enquanto é teste de funcionamento

        horario = agora_br()

        mensagem = (
            "🚨 <b>RADAR ROSA</b>\n\n"
            f"⏰ Horário: <b>{horario}</b>\n"
            "🎯 Sinal detectado pelo collector\n\n"
            "🧠 Aguardando próxima leitura..."
        )

        enviar_mensagem(mensagem)

        print(f"Mensagem enviada às {horario}")

        time.sleep(300)  # 5 minutos (ajuste depois)

    except Exception as e:
        print("Erro no collector:", e)
        time.sleep(10)
