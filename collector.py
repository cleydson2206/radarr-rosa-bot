import os
import time
import sys
from datetime import datetime
import pytz

# ==============================
# CONFIGURAÇÕES
# ==============================

TZ_BR = pytz.timezone("America/Sao_Paulo")

def agora_br():
    return datetime.now(TZ_BR).strftime("%d/%m/%Y %H:%M:%S")

# ==============================
# INÍCIO DO COLETOR
# ==============================

print("🚀 Collector iniciado")
print(f"🕒 Horário BR: {agora_br()}")

# Simula coleta de dados
try:
    for i in range(1, 6):
        print(f"📡 Coletando dados... passo {i}/5")
        time.sleep(2)

    print("✅ Coleta finalizada com sucesso")

except Exception as e:
    print("❌ Erro no collector:")
    print(e)
    sys.exit(1)

# ==============================
# FINALIZAÇÃO
# ==============================

print("🏁 Collector encerrado normalmente")
sys.exit(0)
