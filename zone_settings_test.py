import httpx
from cloudflarest.cloudfluser import AdaptureUser
import pprint
import pandas as pd
from datetime import datetime
import logging  # Step 1: Import the logging module

# Step 2: Configure the logger
logging.basicConfig(
    level=logging.INFO,  # Set the minimum level of logging to INFO
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log format including timestamp, level, and message
    handlers=[
        logging.StreamHandler(),  # Output logs to the console
        logging.FileHandler("program.log", mode='w')  # Also log to a file, program.log
    ]
)

def get_settings(zone_id, headers):
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/settings"
    try:
        res = httpx.get(url, headers=headers)
        res.raise_for_status()  # Check for HTTP request errors
        if res.status_code == 200:
            response = res.json()['result']
            logging.info(f"Successfully fetched settings for zone {zone_id}")
            return response
    except httpx.RequestError as e:
        logging.error(f"Request error for zone {zone_id}: {e}")
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error for zone {zone_id}: {e}")
    except Exception as e:
        logging.error(f"Unexpected error for zone {zone_id}: {e}")
    return {}

def main():
    user = AdaptureUser('GPC', token_name='token')
    headers = user.credentials.headers
    free_zones = [zone for zone in user.zones if 'free' in zone['plan']['legacy_id']]
    client_name = user.client_name
    
    results = []
    logging.info(f"Processing {len(free_zones)} free zones")

    for zone in free_zones:
        account_id = zone["account"]["id"]
        account_name = zone["account"]["name"]
        zone_id  = zone["id"]
        zone_name = zone["name"]
        
        logging.info(f"Processing zone: {zone_name} (Account: {account_name})")
        
        settings = get_settings(zone["id"], headers)
        if not settings:
            logging.warning(f"No settings found for zone {zone_name}")
            continue  # Skip to the next zone if settings are empty
        
        settings_dict = {
            'Account Id': account_id,
            'Account Name': account_name,
            'Zone Id': zone_id,
            'Zone Name': zone_name,
        }

        try:
            for setting in settings:
                setting_id = setting.get("id")
                setting_value = setting.get("value")
                settings_dict[setting_id] = setting_value
        except Exception as e:
            logging.error(f"Error processing settings for zone {zone_id}: {e}")
        
        results.append(settings_dict)
        logging.info(f"Processed zone {zone_name}")

    if results:
        today = datetime.now()
        formatted_date = today.strftime('%b%d')      
        filename =  f"{client_name}settings{formatted_date}.xlsx"
        
        try:
            # Convert results to a DataFrame and save to Excel
            df = pd.DataFrame(results)
            df.to_excel(filename, index=False)
            logging.info(f"Results successfully saved to {filename}")
        except Exception as e:
            logging.error(f"Error saving results to Excel: {e}")
    else:
        logging.warning("No results to save to Excel")

if __name__ == "__main__":
    logging.info("Starting the program")
    main()
    logging.info("Program finished")
