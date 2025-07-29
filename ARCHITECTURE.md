# System Architecture Documentation

## Overview
This project is a Django-based web application with WhatsApp automation capabilities. It consists of a Django backend, a webhook app for handling external integrations, and a Python script (`whatsapp.py`) for automating WhatsApp messaging using Selenium or PyWhatKit.

---

## High-Level Architecture

**Components:**
- **Django Core (`core/`):** Handles web server, routing, and settings.
- **Webhook App (`webhook/`):** Manages webhook endpoints, models, and business logic for external integrations.
- **WhatsApp Automation Script (`whatsapp.py`):** Automates sending messages via WhatsApp Web.
- **Database (`db.sqlite3`):** Stores application data and webhook events.
- **Scripts (`scripts/`):** Contains utility or deployment scripts.

**External Dependencies:**
- **WhatsApp Web:** Used by the automation script for sending messages.
- **Selenium WebDriver:** Used for browser automation.
- **PyWhatKit:** (Optional) Used for WhatsApp messaging.

---

## Component Diagram (Textual)

```
+-------------------+         +-------------------+         +-------------------+
|                   |         |                   |         |                   |
|   User/Client     +-------->+   Django Server   +-------->+   Database        |
|                   |  HTTP   |   (core/)         |  ORM    |   (db.sqlite3)    |
+-------------------+         +-------------------+         +-------------------+
                                      |
                                      | Calls
                                      v
                             +-------------------+
                             |                   |
                             |  Webhook App      |
                             |  (webhook/)       |
                             +-------------------+
                                      |
                                      | Triggers
                                      v
                             +-------------------+
                             |                   |
                             | WhatsApp Script   |
                             | (whatsapp.py)     |
                             +-------------------+
                                      |
                                      | Automates
                                      v
                             +-------------------+
                             |                   |
                             | WhatsApp Web      |
                             +-------------------+
```

---

## Data Flow

1. **User/Client** sends an HTTP request to the Django server (e.g., via a webhook endpoint).
2. **Django Server** processes the request and, if needed, stores/retrieves data from the **Database**.
3. **Webhook App** handles business logic for incoming webhook events.
4. If a WhatsApp message needs to be sent, the **Webhook App** triggers the **WhatsApp Automation Script**.
5. **WhatsApp Script** uses Selenium to automate WhatsApp Web and send the message.
6. **WhatsApp Web** delivers the message to the recipient.

---

## Folder Structure & Responsibilities

- **core/**: Django project configuration (settings, URLs, WSGI/ASGI).
- **webhook/**: Django app for webhook handling (models, views, migrations).
- **whatsapp.py**: Standalone script for WhatsApp automation.
- **db.sqlite3**: SQLite database for persistent storage.
- **scripts/**: Miscellaneous scripts (e.g., deployment, data import/export).

---

## Technologies Used

- **Python 3.11+**
- **Django** (web framework)
- **Selenium** (browser automation)
- **PyWhatKit** (optional WhatsApp automation)
- **SQLite** (default Django database)
- **WhatsApp Web** (external service)

---

## Example Sequence (Webhook to WhatsApp)

1. External service sends a webhook to `/webhook/`.
2. `webhook/views.py` processes the request.
3. If a WhatsApp message is required, the view calls `whatsapp.py` (e.g., via subprocess or direct import).
4. `whatsapp.py` launches Selenium, logs into WhatsApp Web, and sends the message.
5. Status is logged or returned to the user.

---

## Security Considerations

- **Authentication:** Ensure webhook endpoints are protected or validated.
- **Sensitive Data:** Do not log sensitive information.
- **Browser Automation:** Secure the environment where Selenium runs (avoid exposing WhatsApp sessions).

---

## Extensibility

- Add more Django apps for new features.
- Integrate with other messaging platforms by adding new scripts.
- Replace SQLite with PostgreSQL or MySQL for production.

---

## Suggested Diagram (for draw.io or similar)

- Draw rectangles for each component (User, Django Server, Database, Webhook App, WhatsApp Script, WhatsApp Web).
- Use arrows to show the flow as described in the textual diagram above.

---

*Last updated: July 29, 2025*
