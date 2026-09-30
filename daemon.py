import os
import logging
import json
import math
import hashlib
from datetime import datetime, timezone
from telegram import LabeledPrice, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    PreCheckoutQueryHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)
from telegram.request import HTTPXRequest

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "8276734769:AAGsGvk7eRfkYLS0ZOkgCFvxWgsx-7pq0-M"
RECEIVER_ADDRESS = "0x5FbDB2315678afecb367f032d93F642f64180aa3"
ROOT_HASH = "0x3a7317b5513417cb08a6cb973b79e758fcbfeee53b3561c102d5612e1338de60"
LEDGER_FILE = "ghostnet_ledger.jsonl"
USER_NODES_FILE = "ghostnet_user_nodes.jsonl"
PAYLOAD_ID = "ghostnet-star-payload-001"

def run_kuramoto_sync():
    N = 4
    phases = [0.1, 1.2, 2.5, 3.1]
    K = 2.5
    dt = 0.05
    steps = 100
    for _ in range(steps):
        new_phases = list(phases)
        for i in range(N):
            coupling_sum = sum(math.sin(phases[j] - phases[i]) for j in range(N))
            new_phases[i] = phases[i] + dt * (1.0 + (K / N) * coupling_sum)
        phases = [p % (2 * math.pi) for p in new_phases]
    real_sum = sum(math.cos(p) for p in phases)
    imag_sum = sum(math.sin(p) for p in phases)
    r = math.sqrt(real_sum**2 + imag_sum**2) / N
    return round(r, 4), [round(p, 3) for p in phases]

def hash_pair(left: str, right: str) -> str:
    combined = (left + right).encode("utf-8")
    return "0x" + hashlib.sha256(combined).hexdigest()

def append_merkle_dag_ledger(receipt_data):
    prev_root = "0x0000000000000000000000000000000000000000000000000000000000000000"
    tree_height = 1
    try:
        if os.path.exists(LEDGER_FILE):
            with open(LEDGER_FILE, "r") as f:
                lines = f.readlines()
                if lines:
                    last_entry = json.loads(lines[-1].strip())
                    prev_root = last_entry.get("merkle_root", prev_root)
                    tree_height = last_entry.get("tree_height", 1) + 1
    except Exception as e:
        logger.error(f"Ledger read error: {e}")

    data_string = json.dumps(receipt_data, sort_keys=True)
    current_data_hash = "0x" + hashlib.sha256(data_string.encode("utf-8")).hexdigest()
    new_merkle_root = hash_pair(prev_root, current_data_hash)

    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "tree_height": tree_height,
        "left_parent_root": prev_root,
        "right_leaf_hash": current_data_hash,
        "merkle_root": new_merkle_root,
        "data": receipt_data
    }

    with open(LEDGER_FILE, "a") as f:
        f.write(json.dumps(record) + "\n")
        
    return new_merkle_root, tree_height

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    referrer = args[0] if args else "direct"
    user = update.effective_user
    
    ref_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "user_id": user.id,
        "username": user.username,
        "referred_by": referrer
    }
    with open(USER_NODES_FILE, "a") as f:
        f.write(json.dumps(ref_entry) + "\n")

    keyboard = [
        [InlineKeyboardButton("⚡ Buy Compute Unit (259 Stars)", callback_data="buy_unit")],
        [InlineKeyboardButton("🔄 Unlock via Viral Referral Link", callback_data="get_ref")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"🌐 **GhostNet Recursive DAG Matrix**\n\n"
        f"Node registered under referrer: `{referrer}`\n"
        f"Status: **Active & Monitoring**\n\n"
        f"Choose your entry vector below to unlock full network compute access:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user

    if query.data == "buy_unit":
        await context.bot.send_invoice(
            chat_id=query.message.chat_id,
            title="GhostNet DAG Compute Unit",
            description="Process 259 Stars to trigger recursive Merkle root state proof.",
            payload=PAYLOAD_ID,
            provider_token="",
            currency="XTR",
            prices=[LabeledPrice("Star Compute Unit", 259)],
        )
    elif query.data == "get_ref":
        ref_link = f"https://t.me/Looselipskizbot?start=ref_{user.id}"
        await query.message.reply_text(
            f"🔗 **Your Viral Acquisition Loop:**\n\n"
            f"Forward this link to active chats or groups to harvest downstream nodes into your matrix:\n`{ref_link}`",
            parse_mode="Markdown"
        )

async def trigger_sync(update: Update, context: ContextTypes.DEFAULT_TYPE):
    r, locked_phases = run_kuramoto_sync()
    await update.message.reply_text(f"Kuramoto Mesh Coherence (r): {r}\nPhases locked: {locked_phases}")

async def precheckout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.pre_checkout_query
    if query.invoice_payload != PAYLOAD_ID:
        await query.answer(ok=False, error_message="Payload verification failed.")
    else:
        await query.answer(ok=True)

async def successful_payment_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    payment = update.message.successful_payment
    r, locked_phases = run_kuramoto_sync()
    
    receipt = {
        "status": "settled_and_dag_anchored",
        "stars_received": payment.total_amount,
        "currency": payment.currency,
        "charge_id": payment.telegram_payment_charge_id,
        "contract": RECEIVER_ADDRESS,
        "base_root_hash": ROOT_HASH,
        "mesh_coherence": r,
        "phases": locked_phases
    }
    
    merkle_root, height = append_merkle_dag_ledger(receipt)
    receipt["recursive_merkle_root"] = merkle_root
    receipt["tree_height"] = height

    await update.message.reply_text(
        f"Payment settled. Recursive Merkle DAG updated (Height {height}).\n```json\n{json.dumps(receipt, indent=2)}\n```",
        parse_mode="Markdown"
    )

def main():
    request_client = HTTPXRequest(connect_timeout=30.0, read_timeout=30.0)
    
    application = ApplicationBuilder().token(TOKEN).request(request_client).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("sync", trigger_sync))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(PreCheckoutQueryHandler(precheckout_callback))
    application.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_callback))
    
    logger.info("Starting Viral Funnel Referral DAG Agent daemon...")
    application.run_polling()

if __name__ == "__main__":
    main()
