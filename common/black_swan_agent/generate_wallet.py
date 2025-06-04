from solders.keypair import Keypair
import json
import os

# Generate a new keypair
keypair = Keypair()

# Serialize the secret key to a list of integers
secret = list(bytes(keypair))

# Define the wallet path
wallet_path = os.path.expanduser("~/.config/solana")
os.makedirs(wallet_path, exist_ok=True)

# Save the secret key to a JSON file
with open(os.path.join(wallet_path, "id.json"), "w") as f:
    json.dump(secret, f)

# Print the public key
print("Public Key:", keypair.pubkey())

