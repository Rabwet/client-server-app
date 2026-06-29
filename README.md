# Simple Client-Server Application (Flask/HTTP)

A simple client-server application built and tested on localhost, demonstrating
request/response communication and a layered software architecture.

## 1. What this project demonstrates

- A **server** application (Flask) that exposes HTTP endpoints
- A **client** application (Python `requests`) that calls those endpoints
- **Successful communication** between client and server on `localhost:5000`
- A clear **layered architecture** on both the client and server side

## 2. Layered architecture

```
            CLIENT SIDE                              SERVER SIDE
   -------------------------------         -------------------------------
   Console output (user sees this)
            ^
            |
   client/client.py                         server/app.py
   (presentation layer - builds    -- HTTP -->  (presentation / application
    requests, displays responses)   request      layer - Flask routes,
            |                                     receives requests,
            v                                     returns JSON responses)
   'requests' library                                    |
   (application layer HTTP                                v
    handling)                                     server/business_logic.py
            |                                     (business logic layer -
            v                                      validates input, applies
   TCP/IP sockets                                   application rules)
   (transport + network layer)                              |
            |                                                v
            -------------- network (localhost) -----  server/data_layer.py
                                                       (data layer - stores
                                                        and retrieves records,
                                                        currently in-memory)
```

| Layer | Client side | Server side |
|---|---|---|
| Presentation | `client/client.py` builds requests and prints responses | `server/app.py` (Flask routes) receives HTTP requests, returns JSON |
| Application / Transport | Python `requests` library over TCP/IP | Flask's built-in HTTP server over TCP/IP |
| Business Logic | — | `server/business_logic.py` validates input and applies rules |
| Data | — | `server/data_layer.py` stores/retrieves message records |

This separation means each layer only talks to the layer directly below it.
For example, `app.py` never touches `data_layer.py` directly — it always
goes through `business_logic.py`. This makes the system easier to maintain
and would allow swapping the in-memory data layer for a real database
without changing the business logic or presentation layers.

## 3. Project structure

```
client-server-app/
├── server/
│   ├── __init__.py
│   ├── app.py              # presentation layer (Flask routes)
│   ├── business_logic.py   # business logic layer
│   └── data_layer.py       # data layer (in-memory storage)
├── client/
│   ├── __init__.py
│   └── client.py           # client application
├── requirements.txt
└── README.md
```

## 4. How to run it locally

### Step 1: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Start the server (in one terminal)
```bash
python -m server.app
```
You should see:
```
Starting server on http://127.0.0.1:5000
```

### Step 3: Run the client (in a second terminal)
```bash
python -m client.client
```

The client will automatically:
1. Check the server is reachable
2. Send two new messages (POST)
3. Retrieve all messages (GET)
4. Retrieve a single message by id (GET)
5. Retrieve server stats (GET)
6. Send an intentionally invalid message to demonstrate error handling (POST)

## 5. API endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check, lists available endpoints |
| POST | `/messages` | Create a new message (`sender`, `content`) |
| GET | `/messages` | Retrieve all messages |
| GET | `/messages/<id>` | Retrieve a single message by id |
| GET | `/stats` | Get server statistics |

## 6. Example interaction

**Request:**
```http
POST /messages HTTP/1.1
Content-Type: application/json

{"sender": "Caroline", "content": "Hello server, this is my first message."}
```

**Response:**
```json
{
  "success": true,
  "message": "Message received and stored by server.",
  "data": {"id": 1, "sender": "Caroline", "content": "Hello server, this is my first message."}
}
```

A full log of a successful run (client output and server log) is included
in `docs/sample_run_output.txt` as evidence of successful communication.
