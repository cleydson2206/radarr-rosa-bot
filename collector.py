from datetime import datetime
import pytz
import time
import requests

# ================= CONFIG =================
BOT_TOKEN = "8316037466:AAFin8vm0gZ-3GtysKHIg2kSSNp2znHPAUE"
GROUP_ID = -1003690946411
TZ_BR = pytz.timezone("America/Sao_Paulo")

ULTIMO_ENVIO = None

# ================= FUNÇÕES =================
def agora_br():
    return datetime.now(TZ_BR).strftime("%H:%M")

def enviar_para_bot(hora_rosa):
    global ULTIMO_ENVIO

    if hora_rosa == ULTIMO_ENVIO:
        return

    texto = f"/rosa {hora_rosa.replace(':','')}"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": GROUP_ID,
        "text": texto
    }

    try:
        requests.post(url, data=payload, timeout=10)
        print(f"✅ Disparo automático: {texto}")
        ULTIMO_ENVIO = hora_rosa
    except Exception as e:
        print("Erro ao enviar:", e)

# ================= LOOP =================
print("⚙️ WORKER ATIVO")

while True:
    # AQUI entra sua lógica real de leitura do Tip Miner
    # Exemplo simulado:
    hora_detectada = agora_br()

    enviar_para_bot(hora_detectada)

    time.sleep(60)
