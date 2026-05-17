import urllib.request
import json
import ssl
import hashlib

def sha3(text):
    # Standard Keccak-256 (sha3 in Ethereum context)
    # Using sha3 from hashlib (if available, which is sha3_256)
    # Note: hashlib.sha3_256 matches Keccak-256 behavior
    h = hashlib.sha3_256()
    h.update(text.encode('utf-8'))
    return h.hexdigest()

def get_selector(signature):
    # Keccak-256 in solidity starts with 0x and first 4 bytes (8 hex chars)
    # We can use a simple trick or standard hashlib.sha3_256. 
    # Wait, sha3_256 in standard python hashlib is SHA-3, which has a slightly different padding than Keccak-256!
    # Let's write a pure python Keccak-256 implementation, or use a known list of selectors.
    # Fortunately, the ABI file already has the selectors, or we can look them up!
    # Wait! Let's check get_contract_abi.py's output. The method ID for claim(...) was "ed810bc6".
    # For activeWindowEndTime(), let's see. We can just use standard sha3 or let's use a lookup list.
    # Let's write a selector finder or check if there is an online database, or use a direct selector!
    # Actually, "activeWindowEndTime()" selector is "5aef3335" or similar.
    # Let's use a pure Python keccak implementation or calculate Keccak-256 directly.
    pass

# Instead of calculating keccak from scratch in python which is long, 
# we can write a simple script that uses the hashlib or standard EVM calling if available,
# or let's query the Blockscout read contract endpoint which does the execution for us!
# Yes! Blockscout v2 API has an endpoint to query read methods directly without knowing the selector:
# POST https://explorer.billions.network/api/v2/smart-contracts/0x4BB63E4E1AcC5750FD1a6aDF26520126D8c9d6C8/query-read-method
# payload: {"args": [], "method": "activeWindowEndTime"}
# This is incredibly powerful and built into Blockscout! Let's test this!

def query_blockscout_method(method_name):
    address = "0x4BB63E4E1AcC5750FD1a6aDF26520126D8c9d6C8"
    url = f"https://explorer.billions.network/api/v2/smart-contracts/{address}/query-read-method"
    
    payload = {
        "args": [],
        "method": method_name
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
        with urllib.request.urlopen(req, context=ctx) as response:
            res = json.loads(response.read().decode('utf-8'))
            return res
    except Exception as e:
        print(f"Error querying {method_name}: {e}")
        return None

def main():
    print("Querying Distributor contract read methods via Blockscout API...")
    
    # Query active
    active_res = query_blockscout_method("active")
    print(f"active(): {active_res}")
    
    # Query activeWindowStartTime
    start_res = query_blockscout_method("activeWindowStartTime")
    print(f"activeWindowStartTime(): {start_res}")
    
    # Query activeWindowEndTime
    end_res = query_blockscout_method("activeWindowEndTime")
    print(f"activeWindowEndTime(): {end_res}")

if __name__ == "__main__":
    main()
