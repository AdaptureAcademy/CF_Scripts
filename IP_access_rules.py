import httpx
import pandas as pd
from cloudflarest.cloudfluser import AdaptureUser

# Function to retrieve all IP access rules for a given zone, handling pagination
def get_all_ip_access_rules(zone_id, headers, per_page=20):
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/firewall/access_rules/rules?per_page={per_page}"
    
    all_rules = []  # List to hold all IP access rules
    page_number = 1  # Start with the first page
    
    while True:
        print(f"Fetching page {page_number}...")
        
        # Make the API request to get the current page of results
        response = httpx.get(url, headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            rules_on_page = data['result']
            all_rules.extend(rules_on_page)  # Add the rules of the current page to the all_rules list
            
            # Debugging information: Print the number of rules fetched
            print(f"Fetched {len(rules_on_page)} rules from page {page_number}")
            print(f"Total rules fetched so far: {len(all_rules)}")
            
            # Check if there are more pages
            total_pages = data['result_info'].get('total_pages')
            
            if page_number < total_pages:
                # Update the URL to fetch the next page
                page_number += 1  # Increment the page number
                # Dynamically modify the URL to fetch the next page
                url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/firewall/access_rules/rules?per_page={per_page}&page={page_number}"
            else:
                # No more pages, we have all the rules
                print(f"All IP access rules fetched: {len(all_rules)}")
                break
        else:
            # Handle errors and print status code
            print(f"Failed to fetch IP access rules for zone {zone_id}: {response.status_code}, {response.text}")
            break  # Exit the loop if there's an error
    
    return all_rules

# Function to save the IP access rules to an Excel file
def save_to_excel(data, filename='ip_access_rules_zone.xlsx'):
    if data:
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False)
        print(f"Data saved to {filename}")
    else:
        print("No data to save to Excel.")

# Main function to orchestrate fetching and processing IP access rules for a zone
def main():
    user = AdaptureUser('NCR', token_name='token')  # Replace 'xx' with your actual token name
    headers = user.credentials.headers
    
    # Example zone ID - replace with your actual zone ID
    zone_id = '9376cfbacd66a75f0072bb5c42ff11f7'  # Replace with your actual zone ID
    
    # Get all the IP access rules for the given zone
    ip_access_rules = get_all_ip_access_rules(zone_id, headers)
    
    # Save the IP access rules to an Excel file
    save_to_excel(ip_access_rules)

# Run the script
if __name__ == "__main__":
    main()
