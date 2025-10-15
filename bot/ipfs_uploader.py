import ipfshttpclient
from config import IPFS_API_URL

client = ipfshttpclient.connect(IPFS_API_URL)

def upload_to_ipfs(file_path: str) -> str:
    res = client.add(file_path)
    # res = {"Hash": "<CID>", ...}
    cid = res["Hash"]
    # יוצר URI סטנדרטי
    return f"https://ipfs.io/ipfs/{cid}"
