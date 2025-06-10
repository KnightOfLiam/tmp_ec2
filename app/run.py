import subprocess
import threading
import time
import os
import smartvision_token_lib


def run_app(app_name, port):
  subprocess.run(["streamlit", "run", app_name, "--server.port", str(port)])


if __name__ == "__main__":
  # Create data directory if it doesn't exist
  os.makedirs("data", exist_ok=True)

  print("Starting Contact Center Applications...")

  # Start both apps in separate threads
  customer_thread = threading.Thread(
      target=run_app,
      args=("customer_app.py", 8501)
  )

  agent_thread = threading.Thread(
      target=run_app,
      args=("agent_app.py", 8502)
  )

  customer_thread.start()
  agent_thread.start()

  print("Customer app running at: http://localhost:8501")
  print("Agent app running at: http://localhost:8502")

  last_time = 0

  try:
    while True:
      current_time = time.time()
      if current_time - last_time >= 60*50:
        # Refresh tokens every 50 minutes
        # qa_token = smartvision_token_lib.get_qa_token()
        # read_token = smartvision_token_lib.get_read_token()
        # os.environ["sv_qa_token"] = qa_token
        # os.environ["sv_read_token"] = read_token
        # print(os.getenv("test_id"))
        # os.environ["test_id"] = str(int(os.environ["test_id"]) + 1)
        # print(os.getenv("test_id"))
        # print("Refreshing tokens...")
        last_time = current_time
      time.sleep(1)
  except KeyboardInterrupt:
    print("Shutting down...")
