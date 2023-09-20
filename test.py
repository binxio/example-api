import requests

def post_image_to_api(image_path):
    url = "http://127.0.0.1:5000"

    # Assuming the API expects the image as a multipart/form-data POST request
    with open(image_path, 'rb') as img_file:
        files = {'image': img_file}
        response = requests.post(url, files=files)

    # Check if the request was successful
    if response.status_code == 200:
        return response.json()  # Assuming the API returns JSON data
    else:
        return f"Error: Received status code {response.status_code}. Response text: {response.text}"

if __name__ == "__main__":
    result = post_image_to_api("./image01.png")
    print(result)

