import logging
from cloudflarest.cloudfluser import AdaptureUser
import httpx
import pandas as pd
import pprint
from datetime import datetime, timezone

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,  # Adjust log level as needed (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('machine_learning_status.log'),  # Logs will be saved to this file
        logging.StreamHandler()  # Logs will also be output to the console
    ]
)

# This function is being used to get the Machine Learning Status 
def get_machine_learning_status(zone_id, headers):
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/bot_management"
    try:
        response = httpx.get(url, headers=headers)
        if response.status_code == 200:
            logging.info(f"Successfully fetched machine learning status for zone {zone_id}")
            return response.json()
        else:
            logging.warning(f"Failed to fetch data for zone {zone_id}. Status Code: {response.status_code}")
            return None
    except httpx.RequestError as e:
        logging.error(f"Request error occurred for zone {zone_id}: {e}")
        return None

def main():
    # Put the client name in the place of 'xx'
    user = AdaptureUser('xx', token_name='token')
    client_name = user.client_name
    headers = user.credentials.headers
    results = []

    logging.info(f"Starting to fetch machine learning status for client: {client_name}")

    for idx, zone in enumerate(user.zones, start=1):
        logging.debug(f"Processing zone: {zone['name']} ({idx} of {len(user.zones)})")
        ml_status = get_machine_learning_status(zone['id'], headers)
        
        # Log zone processing details
        logging.debug(f"Zone {zone['name']} status: {ml_status}")
        
        # Map the fields from the response
        if ml_status and ml_status['success']:
            result = ml_status['result']
            results.append({
                'Account Name': zone['account']['name'],
                'Zone Name': zone['name'],
                'AI Bots Protection': result.get('ai_bots_protection', 'N/A'),
                'Auto Update Model': result.get('auto_update_model', 'N/A'),
                'Enable JS': result.get('enable_js', 'N/A'),
                'Suppress Session Score': result.get('suppress_session_score', 'N/A'),
                'Using Latest Model': result.get('using_latest_model', 'N/A'),
            })
            logging.info(f"Successfully processed zone: {zone['name']}")
        else:
            logging.warning(f"Skipping zone {zone['name']} due to failed status retrieval")

    if results:
        # Create a DataFrame
        df = pd.DataFrame(results)
        # Export to Excel and format output file
        today = datetime.now()
        formatted_date = today.strftime('%b%d')
        output_file = f'{client_name}machine_learning_status{formatted_date}.xlsx'
        df.to_excel(output_file, index=False)
        logging.info(f"Results exported to {output_file}")
    else:
        logging.warning("No data to export. No valid results fetched.")

if __name__ == "__main__":
    main()
