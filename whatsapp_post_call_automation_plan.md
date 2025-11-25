# WhatsApp Post-Call Catalog Automation – Full Step-by-Step Plan

This document is a **complete, practical roadmap** to build a fully working WhatsApp automation system for your clothing brand. The system will:

- Automatically send a **thank-you message + catalog / products** on WhatsApp **after you finish a call** with a customer.
- Stay **simple and user-friendly** for you and your team (non-technical users).
- Be designed to grow over time (faster, more features, more automation).

You can share this document with developers, or use it yourself as a build checklist.

---

## High-Level Architecture (Plain Language)

To keep things simple, imagine your system as 4 parts working together:

1. **WhatsApp Business Platform (Cloud API)**  
   - Official WhatsApp API from Meta.
   - Sends messages and product catalogs to customers.

2. **Telephony (Call System)**  
   - Service that handles your calls and notifies your system when a call ends.
   - Example providers: Twilio, Exotel, Knowlarity, etc.

3. **Backend Server (Your Logic)**  
   - A small web application (e.g., in Node.js / Python) that receives webhooks and decides *what* to send on WhatsApp.
   - Stores customers, products, calls, and logs in a database.

4. **Simple Admin Panel (Web Dashboard)**  
   - Very user friendly.
   - Lets you turn automation ON/OFF, see logs, manage products, and change basic rules without coding.

---

## Phase 1 – Planning & Decisions (Non-Technical, Very Important)

Before building, decide the following:

1. **Business Rules**
   - Do you want to send a WhatsApp message:
     - After *every* completed call?
     - Only for calls longer than **X seconds** (e.g., 30 seconds)?
   - Do you always send **full catalog**, or
     - Sometimes only **specific product categories** (like “New arrivals” or “Men’s T-shirts”)?

2. **Tech Choices (Developer will implement these)**
   - Backend language:  
     - **Node.js + Express** (recommended) or  
     - Python (FastAPI / Django REST).
   - Database:  
     - PostgreSQL or MySQL.
   - Hosting:  
     - Any reliable cloud provider (Railway, Render, AWS, etc.)

3. **User-Friendliness Goals**
   - Admin panel must be **simple**:
     - Big toggle: “Post-call WhatsApp Automation: ON / OFF”
     - Clear setting: “Minimum call duration for automation: [30] seconds”
     - Easy page: “Products” with basic fields (Name, Price, Stock, Category, Visible on WhatsApp: Yes/No)
   - No technical jargon – use plain words and tooltips (“What does this mean?”).

Document these decisions. They guide the rest of the build.

---

## Phase 2 – Set Up WhatsApp Business (Cloud API)

### Step 2.1: Meta Business and App Setup

1. Create or log in to **Meta Business Manager**.
2. Add your business details and **verify your business** (upload docs if required).
3. Go to **Meta for Developers** and:
   - Create a new app (choose appropriate app type).
   - Add the **WhatsApp** product to this app.

### Step 2.2: Create a WhatsApp Business Account (WABA)

1. Inside Business Manager, create / connect a **WhatsApp Business Account (WABA)**.
2. Connect your developer app to this WABA.

### Step 2.3: Add a WhatsApp Phone Number

1. Choose a phone number for WhatsApp (can be a dedicated number; cannot be used in normal WhatsApp at same time).
2. Register it via SMS / voice OTP.
3. Configure:
   - **Display name** (your brand name)
   - **Business category** (e.g., Clothing brand / Retail)
   - Profile photo (brand logo)
   - Business description, email, website if any.

### Step 2.4: Get API Credentials

From the WhatsApp section in your app, note down:

- `phone_number_id`
- `whatsapp_business_account_id` (WABA ID)
- A **Permanent Access Token** (long-lived)

Give these to your developer securely. They will use them to call the WhatsApp API.

### Step 2.5: Enable Webhooks for WhatsApp

1. In the app settings, configure the **Webhook URL** for WhatsApp events.  
   - Example: `https://yourdomain.com/webhooks/whatsapp`
2. Verify the webhook by responding with the challenge token (developer task).  
3. Subscribe to events:
   - `messages`
   - `message_template_status_update`
   - `message_status`

You now have a working WhatsApp API setup.

---

## Phase 3 – Create Your WhatsApp Catalog

The idea is: customer can browse your **products inside WhatsApp** like a mini store.

### Step 3.1: Prepare Your Product Data

For each SKU, prepare:

- Product name (clear & short)
- Category (e.g., “Men’s T-Shirts”, “Women’s Kurtis”)
- Description (main features, fabric, fit)
- Price (MRP or selling price)
- Product code / SKU
- Stock (optional, can be managed on your side too)
- Product images (clear, high quality, one main image at least)

### Step 3.2: Add Products to WhatsApp Catalog

You or your developer can:

- Use **WhatsApp Business app** directly, or
- Use **Commerce Manager** in Meta Business

For now, to keep it simple:

1. Create your **Catalog**.
2. Add your main SKUs (start with 20–50 popular items).
3. Group by categories using **collections** (e.g., Men, Women, Kids).

Later, you will sync product changes automatically from your database.

---

## Phase 4 – Choose and Configure Your Telephony Provider

To trigger WhatsApp messages **after calls**, you need a call system that:

- Handles calls (inbound/outbound) on your business number.
- Sends a **webhook** (HTTP request) to your backend when a call ends.

### Step 4.1: Select a Provider

Examples (you can pick one based on your country/needs):

- Global: Twilio  
- India-focused: Exotel, Knowlarity, MyOperator, etc.

### Step 4.2: Buy / Configure Your Number

1. Buy a **virtual phone number** (or port your existing one, if supported).
2. Set up call flows:
   - Calls route to your phone / your team.
   - Missed calls go to voicemail (optional).

### Step 4.3: Set the Call Status Webhook

In your telephony provider dashboard, configure:

- **Status Callback URL / Webhook URL** for call events:  
  - Example: `https://yourdomain.com/webhooks/call-status`

Choose events like:

- `initiated`
- `ringing`
- `answered`
- `completed`

Your developer will use these webhooks to know when to send WhatsApp messages.

---

## Phase 5 – Design the Data Model (Database)

### Step 5.1: Database Choice

Use a relational database:

- PostgreSQL (recommended) or MySQL

### Step 5.2: Basic Tables

1. **customers**
   - `id`
   - `name` (nullable if you don’t know yet)
   - `phone_number` (stored in international format, e.g., +91…)
   - `whatsapp_optin` (true/false)
   - `created_at`, `updated_at`

2. **products**
   - `id`
   - `sku`
   - `name`
   - `category`
   - `price`
   - `stock_qty`
   - `image_url`
   - `whatsapp_product_id` (link to WhatsApp catalog item)
   - `is_active` (true/false)

3. **calls**
   - `id`
   - `telephony_call_id`
   - `customer_id` (FK)
   - `from_number`
   - `to_number`
   - `status` (ringing, answered, completed)
   - `duration_seconds`
   - `ended_at`

4. **whatsapp_messages**
   - `id`
   - `customer_id`
   - `wa_message_id`
   - `type` (template, text, catalog, multiproduct)
   - `payload` (JSON – full request/response data)
   - `status` (queued, sent, delivered, read, failed)
   - `created_at`

This structure allows you to track every call and message.

---

## Phase 6 – Build the Backend Foundation (Server & Webhooks)

### Step 6.1: Create Backend Project

Example with Node.js:

1. Initialize project: `npm init`
2. Install dependencies:
   - `express` (web framework)
   - `pg` or `mysql2` (database client)
   - `axios` or `node-fetch` (for making HTTP requests to WhatsApp API)
   - `dotenv` (for environment variables)
3. Create main file `app.js` / `server.js`.

### Step 6.2: Implement Basic Routes

1. `GET /health`
   - Returns `{ status: "ok" }`
   - Used for uptime checks.

2. `POST /webhooks/call-status`
   - Will be called by telephony provider.
   - For now just log the body to console and return `200 OK`.

3. `POST /webhooks/whatsapp`
   - Will be called by WhatsApp.
   - For now just log messages & status updates.

### Step 6.3: Connect to the Database

- Setup DB connection using a config file.
- Write basic functions to:
  - Insert / update customers
  - Insert call records
  - Insert WhatsApp message logs

At this stage, you have:

- A server that can receive webhooks from both telephony and WhatsApp.
- A database to store necessary data.

---

## Phase 7 – Implement the Core Automation Logic

This is where the main magic happens.

### Step 7.1: Call Status Webhook Logic

In `POST /webhooks/call-status` handler:

1. Parse the incoming data:
   - Call status (we only care about `completed`)
   - Caller’s phone number
   - Your business number
   - Call ID
   - Call duration

2. Normalize the phone number:
   - Convert to E.164 format (`+91xxxx` etc.).

3. Upsert customer:
   - If customer with this phone already exists → load it.
   - Else create a new row in `customers` with `whatsapp_optin = false` by default.

4. Create a record in `calls` table with status `completed` and duration.

5. Check if automation should run:
   - If `call status = completed` **AND**
   - `duration_seconds >= minimum_duration_setting` (e.g., 30 sec) **AND**
   - `customer.whatsapp_optin = true`
   - → **trigger WhatsApp follow-up**.

6. Instead of sending immediately, push a job to a queue (for speed & reliability).  
   - For example, use Redis + BullMQ or a similar job queue.

### Step 7.2: WhatsApp Follow-up Job

Create a function like `sendPostCallWhatsApp(customer, call)`:

1. Build & send a **template message** (thank-you + intro).
2. Immediately send a **catalog or multi-product message**.

#### Template Message (Thank You)

- Create and approve a template in Meta called e.g. `post_call_catalog_followup`.
- Example message:

  > Hi {{1}}, thanks for talking with {{2}} from {{3}}.  
  > Tap below to see our latest collection on WhatsApp.

- Variables:
  - {{1}}: Customer name or phone
  - {{2}}: Your name or “Sales Team”
  - {{3}}: Your brand name

Use the WhatsApp Messages API to send this template.

#### Catalog / Product Message

You have two options:

1. **Full Catalog Button**
   - A message that says “Click below to view our catalog” with a button that opens your WhatsApp catalog.

2. **Multi-Product Message**
   - Shows 5–30 selected items.
   - You pick items using their `whatsapp_product_id` from your `products` table.
   - Perfect for sending the **most relevant products** for that customer.

For simplicity in version 1:

- Always send a **“View catalog”** message after the template.
- Later, upgrade to category-wise or personalized lists.

3. Save each WhatsApp API call response into `whatsapp_messages` table.

---

## Phase 8 – Build a Simple, User-Friendly Admin Panel

The admin panel should be **very simple** and designed for non-technical staff.

### Step 8.1: Technology

- Use a simple frontend stack:
  - React / Next.js or
  - Even a simple server-rendered UI (Django admin, Laravel, etc.) if you prefer.

### Step 8.2: Key Screens

1. **Dashboard (Home)**
   - Big toggle: `Post-Call Automation: ON / OFF`
   - Setting: “Minimum call duration before sending WhatsApp” (input box)
   - Stat cards:
     - Today’s calls
     - Today’s WhatsApp follow-ups sent
     - Errors today (if any)

2. **Customers Page**
   - List of customers with:
     - Name
     - Phone
     - WhatsApp opt-in (Yes/No)
   - Button to manually toggle opt-in (if you got consent elsewhere).
   - Simple search bar.

3. **Products Page**
   - Table of products:
     - Name, Category, Price, Stock, Active (Yes/No), In WhatsApp Catalog (Yes/No)
   - Easy forms to add/edit products.
   - Button: “Sync to WhatsApp Catalog” (for developer to implement or run automatically).

4. **Calls & Messages Page**
   - List of recent calls:
     - Customer
     - Duration
     - Whether WhatsApp follow-up was sent
   - List of recent WhatsApp messages:
     - Template name / type
     - Status (sent, delivered, read, failed)
     - Quick filters by date.

### Step 8.3: UX Principles for Simplicity

- Use **plain language**, not technical words:
  - “Send message after call” instead of “post-call automation trigger”.
- Add short explanations / tooltips next to settings:
  - e.g., “Minimum call duration: We only send WhatsApp if the call lasted at least this long. This avoids sending messages after accidental calls.”
- Make important actions big and obvious:
  - Large toggle for automation ON/OFF
  - Clear Save buttons.
- Avoid clutter:
  - Start with only the pages mentioned above.
  - Add more screens only when truly needed.

---

## Phase 9 – Testing the Full Flow

### Step 9.1: Internal Tests

1. Use your telephony provider to call your own mobile number.
2. Have a conversation longer than the minimum duration.
3. End the call.
4. Check that:
   - A new call is recorded in your DB.
   - A follow-up WhatsApp template message arrives.
   - The catalog / product message arrives.

### Step 9.2: Edge Cases to Test

- Very short calls (below duration threshold) → No WhatsApp message.
- Call with a number that **has not given WhatsApp consent** → No message.
- Numbers without WhatsApp account → WhatsApp API should fail gracefully; log error.
- Multiple calls from same customer in one day → Decide whether to send message every time or only once per day (add a rule if needed).

### Step 9.3: Real-World Pilot

1. Run with a **small sample** of real customers (e.g., 10–20 per day).
2. Collect feedback:
   - Did they receive messages reliably?
   - Do they like the format?
   - Are they able to browse and reply easily?
3. Adjust template text and catalog organization based on feedback.

---

## Phase 10 – Optimization & Advanced Features (Make It Faster & Smarter)

Once the basic system works and is stable, you can improve it.

### 10.1 Performance & Speed

1. **Use Job Queues**
   - Make sure WhatsApp messages are sent via a queue worker, not inside webhook handler.
   - This keeps the system fast and avoids timeouts.

2. **Caching**
   - Cache commonly used product lists (e.g., “Top 30 catalog items”) in memory or Redis to avoid repeated database work.

3. **Horizontal Scaling**
   - If your traffic grows, you can run multiple instances of your backend behind a load balancer.

### 10.2 Smarter Product Selection

Instead of always sending the full catalog, you can:

- Send items based on:
  - Customer’s previous purchase history (if you store it).
  - Category they showed interest in (tag them manually or automatically).
  - New arrivals and offers.

For example:
- Tag customers as “Men’s Wear”, “Women’s Wear”, “Kids”, etc.
- When you call a “Men’s Wear” customer, send them a multi-product message with men’s items first.

### 10.3 Multiple Templates & Campaigns

- Have different templates for:
  - New customer (first-time call)
  - Repeat customer
  - Special discount campaign
- Admin panel dropdown: “Default template for post-call messages”

### 10.4 Simple Automation Rules (User-Friendly)

Add a visual “rules” screen with plain language:

- If call duration ≥ 60 seconds → send **full catalog**.
- If call duration between 30–60 seconds → send **top 10 products**.
- If customer is tagged “Loyal customer” → include **special discount message**.

Implementation can be technical inside the backend, but UI should stay simple checkboxes and dropdowns.

### 10.5 Error Monitoring and Alerts

- Integrate simple error logging (e.g. Sentry or a custom error log).
- Send email / WhatsApp to you if:
  - WhatsApp API fails multiple times.
  - Telephony webhook is not received for long periods.

---

## Phase 11 – Maintenance & Future Improvements

### 11.1 Regular Maintenance

- Check WhatsApp templates status and performance.
- Clean up inactive products from catalog.
- Update product prices and stock regularly.
- Review call & message logs to ensure everything is working smoothly.

### 11.2 Future Ideas

- Integrate with your **website or e-commerce system** to sync orders and stock automatically.
- Add a **simple chatbot** to answer FAQs in WhatsApp (delivery time, return policy, size guide, etc.).
- Add **order confirmation** via WhatsApp with item breakdown.
- Add **customer tags** and segments for more personalized follow-ups.

---

## Summary

By following these phases:

1. Set up WhatsApp Business & Catalog  
2. Set up Telephony with Webhooks  
3. Build backend & database for customers, calls, products, messages  
4. Implement post-call WhatsApp automation (template + catalog)  
5. Build a **simple, user-friendly** admin panel  
6. Test thoroughly with real calls  
7. Optimize for speed and add smarter features  

…you’ll have a **fully functional, production-ready** automation system that sends your catalog and products to customers on WhatsApp automatically after calls, and is easy for you and your team to operate.

You can now share this document with your developer and treat it as the **master plan** for building your system from start to finish.
