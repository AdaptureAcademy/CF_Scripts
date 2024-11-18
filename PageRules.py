from cloudflarest.cloudfluser import AdaptureUser
import httpx
import pandas as pd

def get_page_rules(zone_id, headers):
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/pagerules"
    response = httpx.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Failed to fetch page rules:", response.status_code, response.text)
        return None

def main():
    # Replace the xx with the name of the client
    user = AdaptureUser('xx', token_name='token')
    headers = user.credentials.headers
    
    # List of zone names to retrieve page rules for , replace the 'xx' with the name of the zone you want to fetch the data for
    zone_names = ['xx', 'xx']
    all_rows = []  # To store data for all zones

    for zone_name in zone_names:
        # Find the zone by name
        zone = [zone for zone in user.zones if zone['name'] == zone_name]
        
        if not zone:
            print(f"No zone found with the specified name: {zone_name}.")
            continue  # Skip to the next zone if not found
        
        data = get_page_rules(zone[0]['id'], headers)
        
        if data and data.get('success'):
            rules = data['result']
            # Prepare data for DataFrame
            for rule in rules:
                for action in rule.get('actions', []):
                    for target in rule.get('targets', []):
                        all_rows.append({
                            'Zone Name': zone[0]['name'],
                            'Zone ID': zone[0]['id'],
                            'Rule ID': rule['id'],
                            'Status': rule['status'],
                            'Priority': rule['priority'],
                            'Action ID': action['id'],
                            'Action Value': action['value'],
                            'Target': target['target'],
                            'Operator': target['constraint']['operator'],
                            'Target Value': target['constraint']['value'],
                            'Created On': rule['created_on'],
                            'Modified On': rule['modified_on'],
                        })

    if all_rows:
        # Create a DataFrame
        df = pd.DataFrame(all_rows)

        # Export to Excel
        excel_filename = "page_rules.xlsx"
        df.to_excel(excel_filename, index=False)
        print(f"Exported page rules to {excel_filename}")
    else:
        print("No successful responses or no rules found for the specified zones.")

if __name__ == "__main__":
    main()
