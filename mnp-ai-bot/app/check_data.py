import requests

# Check users
print("👥 Users in database:")
response = requests.get("http://localhost:8000/users")
if response.status_code == 200:
    for user in response.json():
        print(f"  - {user['olm_id']}")

# Try to get data for MSISDN 919890123456
print("\n🔍 Checking data for MSISDN 919890123456...")

# First, let's see if we can insert fresh data with current dates
from datetime import datetime, timedelta

# Insert data with CURRENT dates (today's date)
current_time = datetime.now()
seven_days_ago = current_time - timedelta(days=7)

payload = {
    "olm_id": "OLM_ADMIN_001",
    "msisdn": "919890123456",
    "start_time": seven_days_ago.isoformat(),
    "end_time": current_time.isoformat()
}

print(f"\n📅 Querying from {seven_days_ago.date()} to {current_time.date()}")
response = requests.post("http://localhost:8000/analyze", json=payload)

if response.status_code == 200:
    data = response.json()
    print(f"Found {len(data['tabular_journey'])} journey events")
    if len(data['tabular_journey']) == 0:
        print("\n⚠️ No data found. Let's insert sample data with current dates...")
        
        # Insert data with current dates using direct API call
        insert_payload = {
            "olm_id": "OLM_ADMIN_001",
            "msisdn": "919890123456",
            "event_type": "Port_in",
            "operator": "Jio",
            "circle": "Mumbai",
            "result": "Success",
            "txn_id": f"TXN{int(current_time.timestamp())}",
            "details": {"donor": "Airtel"}
        }
        
        # Note: You need a special endpoint to insert data
        print("To add current data, use the test endpoint or direct SQL")