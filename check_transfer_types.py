import urllib.request
import urllib.parse
import json
import ssl

def main():
    token_address = "0xb060E40C3B053C33D458f7105F95DA52741CAb62"
    url = f"https://explorer.billions.network/api/v2/tokens/{token_address}/transfers"
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    unique_transfers = set()
    page = 1
    
    while url and page <= 5: # check first 5 pages of transfers
        print(f"Fetching token transfers page {page}...")
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            with urllib.request.urlopen(req, context=ctx) as response:
                data = json.loads(response.read().decode('utf-8'))
                items = data.get('items', [])
                for item in items:
                    frm = item.get('from', {}).get('hash')
                    frm_name = item.get('from', {}).get('name')
                    to = item.get('to', {}).get('hash')
                    to_name = item.get('to', {}).get('name')
                    method = item.get('method')
                    unique_transfers.add((frm, frm_name, to, to_name, method))
                
                next_params = data.get('next_page_params')
                if next_params:
                    url = f"https://explorer.billions.network/api/v2/tokens/{token_address}/transfers?{urllib.parse.urlencode(next_params)}"
                    page += 1
                else:
                    url = None
        except Exception as e:
            print(f"Error: {e}")
            break
            
    print("\nUnique Transfer Combinations (from -> to [method]):")
    for frm, frm_name, to, to_name, method in sorted(unique_transfers, key=lambda x: str(x[4])):
        print(f"  From: {frm} ({frm_name}) -> To: {to} ({to_name}) [Method: {method}]")

if __name__ == "__main__":
    main()
