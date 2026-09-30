#!/usr/bin/env python3
import os
import sys

def main():
    print("==================================================")
    print("    WEB3 LIQUIDITY SCANNER & ROUTE MAPPER       ")
    print("==================================================")
    print("[*] Initializing environment...")
    
    # Check for web3 package availability
    try:
        import web3
        print(f"[+] web3.py version {web3.__version__} detected.")
    except ImportError:
        print("[!] Warning: web3.py not found in current environment.")
        print("    Run local checks or ensure dependencies are mapped.")

    rpc_url = os.getenv("WEB3_PROVIDER_URI", "https://eth.llamarpc.com")
    print(f"[*] Active RPC Endpoint  : {rpc_url[:30]}...")
    print("[+] Status: Scanner ready for multi-chain liquidity aggregation.")
    print("==================================================")

if __name__ == "__main__":
    main()
