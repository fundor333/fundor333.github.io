import requests

url_api = "http://fundor333.com/pantalone/genera-spese"

# Call the API to generate expenses
response = requests.get(url_api)
if response.status_code == 200:
    print("Expenses generated successfully.")
else:
    print(f"Failed to generate expenses. Status code: {response.status_code}")
    # raise an error for the github action to fail

    raise Exception(f"API call failed with status code: {response.status_code}\n")
