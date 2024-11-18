# Import necessary modules
from cloudflarest.cloudfluser import AdaptureUser  # Importing the AdaptureUser class for Cloudflare API interactions
import httpx  # Importing httpx for making HTTP requests
import pandas as pd  # Importing pandas for data manipulation and exporting to Excel
from pprint import pprint  # Importing pprint for pretty-printing objects

# Function to retrieve settings for a given zone
def get_zone_settings(zone_id, headers):
    # Constructing the URL to fetch zone settings from the Cloudflare API
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/settings"
    # Sending a GET request to the API to retrieve zone settings
    response = httpx.get(url, headers=headers)
    # Checking if the request was successful (HTTP status code 200)
    if response.status_code == 200:
        # If successful, return the 'result' field from the JSON response
        return response.json()['result']
    else:
        # If the request failed, print an error message with the status code
        print(f"Failed to fetch settings for zone {zone_id}: {response.status_code}")
        return None  # Return None to indicate failure

# Main function to orchestrate the fetching and processing of zone settings
def main():
    # Instantiate the AdaptureUser class with required parameters (assumes valid credentials)
    user = AdaptureUser('xx', token_name='token')
    # Extract the headers needed for authentication from the user credentials
    headers = user.credentials.headers
    
    # Create a list of zones, filtering out those from specific accounts
    zones = [
        zone
        for zone in user.zones
        if zone["account"]["name"] not in [
            "Adapturetech@gmail.com's account",
            "Hmustafa@adapture.com's Account"  # Exclude specific accounts
        ]
    ]  
    
    results = []  # Initialize an empty list to hold results for each zone
    
    # Iterate over the filtered list of zones with an index starting at 1
    for idx, zone in enumerate(zones, start=1):
        # Extract relevant details about the zone and its account
        account_id = zone['account']['id']
        account_name = zone['account']['name']
        zone_id = zone['id']
        zone_name = zone['name']
        
        # Call the function to get the settings for the current zone
        settings = get_zone_settings(zone_id, headers)
        # Initialize a dictionary to store settings information for the current zone
        settings_dict = {
            'Account ID': account_id,
            'Account Name': account_name,
            'Zone ID': zone_id,
            'Zone Name': zone_name,
        }

        try:
            # Loop through the settings returned for the current zone
            for setting in settings:
                # Extract the setting ID and value
                setting_id = setting.get("id")
                setting_value = setting.get("value")
                # Add the setting ID and value to the settings dictionary
                settings_dict[setting_id] = setting_value
 
            # Append the settings dictionary to the results list
            results.append(settings_dict)
        except Exception as e:
            # Handle any exceptions that occur during processing and print an error message
            print(f"Error processing settings for zone ID {zone_id}: {e}")
            continue  # Continue to the next zone if an error occurs
 
        # Print progress for the user, indicating how many zones have been processed
        print(f"Processed zone {zone_id} ({idx}/{len(zones)})")

    # Create a DataFrame from the collected results using pandas
    df = pd.DataFrame(results)

    # Export the DataFrame to an Excel file
    output_filename = 'v2_zone_settings.xlsx'  # Define the output file name
    df.to_excel(output_filename, index=False, engine='openpyxl')  # Save DataFrame to an Excel file without the index
    print(f"Data has been exported to {output_filename}")  # Inform the user that the export is complete

# Entry point of the script
if __name__ == "__main__":
    main()  # Call the main function to execute the code
