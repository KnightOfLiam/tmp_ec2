import os
from dotenv import load_dotenv
import requests
import time

# Load environment variables from .env file
load_dotenv()

# Access Credentials
qa_access_key = os.getenv("sv_qa_ak")
qa_secret_key = os.getenv("sv_qa_sk")

read_access_key = os.getenv("sv_read_ak")
read_secret_key = os.getenv("sv_read_sk")


def get_qa_token():
  try:
    token_response = requests.post(
        url="https://app.dcclouds.com/api/smart/open_api/token",
        headers={
            "Content-Type": "application/json"
        },
        json={
            "ak": qa_access_key,
            "sk": qa_secret_key
        }
    )
    token = token_response.json().get('data', {}).get('token')

  except Exception as e:
    print(f"Error QA token: {e}")

  return token


qa_token = get_qa_token()
# print(qa_token)
# 60 分钟有效；
# 部署 ec2, /home/ssm-user 下；


def get_read_token():

  try:
    token_response = requests.post(
        url="https://app.dcclouds.com/api/smart/open_api/token",
        headers={
            "Content-Type": "application/json"
        },
        json={
            "ak": read_access_key,
            "sk": read_secret_key
        }
    )
    token = token_response.json().get('data', {}).get('token')

  except Exception as e:
    print(f"Error Read token: {e}")

  return token


read_token = get_read_token()
# print(read_token)
