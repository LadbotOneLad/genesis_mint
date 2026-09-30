#!/usr/bin/env python3
import os
from web3 import Web3

NETWORKS = {
    "Ethereum": "https://eth.llamarpc.com",
    "Arbitrum": "https://arb1.arbitrum.io/rpc",
    "Optimism": "https://mainnet.optimism.io",
    "Base": "https://mainnet.base.org"
}

def main():
    print("==================================================")
    print("    RPC CONNECTION & BLOCK HEIGHT CHECKER         ")
    print("==================================================")
    
    for chain, rpc_url in NETWORKS.items():
        try:
            w3 = Web3(Web3.HTTPProvider(rpc_url, request_kwargs={'timeout': 5}))
            if w3.is_connected():
                block_number = w3.eth.block_number
                print(f"[+] {chain:<10} : Connected | Block: {block_number}")
            else:
                print(f"[-] {chain:<10} : Connection failed")
        except Exception as e:
            print(f"[x] {chain:<10} : Error -> {str(e)}")

    print("==================================================")

if __name__ == "__main__":
    main()
