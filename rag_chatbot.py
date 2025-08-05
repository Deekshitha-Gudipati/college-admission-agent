import os, requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("IBM_API_KEY")
PROJECT_ID = os.getenv("IBM_PROJECT_ID")
REGION = "au-syd"

def get_ibm_token():
    res = requests.post("https://iam.cloud.ibm.com/identity/token",
                        headers={"Content-Type": "application/x-www-form-urlencoded"},
                        data={"grant_type":"urn:ibm:params:oauth:grant-type:apikey","apikey":API_KEY})
    res.raise_for_status()
    return res.json()["access_token"]

def ask_ibm_granite(prompt_text):
    token = get_ibm_token()
    url = f"https://{REGION}.ml.cloud.ibm.com/ml/v1/text/generation?version=2025-02-11"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "ML-Instance-ID": PROJECT_ID
    }
    body = {
        "model_id": "ibm/granite-3-8b-instruct",
        "project_id": PROJECT_ID,
        "input": prompt_text,
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 300,
            "temperature": 0.7
        }
    }
    res = requests.post(url, headers=headers, json=body)
    res.raise_for_status()
    return res.json()["results"][0]["generated_text"]
