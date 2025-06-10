import streamlit as st
import uuid
import time
from contact_center_lib import save_message, load_chat_history, get_last_update_time

st.set_page_config(page_title="Customer Support Chat", page_icon="💬")
st.title("Customer Support Chat")

# Initialize session state
if "session_id" not in st.session_state:
  st.session_state.session_id = str(uuid.uuid4())
if "last_update_time" not in st.session_state:
  st.session_state.last_update_time = 0

# Chat interface
st.write(f"Chat Session ID: {st.session_state.session_id}")
st.info("Welcome! An agent will respond to your message shortly.")

# Display chat history in a container that will be auto-updated
chat_container = st.container()

# Message input
with st.form("message_form", clear_on_submit=True):
  message = st.text_area("Type your message:", key="current_message")
  send = st.form_submit_button("Send")

  if send and message:
    save_message(st.session_state.session_id, "customer", message)
    st.session_state.last_update_time = int(time.time() * 1000)

# Auto-refresh mechanism
placeholder = st.empty()

# Display chat history
with chat_container:
  chat_history = load_chat_history(st.session_state.session_id)
  for message in chat_history:
    if message["sender"] == "customer":
      st.write(f"**You ({message['timestamp']}):** {message['message']}")
    else:
      st.write(f"**Agent ({message['timestamp']}):** {message['message']}")

# Check for updates every few seconds
current_update_time = get_last_update_time(st.session_state.session_id)
if current_update_time > st.session_state.last_update_time:
  st.session_state.last_update_time = current_update_time
  time.sleep(0.1)  # Small delay to ensure UI updates
  st.rerun()

# Auto-refresh every 3 seconds
with placeholder:
  st.empty()
  time.sleep(3)
  st.rerun()