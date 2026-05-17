import urllib.request
import json
import ssl

def main():
    tx_hash = "0xd65b0c512a8ef7ebad8419e8e0a19bf3f7f5201876692a752b1e40c50588c639"
    url = f"https://explorer.billions.network/api/v2/transactions/{tx_hash}"
    print(f"Fetching transaction details from: {url}")
    
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
            print("Successfully fetched transaction details!")
            print(json.dumps(data, indent=2))
    except Exception as e:
        print(f"Error fetching data: {e}")

if __name__ == "__main__":
    main()
