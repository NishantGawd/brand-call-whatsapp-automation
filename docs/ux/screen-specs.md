# Screen Specifications (MVP)

This document defines field-level specs, data needs, and actions
for all MVP screens. It will guide both backend (API design) and
frontend (Next.js) implementation.

---

## 0. Global – Main App Layout

- URL context: wraps all authenticated routes (e.g. `/dashboard`, `/products`, `/settings/*`).
- Access: Authenticated.
- Purpose: Provide consistent navigation, clean layout, and global UI elements.

### Data Needed

- Current user info:
  - Name, email, role (owner, staff).
  - Tenant name & logo.
- Feature flags (optional, future).
- Notification count (future).

### API Endpoints Used

- `GET /api/auth/me`
- (optional later) `GET /api/notifications/count`

### UI Elements

- **Sidebar** (left):
  - Logo + brand name.
  - Navigation items:
    - Dashboard
    - Products
    - Customers
    - Calls
    - WhatsApp Messages
    - Settings (with nested items)
- **Topbar**:
  - Current tenant name and logo (small).
  - Right side:
    - User avatar with dropdown: “Profile”, “Logout”.
- **Content Area**:
  - Page title and breadcrumbs.
  - Main page content.

### Actions

- Click navigation items → navigate to corresponding pages.
- Click user avatar:
  - “Profile” (future).
  - “Logout” → triggers logout flow.

---

## 1. Login Page

- URL: `/login`
- Access: Public.
- Purpose: Authenticate user and route them to correct post-login flow.

### Data Needed

- None initially; backend will respond with token and user/tenant info.

### API Endpoints Used

- `POST /api/auth/login`
  Request body:
  - `email`: string (required)
  - `password`: string (required)

### Inputs

1. Email
   - Type: string, email.
   - Validation:
     - Required.
     - Valid email format.
2. Password
   - Type: string (password input).
   - Validation:
     - Required.
     - Min length: 8 characters.

### Actions

- **Login** button:
  - On click:
    - Validate inputs on frontend.
    - Call `POST /api/auth/login`.
  - On success:
    - Store JWT/access token securely.
    - Store basic user/tenant info.
    - If tenant not fully set up → redirect to Setup Wizard start (`/setup/brand`).
    - Else → redirect to `/dashboard`.
  - On failure:
    - Show error: “Invalid email or password.” or backend error message.
- **Remember Me** checkbox (optional):
  - If enabled, extend token storage to longer duration.

---

## 2. Setup Wizard – Step 1: Brand Profile

- URL: `/setup/brand`
- Access: Authenticated; only if tenant is not fully set up.
- Purpose: Collect basic brand information.

### Data Needed

- Existing brand profile (if partially filled):
  - Brand name.
  - Primary phone number.
  - Primary WhatsApp number.
  - Logo URL (optional).

### API Endpoints Used

- `GET /api/settings/brand-profile`
- `PUT /api/settings/brand-profile`

### Inputs

1. Brand Name
   - Type: string.
   - Validation:
     - Required.
     - Max length: 100.
2. Brand Logo (optional)
   - Type: file upload (image).
   - Validation:
     - Formats: PNG, JPG, SVG.
     - Max size: 2 MB.
3. Primary business phone number
   - Type: string (phone).
   - Validation:
     - Required.
     - Should be valid E.164 or normalized by backend.
4. Primary WhatsApp number
   - Type: string (phone).
   - Validation:
     - Required.
     - Must be a valid phone number.
     - Can be equal to primary business number or different.

### Actions

- **Save & Continue** button:
  - Calls `PUT /api/settings/brand-profile`.
  - On success:
    - Mark Step 1 as complete (in local wizard state).
    - Navigate to `/setup/whatsapp`.
  - On failure:
    - Show field-level errors where possible.
- **Cancel / Logout** (secondary action in topbar):
  - Return to login or log out (optional).

---

## 3. Setup Wizard – Step 2: WhatsApp Connection

- URL: `/setup/whatsapp`
- Access: Authenticated; tenant not fully set up.
- Purpose: Store WhatsApp Cloud API credentials and verify connection.

### Data Needed

- Existing WhatsApp credentials for tenant (if any):
  - WABA ID (masked or shown).
  - Phone number ID.
  - Status of last connection test.

### API Endpoints Used

- `GET /api/whatsapp/credentials`
- `POST /api/whatsapp/credentials`
- `POST /api/whatsapp/test-message` (or combined with save endpoint)

### Inputs

1. WABA ID
   - Type: string.
   - Validation:
     - Required.
2. Phone Number ID
   - Type: string.
   - Validation:
     - Required.
3. Access Token
   - Type: string (password input).
   - Validation:
     - Required.
     - Min length: 20.
4. Test recipient number
   - Type: string (phone).
   - Default: primary WhatsApp number from Step 1.
   - Validation:
     - Required.
     - Valid phone number.

### Actions

- **Save & Test** button:
  - Calls `POST /api/whatsapp/credentials`.
  - Backend stores credentials securely (encrypt token).
  - Backend sends test message using `POST /api/whatsapp/test-message` or internal logic.
  - On success:
    - Show success banner: “WhatsApp connected successfully.”
    - Enable **Next** button.
  - On failure:
    - Show clear error message (e.g. “Invalid access token”).
- **Back** button:
  - Navigate back to `/setup/brand`.
- **Next** button:
  - Only enabled if last test was successful.
  - Navigates to `/setup/telephony`.

---

## 4. Setup Wizard – Step 3: Telephony Connection

- URL: `/setup/telephony`
- Access: Authenticated; tenant not fully set up.
- Purpose: Store telephony provider credentials and show webhook URL.

### Data Needed

- Existing telephony credentials:
  - Provider name.
  - Credentials (masked).
- Tenant slug (for webhook URL generation).

### API Endpoints Used

- `GET /api/telephony/credentials`
- `POST /api/telephony/credentials`
- Internal (display only): generated webhook URL, e.g.
  - `https://api.yourdomain.com/webhooks/call-status/{tenantSlug}`

### Inputs

1. Provider
   - Type: select dropdown.
   - Options (MVP):
     - `twilio`
     - `exotel`
     - `other` (future).
   - Validation:
     - Required.
2. Provider-specific fields (example for Twilio):
   - Account SID
     - Type: string.
     - Validation: Required.
   - Auth Token
     - Type: string (password).
     - Validation: Required.
3. Main brand phone number (from provider side)
   - Type: string (phone).
   - Validation:
     - Required.

### Actions

- **Save** button:
  - Calls `POST /api/telephony/credentials`.
  - Optional: backend performs a simple verification (e.g. fetch account info).
  - On success:
    - Show success notification.
  - On failure:
    - Show error message and keep form editable.
- **Webhook URL** display:
  - Read-only field containing webhook URL.
  - **Copy** button:
    - Copies URL to clipboard.
- **Back** button:
  - Navigate to `/setup/whatsapp`.
- **Next** button:
  - Navigates to `/setup/products`.

---

## 5. Setup Wizard – Step 4: Product Upload

- URL: `/setup/products`
- Access: Authenticated; tenant not fully set up.
- Purpose: Allow brand to import initial product catalogue.

### Data Needed

- Whether products exist already (for info).
- Sample CSV template URL.

### API Endpoints Used

- `GET /api/products?limit=1` (to see if any exist).
- `POST /api/products/import` (multipart/form-data).

### Inputs

1. Product CSV file
   - Type: file upload.
   - Validation:
     - Required.
     - MIME: `text/csv` (and optionally Excel supported later).
2. Column mapping (if needed for flexible CSV):
   - Show mapping UI based on detected headers.
   - For MVP, assume fixed template and skip mapping.

### Actions

- **Download Template** button:
  - Downloads sample CSV file.
- **Upload File** input:
  - On file selection, show quick validation + preview (first 10 rows).
- **Import** button:
  - Calls `POST /api/products/import`.
  - On success:
    - Show success message: “Imported X products successfully.”
    - Allow “Next” step.
  - On failure:
    - Show list of row-level errors (line number + error).
- **Back** button:
  - Navigate to `/setup/telephony`.
- **Next** button:
  - Navigate to `/setup/automation`.

---

## 6. Setup Wizard – Step 5: Automation Settings

- URL: `/setup/automation`
- Access: Authenticated; tenant not fully set up.
- Purpose: Configure core automation behavior, then finish wizard.

### Data Needed

- Current automation settings for tenant.

### API Endpoints Used

- `GET /api/automation-settings`
- `PUT /api/automation-settings`

### Fields

1. Enable Automation
   - Type: boolean (toggle).
   - Default: `false`.
2. Minimum Call Duration (seconds)
   - Type: integer input or slider.
   - Default: 30.
   - Validation:
     - Required.
     - Min: 0.
     - Max: 3600.
3. Mode
   - Type: select.
   - Options:
     - `thank_you_only`
     - `thank_you_and_catalog`
4. WhatsApp Template Name
   - Type: string.
   - Default: “post_call_follow_up” (or similar).
   - Validation:
     - Required if automation enabled.

### Actions

- **Save & Finish** button:
  - Calls `PUT /api/automation-settings`.
  - Marks tenant as `setup_complete = true`.
  - Redirects to `/dashboard`.
- **Back** button:
  - Navigate to `/setup/products`.

---

## 7. Dashboard Home

- URL: `/dashboard`
- Access: Authenticated; tenant setup_complete = true.
- Purpose: Give high-level view of today’s activity and system health.

### Data Needed

- Summary stats:
  - Calls today (count).
  - WhatsApp messages sent today (count).
- Automation status:
  - Enabled (boolean).
- Recent items:
  - Latest 5 calls with WhatsApp status.
- Integration status:
  - WhatsApp: connected / not connected.
  - Telephony: connected / not connected.
  - Products: count.

### API Endpoints Used

- `GET /api/dashboard/summary`
  - Returns:
    - `calls_today`
    - `messages_today`
    - `automation_enabled`
    - `whatsapp_connected`
    - `telephony_connected`
    - `products_count`
- `GET /api/calls?limit=5&sort=desc`

### UI Elements

- KPI cards across the top:
  - “Calls today”
  - “WhatsApp messages today”
  - “Automation status”
- Recent calls table.
- “Setup health” or “System status” panel.

### Actions

- Click “View all calls” → `/calls`.
- Click “View all messages” → `/messages`.
- Click “Go to automation settings” → `/settings/automation`.
- If integration not connected:
  - Click “Fix now” → relevant settings page.

---

## 8. Products List

- URL: `/products`
- Access: Authenticated.
- Purpose: Manage brand’s product catalogue.

### Data Needed

- Paginated list of products.
- Filters (search, category, active).

### API Endpoints Used

- `GET /api/products?page={page}&page_size={size}&search={term}&category={category}&active={bool}`

### Table Columns

- Product name.
- SKU.
- Category.
- Price.
- Currency (optional).
- Active (boolean).
- Last updated.

### Actions

- **Add Product** button:
  - Opens Create/Edit Product drawer/modal.
- **Edit** icon for row:
  - Opens Create/Edit Product drawer/modal prefilled.
- **Delete** icon:
  - Shows confirmation dialog.
  - On confirm → `DELETE /api/products/{id}`.
- **Import CSV** button:
  - Navigates to `/products/import` (or opens overlay).
- Filters:
  - Search input (name/SKU).
  - Category dropdown.
  - Active only toggle.

---

## 9. Product Create/Edit

- URL: `/products/new` (or modal from `/products`) and `/products/{id}/edit`.
- Access: Authenticated.

### Data Needed

- If editing:
  - Product details by ID.

### API Endpoints Used

- `POST /api/products`
- `PUT /api/products/{id}`
- `GET /api/products/{id}` (if editing)

### Fields

1. Name
   - Type: string, required, max 120.
2. SKU
   - Type: string, required, max 50.
3. Category
   - Type: string or select.
   - Required.
4. Description
   - Type: multi-line text.
   - Optional, max length 1000.
5. Price
   - Type: decimal.
   - Required.
   - Min: 0.
6. Currency
   - Type: select.
   - Default: “INR”.
7. Active
   - Type: boolean.
   - Default: true.
8. Image URL or upload (MVP: URL)
   - Type: string (URL).
   - Optional.

### Actions

- **Save** button:
  - For new → `POST /api/products`.
  - For edit → `PUT /api/products/{id}`.
  - On success: close modal / redirect back + show success toast.
- **Cancel** button:
  - Close modal / navigate back without saving.

---

## 10. Product Import

- URL: `/products/import`
- Access: Authenticated.

### Data Needed

- Sample template URL.
- Last import summary (optional).

### API Endpoints Used

- `POST /api/products/import`

### Inputs

- CSV file upload (same rules as Setup Step 4).

### Actions

- **Download Template** button:
  - Downloads sample CSV.
- **Upload and Import** button:
  - Validates file → `POST /api/products/import`.
  - Show progress (if large).
  - On success: show summary (# added, # updated, # failed).
  - On error: show row-level issues.

---

## 11. Customers List (Read-Only MVP)

- URL: `/customers`
- Access: Authenticated.

### Data Needed

- Paginated list of customers (derived from calls and WhatsApp messages).

### API Endpoints Used

- `GET /api/customers?page={page}&page_size={size}&search={term}`

### Table Columns

- Customer name (if available).
- Phone number.
- Total calls.
- Last call date.
- Last WhatsApp message date.

### Actions

- Click row → (optional) future “Customer detail” page.
- Search by phone or name.

---

## 12. Calls List

- URL: `/calls`
- Access: Authenticated.
- Purpose: Let brand see recent calls and whether WhatsApp automation fired.

### Data Needed

- Paginated list of calls.
- Filters: date range, status, duration.

### API Endpoints Used

- `GET /api/calls?page={page}&page_size={size}&status={status}&from={fromDate}&to={toDate}`

### Table Columns

- Call time (end time).
- Customer phone.
- Call duration (seconds or mm:ss).
- Status (`completed`, `missed`, etc.).
- WhatsApp automation status:
  - icon or label (sent, not eligible, failed).
- Telephony provider (optional).

### Actions

- Filter by:
  - Date range.
  - Status.
  - Has WhatsApp message? (yes/no).
- Click row → show Call Detail drawer/modal.

---

## 13. Call Detail (Minimal MVP)

- URL: `/calls/{id}` or modal opened from `/calls`.
- Access: Authenticated.

### Data Needed

- Call detail by ID.
- Related WhatsApp messages (if any).

### API Endpoints Used

- `GET /api/calls/{id}`
- `GET /api/messages?call_id={id}`

### Display

- Call meta:
  - Date & time.
  - Caller phone.
  - Call duration.
  - Status.
- WhatsApp section:
  - Messages sent for this call (if any), with statuses.

### Actions

- (Optional) Manual resend of WhatsApp message:
  - Button: “Resend follow-up”.
  - Calls new endpoint (future).

---

## 14. WhatsApp Messages List

- URL: `/messages`
- Access: Authenticated.
- Purpose: Provide visibility into all outbound/inbound WhatsApp messages.

### Data Needed

- Paginated list of messages.
- Filters: status, direction, date.

### API Endpoints Used

- `GET /api/messages?page={page}&page_size={size}&status={status}&direction={direction}&from={from}&to={to}`

### Table Columns

- Time.
- Customer phone.
- Direction: `outbound` / `inbound`.
- Message type: `template`, `text`, `image` (MVP: `template`/`text`).
- Status: `queued`, `sent`, `delivered`, `read`, `failed`.
- Source:
  - `automation` or `manual` (future).

### Actions

- Filter by:
  - Date range.
  - Status.
  - Direction.
- Click row → Message Detail modal (optional MVP).

---

## 15. Settings – Brand Profile

- URL: `/settings/brand`
- Access: Authenticated (owner or admin role).

### Data Needed

- Same fields as Setup Step 1.

### API Endpoints Used

- `GET /api/settings/brand-profile`
- `PUT /api/settings/brand-profile`

### Actions

- Edit and save brand name, logo, primary phone numbers.

---

## 16. Settings – WhatsApp Integration

- URL: `/settings/whatsapp`
- Access: Authenticated (owner or admin).

### Data Needed

- WhatsApp credentials (masked).
- Connection status.
- Last test timestamp.

### API Endpoints Used

- `GET /api/whatsapp/credentials`
- `POST /api/whatsapp/credentials`
- `POST /api/whatsapp/test-message`

### Fields

- Same as Setup Step 2.

### Actions

- Save credentials.
- Test connection.
- Show connection status clearly (green/red badge).

---

## 17. Settings – Telephony Integration

- URL: `/settings/telephony`
- Access: Authenticated (owner or admin).

### Data Needed

- Telephony credentials.
- Webhook URL.

### API Endpoints

- `GET /api/telephony/credentials`
- `POST /api/telephony/credentials`

### Fields

- Same as Setup Step 3.

### Actions

- Save credentials.
- “Copy webhook URL” button.
- Show last callback received time (optional).

---

## 18. Settings – Automation Rules

- URL: `/settings/automation`
- Access: Authenticated (owner or admin).

### Data Needed

- Current automation settings.

### API Endpoints

- `GET /api/automation-settings`
- `PUT /api/automation-settings`

### Fields

- Same as Setup Step 5.

### Actions

- Toggle automation ON/OFF.
- Adjust minimum call duration.
- Change mode and template.
- Show info text about what automation does.

---

## 19. Settings – Users & Permissions (Basic MVP)

- URL: `/settings/users`
- Access: Owner only.

### Data Needed

- List of users for tenant.

### API Endpoints Used

- `GET /api/settings/users`
- `POST /api/settings/users` (create)
- `DELETE /api/settings/users/{id}` (optional)
- (Future) `PUT /api/settings/users/{id}`

### Table Columns

- Name.
- Email.
- Role (`owner` / `staff`).

### Actions

- Add user:
  - Name, email, role.
  - (Optional) send invite email later.
- Disable/delete user (MVP: delete).

---

## 20. Admin – Tenant List (Internal)

- URL: `/admin/tenants`
- Access: Internal admin only.

### Data Needed

- Paginated list of tenants.

### API Endpoints Used

- `GET /api/internal/tenants?page={page}&page_size={size}`

### Columns

- Tenant name.
- Slug.
- Created at.
- Setup complete (boolean).

### Actions

- Click row → Tenant detail (future).
- “Create tenant” → `/admin/tenants/new`.

---

## 21. Admin – Tenant Create (Internal)

- URL: `/admin/tenants/new`
- Access: Internal admin only.

### Fields

- Tenant name.
- Slug (auto-generated, editable).
- Owner email (used to create initial user).

### API Endpoints Used

- `POST /api/internal/tenants`

### Actions

- Create tenant + owner user in one action.
- Show generated password or send email (future).

---

## 22. Admin – User Create (Internal)

- URL: `/admin/users/new` (or embedded in tenant create).
- Access: Internal admin only.

### Fields

- Tenant selection.
- Name.
- Email.
- Role (`owner`/`staff`).

### API Endpoints Used

- `POST /api/internal/users`

---

End of MVP screen specs.
