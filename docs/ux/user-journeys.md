# User Journeys

## 1. First-Time Setup (Brand Owner)

### Trigger
- Brand owner installs desktop app or opens web app for the first time.
- Receives login from you (system admin).

### Steps (Happy Path)
1. Owner opens app → sees login screen.
2. Enters email + password → clicks "Login".
3. On first login, system detects tenant has not completed setup → redirects to **Setup Wizard**.
4. Step 1: Brand Profile
   - Fill brand name, logo (optional), primary phone number, primary WhatsApp number.
   - Click "Next".
5. Step 2: Connect WhatsApp
   - Shows instructions (from WhatsApp Cloud docs).
   - Fields: WABA ID, phone number ID, access token.
   - "Test Connection" button sends test message to owner's number.
   - If success → can click "Next"; if fail → shows error and stays.
6. Step 3: Connect Telephony
   - Select provider from dropdown (e.g., Twilio / Exotel / XYZ).
   - Enter provider-specific credentials (e.g., SID, token, base URL).
   - System shows the generated **Webhook URL** for this tenant.
   - Owner must copy this URL into telephony provider config (instructions + link).
   - Click "Next".
7. Step 4: Upload Products
   - Download sample CSV template.
   - Select and upload CSV with products.
   - See preview (first 10 rows) and mapping.
   - If validation passes → import and show success.
   - Click "Next".
8. Step 5: Automation Settings
   - Toggle: "Enable post-call WhatsApp automation" [ON/OFF].
   - Slider/field: "Minimum call duration (seconds)".
   - Dropdown: "Mode" (Thank-you only, Thank-you + Catalog).
   - Confirm.
   - Clicking "Finish" → redirect to Dashboard Home.

### Outcomes
- Tenant has:
  - Brand profile.
  - WhatsApp and telephony configured.
  - Products loaded.
  - Automation configured ON or OFF.
- User lands on Dashboard showing summary.

### Edge Cases to handle
- WhatsApp test fails → clearly show error, instructions.
- Telephony credentials invalid → show error, don’t mark step as complete.
- Product CSV invalid → show per-row errors, allow re-upload.

---

## 2. Daily Usage (Brand Owner or Staff)

### Trigger
- Owner/staff open app after system already set up.

### Steps
1. User logs in.
2. Goes straight to Dashboard (no wizard).
3. Sees widgets:
   - Today's completed calls.
   - Today's WhatsApp messages sent.
   - Automation status (ON/OFF).
4. From Dashboard, they might:
   - Go to **Calls** page:
     - Check recent calls, see which had WhatsApp sent.
   - Go to **Messages** page:
     - See sent WhatsApp messages and their status.
   - Go to **Products**:
     - Update prices, stock, images.
   - Go to **Settings**:
     - Tweak automation rules.
     - Update WhatsApp tokens (if expired).

### Outcomes
- They can understand if system is working today.
- They can adjust automation quickly if needed.

---

## 3. Troubleshooting / Problem Check

### Scenario
- Owner thinks WhatsApp messages are not being sent after calls.

### Steps
1. Owner opens Dashboard.
2. Immediately sees top banner or widget "Automation: OFF" or "WhatsApp not connected" if there is an issue.
3. Goes to **Messages** page:
   - Filters for "Failed" messages.
4. Each failed message row shows:
   - Reason (e.g., invalid phone, WhatsApp API error).
5. Goes to **Settings → WhatsApp Integration**:
   - Sees last tested time + status.
   - Can click "Test Connection" again.

### Outcome
- Owner can see if problem is on their side (wrong token, etc.) or telephony side.
- You can debug easier with consistent error statuses.
