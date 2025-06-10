import streamlit as st
import datetime
import json
import os
import time


def save_message(session_id, sender, message):
  """Save a message to the chat history file."""
  timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

  # Create data directory if it doesn't exist
  os.makedirs("data", exist_ok=True)

  # Path to the chat history file
  file_path = f"data/chat_{session_id}.json"

  # Load existing chat history or create new
  if os.path.exists(file_path):
    with open(file_path, "r") as f:
      chat_history = json.load(f)
  else:
    chat_history = []

  # Add new message
  chat_history.append({
      "timestamp": timestamp,
      "sender": sender,
      "message": message,
      "id": int(time.time() * 1000)  # Add unique ID for messages
  })

  # Save updated chat history
  with open(file_path, "w") as f:
    json.dump(chat_history, f, indent=2)


def load_chat_history(session_id):
  """Load chat history for a specific session."""
  file_path = f"data/chat_{session_id}.json"

  if os.path.exists(file_path):
    with open(file_path, "r") as f:
      return json.load(f)
  return []


def get_active_sessions():
  """Get list of all active chat sessions."""
  os.makedirs("data", exist_ok=True)
  sessions = []

  for filename in os.listdir("data"):
    if filename.startswith("chat_") and filename.endswith(".json"):
      session_id = filename[5:-5]  # Remove 'chat_' prefix and '.json' suffix
      sessions.append(session_id)

  return sessions


def get_last_update_time(session_id):
  """Get the timestamp of the last message in a session."""
  chat_history = load_chat_history(session_id)
  if chat_history:
    return chat_history[-1].get("id", 0)
  return 0
