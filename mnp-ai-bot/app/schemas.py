from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional, List, Dict, Any


class OLMAuth(BaseModel):
    olm_id: str


class MNPRequest(BaseModel):
    olm_id: str
    msisdn: str = Field(..., min_length=10, max_length=15)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

    @field_validator('msisdn')
    def validate_msisdn(cls, v):
        if not v.isdigit():
            raise ValueError('MSISDN must contain only digits')
        return v


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