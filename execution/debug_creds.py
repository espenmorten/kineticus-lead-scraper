
from google.oauth2.service_account import Credentials
import sys

try:
    print("Attempting to load credentials...")
    creds = Credentials.from_service_account_file('credentials.json')
    print("Successfully loaded credentials!")
except Exception as e:
    print(f"Failed to load credentials: {e}")
    # checking private key format
    import json
    with open('credentials.json') as f:
        data = json.load(f)
        pk = data.get('private_key', '')
        print(f"Private Key length: {len(pk)}")
        print(f"Private Key starts with: {pk[:30]!r}")
        print(f"Private Key ends with: {pk[-30:]!r}")
        print(f"Contains \\n literals: {'\\n' in pk}")
