import streamlit as st
import time
from contact_center_lib import save_message, load_chat_history, get_active_sessions, get_last_update_time
from smartvision_lib import qa_chat_with_model, read_summary_with_model
import time


st.set_page_config(page_title="Agent Support Dashboard", layout="wide")
st.title("Agent Support Dashboard")

# Initialize session state
if "selected_session" not in st.session_state:
  st.session_state.selected_session = None
if "last_update_time" not in st.session_state:
  st.session_state.last_update_time = 0
if "llm_responses" not in st.session_state:
  st.session_state.llm_responses = {}
if "session_ended" not in st.session_state:
  st.session_state.session_ended = False
if "conversation_summary" not in st.session_state:
  st.session_state.conversation_summary = ""

# Get active sessions
active_sessions = get_active_sessions()

# Sidebar for session selection
with st.sidebar:
  st.header("Active Sessions")

  if not active_sessions:
    st.info("No active chat sessions")
  else:
    for session in active_sessions:
      if st.button(f"Session: {session}", key=session):
        st.session_state.selected_session = session
        st.session_state.last_update_time = get_last_update_time(session)
        st.rerun()

# Main chat area
if st.session_state.selected_session:
  st.subheader(f"Chat Session: {st.session_state.selected_session}")

  # Create two columns
  col1, col2 = st.columns(2)

  with col1:
    st.subheader("Customer Conversation")

    # Display chat history in a container that will be auto-updated
    chat_container = st.container()

    # Message input
    with st.form("agent_message_form", clear_on_submit=True):
      message = st.text_area("Type your response:",
                             key="agent_current_message")
      col_send, col_end = st.columns([3, 1])
      with col_send:
        send = st.form_submit_button("Send Response")
      with col_end:
        end_session = st.form_submit_button("End Session")

      if send and message:
        save_message(st.session_state.selected_session, "agent", message)
        st.session_state.last_update_time = int(time.time() * 1000)

      if end_session:
        session_file_path = f"data/chat_{st.session_state.selected_session}.json"
        summary = read_summary_with_model(session_file_path)
        st.session_state.conversation_summary = summary
        st.session_state.session_ended = True

    # Display chat history
    with chat_container:
      chat_history = load_chat_history(st.session_state.selected_session)
      for message in chat_history:
        if message["sender"] == "customer":
          st.write(
              f"**Customer ({message['timestamp']}):** {message['message']}")

          # Get LLM response for this customer message if not already processed
          message_id = message.get("id", message["timestamp"])
          if message_id not in st.session_state.llm_responses:
            llm_response = qa_chat_with_model(message["message"])
            st.session_state.llm_responses[message_id] = {
                "customer_message": message["message"],
                "llm_response": llm_response,
                "timestamp": message["timestamp"]
            }
        else:
          st.write(f"**You ({message['timestamp']}):** {message['message']}")

  with col2:
    st.subheader("AI Assistant Suggestions")

    # Display conversation summary if session is ended
    if st.session_state.session_ended and st.session_state.conversation_summary:
      st.success("Session ended")
      st.markdown("### Conversation Summary")
      st.write(st.session_state.conversation_summary)
    else:
      # Display only the latest LLM response
      llm_container = st.container()
      with llm_container:
        # Sort responses by timestamp and get only the latest one
        sorted_responses = sorted(
            st.session_state.llm_responses.values(),
            key=lambda x: x["timestamp"],
            reverse=True
        )

        if sorted_responses:
          latest = sorted_responses[0]
          st.write(
              f"**Customer said ({latest['timestamp']}):** {latest['customer_message']}")
          st.info(f"**AI suggests:** {latest['llm_response']}")

  # Auto-refresh mechanism
  placeholder = st.empty()

  # Check for updates
  current_update_time = get_last_update_time(st.session_state.selected_session)
  if current_update_time > st.session_state.last_update_time:
    st.session_state.last_update_time = current_update_time
    time.sleep(0.1)  # Small delay to ensure UI updates
    st.rerun()

  # Auto-refresh every 3 seconds
  with placeholder:
    st.empty()
    time.sleep(3)
    st.rerun()
else:
  st.info("Select a chat session from the sidebar to begin responding")



import os
import threading
import smartvision_token_lib
def test_change_env():
  last_time = 0
  os.environ["test_id"] = '0'
  while True:
    current_time = time.time()
    if current_time - last_time >= 60*50:
      # Refresh tokens every 50 minutes
      qa_token = smartvision_token_lib.get_qa_token()
      read_token = smartvision_token_lib.get_read_token()
      os.environ["sv_qa_token"] = qa_token
      os.environ["sv_read_token"] = read_token

      last_time = current_time
      print("Refreshing tokens...")
      os.environ["test_id"]=str(int(os.environ["test_id"])+1)
      print("a", os.getenv("test_id"))


test_thread = threading.Thread(
      target=test_change_env,
      daemon=True  # 设置为守护线程
  )

test_thread.start()


print("end1")