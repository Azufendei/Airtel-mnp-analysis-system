# MNP AI Bot - Backend API

A powerful FastAPI-based backend for analyzing Mobile Number Portability (MNP) journeys with AI-generated suggestions and comprehensive logging capabilities.

## 🎯 Overview

The MNP AI Bot provides a REST API that processes MNP journey data from database records and application logs to deliver:
- Complete MNP journey visualization
- Detailed logs analysis with statistics
- AI-powered suggestions for issue resolution
- Real-time data processing

## ✨ Features

### 📊 Data Analysis
- **MNP Journey Tracking**: Monitor all stages of number portability
- **Logs Analysis**: Parse and analyze application logs with statistics
- **Timeline Generation**: Event-based timeline with visualization data
- **Issue Detection**: Automatic detection of critical issues in logs

### 🔐 Security
- **OLM ID Authentication**: Role-based access control
- **User Management**: Admin and user roles with different permissions
- **Session Tracking**: Last login timestamps
- **Input Validation**: Comprehensive request validation

### 🚀 API Features
- **CORS Enabled**: Ready for frontend integration
- **Error Handling**: Graceful error responses with detailed messages
- **Health Checks**: System status monitoring
- **Sample Data**: Built-in endpoints for testing

## 📋 Requirements

- **Python**: 3.8+
- **Database**: PostgreSQL 12+
- **OS**: Windows, macOS, or Linux

## ⚙️ Installation

### 1. Database Setup

#### Windows:
```bash
# Download PostgreSQL 16 from https://www.postgresql.org/download/windows/
# Run installer and note your password
# Open Command Prompt and connect to PostgreSQL

psql -U postgres
CREATE DATABASE mnp_bot_db;
CREATE USER mnp_user WITH PASSWORD 'your_secure_password';
ALTER ROLE mnp_user SET client_encoding TO 'utf8';
ALTER ROLE mnp_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE mnp_user SET default_transaction_deferrable TO ON;
GRANT ALL PRIVILEGES ON DATABASE mnp_bot_db TO mnp_user;
\q
```

#### macOS/Linux:
```bash
# Install PostgreSQL (macOS with Homebrew)
brew install postgresql@15

# Or Linux (Ubuntu/Debian)
sudo apt-get install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
CREATE DATABASE mnp_bot_db;
CREATE USER mnp_user WITH PASSWORD 'your_secure_password';
ALTER ROLE mnp_user SET client_encoding TO 'utf8';
ALTER ROLE mnp_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE mnp_user SET default_transaction_deferrable TO ON;
GRANT ALL PRIVILEGES ON DATABASE mnp_bot_db TO mnp_user;
\q
```

### 2. Environment Setup

```bash
# Clone/navigate to project
cd mnp-ai-bot

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Create .env file
cp .env.example .env

# Update .env with your credentials
# DATABASE_URL=postgresql://mnp_user:your_secure_password@localhost:5432/mnp_bot_db
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Initialize Database

```bash
python setup_db.py
# This creates all tables and seeds initial OLM users
```

## 🚀 Running the Server

### Development Mode
```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at:
- **Base URL**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **Alternative Docs**: http://localhost:8000/redoc

### Production Mode
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 📚 API Endpoints

### Core Analysis Endpoint

#### `POST /analyze`
Main endpoint for MNP journey analysis.

**Request Body**:
```json
{
  "msisdn": "919890123456",
  "olm_id": "USER001",
  "start_time": "2024-01-01T00:00:00Z",
  "end_time": "2024-01-31T23:59:59Z"
}
```

**Response**:
```json
{
  "msisdn": "919890123456",
  "time_range": {
    "start": "2024-01-01T00:00:00Z",
    "end": "2024-01-31T23:59:59Z"
  },
  "tabular_journey": [
    {
      "msisdn": "919890123456",
      "event_type": "Port_in",
      "timestamp": "2024-01-05T10:30:00Z",
      "operator": "Jio",
      "circle": "Mumbai",
      "result": "Success",
      "txn_id": "TXN123456",
      "details": {}
    }
  ],
  "tabular_text": "Journey formatted as text...",
  "logs_analysis": {
    "total_logs": 25,
    "error_count": 2,
    "warning_count": 5,
    "info_count": 18,
    "summary": "Analysis summary...",
    "key_issues": ["Issue 1", "Issue 2"],
    "timeline": {"2024-01-05": 10}
  },
  "suggestions": [
    {
      "category": "Performance",
      "priority": "High",
      "suggestion": "Port in delayed",
      "details": "Detailed explanation..."
    }
  ],
  "status": "Success"
}
```

### Health Check

#### `GET /health`
Check API health status.

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2024-05-25T20:50:07Z",
  "version": "1.0.0"
}
```

### User Management

#### `GET /users`
List all registered OLM IDs.

**Response**:
```json
[
  {
    "olm_id": "USER001",
    "role": "admin",
    "is_active": true,
    "last_login": "2024-05-25T15:30:00Z"
  }
]
```

### Testing Endpoints

#### `POST /test/insert_sample_data`
Insert sample MNP journey and log data for testing.

**Response**:
```json
{
  "message": "Sample data inserted successfully",
  "count": 7
}
```

## 🗄️ Database Schema

### Tables

#### `user_olm`
- `id` (Primary Key)
- `olm_id` (Unique, Index)
- `role` (admin/user)
- `is_active` (Boolean)
- `created_at` (Timestamp)
- `last_login` (Timestamp)

#### `mnp_journey`
- `id` (Primary Key)
- `msisdn` (Phone Number)
- `event_type` (UPC, Port_in, Port_out, NPD_IN, NPD_Out, Number_return)
- `timestamp` (Event Time)
- `operator` (Telecom Operator)
- `circle` (Region)
- `result` (Success/Failed)
- `txn_id` (Transaction ID)
- `details` (JSON Extra Data)
- `created_at` (Record Time)

#### `application_log`
- `id` (Primary Key)
- `msisdn` (Phone Number)
- `log_time` (Log Timestamp)
- `log_level` (ERROR/WARNING/INFO/DEBUG)
- `source` (API/Orchestrator/Database/etc)
- `message` (Log Message)
- `created_at` (Record Time)

## 🔐 Authentication

The API uses OLM ID-based authentication:

1. **Login**: Provide `olm_id` in request body
2. **Validation**: System checks if OLM ID exists and is active
3. **Access**: Active OLM IDs can access all endpoints
4. **Roles**: 
   - `admin`: Can manage users and view all data
   - `user`: Can only view their own data

### Sample OLM IDs (Default)
```
USER001 (admin)
USER002 (user)
USER003 (user)
```

Change these in `app/auth.py` for production.

## 📊 MNP Journey Event Types

- **UPC**: Under Process - Initial stage
- **Port_in**: Number received from donor operator
- **Port_out**: Number released by current operator
- **NPD_IN**: National Portal Day - Incoming
- **NPD_Out**: National Portal Day - Outgoing
- **Number_return**: Reversal/Failed portability

## 🧪 Testing

### Using Python Script
```bash
python test_api.py
```

### Using cURL
```bash
# Health check
curl http://localhost:8000/health

# Get users
curl http://localhost:8000/users

# Analyze MNP
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "msisdn": "919890123456",
    "olm_id": "USER001"
  }'

# Insert sample data
curl -X POST http://localhost:8000/test/insert_sample_data
```

### Using Python Requests
```python
import requests

BASE_URL = "http://localhost:8000"

# Analyze MNP
response = requests.post(
    f"{BASE_URL}/analyze",
    json={
        "msisdn": "919890123456",
        "olm_id": "USER001"
    }
)
print(response.json())
```

## 📁 Project Structure

```
mnp-ai-bot/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app and routes
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic request/response models
│   ├── database.py          # Database configuration
│   ├── auth.py              # Authentication and OLM ID validation
│   ├── mnp_analyzer.py      # MNP analysis logic
│   ├── config.py            # Configuration
│   └── ...
├── setup_db.py              # Database initialization
├── test_api.py              # API testing script
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables
├── .env.example             # Environment template
└── README.md               # This file
```

## 🔧 Configuration

### Environment Variables (.env)

```bash
# Database
DATABASE_URL=postgresql://mnp_user:password@localhost:5432/mnp_bot_db

# API
API_TITLE=MNP AI Bot
API_VERSION=1.0.0

# CORS (for frontend)
CORS_ORIGINS=["http://localhost:3000", "http://localhost:5173"]

# Logging
LOG_LEVEL=INFO
```

## 🚀 Integration with Frontend

The backend is designed to work with the MNP Frontend React application.

### Frontend Communication
```
Frontend (React)
    ↓
POST /analyze
    ↓
Backend (FastAPI)
    ↓
Database + Logs
    ↓
JSON Response
    ↓
Frontend Display
```

### Expected Frontend URL Configuration
```
VITE_API_URL=http://localhost:8000
```

## 📈 Performance Considerations

- **Time Range**: Narrower ranges load faster
- **Indexing**: Database is indexed on MSISDN for quick lookups
- **Connection Pool**: SQLAlchemy connection pooling enabled
- **Async**: FastAPI uses async for non-blocking I/O
- **Caching**: Consider implementing Redis for frequently accessed data

## 🔒 Security Best Practices

### For Production:
1. **HTTPS Only**: Use SSL/TLS certificates
2. **Environment Variables**: Store secrets in .env (not in git)
3. **CORS Whitelist**: Restrict origins to known domains
4. **Database**: Use strong passwords, restrict network access
5. **Rate Limiting**: Implement request rate limiting
6. **API Keys**: Consider implementing API key authentication
7. **Logging**: Don't log sensitive data

### Production Deployment Checklist:
- [ ] Use strong database password
- [ ] Set CORS_ORIGINS to your frontend domain
- [ ] Enable HTTPS
- [ ] Configure firewall rules
- [ ] Set LOG_LEVEL to WARNING
- [ ] Use environment-specific .env files
- [ ] Test all endpoints
- [ ] Monitor error logs

## 🐛 Troubleshooting

### Common Issues

#### Database Connection Error
```
Error: could not connect to server
Solution: 
1. Verify PostgreSQL is running
2. Check DATABASE_URL in .env
3. Verify credentials are correct
4. Check database exists: psql -l
```

#### Port 8000 Already in Use
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :8000
kill -9 <PID>
```

#### OLM ID Not Found
```
Solution:
1. Check OLM ID exists: GET /users
2. Insert sample data: POST /test/insert_sample_data
3. Verify in database: SELECT * FROM user_olm;
```

#### Module Not Found
```bash
# Ensure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt
```

## 📚 API Documentation

### Interactive Docs
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Both provide interactive API exploration and testing.

## 🔄 Development Workflow

1. **Start Database**: PostgreSQL running
2. **Activate venv**: `source venv/bin/activate`
3. **Run Server**: `uvicorn app.main:app --reload`
4. **Test API**: http://localhost:8000/docs
5. **Check Logs**: Console output

## 📊 Logging

Logs are stored in the `application_log` table:

```sql
SELECT * FROM application_log 
WHERE msisdn = '919890123456' 
ORDER BY log_time DESC;
```

## 🤝 Contributing

### To Add New Endpoints:
1. Add route in `main.py`
2. Add request/response schema in `schemas.py`
3. Add database logic as needed
4. Update this README

## 📞 Support

### For Issues:
1. Check error logs in console
2. Verify database connectivity
3. Review troubleshooting section
4. Check PostgreSQL is running

### For Frontend Integration:
See frontend README: `../mnp-frontend/README.md`

## 📜 License

Proprietary - MNP AI Bot

## 🎯 Version

Current Version: **1.0.0**
Release Date: 2024-05-25
Status: Production Ready

---

**Happy Analyzing!** 🚀

For frontend setup, see: [MNP Frontend README](../mnp-frontend/README.md)