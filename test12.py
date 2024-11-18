import httpx
from cloudflarest.cloudfluser import AdaptureUser
import pprint
import pandas as pd
from datetime import datetime
 
 
 
def  get_settings(zone_id,headers):
 
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/settings"
    res = httpx.get(url, headers = headers)
    if res.status_code == 200:
        response = res.json()['result']
   
    return response
 
def main():
    user = AdaptureUser('xx', token_name='token')
    headers = user.credentials.headers
    free_zones = [zone for zone in user.zones if 'free' in zone['plan']['legacy_id']]
    client_name = user.client_name
 
    results = []    
    for zone in free_zones:
        account_id = zone["account"]["id"]
        account_name = zone["account"]["name"]
        zone_id  = zone["id"]
        zone_name = zone["name"]
        print(zone["account"]["name"])
        settings = get_settings(zone["id"],headers)
        pprint.pprint(settings)
        settings_dict = {
            'Account Id': account_id,
            'Account Name' : account_name,
            'Zone Id' : zone_id,
            'Zone Name' : zone_name,
        }
        try:
            for setting in settings:
                setting_id = setting.get("id")
                setting_value = setting.get("value")
                settings_dict[setting_id] = setting_value
        except Exception as e:
            print(f"Error processing settings for zone ID {zone_id}: {e}")
   
       
        results.append(settings_dict)
        print(f"Processed zone {zone_name}")
   
 
    today = datetime.now()
    formatted_date = today.strftime('%b%d')      
    filename =  f"{client_name}settings{formatted_date}.xlsx"
   
   
    # Convert results to a DataFrame and save to Excel
    if results:
        df = pd.DataFrame(results)
        df.to_excel(filename, index= False)
        print("Results successfully saved to excel")
 
 
 
 
   
if __name__ == "__main__":
    main()
 