import requests


url = "http://127.0.0.1:5000/predict_image"


files = {
    "image": open(
        "test_image.jpg",
        "rb"
    )
}


response = requests.post(
    url,
    files=files
)


print("Status Code:")
print(response.status_code)


print("\nResponse:")
print(response.text)