from web3 import Web3
from config import INFURA_URL, PRIVATE_KEY, CONTRACT_ADDRESS, CHAIN_ID

w3 = Web3(Web3.HTTPProvider(INFURA_URL))
account = w3.eth.account.from_key(PRIVATE_KEY)
contract_abi = [ /* ה־ABI של ה־NFT contract שלך */ ]
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)

def mint_nft(to_address: str, token_uri: str) -> str:
    nonce = w3.eth.get_transaction_count(account.address)
    tx = contract.functions.mint(to_address, token_uri).build_transaction({
        "chainId": CHAIN_ID,
        "gas": 300_000,
        "gasPrice": w3.to_wei('50', 'gwei'),
        "nonce": nonce,
    })
    signed = account.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
    return w3.to_hex(tx_hash)
