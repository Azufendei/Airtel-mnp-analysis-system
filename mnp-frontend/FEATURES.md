# MNP Frontend - Feature Documentation

A comprehensive guide to all user interface and analytical capabilities of the MNP Frontend.

---

## 📋 Core Capabilities

### 🔐 1. Authentication & Session Management
- **OAuth2 Password Grant**: Authenticates via `POST /auth/login` with OLM ID and password.
- **JWT Bearer Token Handling**: Token stored securely in `localStorage` and validated on every API call.
- **Axios Interceptor**: Automatically adds `Authorization: Bearer <token>` to outbound requests.
- **Automatic 401 Interception**: Gracefully logs out the user and clears state if the JWT token expires.
- **Operator Role Badge**: Displays user OLM ID alongside role badge (`admin`, `tech`, `support`, `viewer`).

### 🔍 2. Intelligent Subscriber Lookup
- **MSISDN Validation**: Real-time validation for 10-digit standard Indian phone numbers or 13-digit E.164 formats (`91...`).
- **Optional Date Filtering**: Toggleable date range filters to zoom into specific porting dispute intervals.
- **Interactive Loading States**: Spinner and status feedback during backend analysis.

### 📊 3. Chronological Journey Timeline
- **Event Categorization**: Displays event types with color-coded status badges:
  - `UPC`: Unique Porting Code generation
  - `Port_in`: Number ported into operator network
  - `Port_out`: Number ported out from donor operator
  - `NPD_IN`: National Porting Clearinghouse Incoming event
  - `NPD_Out`: National Porting Clearinghouse Outgoing event
  - `Number_return`: Return of subscriber number to original block holder
- **Metadata Inspection**: Expandable JSON details showing donor/recipient operators, rejection error codes, and circle details.

### 📝 4. Gateway Log Intelligence
- **Log Counters**: Instant metric cards showing total gateway logs, error count, warning count, and info messages.
- **Timeline Distribution**: Visual bar chart showing log volume spread across days.
- **Key Issues Parser**: Highlights top critical issues identified across distributed telecom services (API, Orchestrator, Database).

### 💡 5. TRAI Regulatory Compliance & AI Recommendations
- **Categorized Cards**:
  - `Critical`: TRAI compliance violations (e.g. 10-day cooling period breaches).
  - `High`: Operational recommendations to unblock stalled porting requests.
  - `Medium`: Support workflow next actions.
- **Detailed Explanations**: Contextual reasoning synthesized by Groq LLM (`qwen/qwen3.8-27b`) or deterministic rule fallbacks.

### 💾 6. Executive Export & Print Layouts
- **Export to JSON**: One-click download of the complete response payload.
- **Print Optimization**: High-contrast, page-break-aware print stylesheet for physical reports.
