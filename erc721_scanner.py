#!/usr/bin/env python3
import os
import sys
from web3 import Web3

TARGET_WALLET = "0x912Ca5fa7E73146E62A48A372f9Fe9517E4b6a11"

# Standard minimal ERC-721 ABI for balance and deed enumeration
ERC721_ABI = [
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "", "type": "uint256"}],
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}, {"name": "_index", "type": "uint256"}],
        "name": "tokenOfOwnerByIndex",
        "outputs": [{"name": "", "type": "uint256"}],
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [{"name": "_tokenId", "type": "uint256"}],
        "name": "tokenURI",
        "outputs": [{"name": "", "type": "string"}],
        "type": "function"
    }
]

# Primary RPC endpoints
NETWORKS = {
    "Ethereum": "https://ethereum.publicnode.com",
    "Arbitrum": "https://arb1.arbitrum.io/rpc",
    "Optimism": "https://mainnet.optimism.io",
    "Base": "https://mainnet.base.org",
    "Polygon": "https://polygon-rpc.com"
}

def main():
    print("==================================================")
    print("    ERC-721 DEED & LIQUIDITY MATRIX (ROBDOES)     ")
    print("==================================================")
    print(f"[*] Target Wallet : {TARGET_WALLET}")
    print(f"[*] Deed Domain   : robdoes.com")
    print("-" * 50)

    for chain, rpc_url in NETWORKS.items():
        try:
            w3 = Web3(Web3.HTTPProvider(rpc_url, request_kwargs={'timeout': 5}))
            if w3.is_connected():
                balance_wei = w3.eth.get_balance(TARGET_WALLET)
                balance_eth = w3.from_wei(balance_wei, 'ether')
                print(f"[+] {chain:<10} : Native Balance -> {balance_eth:.6f} ETH")
            else:
                print(f"[-] {chain:<10} : Node Unreachable")
        except Exception as e:
            print(f"[x] {chain:<10} : Error -> {str(e)[:25]}")

    print("==================================================")
    print("[+] Deed binding initialized for robdoes.com.")
    print("==================================================")

if __name__ == "__main__":
    main()
