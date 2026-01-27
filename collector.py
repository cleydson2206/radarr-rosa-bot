import time
import datetime
import pytz

TZ_BR = pytz.timezone("America/Sao_Paulo")

print("🟢 Collector iniciado com sucesso")
print("⏰ Fuso horário: Brasil")

def agora():
    return datetime.datetime.now(TZ_BR).strftime("%H:%M:%S")

while True:
    try:
        print(f"📡 Collector ativo | {agora()}")
        time.sleep(30)  # mantém o worker vivo
    except Exception as e:
        print("❌ Erro no collector:", e)
        time.sleep(5)
