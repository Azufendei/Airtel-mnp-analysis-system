from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db, engine, Base
from app.models import UserOLM, MNPJourney, ApplicationLog
from app.schemas import MNPRequest, MNPFullResponse
from app.auth import verify_olm_id, seed_initial_users
from app.mnp_analyzer import MNPAnalyzer

# Create tables - this will now work because Base is properly defined
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MNP AI Bot",
    description="Mobile Number Portability Journey Analysis & Intelligence Bot",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    db = next(get_db())
    seed_initial_users(db)
    print("✅ Database initialized and users seeded")

@app.post("/analyze", response_model=MNPFullResponse)
async def analyze_mnp(
    request: MNPRequest,
    db: Session = Depends(get_db)
):
    if not verify_olm_id(db, request.olm_id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or inactive OLM ID"
        )
    
    analyzer = MNPAnalyzer(db)
    start_time, end_time = analyzer.get_time_range(request.start_time, request.end_time)
    journey = analyzer.fetch_journey(request.msisdn, start_time, end_time)
    logs = analyzer.fetch_logs(request.msisdn, start_time, end_time)
    tabular_text = analyzer.format_tabular_journey(journey)
    logs_analysis = analyzer.analyze_logs(logs)
    suggestions = analyzer.generate_suggestions(journey, logs, logs_analysis)
    
    return MNPFullResponse(
        msisdn=request.msisdn,
        time_range={"start": start_time, "end": end_time},
        tabular_journey=journey,
        tabular_text=tabular_text,
        logs_analysis=logs_analysis,
        suggestions=suggestions,
        status="Success"
    )

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "version": "1.0.0"
    }

@app.post("/test/insert_sample_data")
async def insert_sample_data(db: Session = Depends(get_db)):
    from datetime import datetime, timedelta
    
    # Use current date
    now = datetime.now()
    two_days_ago = now - timedelta(days=2)
    yesterday = now - timedelta(days=1)
    
    sample_journey = [
        MNPJourney(
            msisdn="919890123456",
            event_type="Port_in",
            timestamp=two_days_ago,
            operator="Jio",
            circle="Mumbai",
            result="Success",
            txn_id=f"TXN{int(two_days_ago.timestamp())}",
            details={"donor": "Airtel", "recipient": "Jio"}
        ),
        MNPJourney(
            msisdn="919890123456",
            event_type="NPD_IN",
            timestamp=yesterday,
            operator="Jio",
            circle="Mumbai",
            result="Success",
            txn_id=f"TXN{int(yesterday.timestamp())}",
            details={}
        ),
        MNPJourney(
            msisdn="919890123456",
            event_type="Number_return",
            timestamp=now,
            operator="Airtel",
            circle="Mumbai",
            result="Failed",
            txn_id=f"TXN{int(now.timestamp())}",
            details={"reason": "Cooling period violation"}
        ),
        # Add another MSISDN
        MNPJourney(
            msisdn="919876543210",
            event_type="Port_out",
            timestamp=yesterday - timedelta(hours=5),
            operator="Airtel",
            circle="Delhi",
            result="Success",
            txn_id=f"TXN{int((yesterday - timedelta(hours=5)).timestamp())}",
            details={"port_out_code": "PO123456"}
        ),
    ]
    
    sample_logs = [
        ApplicationLog(
            msisdn="919890123456",
            log_time=two_days_ago - timedelta(minutes=15),
            log_level="INFO",
            source="API",
            message=f"Port-in request received for MSISDN 919890123456 at {two_days_ago}"
        ),
        ApplicationLog(
            msisdn="919890123456",
            log_time=now,
            log_level="ERROR",
            source="Orchestrator",
            message=f"Number return failed: Donor operator rejected due to cooling period violation at {now}"
        ),
        ApplicationLog(
            msisdn="919876543210",
            log_time=yesterday - timedelta(hours=6),
            log_level="INFO",
            source="API",
            message=f"Port-out request initiated for MSISDN 919876543210"
        ),
    ]
    
    # Clear existing data for these MSISDNs (optional)
    for msisdn in ["919890123456", "919876543210"]:
        db.query(MNPJourney).filter(MNPJourney.msisdn == msisdn).delete()
        db.query(ApplicationLog).filter(ApplicationLog.msisdn == msisdn).delete()
    
    for journey in sample_journey:
        db.add(journey)
    
    for log in sample_logs:
        db.add(log)
    
    db.commit()
    return {"message": "Sample data inserted successfully with current dates", "count": len(sample_journey) + len(sample_logs)}

@app.get("/users")
async def list_users(db: Session = Depends(get_db)):
    users = db.query(UserOLM).all()
    return [
        {
            "olm_id": u.olm_id,
            "role": u.role,
            "is_active": u.is_active,
            "last_login": u.last_login
        }
        for u in users
    ]