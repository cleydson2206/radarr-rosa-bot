from playwright.sync_api import sync_playwright
from datetime import datetime
import pytz
import time
import requests

# ================== CONFIGURAÇÕES ==================

BOT_TOKEN = "8316037466:AAFin8vm0gZ-3GtysKHIg2kSSNp2znHPAUE"
CHAT_ID = -1003690946411  # ID do grupo

URL_TIP_MINER = "https://tipminer.com"
TZ_BR = pytz.timezone("America/Sao_Paulo")

# Controle para não duplicar sinais
historico_rosas = []
ULTIMO_ENVIO = None

# ================== FUNÇÕES ==================

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
        print(f"📤 Enviado para o bot: {texto}")
        ULTIMO_ENVIO = hora_rosa
    except Exception as e:
        print("❌ Erro ao enviar para o bot:", e)

# ================== COLETOR ==================

def iniciar_coleta():
    print("🟣 Coletor Tip Miner iniciado (modo headless)")
    print("🕒 Horário Brasília:", agora_br())

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(URL_TIP_MINER, timeout=60000)
        time.sleep(10)  # tempo para carregar tabela

        while True:
            try:
                # 🔴 AJUSTE AQUI SE O TIP MINER MUDAR O HTML
                elementos = page.query_selector_all("div.cell")

                for el in elementos:
                    texto = el.inner_text().strip()

                    if "10" in texto and "x" in texto.lower():
                        horario = agora_br()

                        if horario not in historico_rosas:
                            historico_rosas.append(horario)

                            if len(historico_rosas) >= 2:
                                penultima_rosa = historico_rosas[-2]
                                print("🌹 Rosa detectada:", penultima_rosa)
                                enviar_para_bot(penultima_rosa)

                time.sleep(30)

            except Exception as e:
                print("⚠️ Erro no loop, tentando novamente:", e)
                time.sleep(15)

# ================== START ==================

if __name__ == "__main__":
    iniciar_coleta()
