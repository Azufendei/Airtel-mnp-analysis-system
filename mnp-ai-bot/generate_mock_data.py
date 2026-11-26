import random
import string
from datetime import datetime, timedelta
from app.database import SessionLocal
from app.models import MNPJourney, ApplicationLog, UserOLM

OPERATORS = ["Jio", "Airtel", "Vi", "BSNL"]
CIRCLES = ["Mumbai", "Delhi", "Bangalore", "Kolkata", "Chennai", "Pune", "Hyderabad", "Ahmedabad", "Lucknow", "Chandigarh"]
EVENT_TYPES = ["UPC", "Port_in", "Port_out", "NPD_IN", "NPD_Out", "Number_return"]
SOURCES = ["API", "Orchestrator", "Database", "Donor Gateway", "Recipient Gateway"]
LOG_LEVELS = ["INFO", "WARNING", "ERROR", "DEBUG"]
RESULTS = ["Success", "Failed"]

MSISDNS = [
    "919890123456", "919876543210", "919811223344", "919922334455",
    "919833445566", "919844556677", "919855667788", "919866778899",
    "919877889900", "919988990011", "919800112233", "919911223344",
]

def random_msisdn():
    return random.choice(MSISDNS)

def random_phone():
    return "91" + str(random.randint(7000000000, 9999999999))

def generate_txn_id():
    return "TXN" + "".join(random.choices(string.ascii_uppercase + string.digits, k=10))

def generate_journey_for_msisdn(msisdn, base_time):
    records = []
    total_events = random.randint(3, 8)
    current_time = base_time - timedelta(days=random.randint(30, 90))

    for _ in range(total_events):
        event_type = random.choice(EVENT_TYPES)
        operator = random.choice(OPERATORS)
        circle = random.choice(CIRCLES)
        result = random.choices(RESULTS, weights=[0.75, 0.25])[0]
        txn_id = generate_txn_id()

        details = {}
        if event_type == "Port_in":
            donor = random.choice([o for o in OPERATORS if o != operator])
            details = {"donor": donor, "recipient": operator, "port_in_code": f"PI{random.randint(100000,999999)}"}
        elif event_type == "Port_out":
            details = {"port_out_code": f"PO{random.randint(100000,999999)}", "recipient": random.choice([o for o in OPERATORS if o != operator])}
        elif event_type == "UPC":
            details = {"upc_code": f"UPC{random.randint(100000,999999)}", "validity_days": 15}
        elif event_type == "Number_return" and result == "Failed":
            reasons = ["Cooling period violation", "Donor rejection", "Invalid documents", "System timeout", "Duplicate request"]
            details = {"reason": random.choice(reasons)}

        current_time += timedelta(hours=random.randint(2, 72))
        if current_time > base_time:
            break

        records.append(MNPJourney(
            msisdn=msisdn,
            event_type=event_type,
            timestamp=current_time,
            operator=operator,
            circle=circle,
            result=result,
            txn_id=txn_id,
            details=details,
        ))
    return records

def generate_logs_for_msisdn(msisdn, journey_records):
    logs = []
    for j in journey_records:
        for _ in range(random.randint(0, 4)):
            log_time = j.timestamp + timedelta(seconds=random.randint(-300, 300))
            log_level = random.choices(LOG_LEVELS, weights=[0.5, 0.2, 0.15, 0.15])[0]
            source = random.choice(SOURCES)

            messages = {
                "INFO": [
                    f"Request received for MSISDN {msisdn}",
                    f"Processing {j.event_type} event for {msisdn}",
                    f"Response received from donor network for {msisdn}",
                    f"Database update completed for transaction {j.txn_id}",
                    f"Validation passed for MSISDN {msisdn}",
                ],
                "WARNING": [
                    f"Slow response from donor gateway for MSISDN {msisdn}",
                    f"Retry attempt #{random.randint(1,3)} for transaction {j.txn_id}",
                    f"Cooling period approaching limit for {msisdn}",
                    f"Database connection pool at 80% capacity",
                ],
                "ERROR": [
                    f"Timeout waiting for donor response for MSISDN {msisdn}",
                    f"Failed to process {j.event_type} for {msisdn}: {random.choice(['Connection refused', 'Invalid response format', 'Authentication failed'])}",
                    f"Database error: could not insert record for transaction {j.txn_id}",
                    f"Orchestrator failure: state machine inconsistent for {msisdn}",
                ],
                "DEBUG": [
                    f"Raw response: {{'status': 'pending', 'txn_id': '{j.txn_id}'}}",
                    f"Memory usage: {random.randint(200, 800)}MB",
                    f"Cache hit for MSISDN {msisdn}",
                ],
            }

            msg = random.choice(messages.get(log_level, messages["INFO"]))

            extracted = {}
            if log_level == "ERROR" and "timeout" in msg.lower():
                extracted = {"timeout_seconds": random.randint(10, 60)}

            logs.append(ApplicationLog(
                msisdn=msisdn,
                log_time=log_time,
                log_level=log_level,
                source=source,
                message=msg,
                extracted=extracted,
            ))
    return logs

def generate_all():
    db = SessionLocal()

    try:
        # Clear existing data
        db.query(ApplicationLog).delete()
        db.query(MNPJourney).delete()

        base_time = datetime.utcnow()
        all_journeys = []
        all_logs = []

        for msisdn in MSISDNS:
            journeys = generate_journey_for_msisdn(msisdn, base_time)
            all_journeys.extend(journeys)
            logs = generate_logs_for_msisdn(msisdn, journeys)
            all_logs.extend(logs)

        for r in all_journeys:
            db.add(r)
        for l in all_logs:
            db.add(l)
        db.commit()

        print(f"Inserted {len(all_journeys)} MNP journey records")
        print(f"Inserted {len(all_logs)} application log records")
        print(f"Across {len(MSISDNS)} unique MSISDNs")

        # Summary stats
        event_counts = {}
        for r in all_journeys:
            event_counts[r.event_type] = event_counts.get(r.event_type, 0) + 1
        print(f"\nJourney event distribution: {event_counts}")

        result_counts = {"Success": 0, "Failed": 0}
        for r in all_journeys:
            if r.result in result_counts:
                result_counts[r.result] += 1
        print(f"Result distribution: {result_counts}")

        log_level_counts = {}
        for l in all_logs:
            log_level_counts[l.log_level] = log_level_counts.get(l.log_level, 0) + 1
        print(f"Log level distribution: {log_level_counts}")

    finally:
        db.close()

if __name__ == "__main__":
    generate_all()