import requests

with open("test.mp4", "rb") as f:
    result = requests.post(
        "http://localhost:8000/interview/analysis", files={"file": f}
    )

print(result.json())
