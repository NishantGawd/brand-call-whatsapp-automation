# Wireframes (Layout Descriptions)

These are text-based wireframes describing the layout and visual
hierarchy of the main screens. The goal is a modern, clean, and
professional look:

- Spacious padding and margins.
- Clear visual hierarchy.
- Neutral colors with 1–2 accent colors.
- Smooth hover/focus states.
- Minimal clutter.

---

## 0. Main App Layout (Authenticated)

### Layout

- **Viewport** divided into:
  - Left sidebar (fixed width ~260px).
  - Right content area (flex, full height).
- Background: light neutral (e.g. very light gray), with white cards for content.

### Sidebar

- Top section:
  - Brand logo (small square) + text “Brand Automation”.
  - Small, subtle.
- Navigation:
  - Vertical list with icons + text:
    - Dashboard
    - Products
    - Customers
    - Calls
    - WhatsApp Messages
    - Settings (collapsible group)
  - Active route:
    - Slightly darker background.
    - Left accent border (e.g. a 3px primary color strip).
- Bottom section:
  - Small text: “Logged in as: [user name]”.
  - Link: “Help & Support” (future).

### Topbar (inside content area)

- Left:
  - Page title, e.g. “Dashboard”.
  - Breadcrumb under title (small): e.g. “Home / Dashboard”.
- Right:
  - Tenant selector (future; for now show tenant name only).
  - User avatar:
    - Clicking opens dropdown with “Profile” and “Logout”.

### Content Area

- Overall:
  - Max width ~1200px, centered with margins on large screens.
  - Vertical spacing between sections (cards).

---

## 1. Login Page

### Layout

- Centered, minimal login card over a soft background.

- Background:
  - Full-screen gradient or subtle pattern in brand colors.
- Center card:
  - Width ~400px.
  - White background, rounded corners, soft shadow.
  - Top: small logo + text “Brand Automation”.
  - Title: “Sign in to your brand dashboard”.
  - Description: one-line helper: “Enter your details to continue.”

### Inside Card

- Email input (full width).
- Password input (full width).
- “Remember me” checkbox (left) and “Forgot password?” link (right).
- Primary button:
  - Full-width.
  - Clear label: “Login”.
- Footer text:
  - “Need help? Contact support.”

Modern details:

- Inputs with rounded corners, thin border, focus highlight.
- Button with slight hover lift and color change.

---

## 2. Setup Wizard – General Layout

For all setup steps (`/setup/*`):

- Full-screen, centered content, but within main layout or a simplified header.
- Top area:
  - Small logo on left.
  - Right side: “Exit setup” button (returns to dashboard if allowed, or logout).
- Main card:
  - Centered container, width ~800–900px.
  - Inside:
    - Left: step title + description.
    - Right: form content (fields, etc.)
- Progress indicator:
  - Horizontal stepper at top of card:
    - Step 1: Brand
    - Step 2: WhatsApp
    - Step 3: Telephony
    - Step 4: Products
    - Step 5: Automation
  - Current step highlighted.
  - Completed steps with checkmark.

- Bottom bar:
  - Left: “Back” button (secondary).
  - Right: “Next” or “Save & Continue” button (primary).
  - Buttons aligned to right for clean look.

---

## 3. Setup Step 1 – Brand Profile

### Layout

- Title text: “Tell us about your brand”.
- Subtitle: brief explanation: “We’ll use this to personalize your dashboard and messages.”

- On the right side form:

  - Input: Brand name.
  - File input: Brand logo (with preview circle if uploaded).
  - Input: Primary business phone number.
  - Input: Primary WhatsApp number.

- Form arranged in two columns on desktop:
  - Left column: Text inputs.
  - Right column: Logo upload & preview.
- On mobile:
  - Single column stack.

Visual style:

- Card with white background, rounded corners.
- Slight padding (24–32px).
- Clear labels aligned above fields (not inline).

---

## 4. Setup Step 2 – WhatsApp Connection

### Layout

- Title: “Connect WhatsApp”.
- Subtitle: “Enter your WhatsApp Cloud API details. We’ll send a test message to confirm.”

- Two-column layout:

  - Left column:
    - Small explanation with bullet points:
      - “Use your Meta Business Suite / WhatsApp Cloud credentials.”
      - “We never show your full token after saving.”
    - Info box with link (“How to get these details?”) – opens doc.

  - Right column:
    - Fields stacked vertically:
      - WABA ID.
      - Phone Number ID.
      - Access Token.
      - Test recipient number.

- At bottom of the right column:
  - Button row:
    - Secondary button: “Back”.
    - Primary button: “Save & Test”.

- Below the button:
  - Status area:
    - If not tested yet: info text “No test performed yet.”
    - On success: small green badge “Connected” + “Last tested: <time>”.
    - On failure: red alert box with error details.

---

## 5. Setup Step 3 – Telephony Connection

### Layout

- Title: “Connect your call provider”.
- Subtitle: “We use this to detect completed calls and trigger WhatsApp messages.”

- Two-column layout:

  - Left column:
    - Provider selector (nice dropdown with provider logos).
    - If provider = Twilio:
      - Fields: Account SID, Auth Token, Main phone number.
    - If provider = Exotel:
      - Fields: Account SID, Auth Token, Subdomain, etc.
  - Right column:
    - Read-only card:
      - Label: “Your webhook URL”.
      - Field showing URL in a monospaced font.
      - “Copy” button.
      - Short note:
        - “Paste this into your provider’s webhook callback settings for call status.”

- Bottom:
  - Buttons “Back” and “Save & Continue”.

---

## 6. Setup Step 4 – Product Upload

### Layout

- Title: “Upload your product catalogue”.
- Subtitle: “We’ll use your products for WhatsApp catalog messages and analytics.”

- Main area:

  - Left side:
    - Info card:
      - “1. Download the CSV template.”
      - “2. Fill your products.”
      - “3. Upload the file here.”
    - “Download template” button (outlined).

  - Right side:
    - Drag-and-drop upload zone:
      - Border with dashed outline.
      - Text: “Drop your CSV file here or click to browse.”
      - Small note: “Max 10 MB, CSV only.”
    - Once a file is selected:
      - Show file name, size, and “Change file” link.
      - Show a table preview (first 5–10 rows) below.

- Bottom:
  - If preview is OK:
    - Primary button: “Import products”.
  - After import:
    - “Imported X products successfully, Y rows had issues” message.
    - “Download error report” link if needed.

---

## 7. Setup Step 5 – Automation Settings

### Layout

- Title: “Turn on automation”.
- Subtitle: “Control when and how we send post-call WhatsApp messages.”

- Center card with two main sections:

  - Section 1: Automation toggle
    - Large toggle switch with label:
      - “Enable post-call WhatsApp automation”.
    - Helper text:
      - “We’ll send messages only for completed calls that meet your rules.”

  - Section 2: Rules and message type
    - Grid of fields:
      - Minimum call duration input (integer, with label “seconds”).
      - Mode dropdown:
        - Option cards/styled select:
          - “Thank-you only”
          - “Thank-you + product catalog”
      - Template name input (free text).
    - Info text:
      - “You can change these later in Settings → Automation.”

- Bottom:
  - Buttons:
    - Secondary: “Back”.
    - Primary: “Save & Finish” (ends wizard and goes to dashboard).

---

## 8. Dashboard Home

### Layout

- Top:
  - Page title: “Dashboard”.
  - Subtitle (small): “Today at a glance”.

- Content grid:

  - Row 1: KPI cards (3 or 4 cards):
    - Card 1: “Calls today”
      - Big number.
      - Small caption “vs yesterday” (future).
    - Card 2: “WhatsApp messages today”
      - Big number.
    - Card 3: “Automation status”
      - Shows ON/OFF pill.
      - Button link: “Manage automation”.
    - Card 4 (optional future): “Failed messages today”.

  - Row 2:
    - Left (2/3 width): “Recent calls” card
      - Table of last 5–10 calls.
      - Columns: time, customer, duration, status, WhatsApp icon.
    - Right (1/3 width): “System status” card
      - List with checkmarks or warnings:
        - WhatsApp: Connected / Not connected.
        - Telephony: Connected / Not connected.
        - Products: X products.

- Overall styling:
  - Cards with rounded corners and subtle shadow.
  - Compact but legible typography.
  - Hover effects on clickable elements.

---

## 9. Products List

### Layout

- Top bar:
  - Left: Title “Products”.
  - Right: buttons:
    - Primary: “Add product”.
    - Ghost/secondary: “Import CSV”.

- Filter row below title:
  - Search bar (full-width or left).
  - Category dropdown.
  - Active toggle (“Active only”).

- Table:
  - Scrollable if many items.
  - Columns:
    - Name
    - SKU
    - Category
    - Price
    - Active
    - Actions (edit, delete icons)
  - Each row:
    - Subtle hover background.
    - Right-aligned action icons.

- Pagination:
  - At bottom right: page selector, “Rows per page” dropdown.

- Empty state (if no products):
  - Center message: “No products yet.”
  - Button: “Import from CSV” (primary).

---

## 10. Product Create/Edit

### Layout

- Implementation as **side drawer** or **center modal**:

  - If drawer:
    - Slide in from right, width ~480px.
    - Darkened overlay on rest of screen.
  - If modal:
    - Centered, white box.

- Inside:

  - Title:
    - “Add product” or “Edit product”.
  - Fields stacked vertically with good spacing:
    - Name
    - SKU
    - Category
    - Description (multi-line)
    - Price + Currency (inline group)
    - Active toggle
    - Image URL (small field)

- Footer:
  - Left: “Cancel” (text button).
  - Right: “Save” (primary button).

Modern feel:

- Label using clear and compact text.
- Inputs with consistent width.
- Form validation messages under each field.

---

## 11. Product Import Page

### Layout

Very similar to Setup Step 4, but with a slightly more “dashboard” look.

- Title: “Import products”.
- Subtitle: “Bulk upload or update your catalogue”.

- Two main sections:

  - Left column:
    - Info text and template download.
  - Right column:
    - Drag-and-drop area.
    - Preview + Import actions.

- After import:
  - Show summary card:
    - “X products added, Y updated, Z failed.”
    - Link to export error rows (CSV).

---

## 12. Customers List

### Layout

- Top bar:
  - Title: “Customers”.
- Filter row:
  - Search by phone/name.
- Table:
  - Columns: Name, Phone, Total calls, Last call, Last message.
- Empty state:
  - “Customers will appear automatically as calls and messages happen.”

---

## 13. Calls List

### Layout

- Top bar:
  - Title: “Calls”.
- Filter rows:
  - Date range picker (left).
  - Status dropdown (center).
  - “Has WhatsApp follow-up” toggle (right).

- Table:
  - Columns:
    - Time
    - Customer phone
    - Duration
    - Status
    - WhatsApp (icon representing sent/not sent/failed)
  - Row hover:
    - Slight highlight; clicking opens Call Detail drawer.

- Bottom:
  - Pagination controls.

---

## 14. Call Detail (Drawer)

### Layout

- Presentation as right-side drawer:

  - Title: “Call details”.
  - Close icon (X) in top-right.

- Content sections:

  1. **Call Summary**
     - Time, duration, status.
     - Customer phone number.
  2. **WhatsApp Follow-up**
     - Status: Sent/Failed/Not eligible.
     - If sent:
       - Template name.
       - Timestamp.
  3. **Related messages**
     - List of messages related to this call (timestamps, status).

- Footer (optional):
  - Button: “Open in messages” (jump to message list filtered by this number).

---

## 15. WhatsApp Messages List

### Layout

- Top bar:
  - Title: “WhatsApp messages”.
- Filters:
  - Date range picker.
  - Status dropdown.
  - Direction dropdown (`Outbound`, `Inbound`).

- Table:
  - Columns:
    - Time
    - Customer phone
    - Direction (chip/tag)
    - Type (template/text)
    - Status (colored badge)
    - Source (Automation/Manual – future)
  - Row hover:
    - Slight highlight; click opens detail modal.

- Empty state:
  - “Messages will appear here as automation runs or customers reply.”

---

## 16. Settings – Brand Profile

### Layout

- Settings sections shown as tabs or vertical sub-menu:
  - Brand
  - WhatsApp
  - Telephony
  - Automation
  - Users

- Brand page:

  - Simple card:
    - Brand logo with upload button.
    - Brand name input.
    - Primary phone + WhatsApp number.
  - Save bar:
    - At bottom: “Cancel” and “Save changes”.

---

## 17. Settings – WhatsApp Integration

### Layout

- Title: “WhatsApp integration”.
- Two-column card:

  - Left:
    - Status panel:
      - Large status indicator (green check / red warning).
      - Text: “Connected” or “Not connected.”
      - Last test time.
      - “Test connection” button (secondary).
  - Right:
    - Form fields:
      - WABA ID.
      - Phone number ID.
      - Access token.
    - Save button.

- Under card:
  - Small note with link to docs: “How to set up WhatsApp Cloud API”.

---

## 18. Settings – Telephony Integration

### Layout

- Similar to WhatsApp integration page.

- Two-column card:

  - Left:
    - Provider dropdown with logos.
    - Status (Connected/Not).
  - Right:
    - Provider-specific fields.

- Below:
  - Webhook URL card:
    - Show URL in a monospaced, copyable field.
    - “Copy” button.

---

## 19. Settings – Automation Rules

### Layout

- Title: “Automation rules”.
- Single large card:

  - Top row:
    - Automation toggle with large label and short description.

  - Middle row:
    - Grid of fields:
      - Minimum call duration (numeric).
      - Mode (select, maybe shown as option cards).
      - Template name.

  - Bottom row:
    - Explanation text:
      - “We only send follow-ups after completed calls that match these rules.”

- Footer:
  - Right-aligned “Save changes” button.

---

## 20. Settings – Users & Permissions

### Layout

- Title: “Users & permissions”.
- Intro line: “Manage access for your team.”

- Table:
  - Columns: Name, Email, Role, Actions.
- “Add user” button above table:
  - Opens modal with fields.

---

## 21. Admin – Tenant List

### Layout

- Minimal but consistent with rest of app.

- Top bar:
  - Title: “Tenants (Admin)”.
  - Right: “Create tenant” button.

- Table:
  - Columns: Tenant name, Slug, Setup complete, Created at.
- Rows:
  - Each row clickable → opens tenant context (future).

---

## 22. Admin – Tenant Create

### Layout

- Centered card or drawer:

  - Fields:
    - Tenant name.
    - Slug.
    - Owner email.
  - Text:
    - “We’ll create the tenant and owner user. Share the login with them.”

- Buttons:
  - Cancel (secondary).
  - Create tenant (primary).

---

End of wireframes.
