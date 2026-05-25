#!/usr/bin/env python3
"""
Test script for MNP AI Bot API
This tests the running API server, not the database setup
"""

import requests
import json
import sys

BASE_URL = "http://localhost:8000"

def test_health():
    print("\n🏥 Testing Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Server is healthy!")
            print(f"   Status: {data['status']}")
            print(f"   Version: {data['version']}")
            return True
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server!")
        print("   Make sure the server is running: uvicorn app.main:app --reload")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_insert_sample_data():
    print("\n📝 Inserting Sample Data...")
    try:
        response = requests.post(f"{BASE_URL}/test/insert_sample_data", timeout=5)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data['message']}")
            print(f"   Inserted {data['count']} records")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_list_users():
    print("\n👥 Listing OLM Users...")
    try:
        response = requests.get(f"{BASE_URL}/users", timeout=5)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            users = response.json()
            print(f"✅ Found {len(users)} users:")
            for user in users:
                print(f"   • {user['olm_id']} ({user['role']}) - Active: {user['is_active']}")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_analyze():
    print("\n🔍 Testing MNP Analysis...")
    
    payload = {
        "olm_id": "OLM_ADMIN_001",
        "msisdn": "919890123456"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/analyze", json=payload, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            print("\n📊 TABULAR JOURNEY:")
            print("=" * 60)
            print(data['tabular_text'])
            
            print("\n📋 LOGS ANALYSIS:")
            print("=" * 60)
            print(data['logs_analysis']['summary'])
            
            if data['logs_analysis']['anomalies']:
                print("\n⚠️ Anomalies Detected:")
                for anomaly in data['logs_analysis']['anomalies']:
                    print(f"   • {anomaly}")
            
            print("\n💡 SUGGESTIONS & RECOMMENDATIONS:")
            print("=" * 60)
            for rec in data['suggestions']['recommendations']:
                print(f"   • {rec}")
            
            if data['suggestions']['warnings']:
                print("\n⚠️ Warnings:")
                for warn in data['suggestions']['warnings']:
                    print(f"   • {warn}")
            
            print("\n🎯 NEXT ACTIONS:")
            for action in data['suggestions']['next_actions']:
                print(f"   • {action}")
            
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("🚀 MNP AI Bot API Test Suite")
    print("=" * 60)
    
    # First check if server is running
    if not test_health():
        print("\n❌ Server is not running!")
        print("\nPlease start the server first:")
        print("  1. Open a new terminal")
        print("  2. Run: cd C:\\Users\\gupta\\Desktop\\RandomProjects\\mnp-ai-bot")
        print("  3. Run: venv\\Scripts\\activate")
        print("  4. Run: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
        return
    
    # Run tests
    test_list_users()
    test_insert_sample_data()
    test_analyze()
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("\n💡 Try these:")
    print("   • Open browser: http://localhost:8000/docs")
    print("   • curl http://localhost:8000/users")
    print("   • curl http://localhost:8000/health")

if __name__ == "__main__":
    main()