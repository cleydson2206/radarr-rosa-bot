import time
import requests
from datetime import datetime, timedelta
import pytz

# ================== CONFIG FIXA ==================
BOT_TOKEN = "8316037466:AAFin8vm0gZ-3GtySKHIg2kSSNp2znHPAUE"
GROUP_ID = -1003690946411

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
TZ_BR = pytz.timezone("America/Sao_Paulo")

# ================== FUNÇÕES ==================
def agora_brasilia():
    return datetime.now(TZ_BR)

def enviar_mensagem(texto):
    payload = {
        "chat_id": GROUP_ID,
        "text": texto,
        "parse_mode": "HTML"
    }
    r = requests.post(TELEGRAM_API, json=payload, timeout=15)
    print("Resposta Telegram:", r.text)

def format_hm(dt):
    return dt.strftime("%H:%M")

def normalizar(h, m):
    while m >= 60:
        m -= 60
        h += 1
    if h >= 24:
        h %= 24
    return h, m

# ================== LÓGICA DE TESTE ==================
def gerar_sinal_teste():
    agora = agora_brasilia()
    hora_rosa = agora.strftime("%H:%M")

    h = agora.hour
    m = agora.minute

    # Zonas quentes (exemplo estável)
    z1_h, z1_m = normalizar(h, m + 7)
    z2_h, z2_m = normalizar(h, m + 10)
    z3_h, z3_m = normalizar(h, m + 26)

    mensagem = (
        "🌹 <b>ROSA 10x+ DETECTADO</b>\n\n"
        f"⏰ <b>Horário da rosa:</b> {hora_rosa}\n\n"
        "🎯 <b>ZONAS QUENTES:</b>\n"
        f"🎯 {z1_h:02d}:{z1_m:02d}\n"
        f"🎯 {z2_h:02d}:{z2_m:02d}\n"
        f"🎯 {z3_h:02d}:{z3_m:02d}\n\n"
        "➡️ <b>ENTRAR 1 MINUTO ANTES e 1 MINUTO DEPOIS</b>\n\n"
        "🇧🇷 Horário de Brasília"
    )

    enviar_mensagem(mensagem)

# ================== START ==================
print("📡 Collector ONLINE — Horário Brasília")

# Loop contínuo (envia a cada 5 minutos para teste)
while True:
    try:
        gerar_sinal_teste()
        time.sleep(300)  # 5 minutos
    except Exception as e:
        print("Erro no collector:", e)
        time.sleep(10)
