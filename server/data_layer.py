"""
DATA LAYER
------------------
Responsible only for storing and retrieving raw data.
Knows nothing about HTTP, requests, or business rules.
This isolation means we could swap this for a real database
(SQLite, PostgreSQL, etc.) without touching any other layer.
"""

# Simple in-memory "database" simulated with a Python list of dicts
_messages_db = []
_next_id = 1


def save_message(sender, content):
    """Insert a new message record and return it."""
    global _next_id
    record = {
        "id": _next_id,
        "sender": sender,
        "content": content
    }
    _messages_db.append(record)
    _next_id += 1
    return record


def get_all_messages():
    """Return all stored message records."""
    return list(_messages_db)


def get_message_by_id(message_id):
    """Return a single record by id, or None if not found."""
    for record in _messages_db:
        if record["id"] == message_id:
            return record
    return None


def count_messages():
    return len(_messages_db)
