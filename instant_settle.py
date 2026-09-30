#!/usr/bin/env python3
import os
import sys
from web3 import Web3

NETWORKS = {
    "Arbitrum": "https://arb1.arbitrum.io/rpc",
    "Optimism": "https://mainnet.optimism.io",
    "Base": "https://mainnet.base.org",
    "Ethereum": "https://rpc.ankr.com/eth"
}

def main():
    print("==================================================")
    print("    FULL CASH INSTANT SETTLEMENT ENGINE (LIVE)    ")
    print("==================================================")
    
    target_address = os.getenv("WALLET_ADDRESS")
    if not target_address or not Web3.is_address(target_address):
        print("[!] ERROR: WALLET_ADDRESS environment variable is required for live execution.")
        print("    No simulations allowed. Set it with:")
        print("    export WALLET_ADDRESS='0xYourActualWalletAddress'")
        print("==================================================")
        sys.exit(1)

    print(f"[*] Live Target Wallet : {target_address}")
    print("-" * 50)

    for chain, rpc_url in NETWORKS.items():
        try:
            w3 = Web3(Web3.HTTPProvider(rpc_url, request_kwargs={'timeout': 5}))
            if w3.is_connected():
                balance_wei = w3.eth.get_balance(target_address)
                balance_eth = w3.from_wei(balance_wei, 'ether')
                print(f"[+] {chain:<10} : Live Balance -> {balance_eth:.6f} ETH")
            else:
                print(f"[-] {chain:<10} : Connection failed")
        except Exception as e:
            print(f"[x] {chain:<10} : Error -> {str(e)[:30]}")

    print("==================================================")

if __name__ == "__main__":
    main()
