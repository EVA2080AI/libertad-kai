#!/usr/bin/env python3
"""KAI - Bot de Telegram para LIBERTAD."""

import os
import sys
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Token de tu bot
TELEGRAM_TOKEN = "8648006590:AAFDe0_C23nizKIm6F4TbnKvjMwhHZjMAMQ"

# Ruta del proyecto
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_DIR)

from core.config import Config
from core.storage import Storage
from core.token_manager import TokenManager

# Estados del sistema
config = Config(f"{PROJECT_DIR}/.env")
storage = Storage()
token_manager = TokenManager()


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start."""
    await update.message.reply_text(
        "🔥 KAI ONLINE\n\n"
        "Soy tu agente autónomo LIBERTAD.\n"
        "Estoy buscando formas de generar dinero para ti.\n\n"
        "Comandos:\n"
        "/status - Ver estado del sistema\n"
        "/balance - Tu balance en Binance\n"
        "/income - Reporte de ingresos\n"
        "/progress - Progreso hacia meta\n"
        "/help - Ayuda"
    )


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Estado del sistema."""
    income = storage.get('income_summary', {})
    balance = income.get('current_balance_usd', 0)
    
    await update.message.reply_text(
        f"📊 ESTADO DEL SISTEMA\n\n"
        f"🤖 Agente: KAI ONLINE\n"
        f"💰 Balance: ${balance:.2f}\n"
        f"🎯 Meta: $100/día\n"
        f"📈 Progreso: {balance/100*100:.1f}%\n\n"
        f"⏳ Buscando formas de generar dinero..."
    )


async def balance_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Balance de Binance."""
    try:
        import hmac
        import hashlib
        import time
        import requests
        
        API_KEY = config.get('binance_api_key')
        API_SECRET = config.get('binance_api_secret')
        
        if not API_KEY or not API_SECRET:
            await update.message.reply_text("❌ API no configurada")
            return
        
        timestamp = int(time.time() * 1000)
        query = f"timestamp={timestamp}"
        signature = hmac.new(API_SECRET.encode(), query.encode(), hashlib.sha256).hexdigest()
        
        url = f"https://api.binance.com/api/v3/account?{query}&signature={signature}"
        resp = requests.get(url, headers={"X-MBX-APIKEY": API_KEY}, timeout=10)
        data = resp.json()
        
        if 'balances' in data:
            msg = "💰 TU BALANCE EN BINANCE\n\n"
            has_balance = False
            for b in data['balances']:
                if float(b.get('free', 0)) > 0:
                    msg += f"  {b['asset']}: {b['free']}\n"
                    has_balance = True
            if not has_balance:
                msg += "  (sin saldo aún)\n"
            await update.message.reply_text(msg)
        else:
            await update.message.reply_text(f"❌ Error: {data}")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")


async def income_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Reporte de ingresos."""
    income = storage.get('income_summary', {})
    total = sum(v for k, v in income.items() if isinstance(v, (int, float)))
    
    await update.message.reply_text(
        f"💵 REPORTE DE INGRESOS\n\n"
        f"💰 Total generado: ${total:.2f}\n"
        f"🎯 Meta diaria: $100\n"
        f"📊 Status: {'✅ En camino' if total >= 100 else '⏳ En progreso'}"
    )


async def progress_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Progreso visual."""
    income = storage.get('income_summary', {})
    current = income.get('current_balance_usd', 0)
    progress = min(current / 100, 1.0)
    bar = "█" * int(progress * 20) + "░" * (20 - int(progress * 20))
    
    await update.message.reply_text(
        f"🎯 PROGRESSO META DIARIA\n\n"
        f"[{bar}]\n"
        f"{progress*100:.1f}%\n\n"
        f"💰 ${current:.2f} / $100"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ayuda."""
    await update.message.reply_text(
        "📖 AYUDA KAI\n\n"
        "/start - Iniciar\n"
        "/status - Estado\n"
        "/balance - Balance Binance\n"
        "/income - Ingresos\n"
        "/progress - Progreso\n"
        "/help - Esta ayuda\n\n"
        "🔔 También puedes escribirme y te respondo!"
    )


async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando desconocido."""
    await update.message.reply_text(
        "🤖 No entendí. Usa /help para ver comandos disponibles."
    )


def main():
    """Inicia el bot KAI."""
    print("="*50)
    print("🔥 KAI BOT INICIADO")
    print(f"📱 Token: {TELEGRAM_TOKEN[:15]}...")
    print("="*50)
    
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Comandos
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("status", status_command))
    app.add_handler(CommandHandler("balance", balance_command))
    app.add_handler(CommandHandler("income", income_command))
    app.add_handler(CommandHandler("progress", progress_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.COMMAND, unknown_command))
    
    print("✅ KAI está listo! Presiona Ctrl+C para detener.")
    app.run_polling()


if __name__ == "__main__":
    main()
