# Send Transactions Script

---

## Overview

This script sends transactions to your own validator's `/receive_data` endpoint at regular intervals. It prompts you for necessary transaction details and securely handles sensitive information.

---

## Steps to Use

1. **Clone the Repository**
   - **Command:**
     ```bash
     git clone https://github.com/dnsreicht/sendTxnScript.git
     cd sendTxnScript
     ```

2. **Set Up a Virtual Environment**
   - **Commands:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   - **Note:** On Windows, activate the virtual environment using:
     ```bash
     venv\Scripts\activate
     ```

3. **Install Dependencies**
   - **Command:**
     ```bash
     pip install requests
     ```

4. **Run the Script**
   - **Command:**
     ```bash
     python3 send_transactions.py
     ```
   - **Description:** The script will prompt you for the following information:
     - **Base URL of Your Validator**
       - Example: `http://localhost:8080`
       - **Note:** No default value is provided. You must enter your own validator's base URL.
     - **ZKP Secret**
     - **Sender's Address**
     - **Sender's Private Key**
     - **Receiver's Address**
     - **Amount to Send** (must be a whole number)
     - **Denomination** (Token Ticker)
     - **Number of Times to Send the Transaction** (press Enter for infinite)

5. **Done**
   - The script will start sending transactions based on your input.
   - **Note:** You can stop it anytime by pressing `Ctrl+C`.

---

## Important Notes

- **Validator Requirement**
  - You must have your own validator running and accessible at the base URL you provide.
  - The script sends transactions to the `/receive_data` endpoint of your validator.

- **Security Considerations**
  - The script securely collects sensitive information like private keys without displaying them.
  - Ensure you run the script in a secure environment to protect your data.

- **Adjusting the Interval**
  - The script sends transactions every 5 seconds by default.
  - You can change the interval by modifying the `time.sleep(5)` line in the script.

- **Stopping the Script**
  - If running indefinitely, you can stop the script at any time by pressing `Ctrl+C`.

---


