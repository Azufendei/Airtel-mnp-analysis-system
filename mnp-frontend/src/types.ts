export interface MNPJourneyEvent {
  msisdn: string;
  event_type: string;
  timestamp: string;
  operator: string;
  circle: string;
  result: string;
  txn_id: string;
  details: Record<string, any>;
}

export interface LogEntry {
  msisdn: string;
  log_time: string;
  log_level: string;
  source: string;
  message: string;
}

export interface LogsAnalysis {
  summary: string;
  error_count: number;
  warning_count: number;
  info_count: number;
  key_issues: string[];
  timeline: Record<string, number>;
}

export interface Suggestion {
  category: string;
  priority: string;
  suggestion: string;
  details: string;
}

export interface MNPAnalysisResponse {
  msisdn: string;
  time_range: {
    start: string;
    end: string;
  };
  tabular_journey: MNPJourneyEvent[];
  tabular_text: string;
  logs_analysis: LogsAnalysis;
  suggestions: Suggestion[];
  status: string;
}

export interface MNPRequest {
  msisdn: string;
  olm_id?: string;
  start_time?: string;
  end_time?: string;
}

export interface UserProfile {
  olm_id: string;
  role: string;
  is_active: boolean;
  last_login?: string;
}

export interface AuthContextType {
  olmId: string | null;
  user: UserProfile | null;
  isAuthenticated: boolean;
  login: (olmId: string, password: string) => Promise<void>;
  logout: () => void;
}
