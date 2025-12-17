import requests

url = "http://localhost:8000/download"
data = {"url": "https://youtube.com/shorts/eNPV3OzdA6g?si=zPXSxYP9EZgBLHMu",
        "mode": "video"}
resp = requests.post(url, json=data)
print(resp.status_code)
print(resp.json())