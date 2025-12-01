-- Migration: Add new tables and columns for Phase 1
-- Run this against your database

-- 1. Update tenant_settings table with new columns
ALTER TABLE tenant_settings
ADD COLUMN IF NOT EXISTS whatsapp_phone_number_id VARCHAR(100),
ADD COLUMN IF NOT EXISTS whatsapp_business_account_id VARCHAR(100),
ADD COLUMN IF NOT EXISTS whatsapp_access_token TEXT,
ADD COLUMN IF NOT EXISTS whatsapp_webhook_verify_token VARCHAR(255),
ADD COLUMN IF NOT EXISTS webhook_secret_key VARCHAR(255),
ADD COLUMN IF NOT EXISTS thank_you_message TEXT DEFAULT 'Thank you for calling! Here''s our latest catalog:',
ADD COLUMN IF NOT EXISTS include_catalog BOOLEAN DEFAULT TRUE,
ADD COLUMN IF NOT EXISTS catalog_header_message TEXT DEFAULT 'Browse our exclusive collection:',
ADD COLUMN IF NOT EXISTS catalog_footer_message TEXT DEFAULT 'Reply with product number to inquire!',
ADD COLUMN IF NOT EXISTS message_delay_seconds INTEGER DEFAULT 5,
ADD COLUMN IF NOT EXISTS is_whatsapp_configured BOOLEAN DEFAULT FALSE,
ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE,
ADD COLUMN IF NOT EXISTS created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE;

-- 2. Update calls table with automation tracking
ALTER TABLE calls
ADD COLUMN IF NOT EXISTS automation_triggered BOOLEAN DEFAULT FALSE,
ADD COLUMN IF NOT EXISTS automation_triggered_at TIMESTAMP WITH TIME ZONE,
ADD COLUMN IF NOT EXISTS automation_status VARCHAR(50);

-- 3. Create message_logs table
CREATE TABLE IF NOT EXISTS message_logs (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER NOT NULL REFERENCES tenants(id),
    call_id INTEGER REFERENCES calls(id),
    recipient_phone VARCHAR(20) NOT NULL,
    recipient_name VARCHAR(255),
    message_type VARCHAR(50) NOT NULL,
    message_content TEXT,
    media_url TEXT,
    whatsapp_message_id VARCHAR(255),
    status VARCHAR(50) DEFAULT 'pending',
    error_message TEXT,
    api_response JSONB,
    retry_count INTEGER DEFAULT 0,
    max_retries INTEGER DEFAULT 3,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    sent_at TIMESTAMP WITH TIME ZONE,
    delivered_at TIMESTAMP WITH TIME ZONE
);

-- 4. Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_message_logs_tenant_id ON message_logs(tenant_id);
CREATE INDEX IF NOT EXISTS idx_message_logs_status ON message_logs(status);
CREATE INDEX IF NOT EXISTS idx_message_logs_created_at ON message_logs(created_at);
CREATE INDEX IF NOT EXISTS idx_calls_caller_phone ON calls(caller_phone);
CREATE INDEX IF NOT EXISTS idx_tenant_settings_tenant_id ON tenant_settings(tenant_id);

-- 5. Update tenants table
ALTER TABLE tenants
ADD COLUMN IF NOT EXISTS business_name VARCHAR(255),
ADD COLUMN IF NOT EXISTS business_phone VARCHAR(20),
ADD COLUMN IF NOT EXISTS business_email VARCHAR(255),
ADD COLUMN IF NOT EXISTS business_address VARCHAR(500),
ADD COLUMN IF NOT EXISTS is_setup_complete BOOLEAN DEFAULT FALSE;
