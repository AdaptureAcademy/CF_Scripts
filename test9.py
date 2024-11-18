from cloudflarest.cloudfluser import AdaptureUser
import httpx
import pandas as pd
from pprint import pprint

# Function to get zone settings
def get_zone_settings(zone_id, headers):
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/settings"
    response = httpx.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['result']
    else:
        print(f"Failed to fetch settings for zone {zone_id}: {response.status_code}")

        return None

    
def main():
    # Assuming `user` is already instantiated correctly and `zones` is populated
    user = AdaptureUser('GPC', token_name='token')
    headers = user.credentials.headers
    # Get all zones
    # zones = [
    #     zone
    #     for zone in user.zones
    #     if "enterprise" in zone["plan"]["name"].lower()
    #     and zone["account"]["name"]
    #     not in [
    #         "Omni Hotels and Resorts",
    #         "NFR-US-Adapture",
    #         "Adapturetech@gmail.com's account",
    #         "AMC Theatres",
    #         "Fossil Partners Enterprise Account"
    #     ]
    # ]  

    # zones = [
    #     zone
    #     for zone in user.zones
    #     if zone["account"]["name"] not in [
    #         "Adapturetech@gmail.com's account",
    #         "Hmustafa@adapture.com's Account"
    #     ]
    # ]  
    # Define a list of zones that are on either the free plan or the enterprise plan
    zones = [
          zone
          for zone in user.zones
          if zone["account"]["name"] not in [
          "Adapturetech@gmail.com's account",
         "Hmustafa@adapture.com's Account"
         ] and (
         "free" in zone["plan"]["name"].lower() or 
         "enterprise" in zone["plan"]["name"].lower()
        )

        ]

    results = []
    for idx,zone in enumerate(zones, start=1):
        account_id = zone['account']['id']
        account_name = zone['account']['name']
        zone_id = zone['id']
        zone_name = zone['name']
        settings = get_zone_settings(zone_id, headers)
        settings_dict = {
            'Account ID': account_id,
            'Account Name': account_name,
            'Zone ID': zone_id,
            'Zone Name': zone_name,
        }

        try:
            for setting in settings:
                setting_id = setting.get("id")
                setting_value = setting.get("value")
                settings_dict[setting_id] = setting_value
 
            results.append(settings_dict)
        except Exception as e:
            print(f"Error processing settings for zone ID {zone_id}: {e}")
            continue
 
        print(f"Processed zone {zone_id} ({idx}/{len(zones)})")

    # Create a DataFrame from the collected settings
    df = pd.DataFrame(results)

    # Export the DataFrame to an Excel file
    output_filename = 'v3_zone_settings.xlsx'
    df.to_excel(output_filename, index=False, engine='openpyxl')
    print(f"Data has been exported to {output_filename}")

if __name__ == "__main__":
    main()

