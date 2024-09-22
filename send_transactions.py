import requests
import time
import getpass
import uuid
from urllib.parse import urlparse
import logging
import json
from decimal import Decimal, InvalidOperation

class TransactionSender:
    def __init__(self, config):
        self.config = config
        self.session = self._setup_session()
        self.logger = self._setup_logging()
        self.zkp_secret = self.generate_zkp_secret()

    def _setup_logging(self):
        logger = logging.getLogger('TransactionSender')
        logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        fh = logging.FileHandler("send_transactions.log")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        logger.propagate = False

        return logger

    def _setup_session(self):
        session = requests.Session()
        retries = requests.adapters.Retry(
            total=5,
            backoff_factor=1,
            status_forcelist=[500, 502, 503, 504]
        )
        adapter = requests.adapters.HTTPAdapter(max_retries=retries)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    def generate_zkp_secret(self):
        secret = str(uuid.uuid4())
        try:
            response = self.session.post("https://zkp.synnq.io/generate", json={"secret": secret})
            if response.status_code == 200:
                self.logger.info("ZKP Secret generated successfully.")
                return secret
            else:
                self.logger.error(f"Failed to generate ZKP Secret. Status Code: {response.status_code}")
                self.logger.error(f"Response: {response.text}")
                return None
        except Exception as e:
            self.logger.error(f"Error generating ZKP Secret: {e}")
            return None

    def get_node_id(self):
        nodes_endpoint = "https://node.synnq.io/nodes"
        try:
            response = self.session.get(nodes_endpoint)
            if response.status_code == 200:
                nodes = response.json()
                host = urlparse(self.config['base_url']).netloc or self.config['base_url'].rstrip('/')
                for node in nodes:
                    if node.get("address") == host:
                        node_id = node.get("id")
                        if node_id:
                            self.logger.info(f"Node ID retrieved: {node_id}")
                            return node_id
                self.logger.warning(f"No node found with address matching {host}. Using default endpoint.")
                return None
            else:
                self.logger.error(f"Failed to retrieve Node ID. Status Code: {response.status_code}")
                self.logger.error(f"Response: {response.text}")
                return None
        except Exception as e:
            self.logger.error(f"Error retrieving Node ID: {e}")
            return None

    def map_transaction_type_to_data_type(self, transaction_type):
        mapping = {
            "payment": "type_of_data",
            "storage": "storage"
        }
        return mapping.get(transaction_type, "type_of_data")

    def construct_payload(self, node_id):
        transaction_type = self.config.get('payment')
        if node_id:
            payload = {
                "secret": self.zkp_secret,
                "data": {
                    "transaction_type": "payment",
                    "sender": self.config['sender_address'],
                    "private_key": self.config['sender_private_key'],
                    "receiver": self.config['receiver_address'],
                    "amount": (self.config['amount']),
                    "denom": self.config['denom'],
                    "flags": 1,
                    "fee": 1,
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
        else:
            payload = {
                "secret": self.zkp_secret,
                "transaction_type": "payment",
                "sender": self.config['sender_address'],
                "private_key": self.config['sender_private_key'],
                "receiver": self.config['receiver_address'],
                "amount": (self.config['amount']),
                "denom": self.config['denom'],
                "flags": 1,
                "fee": 1,
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
        return payload

    def mask_sensitive_data(self, payload):
        masked_payload = json.loads(json.dumps(payload))
        if 'private_key' in masked_payload:
            masked_payload['private_key'] = "*****"
        elif 'data' in masked_payload and 'private_key' in masked_payload['data']:
            masked_payload['data']['private_key'] = "*****"
        return masked_payload

    def send_transaction(self, endpoint, payload, fallback_endpoint=None, fallback_payload=None):
        try:
            self.logger.debug(f"Payload being sent: {json.dumps(self.mask_sensitive_data(payload), indent=4)}")
            response = self.session.post(endpoint, json=payload)
            if response.status_code in [200, 201]:
                self.logger.info(f"Transaction successful. Status Code: {response.status_code}")
                try:
                    response_json = response.json()
                    pretty_response = json.dumps(response_json, indent=4)
                    self.logger.info(f"Response:\n{pretty_response}")
                except ValueError:
                    self.logger.info(f"Response: {response.text}")
            else:
                self.logger.error(f"Failed to send transaction. Status Code: {response.status_code}")
                try:
                    response_json = response.json()
                    pretty_response = json.dumps(response_json, indent=4)
                    self.logger.error(f"Response:\n{pretty_response}")
                except ValueError:
                    self.logger.error(f"Response: {response.text}")
                if fallback_endpoint and fallback_payload:
                    self.logger.info("Attempting to send transaction to fallback endpoint...")
                    self.send_transaction(fallback_endpoint, fallback_payload)
        except Exception as e:
            self.logger.error(f"Error sending transaction: {e}")
            if fallback_endpoint and fallback_payload:
                self.logger.info("Attempting to send transaction to fallback endpoint...")
                self.send_transaction(fallback_endpoint, fallback_payload)

    def run(self):
        node_id = self.get_node_id()

        if node_id:
            primary_endpoint = f"{self.config['base_url']}/receive_data"
            fallback_endpoint = "https://node.synnq.io/receive_data"
            self.logger.info("Using custom validator endpoint.")
        else:
            primary_endpoint = "https://rest.synnq.io/transaction"
            fallback_endpoint = None
            self.logger.info("Using default validator endpoint: https://rest.synnq.io/transaction")

        primary_payload = self.construct_payload(node_id)
        fallback_payload = self.construct_payload(None) if node_id else None

        num_times = self.config.get('num_times', 1)
        count = 1

        while num_times == 0 or count <= num_times:
            target = f"Node ID: {node_id}" if node_id else "https://rest.synnq.io/transaction"
            self.logger.info(f"Sending transaction {count}{'/' + str(num_times) if num_times else ''} to {target}...")
            self.send_transaction(primary_endpoint, primary_payload, fallback_endpoint, fallback_payload)
            count += 1
            time.sleep(self.config.get('interval', 5))

def get_user_input():
    print("Enter the base URL of your validator.")
    print("Leave blank to use the default validator at https://rest.synnq.io")
    base_url = input("Base URL (e.g., http://localhost:8080): ").strip() or "https://rest.synnq.io"
    use_custom_validator = base_url != "https://rest.synnq.io"

    sender_address = input("Enter the Sender's Address: ").strip()
    sender_private_key = getpass.getpass("Enter the Sender's Private Key: ").strip()
    receiver_address = input("Enter the Receiver's Address: ").strip()

    while True:
        try:
            amount_input = input("Enter the Amount to Send (whole number only): ").strip()
            amount = int(amount_input)
            if amount > 0:
                break
            else:
                print("Amount must be a non-negative number.")
        except InvalidOperation:
            print("Invalid amount. Please enter a valid number.")

    denom = input("Enter the Denomination (Token Ticker): ").strip()

    num_times_input = input("Enter the number of times to send the transaction (default is 1): ").strip()
    num_times = int(num_times_input) if num_times_input.isdigit() else 1

    return {
        "base_url": base_url,
        "use_custom_validator": use_custom_validator,
        "sender_address": sender_address,
        "sender_private_key": sender_private_key,
        "receiver_address": receiver_address,
        "amount": amount,
        "denom": denom,
        "num_times": num_times,
        "interval": 0.1,
    }

if __name__ == "__main__":
    config = get_user_input()
    sender = TransactionSender(config)
    if sender.zkp_secret:
        sender.run()
    else:
        print("Failed to generate ZKP Secret. Exiting.")
