import urllib.request
import json
import ssl

def main():
    address = "0x4BB63E4E1AcC5750FD1a6aDF26520126D8c9d6C8"
    url = f"https://explorer.billions.network/api/v2/smart-contracts/{address}"
    print(f"Fetching contract info from: {url}")
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            data = json.loads(response.read().decode('utf-8'))
            print("Successfully fetched contract info!")
            print(f"Contract Name: {data.get('name')}")
            
            # Print ABI functions that might indicate endTime or deadline
            abi = data.get('abi', [])
            if abi:
                print("\nRead functions found in ABI:")
                for item in abi:
                    if item.get('type') == 'function' and item.get('stateMutability') in ['view', 'pure']:
                        inputs = ", ".join([f"{i['type']} {i['name']}" for i in item.get('inputs', [])])
                        outputs = ", ".join([f"{o['type']}" for o in item.get('outputs', [])])
                        print(f"  - {item['name']}({inputs}) returns ({outputs})")
            else:
                print("No ABI found in response.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
