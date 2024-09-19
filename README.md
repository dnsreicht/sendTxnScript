# Send Transactions Script

**Base URL:** `http://rest.synnq.io`

---

## Overview

This script sends transactions to a server endpoint at regular intervals. It prompts the user for necessary transaction details and securely handles sensitive information.

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
     - **Base URL** (press Enter to use default: `http://rest.synnq.io`)
     - **ZKP Secret**
     - **Sender's Address**
     - **Sender's Private Key**
     - **Receiver's Address**
     - **Amount to Send** (must be a whole number)
     - **Denomination** (Token Ticker)
     - **Number of Times to Send the Transaction** (press Enter for infinite)

5. **Done**
   - The script will start sending transactions based on your input. You can stop it anytime by pressing `Ctrl+C`.

---


