import urllib.request
import json
import ssl

def main():
    url = "https://explorer.billions.network/api/v2/tokens/0xb060E40C3B053C33D458f7105F95DA52741CAb62/transfers"
    print(f"Fetching from: {url}")
    
    # Create an unverified SSL context just in case there are certificate issues
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
            print("Successfully fetched data!")
            print(f"Keys in response: {list(data.keys())}")
            if 'items' in data:
                print(f"Number of items in page: {len(data['items'])}")
                if len(data['items']) > 0:
                    print("Sample item structure:")
                    print(json.dumps(data['items'][0], indent=2))
            else:
                print("Full response preview:")
                print(json.dumps(data, indent=2)[:1000])
    except Exception as e:
        print(f"Error fetching data: {e}")

if __name__ == "__main__":
    main()
