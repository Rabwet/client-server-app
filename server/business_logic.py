"""
BUSINESS LOGIC LAYER (SERVICE LAYER)
------------------
Sits between the presentation layer (Flask routes) and the
data layer. Applies validation rules and application logic.
The presentation layer never talks to data_layer.py directly;
it always goes through this layer.
"""

from server import data_layer


class ValidationError(Exception):
    """Raised when incoming data fails business rules."""
    pass


def process_new_message(sender, content):
    """
    Validate and process an incoming client message,
    then delegate persistence to the data layer.
    """
    if not sender or not isinstance(sender, str):
        raise ValidationError("Field 'sender' is required and must be text.")

    if not content or not isinstance(content, str):
        raise ValidationError("Field 'content' is required and must be text.")

    if len(content) > 500:
        raise ValidationError("Field 'content' must be 500 characters or fewer.")

    sender_clean = sender.strip()
    content_clean = content.strip()

    saved_record = data_layer.save_message(sender_clean, content_clean)
    return saved_record


def retrieve_all_messages():
    """Business rule: return messages newest-first."""
    messages = data_layer.get_all_messages()
    return list(reversed(messages))


def retrieve_message(message_id):
    record = data_layer.get_message_by_id(message_id)
    if record is None:
        raise ValidationError(f"No message found with id {message_id}.")
    return record


def get_server_stats():
    return {
        "total_messages": data_layer.count_messages()
    }
