import requests
import pandas as pd
import pprint
from cloudflarest.cloudfluser import AdaptureUser
from datetime import datetime, timezone
 
def get_waf_status(headers, zone_id):
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/waf_migration/status"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        if response.status_code == 200:
            data = response.json()
            return {
                "zone_id": zone_id,
                "created": data['result']['created'],
                "migration_state": data['result']['migration_state'],
                "new_waf_status": data['result']['new_waf_status'],
                "old_waf_status": data['result']['old_waf_status'],
                "source": data['result']['source']
            }
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving WAF status: {e}")
        if e.response is not None:
            print(f"Response content: {e.response.text}")
        return None
 
def main():
    user = AdaptureUser('GPC', token_name='token')
    headers = user.credentials.headers
    client_name = user.client_name
    # selected_zones = [zone for zone in user.zones if zone["name"] in ['gomezcollege.shop', 'napaonline.com']]
   
    selected_zones = [
        zone
        for zone in user.zones
        if "enterprise" in zone["plan"]["name"].lower()
        and zone["account"]["name"]
        not in [
            "Omni Hotels and Resorts",
            "NFR-US-Adapture",
            "Adapturetech@gmail.com's account",
            "AMC Theatres",
            "Fossil Partners Enterprise Account",
            "Agarcia@adapture.com's Account"
        ]
    ]
 
    results = []
    for idx,zone in enumerate(selected_zones):
        print(f"processing_zone :{zone['name']} zones left: {len(user.zones) - idx} of {len(user.zones)}")
        result = get_waf_status(headers, zone['id'])
        if result:
            results.append(result)
 
    today = datetime.now()
    formatted_date = today.strftime('%b%d')      
    filename =  f"{client_name}waf_status{formatted_date}.xlsx"
   
   
    # Convert results to a DataFrame and save to Excel
    if results:
        df = pd.DataFrame(results)
        df.to_excel(filename, index= False)
        print("Results successfully saved to waf_status.xlsx")
 
if __name__ == "__main__":
    main()