import requests
import time
import getpass

# Prompt the user for the base URL
print("Please enter the base URL of your validator.")
base_url = input("Base URL (e.g., http://localhost:8080): ").strip()

# Ensure the base URL is provided
while not base_url:
    print("Base URL cannot be empty. Please enter a valid URL.")
    base_url = input("Base URL (e.g., http://localhost:8080): ").strip()

# Remove any trailing slashes from the base URL
base_url = base_url.rstrip('/')

# Construct the endpoint URL
endpoint_url = f"{base_url}/receive_data"

# Prompt the user for required information
zkp_secret = input("Enter your ZKP Secret: ").strip()
sender_address = input("Enter the Sender's Address: ").strip()
sender_private_key = getpass.getpass("Enter the Sender's Private Key: ").strip()
receiver_address = input("Enter the Receiver's Address: ").strip()

# Validate and parse the amount
while True:
    amount_input = input("Enter the Amount to Send (must be a whole number): ").strip()
    try:
        amount = int(amount_input)
        if amount >= 0:
            break
        else:
            print("Amount must be a non-negative integer.")
    except ValueError:
        print("Invalid amount. Please enter a whole number.")

denom = input("Enter the Denomination (Token Ticker): ").strip()

# Optional: Ask how many times to send the transaction
num_times_input = input("Enter the number of times to send the transaction (default is infinite): ").strip()
if num_times_input.isdigit():
    num_times = int(num_times_input)
else:
    num_times = 0  # Infinite loop if no valid number is provided

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
        "fee": 1,  # Adjust as necessary
        "flags": 1,  # Adjust as necessary
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

# Function to send the transaction
def send_transaction():
    try:
        response = requests.post(endpoint_url, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Sending transactions
if num_times > 0:
    for _ in range(num_times):
        send_transaction()
        time.sleep(5)
else:
    while True:
        send_transaction()
        time.sleep(5)
