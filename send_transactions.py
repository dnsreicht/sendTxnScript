import requests
import time
import getpass
import uuid
from urllib.parse import urlparse

# Function to generate ZKP secret
def generate_zkp_secret():
    generated_secret = str(uuid.uuid4())
    zkp_payload = {"secret": generated_secret}
    try:
        response = requests.post("https://zkp.synnq.io/generate", json=zkp_payload)
        if response.status_code == 200:
            print("ZKP Secret generated successfully.")
            return generated_secret
        else:
            print(f"Failed to generate ZKP Secret. Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"An error occurred while generating ZKP Secret: {e}")
        return None

# Function to retrieve node ID based on matching address and validator type
def get_node_id(base_url, is_default_validator):
    try:
        # Nodes endpoint is the same for both validators as per your latest input
        nodes_endpoint = "https://node.synnq.io/nodes"
        
        # Fetch the nodes list from the endpoint
        response = requests.get(nodes_endpoint)
        if response.status_code == 200:
            nodes = response.json()
            if isinstance(nodes, list) and len(nodes) > 0:
                # Parse the base URL to extract the network location (netloc)
                parsed_url = urlparse(base_url)
                host_port = parsed_url.netloc if parsed_url.netloc else base_url.rstrip('/')

                # Iterate through the list to find a matching address
                for node in nodes:
                    if node.get("address") == host_port:
                        node_id = node.get("id")
                        if node_id:
                            print(f"Node ID retrieved: {node_id}")
                            return node_id
                        else:
                            print(f"Node with address {host_port} does not have an 'id'.")
                            return None
                # If no matching address is found
                print(f"No node found with address matching {host_port}.")
                return None
            else:
                print("No nodes found in the response.")
                return None
        else:
            print(f"Failed to retrieve Node ID. Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"An error occurred while retrieving Node ID: {e}")
        return None

# Function to send transaction with optional fallback
def send_transaction(endpoint, payload, fallback_endpoint=None, fallback_payload=None):
    try:
        response = requests.post(endpoint, json=payload)
        if response.status_code in [200, 201]:
            print(f"Transaction successful. Status Code: {response.status_code}")
            print(f"Response Body: {response.text}")
        else:
            print(f"Failed to send transaction. Status Code: {response.status_code}")
            print(f"Response Body: {response.text}")
            # If fallback is provided, attempt to send to fallback
            if fallback_endpoint and fallback_payload:
                print("Attempting to send transaction to fallback endpoint...")
                fallback_response = requests.post(fallback_endpoint, json=fallback_payload)
                if fallback_response.status_code in [200, 201]:
                    print(f"Fallback Transaction successful. Status Code: {fallback_response.status_code}")
                    print(f"Response Body: {fallback_response.text}")
                else:
                    print(f"Fallback Transaction failed. Status Code: {fallback_response.status_code}")
                    print(f"Response Body: {fallback_response.text}")
    except Exception as e:
        print(f"An error occurred while sending transaction: {e}")
        # If fallback is provided, attempt to send to fallback
        if fallback_endpoint and fallback_payload:
            try:
                print("Attempting to send transaction to fallback endpoint...")
                fallback_response = requests.post(fallback_endpoint, json=fallback_payload)
                if fallback_response.status_code in [200, 201]:
                    print(f"Fallback Transaction successful. Status Code: {fallback_response.status_code}")
                    print(f"Response Body: {fallback_response.text}")
                else:
                    print(f"Fallback Transaction failed. Status Code: {fallback_response.status_code}")
                    print(f"Response Body: {fallback_response.text}")
            except Exception as fallback_e:
                print(f"An error occurred while sending fallback transaction: {fallback_e}")

# Function to construct payload for custom validator
def construct_custom_validator_payload(zkp_secret, sender_address, sender_private_key, receiver_address, amount, denom, node_id=None):
    payload = {
        "secret": zkp_secret,
        "data": {
            "transaction_type": "payment",
            "sender": sender_address,
            "private_key": sender_private_key,
            "receiver": receiver_address,
            "amount": amount,
            "denom": denom,
            "fee": 1,
            "flags": 1,
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
    if node_id:
        payload["data"]["node_id"] = node_id
    return payload

# Function to construct payload for default validator
def construct_default_validator_payload(zkp_secret, sender_address, sender_private_key, receiver_address, amount, denom, node_id=None):
    payload = {
        "secret": zkp_secret,
        "transaction_type": "payment",
        "sender": sender_address,
        "private_key": sender_private_key,
        "receiver": receiver_address,
        "amount": amount,
        "denom": denom,
        "flags": 1,
        "data_type": "storage",
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
    if node_id:
        payload["node_id"] = node_id
    return payload

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

# Construct the primary and fallback endpoint URLs based on the validator
if use_default_validator:
    primary_endpoint = f"{base_url}/transaction"  # Use /transaction endpoint for default validator
    fallback_endpoint = "https://node.synnq.io/transaction"  # Fallback URL for default validator
else:
    primary_endpoint = f"{base_url}/receive_data"  # Use /receive_data endpoint for custom validator
    fallback_endpoint = "https://node.synnq.io/receive_data"  # Fallback URL for custom validator

# Initialize fallback_payload to None to prevent NameError
fallback_payload = None

# Retrieve Node ID
node_id = get_node_id(base_url, use_default_validator)
if not node_id:
    # Prompt the user to proceed without node_id
    proceed = input("No Matching ID found, do you want to proceed without a Node ID? (yes/no): ").strip().lower()
    if proceed in ['yes', 'y']:
        node_id = None  # Explicitly set node_id to None
        # When proceeding without node_id, transactions should be sent to fallback_endpoint directly
        # No further fallback is needed
    else:
        print("Cannot proceed without a valid Node ID.")
        exit(1)

# Generate ZKP Secret (always generate)
zkp_secret = generate_zkp_secret()
if not zkp_secret:
    print("Cannot proceed without a valid ZKP Secret.")
    exit(1)

# Prompt the user for required information
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

# Prepare the payload based on the validator type
if use_default_validator:
    # Payload structure for the default validator using /transaction endpoint
    payload = construct_default_validator_payload(
        zkp_secret,
        sender_address,
        sender_private_key,
        receiver_address,
        amount,
        denom,
        node_id
    )
    # Prepare fallback payload (same as primary for default validator)
    fallback_payload = payload.copy()
else:
    # Payload structure for custom validator using /receive_data endpoint (includes secret)
    payload = construct_custom_validator_payload(
        zkp_secret,
        sender_address,
        sender_private_key,
        receiver_address,
        amount,
        denom,
        node_id
    )
    # Prepare fallback payload (same structure as primary)
    if node_id:
        fallback_payload = construct_custom_validator_payload(
            zkp_secret,
            sender_address,
            sender_private_key,
            receiver_address,
            amount,
            denom,
            node_id
        )
    else:
        # If no node_id, fallback_payload can be the same as payload
        fallback_payload = payload.copy()

# If no node_id is found and proceeding, set fallback_payload to None
if not node_id:
    fallback_payload = None

# Function to send transaction with proper payload
def send_transaction_wrapper():
    try:
        if node_id:
            # If node_id is available, send to primary_endpoint with node_id
            transaction_target = node_id
        else:
            # If no node_id, send to fallback_endpoint
            transaction_target = fallback_endpoint.split('/')[2]  # Extract base URL without path
        print(f"\nSending transaction to {transaction_target}...")
        send_transaction(primary_endpoint, payload, fallback_endpoint, fallback_payload)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        # As per user request, if fallback_payload is not defined, send to rest.synnq.io
        if 'fallback_payload' not in locals() or fallback_payload is None:
            print("Sending transaction to https://rest.synnq.io as a final fallback.")
            rest_endpoint = "https://rest.synnq.io/transaction"
            # Construct payload for rest.synnq.io
            rest_payload = {
                "secret": zkp_secret,
                "transaction_type": "payment",
                "sender": sender_address,
                "private_key": sender_private_key,
                "receiver": receiver_address,
                "amount": amount,
                "denom": denom,
                "flags": 1,
                "data_type": "storage",
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
            if node_id:
                rest_payload["node_id"] = node_id
            try:
                rest_response = requests.post(rest_endpoint, json=rest_payload)
                if rest_response.status_code in [200, 201]:
                    print(f"Final Fallback Transaction successful. Status Code: {rest_response.status_code}")
                    print(f"Response Body: {rest_response.text}")
                else:
                    print(f"Final Fallback Transaction failed. Status Code: {rest_response.status_code}")
                    print(f"Response Body: {rest_response.text}")
            except Exception as rest_e:
                print(f"An error occurred while sending final fallback transaction: {rest_e}")

# Sending transactions
if num_times > 0:
    for i in range(num_times):
        print(f"\nSending transaction {i+1}/{num_times} to {'Node ID: ' + node_id if node_id else 'https://node.synnq.io'}...")
        send_transaction_wrapper()
        time.sleep(5)
else:
    count = 1
    while True:
        print(f"\nSending transaction {count} to {'Node ID: ' + node_id if node_id else 'https://node.synnq.io'}...")
        send_transaction_wrapper()
        count += 1
        time.sleep(5)
