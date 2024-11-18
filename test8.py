from cloudflarest.cloudfluser import AdaptureUser
import httpx
import pandas as pd
from pprint import pprint

# Function to get zone settings
def get_zone_settings(zone_id, headers):
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/settings"
    response = httpx.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch settings for zone {zone_id}: {response.status_code}")
        return None

# Function to process zone settings and export them to an Excel file
def process_and_export_to_excel(zones, headers):
    all_settings = []

    for zone in zones[:10]:
        zone_id = zone['id']
        zone_settings = get_zone_settings(zone_id, headers)

        if zone_settings and zone_settings.get('success', False):
            for setting in zone_settings['result']:
                setting_data = {
                    'Zone Name': zone['name'],
                    'Setting ID': setting['id'],
                    'Editable': setting['editable'],
                    'Value': setting['value'],
                    'Modified On': setting.get('modified_on', 'N/A')
                }
                all_settings.append(setting_data)

    # Create a DataFrame from the collected settings
    df = pd.DataFrame(all_settings)

    # Export the DataFrame to an Excel file
    output_filename = 'cloudflare_zone_settings.xlsx'
    df.to_excel(output_filename, index=False, engine='openpyxl')
    print(f"Data has been exported to {output_filename}")

def main():
    # Assuming `user` is already instantiated correctly and `zones` is populated
    user = AdaptureUser('GPC', token_name='token')
    headers = user.credentials.headers
    # Get all zones
    zones = [
        zone
        for zone in user.zones
        if "enterprise" in zone["plan"]["name"].lower()
        and zone["account"]["name"]
        not in [
            "Omni Hotels and Resorts",
            "NFR-US-Adapture",
            "Adapturetech@gmail.com's account",
            "AMC Theatres",
            "Fossil Partners Enterprise Account"
        ]
    ]  
    
    # Process the data and export it
    process_and_export_to_excel(zones, headers)

if __name__ == "__main__":
    main()
