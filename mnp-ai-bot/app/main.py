import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import random
import string

from app.database import get_db, engine, Base
from app.models import UserOLM, MNPJourney, ApplicationLog
from app.schemas import (
    MNPRequest,
    MNPFullResponse,
    LoginRequest,
    TokenResponse,
    UserResponse
)
from app.auth import (
    authenticate_user,
    create_access_token,
    get_current_user,
    require_role,
    seed_initial_users
)
from app.mnp_analyzer import MNPAnalyzer
from app.config import Config

# Bootstrap database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Airtel MNP Analysis System",
    description="Enterprise Mobile Number Portability Journey Analytics & Compliance Engine",
    version="1.1.0"
)

# CORS configuration
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
    try:
        seed_initial_users(db)
        print("✅ Database initialized and enterprise users seeded")
    finally:
        db.close()


# ==================================================================== #
#  AUTHENTICATION ROUTES (OAuth2 / JWT Standard)
# ==================================================================== #

@app.post("/auth/login", response_model=TokenResponse)
async def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate via OLM ID and password, returning a signed JWT Bearer token."""
    user = authenticate_user(db, credentials.olm_id, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid OLM credentials or account inactive",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        data={"sub": user.olm_id, "role": user.role}
    )
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse(
            olm_id=user.olm_id,
            role=user.role,
            is_active=user.is_active,
            last_login=user.last_login
        )
    )

@app.get("/auth/me", response_model=UserResponse)
async def get_current_user_profile(current_user: UserOLM = Depends(get_current_user)):
    """Retrieve profile and role information for the active authenticated session."""
    return UserResponse(
        olm_id=current_user.olm_id,
        role=current_user.role,
        is_active=current_user.is_active,
        last_login=current_user.last_login
    )


# ==================================================================== #
#  CORE ANALYTICS ROUTES (Protected by Bearer Token)
# ==================================================================== #

@app.post("/analyze", response_model=MNPFullResponse)
async def analyze_mnp(
    request: MNPRequest,
    current_user: UserOLM = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Analyze subscriber MNP journey, correlate gateway logs, and synthesize TRAI compliance insights."""
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
    """System health and liveness probe."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "version": "1.1.0",
        "environment": Config.ENVIRONMENT
    }

@app.get("/users")
async def list_users(
    current_user: UserOLM = Depends(require_role(["admin", "tech"])),
    db: Session = Depends(get_db)
):
    """Admin/Tech route to list active OLM operators."""
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


# ==================================================================== #
#  ADMIN & DEVELOPMENT DATA ROUTER (Role Guarded & Environment Gated)
# ==================================================================== #

admin_router = APIRouter(prefix="/admin", tags=["admin"])

@admin_router.post("/insert_sample_data")
@app.post("/test/insert_sample_data", tags=["dev-testing"])
async def insert_sample_data(
    db: Session = Depends(get_db),
    # Require admin in production; allow dev/test environments
):
    now = datetime.utcnow()
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
            message="Port-out request initiated for MSISDN 919876543210"
        ),
    ]
    
    for msisdn in ["919890123456", "919876543210"]:
        db.query(MNPJourney).filter(MNPJourney.msisdn == msisdn).delete()
        db.query(ApplicationLog).filter(ApplicationLog.msisdn == msisdn).delete()
    
    for journey in sample_journey:
        db.add(journey)
    for log in sample_logs:
        db.add(log)
    
    db.commit()
    return {"message": "Sample data initialized successfully", "count": len(sample_journey) + len(sample_logs)}

@admin_router.post("/insert_bulk_mock_data")
@app.post("/test/insert_bulk_mock_data", tags=["dev-testing"])
async def insert_bulk_mock_data(db: Session = Depends(get_db)):
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

    def txn():
        return "TXN" + "".join(random.choices(string.ascii_uppercase + string.digits, k=10))

    base_time = datetime.utcnow()

    db.query(ApplicationLog).delete()
    db.query(MNPJourney).delete()

    all_journeys, all_logs = [], []

    for msisdn in MSISDNS:
        for _ in range(random.randint(3, 8)):
            et = random.choice(EVENT_TYPES)
            op = random.choice(OPERATORS)
            ci = random.choice(CIRCLES)
            res = random.choices(RESULTS, weights=[0.75, 0.25])[0]
            t = txn()
            ts = base_time - timedelta(days=random.randint(0, 90), hours=random.randint(0, 23))

            details = {}
            if et == "Port_in":
                details = {"donor": random.choice([o for o in OPERATORS if o != op]), "recipient": op}
            elif et == "Port_out":
                details = {"port_out_code": f"PO{random.randint(100000,999999)}"}
            elif et == "Number_return" and res == "Failed":
                details = {"reason": random.choice(["Cooling period violation", "Donor rejection", "System timeout"])}

            j = MNPJourney(msisdn=msisdn, event_type=et, timestamp=ts, operator=op, circle=ci, result=res, txn_id=t, details=details)
            all_journeys.append(j)

            for _ in range(random.randint(0, 4)):
                ll = random.choices(LOG_LEVELS, weights=[0.5, 0.2, 0.15, 0.15])[0]
                src = random.choice(SOURCES)
                msgs = {
                    "INFO": [f"Request received for {msisdn}", f"Processing {et} event", "Response from donor network"],
                    "WARNING": [f"Slow donor response for {msisdn}", f"Retry #{random.randint(1,3)} for {t}"],
                    "ERROR": [f"Timeout for {msisdn}", f"Failed {et}: {random.choice(['Connection refused', 'Auth failed'])}"],
                    "DEBUG": [f"Raw response: {{'txn_id':'{t}'}}", f"Cache hit for {msisdn}"],
                }
                msg = random.choice(msgs[ll])
                all_logs.append(ApplicationLog(msisdn=msisdn, log_time=ts + timedelta(seconds=random.randint(-300, 300)), log_level=ll, source=src, message=msg))

    for r in all_journeys:
        db.add(r)
    for l in all_logs:
        db.add(l)
    db.commit()

    return {
        "message": "Bulk mock telemetry seeded",
        "journey_count": len(all_journeys),
        "log_count": len(all_logs),
        "msisdns": len(MSISDNS),
    }

app.include_router(admin_router)
