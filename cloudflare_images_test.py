import httpx
from cloudflarest.cloudfluser import AdaptureUser
from pprint import pprint

def get_batch_token(account_id, headers):
    url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/images/v1/batch_token"
    res = httpx.get(url, headers=headers)
    if res.status_code == 200:
        response = res.json()
    elif res.status_code == 403:
        response = res.json()
        print(f"\nError Code: {response['errors'][0]['code']} Message: {response['errors'][0]['message']}")
        return
    else:
        print(f"Error fetching Images for account {account_id}")
        response = []
    return response

# Function to get the settings of a Cloudflare zone
def get_account_images(account_id, headers):
    url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/images/v1"
    res = httpx.get(url, headers=headers)
    if res.status_code == 200:
        response = res.json()
    else:
        print(f"Error fetching Images for account {account_id}")
        response = []
    return response




def post_account_images(account_id, headers, image_path, metadata=None, require_signed_urls=False, url=None):
    
    url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/images/v1"
    
    # Ensure the image exists
    try:
        with open(image_path, 'rb') as image_file:
            files = {'file': image_file}
            
            # Prepare the metadata as form fields, if provided
            form_data = {
                'metadata': metadata if metadata else '',
                'requireSignedURLs': str(require_signed_urls).lower(),
                'url': url if url else ''
            }
            
            # Send the POST request to Cloudflare Image API
            response = httpx.post(url, headers=headers, files=files, data=form_data)
            
            # Check if the response is successful
            if response.status_code == 200:
                print(f"Image uploaded successfully to account {account_id}")
                return response.json()  # Return the response JSON if successful
            else:
                print(f"Failed to upload image. Status Code: {response.status_code}")
                print(response.text)  # Print the error message for debugging
                return None
    except FileNotFoundError:
        print(f"Error: The file at {image_path} was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def main():
    user = AdaptureUser('GPC', token_name='token')
    headers = user.credentials.headers
    # ce1bb47d4c5f685f3d9d4e7be1a4836d
    image_path = r"C:\Users\Hassan Mustafa\Desktop\repos\PageRules\dog.jpg"
    selected_account = [account for account in user.accounts if account['id'] == 'ce1bb47d4c5f685f3d9d4e7be1a4836d']
    for account in selected_account:
        account_id = account['id']
        token = get_batch_token(account_id, headers)
        if token:
            post_account_images(account_id,headers,image_path)
            images = get_account_images(account_id,headers)
            pprint(images)
        
        print("No token Found")


        
# Run the script
if __name__ == "__main__":
    main()
