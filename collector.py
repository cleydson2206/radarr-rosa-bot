import os
import time
import requests
from datetime import datetime
import pytz
from playwright.sync_api import sync_playwright

BOT_TOKEN = os.getenv("8316037466:AAFin8vm0gZ-3GtysKHIg2kSSNp2znHPAUE")
GROUP_ID = int(os.getenv("-1003690946411"))

TZ_BR = pytz.timezone("America/Sao_Paulo")
TIPMINER_URL = "https://tipminer.com"

ULTIMO_ENVIO = None

def agora_br():
    return datetime.now(TZ_BR).strftime("%H:%M")

def enviar_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": GROUP_ID,
        "text": msg,
        "parse_mode": "HTML"
    }
    requests.post(url, data=payload, timeout=10)

def detectar_rosa(valor):
    return valor >= 10.0  # ajuste se quiser

print("🟣 Worker iniciado")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(TIPMINER_URL, timeout=60000)

    while True:
        try:
            page.wait_for_selector("div", timeout=10000)

            textos = page.eval_on_selector_all(
                "div",
                "els => els.map(e => e.innerText)"
            )

            for t in textos:
                if "x" in t:
                    try:
                        valor = float(t.replace("x", "").replace(",", "."))
                        if detectar_rosa(valor):
                            hora = agora_br()
                            global ULTIMO_ENVIO
                            if hora != ULTIMO_ENVIO:
                                enviar_telegram(
                                    f"🌹 <b>ROSA DETECTADA</b>\n"
                                    f"🎯 Multiplicador: <b>{valor}x</b>\n"
                                    f"⏰ Entrada: <b>{hora}</b>"
                                )
                                ULTIMO_ENVIO = hora
            time.sleep(5)

        except Exception as e:
            print("Erro:", e)
            time.sleep(5)
