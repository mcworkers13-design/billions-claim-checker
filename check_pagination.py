import urllib.request
import json
import ssl

def main():
    distributor = "0x4BB63E4E1AcC5750FD1a6aDF26520126D8c9d6C8"
    url = f"https://explorer.billions.network/api/v2/addresses/{distributor}/transactions"
    
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
            print("Next page params:")
            print(json.dumps(data.get('next_page_params'), indent=2))
    except Exception as e:
        print(f"Error fetching data: {e}")

if __name__ == "__main__":
    main()
