from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional, List, Dict, Any


class LoginRequest(BaseModel):
    olm_id: str
    password: str


class UserResponse(BaseModel):
    olm_id: str
    role: str
    is_active: bool
    last_login: Optional[datetime] = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class MNPRequest(BaseModel):
    msisdn: str = Field(..., min_length=10, max_length=15)
    olm_id: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

    @field_validator('msisdn')
    def validate_msisdn(cls, v):
        digits_only = ''.join(c for c in v if c.isdigit())
        if not digits_only:
            raise ValueError('MSISDN must contain digits')
        return digits_only


class MNPJourneyResponse(BaseModel):
    event_type: str
    timestamp: datetime
    operator: Optional[str]
    circle: Optional[str]
    result: Optional[str]
    txn_id: Optional[str]
    details: Dict[str, Any]


class LogAnalysisResponse(BaseModel):
    summary: str
    error_count: int
    warning_count: int
    info_count: int
    key_issues: List[str]
    timeline: Dict[str, int]


class SuggestionItem(BaseModel):
    category: str
    priority: str
    suggestion: str
    details: str


class MNPFullResponse(BaseModel):
    msisdn: str
    time_range: Dict[str, datetime]
    tabular_journey: List[MNPJourneyResponse]
    tabular_text: str
    logs_analysis: LogAnalysisResponse
    suggestions: List[SuggestionItem]
    status: str


class AIAnalysisOutput(BaseModel):
    root_cause: str = ""
    recommendations: List[str] = []
    warnings: List[str] = []
    next_actions: List[str] = []
