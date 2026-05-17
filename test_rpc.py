import urllib.request
import json
import ssl

def test_rpc(url):
    print(f"Testing RPC endpoint: {url}")
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_blockNumber",
        "params": [],
        "id": 1
    }
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0'
        }
    )
    
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=5) as response:
            res = json.loads(response.read().decode('utf-8'))
            if 'result' in res:
                block_hex = res['result']
                block_dec = int(block_hex, 16)
                print(f"  [SUCCESS] Current Block: {block_dec} (Hex: {block_hex})")
                return True
            else:
                print(f"  [ERROR] Response structure invalid: {res}")
    except Exception as e:
        print(f"  [FAILED] Connection failed: {e}")
    return False

def main():
    endpoints = [
        "https://rpc.billions.network",
        "https://rpc-mainnet.billions.network",
        "https://rpc-testnet.billions.network",
        "http://rpc.billions.network",
        "https://explorer.billions.network/api/eth-rpc" # Some blockscouts expose the RPC on this subpath
    ]
    
    for ep in endpoints:
        if test_rpc(ep):
            print(f"\nFound working RPC endpoint! --> {ep}")
            break

if __name__ == "__main__":
    main()
