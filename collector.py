from playwright.sync_api import sync_playwright
from datetime import datetime
import pytz
import time
import requests

# ================= CONFIGURAÇÕES =================
BOT_TOKEN = "8316037466:AAFin8vm0gZ-3GtysKHIg2kSSNp2znHPAUE"
CHAT_ID = -1003690946411  # ID do grupo

URL_TIP_MINER = "https://tipminer.com"
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
        "chat_id": CHAT_ID,
        "text": texto
    }

    try:
        requests.post(url, data=payload, timeout=10)
        print(f"✅ Enviado: {texto}")
        ULTIMO_ENVIO = hora_rosa
    except Exception as e:
        print("❌ Erro ao enviar:", e)

# ================= COLETOR =================
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(URL_TIP_MINER)

    print("🚀 Coletor iniciado")

    while True:
        try:
            # ⬇️ AJUSTE O SELETOR conforme o Tip Miner
            rosa = page.query_selector(".rosa, .pink, .highlight")

            if rosa:
                hora = agora_br()
                enviar_para_bot(hora)

            time.sleep(20)

        except Exception as e:
            print("Erro no loop:", e)
            time.sleep(30)
