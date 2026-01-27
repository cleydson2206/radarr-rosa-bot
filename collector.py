from playwright.sync_api import sync_playwright
from datetime import datetime
import pytz
import time
import requests

# ================= CONFIG =================
BOT_TOKEN = "8316037466:AAFin8vm0gZ-3GtysKHIg2kSSNp2znHPAUE"
BOT_CHAT_ID = -1003690946411

TIP_MINER_URL = "https://tipminer.com"

TZ_BR = pytz.timezone("America/Sao_Paulo")

# Guarda horários das rosas detectadas
historico_rosas = []

# Evita disparos duplicados
ultimo_enviado = None

# ================= FUNÇÕES =================
def agora_brasilia():
    return datetime.now(TZ_BR).strftime("%H:%M")

def enviar_para_bot(hora_rosa):
    global ultimo_enviado

    if hora_rosa == ultimo_enviado:
        return

    ultimo_enviado = hora_rosa

    comando = f"/rosa {hora_rosa.replace(':','')}"
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": BOT_CHAT_ID,
            "text": comando
        }
    )

def extrair_numero(texto):
    try:
        return float(texto.replace("x", "").replace(",", "."))
    except:
        return 0.0

# ================= START =================
print("🤖 Collector Tip Miner ONLINE")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(TIP_MINER_URL, timeout=60000)

    while True:
        try:
            # 🔴 AJUSTE AQUI SE O SITE MUDAR 🔴
            # Esse seletor deve apontar para o ÚLTIMO multiplicador
            elementos = page.query_selector_all("span")

            if not elementos:
                time.sleep(5)
                continue

            texto = elementos[0].inner_text()
            valor = extrair_numero(texto)

            # ROSA 10x+
            if valor >= 10:
                hora = agora_brasilia()

                if hora not in historico_rosas:
                    historico_rosas.append(hora)
                    print(f"🌹 Rosa detectada às {hora}")

                    # Usa PENÚLTIMA ROSA
                    if len(historico_rosas) >= 2:
                        penultima = historico_rosas[-2]
                        print(f"🎯 Usando penúltima rosa: {penultima}")
                        enviar_para_bot(penultima)

            time.sleep(4)

        except Exception as e:
            print("Erro no collector:", e)
            time.sleep(10)
