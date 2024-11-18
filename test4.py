from cloudflarest.cloudfluser import AdaptureUser
import httpx


def get_zones(zone_id, headers):
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}"
    response = httpx.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Failed to retrieve zone {zone_id}: {response.status_code}")
        return None

def main():
    # Put the client name in the place of 'xx'
    user = AdaptureUser('GPC', token_name='token')
    client_name = user.client_name
    headers = user.credentials.headers
    # results = []

    # Get only the first 10 zones
    for idx, zone in enumerate(user.zones[:10], start=1):  # Limit to the first 10 zones
        zones = get_zones(zone['id'], headers)
        if zones:
            print(f"zone: {zone['name']} zones left: {idx} of {len(user.zones[:10])}")

if __name__ == "__main__":
    from pprint import pprint
    user = AdaptureUser('GPC', token_name='token')
    # main()
    pprint(user.zones)
