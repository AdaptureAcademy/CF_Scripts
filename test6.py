from cloudflarest.cloudfluser import AdaptureUser
import httpx


def get_account_members(account_id, headers):
    url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/members"
    response = httpx.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()['result']
        return data
    else:
        print(f"Failed to retrieve zone {account_id}: {response.status_code}")
        return None

# def main():
#     # Put the client name in the place of 'xx'
#     user = AdaptureUser('GPC', token_name='token')
#     client_name = user.client_name
#     headers = user.credentials.headers
#     # results = []

#     # Get only the first 10 zones
#     # for idx, zone in enumerate(user.zones[:10], start=1):  # Limit to the first 10 zones
#     #     zones = get_zones(zone['id'], headers)
#     #     if zones:
#     #         print(f"zone: {zone['name']} zones left: {idx} of {len(user.zones[:10])}")

if __name__ == "__main__":
    from pprint import pprint
    user = AdaptureUser('GPC', token_name='token')
    all_members = []
    for account in user.accounts:
        members = get_account_members(account['id'],headers = user.credentials.headers)
        for member in members:
            pprint(member)
            input()
        all_members.extend(members)
    pprint(all_members)     
        
    # main()
    # pprint(user.zones)
