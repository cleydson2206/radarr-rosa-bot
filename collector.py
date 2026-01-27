import time
from datetime import datetime
import pytz

TZ_BR = pytz.timezone("America/Sao_Paulo")

def agora_br():
    return datetime.now(TZ_BR).strftime("%H:%M:%S")

print("🟢 Collector iniciado com sucesso")

while True:
    try:
        print(f"📡 Coletando dados... {agora_br()}")

        # 👉 AQUI entra sua lógica real de coleta
        # ex: leitura de API, scraping, cálculo, etc

        time.sleep(60)  # roda a cada 60 segundos

    except Exception as e:
        print("❌ Erro no collector:", e)
        time.sleep(10)
