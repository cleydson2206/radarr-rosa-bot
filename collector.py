from playwright.sync_api import sync_playwright
from datetime import datetime
import pytz
import time
import requests

# ================= CONFIGURAÇÕES =================

BOT_TOKEN = "8316037466:AAFin8vm0gZ-3GtysKHIg2kSSNp2znHPAUE"
CHAT_ID = -1003690946411  # grupo ou bot que recebe /rosa

URL_TIP_MINER = "https://tipminer.com"

TZ_BR = pytz.timezone("America/Sao_Paulo")

# evita disparos duplicados
ultimo_horario_enviado = None


# ================= FUNÇÕES =================

def agora_br():
    return datetime.now(TZ_BR)

def enviar_para_bot(hora_rosa):
    global ultimo_horario_enviado

    if hora_rosa == ultimo_horario_enviado:
        return

    ultimo_horario_enviado = hora_rosa

    comando = f"/rosa {hora_rosa.replace(':','')}"

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": comando
    }

    requests.post(url, data=payload)
    print(f"🚀 Rosa enviada ao bot: {hora_rosa}")


# ================= COLETOR =================

def iniciar_coletor():
    print("🟢 Coletor Radar Rosa iniciado")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        page = browser.new_page()
        page.goto(URL_TIP_MINER, timeout=60000)

        while True:
            try:
                # ⚠️ SIMULAÇÃO BASE
                # Aqui depois você substitui pela leitura real do Tip Miner

                agora = agora_br()
                segundo = agora.second

                # exemplo: simula rosa quando segundo == 0
                if segundo == 0:
                    hora_rosa = agora.strftime("%H:%M")
                    enviar_para_bot(hora_rosa)
                    time.sleep(60)  # evita loop duplo

                time.sleep(1)

            except Exception as e:
                print("❌ Erro no coletor:", e)
                time.sleep(5)


# ================= START =================

if __name__ == "__main__":
    iniciar_coletor()
