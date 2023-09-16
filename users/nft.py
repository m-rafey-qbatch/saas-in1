import os
import secrets
from dotenv import load_dotenv
from thirdweb import ThirdwebSDK
from thirdweb.types import SDKOptions
from eth_account import Account
from web3 import Web3
from thirdweb import ThirdwebSDK
from thirdweb.types.nft import NFTMetadataInput
from thirdweb.types.sdk import SDKOptions, GasSettings, GasSpeed
from thirdweb.types import SDKOptions

# Load the .env file from the 'battle-website' directory
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Access the environment variables
THIRDWEB_API_KEY = os.getenv('THIRDWEB_API_KEY')
PRIVATE_KEY = os.getenv('PRIVATE_KEY')
CLIENT_ID = os.getenv('CLIENT_ID')

# Generating a random hexadecimal string and storing it in priv variable
priv = secrets.token_hex(32)
# Attaching 0x prefix to our 64 character hexadecimal string stored in priv and storing the new string in variable private_key.
private_key = "0x" + priv
# Creating a new account using the private_key and storing it in variable acct
wallet_account = Account.from_key(private_key)
# Get the Ethereum wallet address from the Account instance
wallet_address = wallet_account.address

# Create the gas settings with your desired values
gas_settings = GasSettings(max_price_in_gwei=300000000000, speed=GasSpeed.FAST)

# Create SDK options with the gas settings
options = SDKOptions(gas_settings=gas_settings)

# Create a valid signer using your private key
signer = Account.from_key(PRIVATE_KEY)

# Create the SDK
print("Creating SDK...")
sdk = ThirdwebSDK("goerli", options=SDKOptions(secret_key=THIRDWEB_API_KEY))
print("SDK created.")

sdk.update_signer(signer)


contract = sdk.get_contract("0xACC9F82e68611630B718D646951538C81b7a57ab")

image_path = "/Users/shanesmainaccount/Desktop/battlenyc/battle-website/media/nft_images/apple-edtech-logo.png"

metadata = NFTMetadataInput.from_json({
    "name": "Cool NFT",
    "description": "This is a cool NFT",
    "image": open(image_path, "rb"),
})

print("Minting NFT...")
tx = contract.erc721.mint_to(wallet_address, metadata)
print("NFT minted successfully.")
receipt = tx.receipt
token_id = tx.id
nft = tx.data()

print("Transaction Receipt:")
print(receipt)
print("NFT Token ID:", token_id)
print("NFT Data:", nft)
