from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models import MNPJourney, ApplicationLog
from tabulate import tabulate
from groq import Groq
from app.config import Config
import json
import logging

# Setup logging
logger = logging.getLogger(__name__)

class MNPAnalyzer:
    def __init__(self, db: Session):
        self.db = db
        # Initialize Groq client only if API key is available
        if Config.GROQ_API_KEY:
            self.groq_client = Groq(api_key=Config.GROQ_API_KEY)
            self.groq_available = True
        else:
            self.groq_available = False
            logger.warning("GROQ_API_KEY not found. Using rule-based suggestions only.")

    # ------------------------------------------------------------------ #
    #  Data fetching
    # ------------------------------------------------------------------ #

    def fetch_journey(self, msisdn: str, start_time: datetime, end_time: datetime) -> List[Dict]:
        records = self.db.query(MNPJourney).filter(
            and_(
                MNPJourney.msisdn == msisdn,
                MNPJourney.timestamp >= start_time,
                MNPJourney.timestamp <= end_time
            )
        ).order_by(MNPJourney.timestamp).all()

        return [
            {
                "event_type": r.event_type,
                "timestamp": r.timestamp,
                "operator": r.operator,
                "circle": r.circle,
                "result": r.result,
                "txn_id": r.txn_id,
                "details": r.details
            }
            for r in records
        ]

    def fetch_logs(self, msisdn: str, start_time: datetime, end_time: datetime) -> List[Dict]:
        logs = self.db.query(ApplicationLog).filter(
            and_(
                ApplicationLog.msisdn == msisdn,
                ApplicationLog.log_time >= start_time,
                ApplicationLog.log_time <= end_time
            )
        ).order_by(ApplicationLog.log_time).all()

        return [
            {
                "log_time": l.log_time,
                "log_level": l.log_level,
                "source": l.source,
                "message": l.message,
                "extracted": l.extracted
            }
            for l in logs
        ]

    # ------------------------------------------------------------------ #
    #  Formatting
    # ------------------------------------------------------------------ #

    def format_tabular_journey(self, journey: List[Dict]) -> str:
        if not journey:
            return "No MNP journey records found for the given MSISDN and time range."

        table_data = []
        for event in journey:
            table_data.append([
                event['event_type'],
                event['timestamp'].strftime("%Y-%m-%d %H:%M:%S"),
                event['operator'] or '-',
                event['circle'] or '-',
                event['result'] or '-',
                event['txn_id'] or '-'
            ])

        headers = ["Event Type", "Timestamp", "Operator", "Circle", "Result", "Txn ID"]
        return tabulate(table_data, headers=headers, tablefmt="grid")

    # ------------------------------------------------------------------ #
    #  Log analysis (rule-based — fast, no API call)
    # ------------------------------------------------------------------ #

    def analyze_logs(self, logs: List[Dict]) -> Dict:
        if not logs:
            return {
                "summary": "No logs found for this time period.",
                "error_count": 0,
                "warning_count": 0,
                "info_count": 0,
                "key_issues": [],
                "timeline": {}
            }

        error_count = 0
        warning_count = 0
        info_count = 0
        key_issues = []
        timeline_dict = {}

        for log in logs:
            log_level = log['log_level'].upper()
            if log_level == 'ERROR':
                error_count += 1
            elif log_level == 'WARNING':
                warning_count += 1
            elif log_level == 'INFO':
                info_count += 1

            # Build timeline as Record<string, number>
            time_key = log['log_time'].strftime("%Y-%m-%d %H:%M")
            timeline_dict[time_key] = timeline_dict.get(time_key, 0) + 1

        # Detect anomalies and create key issues
        if error_count > 5:
            key_issues.append(f"High error rate detected: {error_count} errors in {len(logs)} logs")

        for log in logs:
            msg_lower = log['message'].lower()
            if 'timeout' in msg_lower:
                key_issues.append(f"Timeout detected at {log['log_time'].strftime('%Y-%m-%d %H:%M:%S')} from {log['source']}")
            if 'failed' in msg_lower and 'port' in msg_lower:
                key_issues.append(f"Porting failure detected at {log['log_time'].strftime('%Y-%m-%d %H:%M:%S')}")
            if 'database' in msg_lower and 'error' in msg_lower:
                key_issues.append(f"Database error detected at {log['log_time'].strftime('%Y-%m-%d %H:%M:%S')}")

        summary = f"Analyzed {len(logs)} log entries. Found {error_count} errors, {warning_count} warnings, and {info_count} info messages."

        return {
            "summary": summary,
            "error_count": error_count,
            "warning_count": warning_count,
            "info_count": info_count,
            "key_issues": key_issues[:10],
            "timeline": timeline_dict
        }

    # ------------------------------------------------------------------ #
    #  AI-powered suggestions (Groq) with rule-based fallback
    #  Note: Only works with GROQ_API_KEY set in .env
    # ------------------------------------------------------------------ #

    def generate_suggestions(self, journey: List[Dict], logs: List[Dict], analysis: Dict) -> Dict:
        # Check if Groq is available and configured
        if self.groq_available and Config.GROQ_API_KEY:
            try:
                return self._ai_suggestions(journey, logs, analysis)
            except Exception as e:
                logger.error(f"Groq AI failed: {e}, falling back to rule-based")
                return self._rule_based_suggestions(journey, analysis)
        else:
            logger.info("Groq not available, using rule-based suggestions")
            return self._rule_based_suggestions(journey, analysis)

    def _ai_suggestions(self, journey: List[Dict], logs: List[Dict], analysis: Dict) -> Dict:
        journey_summary = self._build_journey_context(journey)
        logs_summary = self._build_logs_context(logs, analysis)
        metrics = self._calculate_metrics(journey, logs)

        prompt = f"""You are an expert MNP (Mobile Number Portability) analyst for Indian telecom (TRAI regulations).

## MNP Journey Data:
{journey_summary}

## Application Logs & Errors:
{logs_summary}

## Key Metrics:
- Total events: {metrics['total_events']}
- Success rate: {metrics['success_rate']:.1f}%
- Failed events: {metrics['failed_count']}
- Time span: {metrics['time_span_days']} days

## Current Issues Detected:
{chr(10).join(analysis.get('anomalies', ['None detected']))}

## TRAI Regulations to consider:
- Cooling period: 10 days minimum before number return
- Porting time: Within 4 days for same circle
- UPC validity: 15 days from generation

Based on this data, provide:
1. Root Cause Analysis (What likely caused any failures?)
2. Specific Recommendations (Actionable steps to resolve issues)
3. Compliance Warnings (Any TRAI violations or risks)
4. Next Actions (Priority order for support team)

Respond ONLY in JSON format:
{{
    "root_cause": "Brief root cause analysis",
    "recommendations": ["rec1", "rec2", "rec3", "rec4", "rec5"],
    "warnings": ["warning1", "warning2", "warning3"],
    "next_actions": ["action1", "action2", "action3"]
}}"""

        response = self.groq_client.chat.completions.create(
            model=Config.GROQ_MODEL,
            messages=[
                {"role": "system", "content": "You are an expert MNP analyst. Respond only with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1000,
        )

        raw = response.choices[0].message.content.strip()
        
        # Strip markdown fences if present
        if raw.startswith("```json"):
            raw = raw[7:]
        elif raw.startswith("```"):
            raw = raw[3:]
        if raw.endswith("```"):
            raw = raw[:-3]

        result = json.loads(raw.strip())

        suggestions = []
        
        # Add recommendations as high priority suggestions
        for rec in result.get("recommendations", [])[:3]:
            suggestions.append({
                "category": "Recommendations",
                "priority": "high",
                "suggestion": rec,
                "details": "This is a recommended action based on AI analysis of your MNP journey."
            })
        
        # Add warnings as critical priority suggestions
        for warn in result.get("warnings", [])[:2]:
            suggestions.append({
                "category": "Warnings",
                "priority": "critical",
                "suggestion": warn,
                "details": "This warning indicates a potential issue with your MNP process."
            })
        
        # Add next actions as medium priority suggestions
        for action in result.get("next_actions", [])[:2]:
            suggestions.append({
                "category": "Next Actions",
                "priority": "medium",
                "suggestion": action,
                "details": "This is a priority action for the support team."
            })
        
        return suggestions

    def _build_journey_context(self, journey: List[Dict]) -> str:
        if not journey:
            return "No journey events recorded."

        context = []
        for e in journey:
            context.append(
                f"- {e['event_type']} | {e['timestamp'].strftime('%Y-%m-%d %H:%M')} | "
                f"Operator: {e['operator'] or 'N/A'} | Circle: {e['circle'] or 'N/A'} | "
                f"Result: {e['result'] or 'N/A'} | TXN: {e['txn_id']}"
            )
            if e.get('details'):
                context.append(f"  Details: {json.dumps(e['details'])}")
        return "\n".join(context)

    def _build_logs_context(self, logs: List[Dict], analysis: Dict) -> str:
        if not logs:
            return "No logs available."

        context = []
        
        # Add key issues if available
        if analysis.get('key_issues'):
            context.append(f"KEY ISSUES ({len(analysis['key_issues'])}):")
            for issue in analysis['key_issues'][:5]:
                context.append(f"  - {issue}")

        # Add log level distribution
        log_levels = {}
        for log in logs:
            level = log['log_level']
            log_levels[level] = log_levels.get(level, 0) + 1
        
        if log_levels:
            context.append("\nLOG DISTRIBUTION:")
            for level, count in log_levels.items():
                context.append(f"  - {level}: {count}")

        return "\n".join(context) if context else "No significant issues in logs."

    def _calculate_metrics(self, journey: List[Dict], logs: List[Dict]) -> Dict:
        total_events = len(journey)
        success_count = len([e for e in journey if e.get('result') == 'Success'])
        failed_count = len([e for e in journey if e.get('result') == 'Failed'])
        success_rate = (success_count / total_events * 100) if total_events > 0 else 0

        time_span_days = 0
        if len(journey) >= 2:
            start = min(e['timestamp'] for e in journey)
            end = max(e['timestamp'] for e in journey)
            time_span_days = (end - start).days

        return {
            'total_events': total_events,
            'success_count': success_count,
            'failed_count': failed_count,
            'success_rate': success_rate,
            'time_span_days': time_span_days,
            'total_logs': len(logs)
        }

    def _rule_based_suggestions(self, journey: List[Dict], analysis: Dict) -> List[Dict]:
        recommendations = []
        warnings = []
        next_actions = []

        failed_events = [e for e in journey if e.get('result') == 'Failed']
        if failed_events:
            for event in failed_events:
                recommendations.append(f"Investigate failed {event['event_type']} on {event['timestamp'].strftime('%Y-%m-%d')}")

        port_in_events = [e for e in journey if e['event_type'] == 'Port_in' and e.get('result') == 'Success']
        return_events = [e for e in journey if e['event_type'] == 'Number_return']

        for port_in in port_in_events:
            for return_event in return_events:
                time_diff = (return_event['timestamp'] - port_in['timestamp']).days
                if time_diff < 10:
                    warnings.append(f"Number return within {time_diff} days of port-in — 10-day cooling period violation")
                    recommendations.append("Wait for cooling period to complete before retrying number return")

        # Check key issues from analysis
        key_issues = analysis.get('key_issues', [])
        for issue in key_issues:
            issue_lower = issue.lower()
            if 'database' in issue_lower and 'error' in issue_lower:
                recommendations.append("Check database connectivity and query performance")
                next_actions.append("Verify database connection pool settings")
            if 'timeout' in issue_lower:
                recommendations.append("Review API timeout configurations")
                next_actions.append("Increase API timeout values or optimize donor network calls")
            if 'orchestrator' in issue_lower:
                recommendations.append("Review orchestration workflow for race conditions")
                next_actions.append("Check workflow state management")

        if not recommendations:
            recommendations.append("All MNP events completed successfully")
            recommendations.append("Monitor for any delayed porting requests")
        if not next_actions:
            next_actions.append("No immediate actions required")

        suggestions = []
        
        # Add recommendations as high priority suggestions
        for rec in recommendations[:3]:
            suggestions.append({
                "category": "Recommendations",
                "priority": "high",
                "suggestion": rec,
                "details": "This is a recommended action based on analysis of your MNP journey."
            })
        
        # Add warnings as critical priority suggestions
        for warn in warnings[:2]:
            suggestions.append({
                "category": "Warnings",
                "priority": "critical",
                "suggestion": warn,
                "details": "This warning indicates a potential issue with your MNP process."
            })
        
        # Add next actions as medium priority suggestions
        for action in next_actions[:2]:
            suggestions.append({
                "category": "Next Actions",
                "priority": "medium",
                "suggestion": action,
                "details": "This is a priority action for the support team."
            })
        
        return suggestions

    # ------------------------------------------------------------------ #
    #  Time range helper
    # ------------------------------------------------------------------ #

    def get_time_range(self, start_time: Optional[datetime], end_time: Optional[datetime]) -> Tuple[datetime, datetime]:
        if end_time is None:
            end_time = datetime.utcnow()
        if start_time is None:
            start_time = end_time - timedelta(days=7)
        return start_time, end_time