import os
import requests
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv()

# Access Credentials
qa_token = os.getenv("sv_qa_token")
read_token = os.getenv("sv_read_token")


def get_qa_model_info():
  res = requests.get(
      url="https://app.dcclouds.com/api/smart/open_api/model_info/35b406218af44ec8b5d4809de7ee42f4",
      headers={
          "Content-Type": "application/json",
          "Authorization": qa_token
      }
  )

  model_info_list = res.json().get('data')

  return model_info_list


# model_info = get_qa_model_info()
# print(model_info)
# [{'id': '76abbdf0fcdc4fbcae2cb2238d8a7a40', 'name': 'gpt-4o', 'manu_facturer': 'azure'}]


def get_read_model_info():
  res = requests.get(
      url="https://app.dcclouds.com/api/smart/open_api/model_info/c28fab8553df40559ad9aef34347ffd7",
      headers={
          "Content-Type": "application/json",
          "Authorization": read_token
      }
  )

  model_info_list = res.json().get('data')

  return model_info_list


# model_info = get_read_model_info()
# print(model_info)
# [{'id': '76abbdf0fcdc4fbcae2cb2238d8a7a40', 'name': 'gpt-4o', 'manu_facturer': 'azure'}]


def get_read_category_info():
  res = requests.get(
      url="https://app.dcclouds.com/api/smart/open_api/v2/category/c28fab8553df40559ad9aef34347ffd7",
      headers={
          "Content-Type": "application/json",
          "Authorization": read_token
      }
  )

  category_info_list = res.json().get('data')
  
  return category_info_list


category_info_list = get_read_category_info()
print(category_info_list)

# [{'question_id': 'd7a3755ae0774ea6b124b3948823b36b', 'question_title': '客户服务小结', 'question_order': 2, 'prompt_id': '59ee849d1bf142c2aeda9ead25ee802c', 'prompt_form': '[]'}, {'question_id': 'c83685bab55745e2b5d011d6b214893b', 'question_title': '工单内容生成', 'question_order': 3, 'prompt_id': '6f0b430d25474b208fb90166cf1a25e2', 'prompt_form': '[]'}]
