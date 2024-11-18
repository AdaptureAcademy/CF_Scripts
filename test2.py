from cloudflarest.cloudfluser import AdaptureUser
import httpx
import pprint


def get_page_rules(zone_id, headers):
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/pagerules"
    response = httpx.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data



def main():
    user = AdaptureUser('xx',token_name='token')
    headers = user.credentials.headers
    zone = [zone for zone in user.zones if zone['name'] == 'xx']
    data = get_page_rules(zone[0]['id'],headers)
    pprint.pprint(data)
    

if __name__ == "__main__":
    main()
