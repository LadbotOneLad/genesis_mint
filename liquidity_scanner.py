#!/usr/bin/env python3
import os
import sys
from web3 import Web3

# Multi-chain public RPC endpoints for balance aggregation
NETWORKS = {
    "Ethereum": "https://eth.llamarpc.com",
    "Arbitrum": "https://arb1.arbitrum.io/rpc",
    "Optimism": "https://mainnet.optimism.io",
    "Base": "https://mainnet.base.org"
}

def main():
    print("==================================================")
    print("    MULTI-CHAIN LIQUIDITY BALANCE CHECKER       ")
    print("==================================================")
    
    target_address = os.getenv("WALLET_ADDRESS")
    if not target_address or not Web3.is_address(target_address):
        print("[!] Warning: WALLET_ADDRESS environment variable not set or invalid.")
        print("    Set it using: export WALLET_ADDRESS='0xYourAddressHere'")
        print("==================================================")
        return

    print(f"[*] Target Wallet        : {target_address}")
    print("-" * 50)

    for chain, rpc_url in NETWORKS.items():
        try:
            w3 = Web3(Web3.HTTPProvider(rpc_url))
            if w3.is_connected():
                balance_wei = w3.eth.get_balance(target_address)
                balance_eth = w3.from_wei(balance_wei, 'ether')
                print(f"[+] {chain:<10} : {balance_eth:.6f} native")
            else:
                print(f"[-] {chain:<10} : Connection failed")
        except Exception as e:
            print(f"[x] {chain:<10} : Error ({str(e)})")

    print("==================================================")

if __name__ == "__main__":
    main()
