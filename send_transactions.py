import requests
import time
import getpass

# Prompt the user for the base URL
print("Enter the base URL of your validator.")
print("Leave blank to use the default validator at https://rest.synnq.io")
base_url = input("Base URL (e.g., http://localhost:8080): ").strip()

# Determine if the default validator is used
if not base_url:
    base_url = "https://rest.synnq.io"
    use_default_validator = True
else:
    # Remove any trailing slashes from the base URL
    base_url = base_url.rstrip('/')
    use_default_validator = False

# Construct the endpoint URL based on the validator
if use_default_validator:
    endpoint_url = f"{base_url}/transaction"  # Use /transaction endpoint for default validator
else:
    endpoint_url = f"{base_url}/receive_data"  # Use /receive_data endpoint for custom validator

# Prompt the user for required information
if not use_default_validator:
    zkp_secret = input("Enter your ZKP Secret: ").strip()
else:
    zkp_secret = None  # Not needed for default validator

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

# Prepare the payload based on the validator
if use_default_validator:
    # Payload structure for the default validator using /transaction endpoint
    payload = {
        "transaction_type": "payment",
        "sender": sender_address,
        "private_key": sender_private_key,
        "receiver": receiver_address,
        "amount": amount,
        "denom": denom,
        "flags": 1,  # Adjust as necessary
        "data_type": "storage",
        "data": {
            "key": "value"
        },
        "metadata": {
            "key": "value"
        },
        "model_type": "default_model"
    }
else:
    # Payload structure for custom validator using /receive_data endpoint (includes secret)
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
