# 📘 Backend API Documentation For 90 North enfund.io Assignment

## 📌 Project Overview
This project is a Django-based backend system that integrates:
- **Google OAuth 2.0** for secure user authentication.
- **Google Drive API** for file upload, fetching, and downloading.
- **WebSockets** for real-time chat between authenticated users.

The backend is built using Django, Django REST Framework, Django Channels, and Google APIs. It supports both HTTP-based API interactions and WebSockets for real-time communication.

---

## 🚀 Installation & Setup

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/yourusername/backend-project.git
cd backend-project
```

### **2️⃣ Create a Virtual Environment**
```bash
python -m venv .venv
source .venv/bin/activate  # For macOS/Linux
# For Windows: .venv\Scripts\activate
```

### **3️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4️⃣ Set Up Environment Variables**
Create a `.env` file in the root directory and add:
```python
# Secret Key Configuration Settings
# ---------------------------------
SECRET_KEY=<django_secret_key>

# Debug Configuration Settings
# ----------------------------
DEBUG=True

# Allowed Hosts Configuration Settings
# ------------------------------------
ALLOWED_HOSTS=localhost,127.0.0.1

# Google OAuth2 Configuration Settings
# ------------------------------------
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=http://localhost:8000/api/v1/auth/google/callback
```
Replace the values with the actual credentials obtained from Google Cloud Console.

### **5️⃣ Apply Migrations & Run Server**
```bash
python manage.py migrate
python manage.py runserver
```

Your backend will now be running at `http://127.0.0.1:8000/`.

---

## 📌 API Endpoints

### **1️⃣ Google OAuth 2.0 Authentication**
| Method | Endpoint                        | Description                                     |
| ------ | ------------------------------- | ----------------------------------------------- |
| `GET`  | `/api/v1/auth/google/`          | Get Google OAuth login URL                      |
| `GET`  | `/api/v1/auth/google/callback/` | Handle Google OAuth callback & return user info |

Example Response:
```json
{
    "message": "Sign in request was successful",
    "data": {
        "user": {
            "id": "1061708733286256565435",
            "email": "your.google.email@gmail.com",
            "verified_email": "<true/false>",
            "name": "<full_name>",
            "given_name": "<first_name>",
            "family_name": "<last_name>",
            "picture": "<profile_picture_url>"
        },
        "tokens": {
            "access_token": "<access_token>",
            "expires_in": 3599,
            "refresh_token": "<refresh_token>",
            "scope": "<scope_url>",
            "token_type": "Bearer",
            "id_token": "<id_token>",
            "refresh_token_expires_in": 604799
        }
    },
    "errors": []
}
```

---

### **2️⃣ Google Drive API**
| Method | Endpoint                              | Description                             |
| ------ | ------------------------------------- | --------------------------------------- |
| `POST` | `api/v1/google/drive/upload/`         | Upload a file to Google Drive           |
| `GET`  | `api/v1/google/drive/list/`           | Fetch list of user’s Google Drive files |
| `GET`  | `api/v1/google/drive/list/{file_id}/` | View and Download a single file from Google Drive       |

#### **Uploading a File to Google Drive**
**Request:**
```http
POST /api/v1/google/drive/upload/
Authorization: Bearer ACCESS_TOKEN
Content-Type: multipart/form-data
```

**Form Data:**
```
file: <file_to_upload>
```

**Response:**
```json
{
  "message": "File uploaded successfully.",
  "data": {
    "id": "<id>",
    "name": "<file_name>",
    "webContentLink": "<file_download_link>",
    "webViewLink": "file_view_link"
  },
  "errors": []
}
```

#### **Fetching List of Google Drive Files**
**Request:**
```http
GET /api/v1/google/drive/list/
Authorization: Bearer ACCESS_TOKEN
```

**Response:**
```json
{
  "message": "Files fetched successfully.",
  "data": [
    {
      "id": "<id>",
      "name": "<file_name>",
      "webContentLink": "<file_download_link>",
      "webViewLink": "file_view_link",
      "mimeType": "image/png",
      "size": "976261",
      "createdTime": "2025-03-03T12:51:58.853Z",
      "modifiedTime": "2025-03-03T12:51:58.853Z"
    },
    {
      "id": "<id>",
      "name": "<file_name>",
      "webContentLink": "<file_download_link>",
      "webViewLink": "file_view_link",
      "mimeType": "application/pdf",
      "size": "976261",
      "createdTime": "2025-03-03T12:51:58.853Z",
      "modifiedTime": "2025-03-03T12:51:58.853Z"
    }
  ],
  "errors": []
}
```

#### **Downloading a File from Google Drive**
**Request:**
```http
GET /api/v1/google/drive/list/{file_id}/
Authorization: Bearer ACCESS_TOKEN
```

**Response:**
```json
{
  "message": "File downloaded successfully.",
  "data": {
    "id": "<id>",
    "name": "<file_name>",
    "webContentLink": "<file_download_link>",
    "webViewLink": "file_view_link",
    "mimeType": "application/pdf",
    "size": "976261",
    "createdTime": "2025-03-03T12:51:58.853Z",
    "modifiedTime": "2025-03-03T12:51:58.853Z"
  },
  "errors": []
}
```


**Common Error Response is Look like this:**
```json
{
  "message": "File list request was not successful.",
  "data": null,
  "errors": [
    {
      "field": "<error_field>",
      "code": "<error_code>",
      "message": "<error_message>",
      "details": null
    },
  ]
}
```

---

### **3️⃣ WebSocket Chat**
| WebSocket | Endpoint                                             | Description               |
| --------- | ---------------------------------------------------- | ------------------------- |
| `WS`      | `ws://127.0.0.1:8000/ws/v1/chat/?token=ACCESS_TOKEN` | Real-time chat connection |

#### **Connecting to WebSocket Chat**
- Use a WebSocket client (Postman or a frontend app).
- Send messages using JSON format:
```json
{ "message": "Hello from Postman!" }
```
- Receive messages in the format:
```json
{ "message": "User1: Hello, world!" }
```

---

## 🧪 Testing with Postman
1. **Import the Postman Collection (`postman_collection.json`).**
2. **Use OAuth 2.0 authentication to obtain an access token.**
3. **Test HTTP endpoints for authentication, file upload, and retrieval.**
4. **Test WebSocket chat using Postman’s WebSocket feature.**

---
