#!/usr/bin/env python3
import os
import sys
from web3 import Web3

TARGET_WALLET = "0x912Ca5fa7E73146E62A48A372f9Fe9517E4b6a11"

# Hardened Multi-Provider / Redundant Grid
NETWORKS = {
    "Ethereum": "https://ethereum.publicnode.com",
    "Arbitrum": "https://arb1.arbitrum.io/rpc",
    "Optimism": "https://mainnet.optimism.io",
    "Base": "https://mainnet.base.org",
    "Polygon": "https://polygon-rpc.com",
    "BNB Smart Chain": "https://bsc-dataseed.binance.org",
    "Avalanche": "https://api.avax.network/ext/bc/C/rpc",
    "Fantom": "https://rpc.ftm.tools",
    "Arbitrum Nova": "https://nova.arbitrum.io/rpc",
    "Gnosis": "https://rpc.gnosischain.com"
}

def main():
    print("==================================================")
    print("    FULL CASH INSTANT SETTLEMENT ENGINE (GRID)    ")
    print("==================================================")
    
    if not Web3.is_address(TARGET_WALLET):
        print("[!] ERROR: Invalid target wallet address configured.")
        sys.exit(1)

    print(f"[*] Target Wallet : {TARGET_WALLET}")
    print("-" * 50)

    for chain, rpc_url in NETWORKS.items():
        try:
            w3 = Web3(Web3.HTTPProvider(rpc_url, request_kwargs={'timeout': 5}))
            if w3.is_connected():
                balance_wei = w3.eth.get_balance(TARGET_WALLET)
                balance_eth = w3.from_wei(balance_wei, 'ether')
                print(f"[+] {chain:<16} : {balance_eth:.6f} Native")
            else:
                print(f"[-] {chain:<16} : Connection failed")
        except Exception as e:
            print(f"[x] {chain:<16} : Error -> {str(e)[:25]}")

    print("==================================================")

if __name__ == "__main__":
    main()
