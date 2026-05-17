import csv
import json

def main():
    print("Reading detailed claims from claims_detailed.csv...")
    claims = []
    
    with open('claims_detailed.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            claims.append({
                'tx': row['Tx Hash'],
                'block': int(row['Block Number']),
                'timestamp': row['Timestamp'],
                'address': row['Claimant Address'],
                'amount': float(row['Amount BILL'])
            })
            
    print(f"Loaded {len(claims)} records. Sorting by claim amount...")
    # Sort descending by amount, then by timestamp descending
    claims.sort(key=lambda x: (-x['amount'], x['timestamp']))
    
    # Assign ranks
    for rank, claim in enumerate(claims, 1):
        claim['rank'] = rank
        
    print("Compiling into data.js...")
    with open('data.js', 'w', encoding='utf-8') as f:
        f.write("// Instant client-side database for $BILL Allocation Explorer\n")
        f.write("const claimsData = ")
        json.dump(claims, f, separators=(',', ':'))
        f.write(";\n")
        
    print(f"Successfully generated data.js with {len(claims)} records!")

if __name__ == "__main__":
    main()
