import telebot
from datetime import datetime, timedelta
import pytz
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# =========================
# CONFIGURAÇÕES
# =========================
TOKEN = "8316037466:AAFin8vm0gZ-3GtysKHIg2kSSNp2znHPAUE"
CHAT_ID = -8523974497  # 👈 TROQUE PELO ID DO SEU GRUPO

LINK_APOSTA_MAX = "https://v2.aviatorspy.com/apostamax"
LINK_TIP_MINER = "https://tipminer.com"

TZ = pytz.timezone("America/Sao_Paulo")
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# =========================
# FUNÇÕES
# =========================
def calcular_zonas(hora_str):
    base = datetime.strptime(hora_str, "%H:%M")
    zonas = [
        base + timedelta(minutes=7),
        base + timedelta(minutes=10),
        base + timedelta(minutes=26),
    ]
    return [z.strftime("%H:%M") for z in zonas]

def criar_botoes():
    teclado = InlineKeyboardMarkup(row_width=2)
    teclado.add(
        InlineKeyboardButton("🚀 Abrir Aposta Max", url=LINK_APOSTA_MAX),
        InlineKeyboardButton("📊 Abrir Tip Miner", url=LINK_TIP_MINER)
    )
    return teclado

# =========================
# RECEBER HORÁRIO (MANUAL)
# =========================
@bot.message_handler(func=lambda m: True)
def receber_hora(msg):
    texto = msg.text.strip()

    # aceita apenas HH:MM
    if len(texto) == 5 and texto[2] == ":":
        try:
            datetime.strptime(texto, "%H:%M")
        except:
            return

        zonas = calcular_zonas(texto)

        agora = datetime.now(TZ).strftime("%H:%M")

        mensagem = (
            "🌹 <b>ROSA 10x+ DETECTADO</b>\n\n"
            f"⏰ <b>Horário da rosa:</b> {texto}\n"
            f"🕒 <b>Análise gerada:</b> {agora}\n\n"
            "🎯 <b>ZONAS QUENTES:</b>\n"
            f"🎯 {zonas[0]}\n"
            f"🎯 {zonas[1]}\n"
            f"🎯 {zonas[2]}\n\n"
            "⚠️ Aguarde confirmação de padrão\n"
            "⏱️ Horário de Brasília"
        )

        bot.send_message(
            CHAT_ID,
            mensagem,
            reply_markup=criar_botoes()
        )

# =========================
# LOOP
# =========================
print("🤖 Radar Rosa Bot com botões ATIVO")
bot.infinity_polling()
