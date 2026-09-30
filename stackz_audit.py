import os
import json

LEDGER_FILE = "ghostnet_ledger.jsonl"
USER_NODES_FILE = "ghostnet_user_nodes.jsonl"

def audit_matrix():
    total_stars = 0
    tx_count = 0
    
    if os.path.exists(LEDGER_FILE):
        with open(LEDGER_FILE, "r") as f:
            for line in f:
                if line.strip():
                    entry = json.loads(line.strip())
                    data = entry.get("data", {})
                    if "stars_received" in data:
                        total_stars += data["stars_received"]
                        tx_count += 1

    total_nodes = 0
    if os.path.exists(USER_NODES_FILE):
        with open(USER_NODES_FILE, "r") as f:
            total_nodes = sum(1 for line in f if line.strip())

    # Estimated conversion metrics (approx $0.012 USD per Star)
    est_usd = total_stars * 0.012
    fragment_progress = min(100.5, (total_stars / 1000) * 100)

    print("==========================================")
    print("       GHOSTNET FIN-OPS MATRIX AUDIT      ")
    print("==========================================")
    print(f"[*] Total Downstream User Nodes : {total_nodes}")
    print(f"[*] Settled Transactions        : {tx_count}")
    print(f"[*] Cumulative Stars (XTR)      : {total_stars} ⭐")
    print(f"[*] Estimated USD Value         : ${est_usd:.2f}")
    print(f"[*] Fragment Payout Threshold   : {fragment_progress:.1f}% (Min: 1,000 ⭐)")
    print("==========================================")
    
    if total_stars >= 1000:
        print("[+] STATUS: Threshold cleared! Ready for Fragment TON export.")
    else:
        print(f"[!] STATUS: Accumulating. Need {1000 - total_stars} more Stars to unlock Fragment withdrawal.")

if __name__ == "__main__":
    audit_matrix()
