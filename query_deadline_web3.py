from web3 import Web3
import json
import ssl

def main():
    rpc_url = "https://rpc-mainnet.billions.network"
    distributor_address = "0x4BB63E4E1AcC5750FD1a6aDF26520126D8c9d6C8"
    
    # Simple ABI with only the view functions we need
    abi = [
        {
            "inputs": [],
            "name": "active",
            "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [],
            "name": "activeWindowStartTime",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [],
            "name": "activeWindowEndTime",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function"
        }
    ]
    
    print(f"Connecting to RPC: {rpc_url}")
    # Disable SSL verification for connection just in case
    w3 = Web3(Web3.HTTPProvider(rpc_url, request_kwargs={'verify': False}))
    
    if not w3.is_connected():
        print("Failed to connect to RPC endpoint!")
        return
        
    print("Connected successfully!")
    contract = w3.eth.contract(address=w3.to_checksum_address(distributor_address), abi=abi)
    
    try:
        is_active = contract.functions.active().call()
        start_time = contract.functions.activeWindowStartTime().call()
        end_time = contract.functions.activeWindowEndTime().call()
        
        print("\n--- DISTRIBUTOR CONTRACT STATUS ---")
        print(f"Is Claim Active?          {is_active}")
        print(f"Active Window Start (Unix): {start_time}")
        print(f"Active Window End (Unix):   {end_time}")
        
        # Convert unix times to readable dates
        import datetime
        start_date = datetime.datetime.fromtimestamp(start_time, tz=datetime.timezone.utc)
        end_date = datetime.datetime.fromtimestamp(end_time, tz=datetime.timezone.utc)
        
        print(f"Active Window Start (UTC):  {start_date.strftime('%Y-%m-%d %H:%M:%S')} UTC")
        print(f"Active Window End (UTC):    {end_date.strftime('%Y-%m-%d %H:%M:%S')} UTC")
        
        # Save this to a JSON file so our app can load it!
        with open('claim_status.json', 'w') as f:
            json.dump({
                'active': is_active,
                'startTime': start_time,
                'endTime': end_time,
                'startDate': start_date.strftime('%Y-%m-%d %H:%M:%S'),
                'endDate': end_date.strftime('%Y-%m-%d %H:%M:%S')
            }, f, indent=2)
        print("\nSaved contract status to claim_status.json")
    except Exception as e:
        print(f"Error calling contract view methods: {e}")

if __name__ == "__main__":
    main()
