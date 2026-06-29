"""
PRESENTATION LAYER (APPLICATION / HTTP LAYER)
------------------
This is the only layer that knows about HTTP. It receives
requests from the client over the network (transport layer
below it, handled by TCP/IP and Flask's built-in server),
converts them into plain Python calls to the business logic
layer, and converts the results back into HTTP responses
(JSON over HTTP).

LAYER STACK IN THIS APPLICATION:

  Client (presentation)
        |  HTTP request (application layer protocol)
        v
  TCP/IP (transport + network layer, handled by the OS/sockets)
        v
  Flask routes        <-- THIS FILE (presentation/application layer, server side)
        v
  business_logic.py   <-- business logic layer (validation, rules)
        v
  data_layer.py        <-- data layer (storage)
"""

from flask import Flask, request, jsonify
from server import business_logic

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    """Simple health check endpoint."""
    return jsonify({
        "status": "Server is running",
        "available_endpoints": {
            "POST /messages": "Send a new message to the server",
            "GET /messages": "Retrieve all messages",
            "GET /messages/<id>": "Retrieve a single message by id",
            "GET /stats": "Server statistics"
        }
    })


@app.route("/messages", methods=["POST"])
def create_message():
    """Client sends a new message here."""
    payload = request.get_json(silent=True) or {}
    sender = payload.get("sender")
    content = payload.get("content")

    try:
        record = business_logic.process_new_message(sender, content)
        return jsonify({
            "success": True,
            "message": "Message received and stored by server.",
            "data": record
        }), 201
    except business_logic.ValidationError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400


@app.route("/messages", methods=["GET"])
def list_messages():
    """Client requests all messages."""
    records = business_logic.retrieve_all_messages()
    return jsonify({
        "success": True,
        "count": len(records),
        "data": records
    }), 200


@app.route("/messages/<int:message_id>", methods=["GET"])
def get_message(message_id):
    """Client requests one message by id."""
    try:
        record = business_logic.retrieve_message(message_id)
        return jsonify({
            "success": True,
            "data": record
        }), 200
    except business_logic.ValidationError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 404


@app.route("/stats", methods=["GET"])
def stats():
    return jsonify({
        "success": True,
        "data": business_logic.get_server_stats()
    }), 200


if __name__ == "__main__":
    print("=" * 60)
    print(" Starting server on http://127.0.0.1:5000")
    print(" Layers active: Presentation -> Business Logic -> Data")
    print("=" * 60)
    app.run(host="127.0.0.1", port=5000, debug=False)
