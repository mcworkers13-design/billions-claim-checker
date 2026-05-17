import urllib.request
import json
import ssl

def main():
    address = "0x4BB63E4E1AcC5750FD1a6aDF26520126D8c9d6C8"
    url = f"https://explorer.billions.network/api/v2/smart-contracts/{address}"
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    req = urllib.request.Request(
        url,
        headers={
            'User-Agent': 'Mozilla/5.0'
        }
    )
    
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            data = json.loads(response.read().decode('utf-8'))
            abi = data.get("abi", [])
            print(f"Fetched verified ABI for {address}. Found {len(abi)} entries.")
            
            functions = []
            for item in abi:
                if item.get("type") == "function":
                    name = item.get("name")
                    inputs = [f"{i.get('type')} {i.get('name')}" for i in item.get("inputs", [])]
                    outputs = [f"{o.get('type')}" for o in item.get("outputs", [])]
                    mutability = item.get("stateMutability", "")
                    
                    functions.append({
                        "name": name,
                        "inputs": inputs,
                        "outputs": outputs,
                        "mutability": mutability
                    })
            
            print("\n--- READ FUNCTIONS ---")
            for f in sorted([x for x in functions if x["mutability"] in ["view", "pure"]], key=lambda x: x["name"]):
                print(f"{f['name']}({', '.join(f['inputs'])}) -> ({', '.join(f['outputs'])}) [{f['mutability']}]")
                
            print("\n--- WRITE FUNCTIONS ---")
            for f in sorted([x for x in functions if x["mutability"] not in ["view", "pure"]], key=lambda x: x["name"]):
                print(f"{f['name']}({', '.join(f['inputs'])}) -> ({', '.join(f['outputs'])}) [{f['mutability']}]")
                
    except Exception as e:
        print(f"Error fetching ABI: {e}")

if __name__ == "__main__":
    main()
