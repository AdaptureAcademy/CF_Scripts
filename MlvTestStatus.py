from cloudflarest.cloudfluser import AdaptureUser
import httpx
import pandas as pd
import pprint
from datetime import datetime, timezone


def get_machine_learning_status(zone_id, headers):
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/bot_management"
    response = httpx.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data


def main():
    user = AdaptureUser('HD', token_name='token')
    client_name = user.client_name
    headers = user.credentials.headers
    results = []

    for idx,zone in enumerate(user.zones):
        ml_status = get_machine_learning_status(zone['id'], headers)
        print(f"zone: {zone['name']} zones left: {idx} of {len(user.zones)}")
        # print(zone['name'])
        # pprint.pprint(ml_status)

        # Map the fields from the response
        if ml_status and ml_status['success']:
            result = ml_status['result']
            results.append({
                'Account Name':zone['account']['name'],
                'Zone Name': zone['name'],
                'AI Bots Protection': result.get('ai_bots_protection', 'N/A'),
                'Auto Update Model': result.get('auto_update_model', 'N/A'),
                'Enable JS': result.get('enable_js', 'N/A'),
                'Suppress Session Score': result.get('suppress_session_score', 'N/A'),
                'Using Latest Model': result.get('using_latest_model', 'N/A'),
            })

    # Create a DataFrame
    df = pd.DataFrame(results)

    # Export to Excel and format output file
    today = datetime.now()
    formatted_date = today.strftime('%b%d')
    df.to_excel(f'{client_name}machine_learning_status{formatted_date}.xlsx', index=False)


if __name__ == "__main__":
    main()
