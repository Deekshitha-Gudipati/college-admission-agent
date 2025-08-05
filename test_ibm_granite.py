import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("IBM_API_KEY")
PROJECT_ID = os.getenv("IBM_PROJECT_ID")  # You must set this in your .env

def get_ibm_token():
    url = "https://iam.cloud.ibm.com/identity/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "apikey": API_KEY,
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey"
    }
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    return response.json()["access_token"]

def ask_ibm_granite(prompt):
    token = get_ibm_token()
    
    url = "https://au-syd.ml.cloud.ibm.com/ml/v2/inference"  # Correct region

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
        "ML-Instance-ID": PROJECT_ID
    }

    payload = {
        "model_id": "granite-3-8b-instruct",  # Or whatever you're using
        "input": prompt,
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 300,
            "temperature": 0.7
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["results"][0]["generated_text"]

# 🔍 Run test
response = ask_ibm_granite("What is EAMCET?")
print("Generated Answer:\n", response)
