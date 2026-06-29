"""
CLIENT APPLICATION
------------------
This is the client-side presentation layer. It builds HTTP
requests, sends them to the server over the network (via the
'requests' library, which itself sits on top of TCP/IP sockets),
and displays the server's responses to the user.

LAYER STACK ON THE CLIENT SIDE:

  User / console output      <-- what you see printed
        ^
  client.py (this file)      <-- presentation layer, client side
        |  builds + sends HTTP requests
        v
  'requests' library          <-- application layer HTTP handling
        v
  TCP/IP sockets               <-- transport + network layer
        v
  -------- network --------
        v
  Server (Flask, see server/app.py)
"""

import requests
import time
import sys

BASE_URL = "http://127.0.0.1:5000"


def print_section(title):
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)


def check_server_is_up():
    print_section("STEP 0: Checking server is reachable")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=3)
        print(f"Request:  GET {BASE_URL}/")
        print(f"Status code: {response.status_code}")
        print(f"Response body: {response.json()}")
        return True
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to server.")
        print("Make sure the server is running first:")
        print("    python -m server.app")
        return False


def send_message(sender, content):
    print_section(f"STEP: Client sends a message from '{sender}'")
    request_body = {"sender": sender, "content": content}
    print(f"Request:  POST {BASE_URL}/messages")
    print(f"Request body: {request_body}")

    response = requests.post(f"{BASE_URL}/messages", json=request_body, timeout=3)

    print(f"Status code: {response.status_code}")
    print(f"Response body: {response.json()}")
    return response


def get_all_messages():
    print_section("STEP: Client requests all stored messages")
    print(f"Request:  GET {BASE_URL}/messages")

    response = requests.get(f"{BASE_URL}/messages", timeout=3)

    print(f"Status code: {response.status_code}")
    print(f"Response body: {response.json()}")
    return response


def get_single_message(message_id):
    print_section(f"STEP: Client requests message id={message_id}")
    print(f"Request:  GET {BASE_URL}/messages/{message_id}")

    response = requests.get(f"{BASE_URL}/messages/{message_id}", timeout=3)

    print(f"Status code: {response.status_code}")
    print(f"Response body: {response.json()}")
    return response


def get_stats():
    print_section("STEP: Client requests server stats")
    print(f"Request:  GET {BASE_URL}/stats")

    response = requests.get(f"{BASE_URL}/stats", timeout=3)

    print(f"Status code: {response.status_code}")
    print(f"Response body: {response.json()}")
    return response


def demo_validation_error():
    print_section("STEP: Client sends an INVALID message (missing content)")
    request_body = {"sender": "Caroline"}
    print(f"Request:  POST {BASE_URL}/messages")
    print(f"Request body: {request_body}")

    response = requests.post(f"{BASE_URL}/messages", json=request_body, timeout=3)

    print(f"Status code: {response.status_code}")
    print(f"Response body: {response.json()}")
    return response


def main():
    if not check_server_is_up():
        sys.exit(1)

    time.sleep(0.5)
    send_message("Caroline", "Hello server, this is my first message.")

    time.sleep(0.5)
    send_message("Caroline", "This is a second message to test multiple records.")

    time.sleep(0.5)
    get_all_messages()

    time.sleep(0.5)
    get_single_message(1)

    time.sleep(0.5)
    get_stats()

    time.sleep(0.5)
    demo_validation_error()

    print_section("DEMO COMPLETE: client-server communication successful")


if __name__ == "__main__":
    main()
