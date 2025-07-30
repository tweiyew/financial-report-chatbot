from dotenv import load_dotenv
import os
from vertexai import init

load_dotenv() 

init(
    project=os.getenv("GCP_PROJECT_ID"),
    location=os.getenv("GCP_LOCATION", "us-central1")
)