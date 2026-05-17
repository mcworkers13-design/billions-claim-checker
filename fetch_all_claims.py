import urllib.request
import urllib.parse
import json
import ssl
import csv
import time
from datetime import datetime

def main():
    distributor = "0x4BB63E4E1AcC5750FD1a6aDF26520126D8c9d6C8"
    base_url = f"https://explorer.billions.network/api/v2/addresses/{distributor}/transactions"
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    detailed_claims = []
    aggregated_claims = {}
    
    url = base_url
    page = 1
    total_tx_count = 0
    claim_count = 0
    
    print("Starting data retrieval from Billions Network explorer...")
    print(f"Distributor Contract: {distributor}\n")
    
    while url:
        print(f"Fetching page {page}...")
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        
        # Simple retry mechanism
        retries = 3
        data = None
        while retries > 0:
            try:
                with urllib.request.urlopen(req, context=ctx) as response:
                    data = json.loads(response.read().decode('utf-8'))
                    break
            except Exception as e:
                print(f"Error fetching page {page} (retries left {retries-1}): {e}")
                retries -= 1
                time.sleep(1)
        
        if not data:
            print("Failed to fetch page. Exiting loop.")
            break
            
        items = data.get('items', [])
        if not items:
            print("No items found. Finished fetching.")
            break
            
        total_tx_count += len(items)
        
        for tx in items:
            # Check if this is a successful claim transaction
            is_claim = tx.get('method') == 'claim'
            is_success = tx.get('status') == 'ok' or tx.get('result') == 'success'
            
            if is_claim and is_success:
                tx_hash = tx.get('hash')
                block_number = tx.get('block_number')
                timestamp_str = tx.get('timestamp') # format: "2026-05-17T19:58:14.000000Z"
                
                # Format timestamp for better readability
                if timestamp_str:
                    try:
                        dt = datetime.strptime(timestamp_str.split('.')[0], "%Y-%m-%dT%H:%M:%S")
                        formatted_time = dt.strftime("%Y-%m-%d %H:%M:%S")
                    except Exception:
                        formatted_time = timestamp_str
                else:
                    formatted_time = "N/A"
                
                decoded_input = tx.get('decoded_input', {})
                if decoded_input:
                    parameters = decoded_input.get('parameters', [])
                    amount_wei = None
                    on_behalf_of = None
                    
                    for param in parameters:
                        name = param.get('name')
                        val = param.get('value')
                        if name == '_amount':
                            amount_wei = int(val)
                        elif name == '_onBehalfOf':
                            on_behalf_of = val
                            
                    if amount_wei is not None and on_behalf_of:
                        amount_bill = amount_wei / 10**18
                        claim_count += 1
                        
                        detailed_claims.append({
                            'tx_hash': tx_hash,
                            'block_number': block_number,
                            'timestamp': formatted_time,
                            'claimant': on_behalf_of,
                            'amount_bill': amount_bill
                        })
                        
                        if on_behalf_of not in aggregated_claims:
                            aggregated_claims[on_behalf_of] = {
                                'total_amount': 0.0,
                                'claim_count': 0
                            }
                        aggregated_claims[on_behalf_of]['total_amount'] += amount_bill
                        aggregated_claims[on_behalf_of]['claim_count'] += 1
                        
        next_params = data.get('next_page_params')
        if next_params:
            url = f"{base_url}?{urllib.parse.urlencode(next_params)}"
            page += 1
        else:
            url = None
            
    print(f"\nFinished fetching data.")
    print(f"Total transactions analyzed: {total_tx_count}")
    print(f"Total claim events found: {claim_count}")
    print(f"Total unique claimants: {len(aggregated_claims)}")
    
    # Save detailed claims
    detailed_file = 'claims_detailed.csv'
    with open(detailed_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Tx Hash', 'Block Number', 'Timestamp', 'Claimant Address', 'Amount BILL'])
        for claim in detailed_claims:
            writer.writerow([
                claim['tx_hash'],
                claim['block_number'],
                claim['timestamp'],
                claim['claimant'],
                f"{claim['amount_bill']:.2f}"
            ])
            
    # Save aggregated claims
    aggregated_file = 'claims_aggregated.csv'
    with open(aggregated_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Claimant Address', 'Total Amount BILL', 'Number of Claims'])
        for addr, info in sorted(aggregated_claims.items(), key=lambda x: x[1]['total_amount'], reverse=True):
            writer.writerow([
                addr,
                f"{info['total_amount']:.2f}",
                info['claim_count']
            ])
            
    print(f"\nSaved detailed claims to {detailed_file}")
    print(f"Saved aggregated summary to {aggregated_file}")
    
    # Print a preview of top 10 claimants
    print("\n--- TOP 10 CLAIMANTS ---")
    top_10 = sorted(aggregated_claims.items(), key=lambda x: x[1]['total_amount'], reverse=True)[:10]
    for i, (addr, info) in enumerate(top_10, 1):
        print(f"{i}. {addr}: {info['total_amount']:,.2f} BILL ({info['claim_count']} claim(s))")

if __name__ == "__main__":
    main()
