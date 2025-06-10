import json
import os
from dotenv import load_dotenv
import requests
import threading
import smartvision_token_lib
import time

# Load environment variables from .env file
load_dotenv()






def qa_chat_with_model(question):
  qa_token = os.getenv("sv_qa_token")
  res = requests.post(
      url="https://app.dcclouds.com/api/smart/open_api/conversation/35b406218af44ec8b5d4809de7ee42f4",
      headers={
          "Content-Type": "application/json",
          "Authorization": qa_token
      },
      json={
          "question": question,
          "model_id": '76abbdf0fcdc4fbcae2cb2238d8a7a40',
          "answer_type": 0
      }
  )

  answer = res.json().get('data', {}).get('data')

  return answer


def read_upload_file(file_path):
  read_token = os.getenv("sv_read_token")
  print("Uploading file:", file_path)
  res = requests.post(
      url="https://app.dcclouds.com/api/smart/open_api/upload_file/c28fab8553df40559ad9aef34347ffd7",
      headers={
          "Authorization": read_token
      },
      files={
          "file": open(file_path, 'rb')
      },
      data={
          "model_id": '76abbdf0fcdc4fbcae2cb2238d8a7a40',
          "category_id": 'd7a3755ae0774ea6b124b3948823b36b'
      }
  )
  print("Upload response:", res.json())
  file_info = res.json().get('data', {})

  return file_info


def convert_json_to_txt(chat_history_path):
  with open(chat_history_path, 'r') as f:
    chat_history = json.load(f)
    txt_path = chat_history_path.replace('.json', '.txt')

    with open(txt_path, 'w') as txt_file:
      for item in chat_history:
        sender = item.get('sender', '')
        message = item.get('message', '')
        txt_file.write(f"{sender}: {message}\n")

  return txt_path


def read_summary_with_model(chat_history_path):
  read_token = os.getenv("sv_read_token")
  # Convert to txt
  txt_file_path = convert_json_to_txt(chat_history_path)

  # Upload file
  file_info = read_upload_file(txt_file_path)
  file_id = file_info['id']
  file_name = file_info['name']

  # Conversation with file and prompt
  res = requests.post(
      url="https://app.dcclouds.com/api/smart/open_api/v2/conversation/c28fab8553df40559ad9aef34347ffd7",
      headers={
          "Content-Type": "application/json",
          "Authorization": read_token
      },
      json={
          "model_id": '76abbdf0fcdc4fbcae2cb2238d8a7a40',
          "prompt_id": '59ee849d1bf142c2aeda9ead25ee802c',
          "file_id": file_id
      }
  )

  answer = res.json().get('data', {}).get('data')

  return answer
