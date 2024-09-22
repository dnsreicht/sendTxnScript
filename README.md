# Transaction Sender

# Transaction Sender

A Python script to automate sending transactions to a validator API. It incorporates Zero-Knowledge Proof (ZKP) secret generation, node ID retrieval, and supports both custom and default validator endpoints with options for `"payment"` and `"storage"` transaction types.

## Prompts

- **Base URL**: Enter your validator's base URL or leave blank to use the default (`https://rest.synnq.io`).
- **Sender's Address**: Your wallet address.
- **Sender's Private Key**: Your private key (input is hidden for security).
- **Receiver's Address**: Recipient's wallet address.
- **Amount to Send**: Enter a whole number (e.g., `100`).
- **Denomination**: Token ticker (e.g., `scam`).
- **Number of Transactions**: How many times to send the transaction (default is `1`).

## How It Works

### Initialization

The script initializes by setting up the HTTP session with retry mechanisms and configuring the logging system to handle different log levels for the console and log files.

### ZKP Secret Generation

- Generates a unique UUID as the ZKP secret.
- Sends a POST request to `https://zkp.synnq.io/generate` with the secret.
- Logs the success or failure of the secret generation.

### Node ID Retrieval

- Sends a GET request to `https://node.synnq.io/nodes` to retrieve a list of nodes.
- Parses the list to find a node that matches the provided validator base URL.
- If found, retrieves and logs the Node ID; otherwise, defaults to the standard endpoint.

### Payload Construction

- Constructs the transaction payload based on whether a Node ID was retrieved.
- Includes necessary transaction details such as sender, receiver, amount, denomination, and transaction type.

### Transaction Sending

- Sends the constructed payload to the appropriate endpoint.

### Logging

- Logs essential information and errors to both the console and a log file (`send_transactions.log`).

## Configuration

All configurations are handled interactively through user prompts. Ensure you provide accurate information to avoid transaction failures.

## Logging

- **Console**: Displays `INFO` level logs for transaction status and general information.

## Installation

1. **Clone the Repository**
    ```bash
    git clone https://github.com/dnsreicht/sendTxnScript.git
    cd sendTxnScript
    ```

2. **Create a Virtual Environment (Optional but Recommended)**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install Dependencies**
    ```bash
    pip install requests

## Usage

Run the script and follow the prompts:

```bash
python3 send_transactions.py


