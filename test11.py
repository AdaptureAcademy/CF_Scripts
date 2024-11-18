from cloudflarest.cloudfluser import AdaptureUser
import httpx
import pandas as pd
from pprint import pprint


    
def main():
    # Assuming `user` is already instantiated correctly and `zones` is populated
    user = AdaptureUser('GPC', token_name='token')
    headers = user.credentials.headers
    # Get all zones
    zones_free = [
          zone
          for zone in user.zones
          if "free" in zone["plan"]["name"].lower() 
          
    ]
    
    zones_enterprise = [
          zone
          for zone in user.zones
          if "enterprise" in zone["plan"]["name"].lower()
        ]
    

    print(f"Number of free zones :{len(zones_free)}")
    print(f"Number of enterprise zones: {len(zones_enterprise)}")

    

if __name__ == "__main__":
    main()

