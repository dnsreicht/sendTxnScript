# Send Transactions Script

**Default Base URL:** `https://rest.synnq.io`

---

## Overview

This script sends transactions to a validator's endpoint at regular intervals. It adjusts the endpoint and payload based on whether you're using the default validator (`https://rest.synnq.io`) or your own custom validator.

---

## Endpoints

- **Default Validator**
  - **Base URL:** `https://rest.synnq.io`
  - **Endpoint:** `/transaction`
  - **Method:** `POST`
  - **Description:** Submit transactions to the default validator.

- **Custom Validator**
  - **Base URL:** *Your custom validator's URL*
  - **Endpoint:** `/receive_data`
  - **Method:** `POST`
  - **Description:** Submit transactions to your custom validator.

---

## Payload Structures

### Using Default Validator (`https://rest.synnq.io`)

```json
{
  "transaction_type": "payment",
  "sender": "wallet_address",
  "private_key": "privatekey",
  "receiver": "wallet_address",
  "amount": 10,
  "denom": "ticker",
  "flags": 1,
  "data_type": "storage",
  "data": {
    "key": "value"
  },
  "metadata": {
    "key": "value"
  },
  "model_type": "default_model"
}
