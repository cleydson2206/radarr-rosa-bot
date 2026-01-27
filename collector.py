from playwright.sync_api import sync_playwright
from datetime import datetime
import pytz
import time
import requests

# ================= CONFIG =================
BOT_TOKEN = "8316037466:AAFin8vm0gZ-3GtysKHIg2kSSNp2znHPAUE"
CHAT_ID = -1003690946411  # MESMO ID do grupo
URL_TIP_MINER = "https://tipminer.com"
TZ_BR = pytz.timezone("America/Sao_Paulo")

ULTIMO_ENVIO = None
# =========================================

def hora_br():
    return datetime.now(TZ_BR).strftime("%H:%M")

def enviar_para_telegram(hora_rosa):
    global ULTIMO_ENVIO

    if hora_rosa == ULTIMO_ENVIO:
        return

    texto = f"🌹 <b>ROSA DETECTADA</b>\n⏰ <b>{hora_rosa.replace(':','')}</b>"

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": texto,
        "parse_mode": "HTML"
    }

    try:
        requests.post(url, data=payload, timeout=10)
        print(f"✅ Rosa enviada: {hora_rosa}")
        ULTIMO_ENVIO = hora_rosa
    except Exception as e:
        print("❌ Erro ao enviar:", e)

def monitorar():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(URL_TIP_MINER, timeout=60000)

        print("👀 Monitorando TipMiner...")

        while True:
            try:
                # ⚠️ EXEMPLO (AJUSTE SELETOR SE NECESSÁRIO)
                rosa = page.locator(".pink").first

                if rosa:
                    hora = hora_br()
                    enviar_para_telegram(hora)

                time.sleep(15)

            except Exception as e:
                print("Erro:", e)
                time.sleep(10)

if __name__ == "__main__":
    monitorar()
