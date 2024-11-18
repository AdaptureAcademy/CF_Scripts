from cloudflarest.cloudfluser import AdaptureUser
import httpx
from pprint import pprint 
import pandas as pd

def get_zone_settings(zone_id, headers):
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/settings"
    response = httpx.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Failed to fetch zone settings:", response.status_code, response.text)
        return None

def main():
    user = AdaptureUser('GPC', token_name='token')
    headers = user.credentials.headers
    zones = user.zones  # Get all zones
    # pprint(f"Zones: {zones}")
    all_zone_settings = []  # To store the settings for all zones

    for zone in zones:
        zone_id = zone['id']  # Get the ID of the zone
        zone_settings = get_zone_settings(zone_id, headers)  # Fetch the zone settings
        pprint(zone_settings)
        print(zone['name'])
        print('')
        # if zone_settings:  # Only append if the request was successful
        #     all_zone_settings.append({
        #         'zone_name': zone['name'],
        #         'zone_id': zone_id,
        #         'settings': zone_settings
        #     })

        # Print out the settings for all zones
     

if __name__ == "__main__":
    main()
