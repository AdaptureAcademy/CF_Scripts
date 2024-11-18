from cloudflarest.cloudfluser import AdaptureUser
import httpx
import pprint
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
    user = AdaptureUser('xx', token_name='token')
    headers = user.credentials.headers
    zone = [zone for zone in user.zones if zone['name'] == 'xx']
    
    if not zone:
        print("No zone found with the specified name.")
        return
    
    data = get_page_rules(zone[0]['id'], headers)
    
    if data and data.get('success'):
        rules = data['result']
        # Prepare data for DataFrame
        rows = []
        for rule in rules:
            for action in rule.get('actions', []):
                for target in rule.get('targets', []):
                    rows.append({
                        'Zone Name':zone[0]['name'],
                        'Zone ID':zone[0]['id'],
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

        # Create a DataFrame
        df = pd.DataFrame(rows)

        # Export to Excel
        excel_filename = "page_rules.xlsx"
        df.to_excel(excel_filename, index=False)
        print(f"Exported page rules to {excel_filename}")
    else:
        print("No successful response or no rules found.")

if __name__ == "__main__":
    main()
