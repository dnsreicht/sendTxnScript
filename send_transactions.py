import requests
import time
import getpass

# Prompt the user for the base URL, with a default value
base_url = input("Enter the base URL (default: http://rest.synnq.io): ")
if not base_url.strip():
    base_url = "http://rest.synnq.io"

# Ensure the base_url does not end with a slash
base_url = base_url.rstrip('/')

# Construct the endpoint URL
endpoint_url = f"{base_url}/receive_data"

# Prompt the user for required information
zkp_secret = input("Enter your ZKP Secret: ")
sender_address = input("Enter the Sender's Address: ")
sender_private_key = getpass.getpass("Enter the Sender's Private Key: ")
receiver_address = input("Enter the Receiver's Address: ")

# Validate and parse the amount
while True:
    amount_input = input("Enter the Amount to Send (must be a whole number): ")
    try:
        amount = int(amount_input)
        if amount >= 0:
            break
        else:
            print("Amount must be a non-negative integer.")
    except ValueError:
        print("Invalid amount. Please enter a whole number.")

denom = input("Enter the Denomination (Token Ticker): ")

# Optional: Ask how many times to send the transaction
num_times_input = input("Enter the number of times to send the transaction (default is infinite): ")
num_times = int(num_times_input) if num_times_input.strip() else 0

# Prepare the payload
payload = {
    "secret": zkp_secret,
    "data": {
        "transaction_type": "payment",
        "sender": sender_address,
        "private_key": sender_private_key,
        "receiver": receiver_address,
        "amount": amount,
        "denom": denom,
        "fee": 1,  # Ensure fee is an integer
        "flags": 1,  # Ensure flags is an integer
        "data_type": "type_of_data",
        "data": {
            "data": "some_data" 
        },
        "metadata": {
            "meta": {
                "value": "some_metadata_value"
            }
        },
        "model_type": "default_model"
    }
}

# Print the payload for debugging purposes (optional)
# import json
# print("Payload being sent:")
# print(json.dumps(payload, indent=4))

if num_times > 0:
    for _ in range(num_times):
        try:
            response = requests.post(endpoint_url, json=payload)
            print(f"Status Code: {response.status_code}")
            print(f"Response Body: {response.text}")
        except Exception as e:
            print(f"An error occurred: {e}")
        time.sleep(5)
else:
    while True:
        try:
            response = requests.post(endpoint_url, json=payload)
            print(f"Status Code: {response.status_code}")
            print(f"Response Body: {response.text}")
        except Exception as e:
            print(f"An error occurred: {e}")
        time.sleep(5)
