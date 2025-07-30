import requests
import sys

# CONFIG
API_BASE = "http://127.0.0.1:8000"
PDF_PATH = "../data/uploads/ishares.pdf"
QUESTION = "What is the net assets of share class (M)?" 

with open(PDF_PATH, "rb") as f:
    files = {"file": (PDF_PATH, f, "application/pdf")}
    print("Uploading PDF...")
    response = requests.post(f"{API_BASE}/upload-pdf", files=files)

# DEBUG
if response.status_code != 200:
    print("Upload failed")
    print("Status code:", response.status_code)
    print("Response headers:", response.headers)
    print("Response text:", response.text)
    sys.exit(1)

file_id = response.json()["file_id"]
print("Upload successful. File ID:", file_id)

# STEP 2: Ask question
print(f"Asking: {QUESTION}")
response = requests.post(
    f"{API_BASE}/ask-question",
    json={"question": QUESTION, "file_id": file_id}
)

if response.status_code != 200:
    print("Question failed:", response.json())
    sys.exit(1)

print("Answer:", response.json()["answer"])
