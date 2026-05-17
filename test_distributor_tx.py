import urllib.request
import json
import ssl

def main():
    distributor = "0x4BB63E4E1AcC5750FD1a6aDF26520126D8c9d6C8"
    url = f"https://explorer.billions.network/api/v2/addresses/{distributor}/transactions"
    print(f"Fetching transactions for Distributor: {url}")
    
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
            print("Successfully fetched transactions!")
            print(f"Keys in response: {list(data.keys())}")
            if 'items' in data and len(data['items']) > 0:
                print(f"Number of transactions in page: {len(data['items'])}")
                print("Sample transaction structure:")
                print(json.dumps(data['items'][0], indent=2))
            else:
                print("No transactions found or structure is different.")
    except Exception as e:
        print(f"Error fetching data: {e}")

if __name__ == "__main__":
    main()
