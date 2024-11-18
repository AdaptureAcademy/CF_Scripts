import httpx

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
