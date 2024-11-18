from cloudflarest.cloudfluser import AdaptureUser
import httpx
from pprint import pprint


def get_account_rulesets(account_id, headers):
    url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/rulesets"
    response = httpx.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Failed to retrieve account rulesets for {account_id}: {response.status_code} - {response.text}")
        return None
    

def main():
    # Initialize the user with your token name
    user = AdaptureUser('GPC', token_name='token')
    headers = user.credentials.headers

    # Replace 'your_account_id' with the actual account ID you want to query
    account_id = '2d68f563bf568e9a368f7d726981f7c2'
    
    # Fetch the rulesets for the specified account ID
    data = get_account_rulesets(account_id=account_id, headers=headers)
    
    # Print the retrieved data in a pretty format
    pprint(data)

# Entry point for the script
if __name__ == "__main__":
    main()
