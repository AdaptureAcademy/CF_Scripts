from cloudflarest.cloudfluser import AdaptureUser
import httpx
import pandas as pd
from pprint import pprint

def get_zone_wafrules(zone_id, headers):
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/firewall/waf/packages/rules"
    response = httpx.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Failed to retrieve zone rulesets for {zone_id}: {response.status_code} - {response.text}")
        return None

def main():
    # Initialize the user with your token name
    user = AdaptureUser('GPC', token_name='token')
    headers = user.credentials.headers

    # Replace 'your_zone_id' with the actual zone ID you want to query
    zone_id = '6edc93e749dfeced681d77c5027c4697'
    
    # Fetch the rulesets for the specified zone ID
    data = get_zone_wafrules(zone_id=zone_id, headers=headers)
    
    # Check if data was retrieved successfully
    if data and data.get('success'):
        # Create a DataFrame from the rulesets
        rulesets = data['result']
        df = pd.DataFrame(rulesets)
        
        # Save the DataFrame to an Excel file
        excel_file_path = 'napa_cloudflare_rulesets.xlsx'
        df.to_excel(excel_file_path, index=False)
        print(f"Data has been written to {excel_file_path}")

    else:
        print("No data found or retrieval was unsuccessful.")

# Entry point for the script
if __name__ == "__main__":
    main()
