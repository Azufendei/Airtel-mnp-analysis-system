# Getting Started - MNP AI Bot Backend

A quick guide to set up and run the MNP AI Bot backend API locally.

## ⚡ Quick Start (10 minutes)

### Prerequisites
- Python 3.8+ installed
- PostgreSQL 12+ installed and running
- pip and virtualenv available

### 1. Setup Virtual Environment
```bash
cd mnp-ai-bot

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your database credentials
# DATABASE_URL=postgresql://mnp_user:your_secure_password@localhost:5432/mnp_bot_db
```

### 4. Setup Database
```bash
# Initialize database tables
python setup_db.py
```

### 5. Start Server
```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at: **http://localhost:8000**
- Swagger Docs: **http://localhost:8000/docs**
- ReDoc Docs: **http://localhost:8000/redoc**

## 🗄️ Database Setup

### Windows PostgreSQL Setup
```bash
# Open pgAdmin or psql
psql -U postgres

# Create database and user
CREATE DATABASE mnp_bot_db;
CREATE USER mnp_user WITH PASSWORD 'your_secure_password';
ALTER ROLE mnp_user SET client_encoding TO 'utf8';
ALTER ROLE mnp_user SET default_transaction_isolation TO 'read committed';
GRANT ALL PRIVILEGES ON DATABASE mnp_bot_db TO mnp_user;
```

### macOS PostgreSQL Setup
```bash
# Install with Homebrew
brew install postgresql@15
brew services start postgresql@15

# Create database
createuser -P mnp_user  # prompts for password
createdb -O mnp_user mnp_bot_db
```

### Linux PostgreSQL Setup
```bash
sudo apt-get install postgresql postgresql-contrib
sudo -u postgres psql

CREATE DATABASE mnp_bot_db;
CREATE USER mnp_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE mnp_bot_db TO mnp_user;
```

## 🧪 Testing the API

### Check Health
```bash
curl http://localhost:8000/health
```

### Insert Sample Data
```bash
curl -X POST http://localhost:8000/test/insert_sample_data
```

### Analyze MNP
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "msisdn": "919890123456",
    "olm_id": "USER001"
  }'
```

## 📊 Database Management (Local CLI Only)

Database operations are restricted to local file-based usage. Use the `db_cli.py` script:

### Check Database Stats
```bash
python db_cli.py stats
```

### Query Journey Records
```bash
python db_cli.py query mnp_journey --msisdn 919890123456
```

### Add a Journey Record

1. Create `journey_data.json`:
```json
{
  "msisdn": "919876543210",
  "event_type": "Port_out",
  "timestamp": "2026-05-26T10:30:00",
  "operator": "Airtel",
  "circle": "Delhi",
  "result": "Success",
  "txn_id": "TXN123456",
  "details": {"port_out_code": "PO123"}
}
```

2. Add record:
```bash
python db_cli.py add journey journey_data.json
```

### Other Database Operations
```bash
# Add log
python db_cli.py add log log_data.json

# Update record
python db_cli.py update journey <ID> update_data.json

# Delete record (with confirmation)
python db_cli.py delete journey <ID>

# View table structure
python db_cli.py structure mnp_journey
```

**See DATABASE_CLI_GUIDE.md for complete CLI documentation.**

## 📋 Default OLM IDs
- `USER001` (admin)
- `USER002` (user)
- `USER003` (user)

## 🚀 Available Commands

```bash
# Development server with auto-reload
uvicorn app.main:app --reload --port 8000

# Production server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# Database initialization
python setup_db.py

# Test API
python test_api.py
```

## 📚 For More Information

- See [README.md](./README.md) for detailed documentation
- Frontend setup: See [../mnp-frontend/README.md](../mnp-frontend/README.md)
- API documentation: http://localhost:8000/docs

## ⚠️ Troubleshooting

### Database Connection Error
```
Verify:
1. PostgreSQL is running
2. DATABASE_URL in .env is correct
3. Database user exists
4. Network connectivity is available
```

### Port 8000 Already in Use
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :8000
kill -9 <PID>
```

### Module Not Found
```bash
# Ensure venv is activated
# Reinstall dependencies
pip install -r requirements.txt
```

### Virtual Environment Issues
```bash
# Delete and recreate venv
rm -rf venv
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```
