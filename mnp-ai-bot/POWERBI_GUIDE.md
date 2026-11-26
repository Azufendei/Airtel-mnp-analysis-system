# Power BI Desktop Integration Guide

This guide covers connecting Power BI Desktop (free) to the MNP AI Bot's PostgreSQL database for reporting and dashboards.

---

## 1. Prerequisites

- Power BI Desktop (free) — download from https://powerbi.microsoft.com/desktop/
- PostgreSQL ODBC driver (for the native connector path)
- MNP AI Bot database running with data (run `generate_mock_data.py` or hit `POST /test/insert_bulk_mock_data`)

## 2. Connect Power BI to PostgreSQL

### Option A: Native PostgreSQL connector (recommended)

1. Open Power BI Desktop → **Get Data** → **PostgreSQL database**
2. Fill in:
   - **Server**: `localhost`
   - **Database**: `mnp_bot_db`
   - **Data Connectivity mode**: `Import`
3. Authenticate with:
   - **User name**: `postgres`
   - **Password**: (your postgres password from `.env`)
4. Select tables: `mnp_journey`, `application_logs`, `user_olm`

### Option B: ODBC connector (fallback)

1. Install PostgreSQL ODBC driver from https://www.postgresql.org/ftp/odbc/
2. Open Power BI Desktop → **Get Data** → **ODBC**
3. Select the PostgreSQL ODBC DSN (or create one via Windows ODBC Data Sources)
4. Enter credentials

## 3. Data Model Setup

After loading tables, set up relationships in the **Model** view:

```
mnp_journey.msisdn ──┬── application_logs.msisdn
                     └── (many-to-many via msisdn)
```

**Key columns by table:**

| Table | Column | Purpose |
|---|---|---|
| `mnp_journey` | `event_type` | UPC, Port_in, Port_out, NPD_IN, NPD_Out, Number_return |
| `mnp_journey` | `operator` | Telecom operator (Jio, Airtel, Vi, BSNL) |
| `mnp_journey` | `circle` | Region/circle |
| `mnp_journey` | `result` | Success / Failed |
| `mnp_journey` | `timestamp` | Event date/time |
| `application_logs` | `log_level` | INFO, WARNING, ERROR, DEBUG |
| `application_logs` | `source` | API, Orchestrator, Database, etc. |
| `user_olm` | `role` | admin, viewer, tech |

## 4. Recommended Reports & Visuals

### Dashboard 1: MNP Journey Overview

| Visual | Configuration |
|---|---|
| **Card** | Count of `txn_id` (total journeys) |
| **Card** | Count of `result = "Failed"` (failure count) |
| **Donut chart** | `result` by count |
| **Stacked bar chart** | `event_type` by count, colored by `result` |
| **Line chart** | Count of events over `timestamp` (by month/day) |

### Dashboard 2: Operator & Circle Performance

| Visual | Configuration |
|---|---|
| **Clustered bar chart** | `operator` on axis, count of `result` as values |
| **Map (if available)** | `circle` as location, count of events as size |
| **Matrix** | Rows: `operator`, Columns: `circle`, Values: count of events |
| **100% stacked bar** | `operator` by `result` (Success vs Failed %) |

### Dashboard 3: Log Analysis

| Visual | Configuration |
|---|---|
| **Donut chart** | `log_level` distribution |
| **Bar chart** | `source` by count of `ERROR` logs |
| **Line chart** | Error count over time (daily trend) |
| **Table** | Top 10 error messages by frequency (use `message` column) |

### Dashboard 4: MSISDN Drill-Through

Create a drill-through page:
- Filter: `msisdn`
- Visuals: journey timeline, log breakdown per MSISDN
- KPI cards: total events, success %, error count

## 5. DAX Measures (Optional)

Paste these into the **Table tools** → **New measure**:

```dax
Success Rate = DIVIDE(
    COUNTROWS(FILTER(mnp_journey, mnp_journey[result] = "Success")),
    COUNTROWS(mnp_journey),
    0
) * 100
```

```dax
Failed Count = COUNTROWS(
    FILTER(mnp_journey, mnp_journey[result] = "Failed")
)
```

```dax
Error Log % = DIVIDE(
    COUNTROWS(FILTER(application_logs, application_logs[log_level] = "ERROR")),
    COUNTROWS(application_logs),
    0
) * 100
```

```dax
Operator Success % =
VAR SelectedOp = SELECTEDVALUE(mnp_journey[operator])
VAR TotalOp = COUNTROWS(FILTER(mnp_journey, mnp_journey[operator] = SelectedOp))
VAR SuccessOp = COUNTROWS(FILTER(mnp_journey, mnp_journey[operator] = SelectedOp && mnp_journey[result] = "Success"))
RETURN DIVIDE(SuccessOp, TotalOp, 0) * 100
```

## 6. Refreshing Data

| Method | How |
|---|---|
| **Manual refresh** | Home → Refresh (or Ctrl+R) |
| **Scheduled refresh** | NOT available in free Power BI Desktop (requires Pro + Power BI Service) |
| **Auto-refresh on open** | File → Options → Data → "Refresh data when opening file" |

## 7. Sharing Reports (Free Version Limitations)

| Capability | Free | Pro |
|---|---|---|
| Publish to Power BI Service | ❌ | ✅ ($10/user/month) |
| Share .pbix file via email/SharePoint | ✅ | ✅ |
| Scheduled cloud refresh | ❌ | ✅ |
| Create dashboards in cloud | ❌ | ✅ |
| Export to PDF | ✅ | ✅ |
| Drill-through / slicers | ✅ | ✅ |

**Workaround for sharing**: Export the .pbix file and share it. Recipients also need Power BI Desktop (free) to open it.

## 8. Troubleshooting

| Problem | Fix |
|---|---|
| "Cannot connect to PostgreSQL" | Ensure PostgreSQL service is running on Windows (check Services.msc → postgresql-x64-16) |
| "SSL not enabled" | In Power BI connector, set SSL Mode to `disable` or update `pg_hba.conf` |
| "Table not found" | Table name is `application_logs` (note: plural, with `_`) |
| "Data types mismatch" | In Power Query Editor, change column types: `timestamp` → Date/Time, `result` → Text |

### WSL Connectivity Issue

If you're running WSL (Windows Subsystem for Linux), PostgreSQL running on Windows won't be reachable from WSL by default because Windows Firewall blocks inbound connections to the WSL virtual network interface.

**Solution: Run everything from Windows CMD/PowerShell**

```cmd
cd C:\Users\gupta\Desktop\RandomProjects\mnp-ai-bot
venv\Scripts\python.exe generate_mock_data.py   # Insert mock data
venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000   # Start API
```

Or, run with admin privileges to add a firewall rule:
```powershell
# Run PowerShell as Administrator
New-NetFirewallRule -DisplayName "PostgreSQL WSL" -Direction Inbound -Protocol TCP -LocalPort 5432 -Action Allow -RemoteAddress 172.16.0.0/12
```

Then update `.env` to use the Windows gateway IP:
```
DATABASE_URL=postgresql://postgres:Code.C.C..L.L.Geass@172.21.192.1:5432/mnp_bot_db
```

---

**Tip**: Start with the "MNP Journey Overview" dashboard — it gives the quickest insight into your data quality and porting patterns.