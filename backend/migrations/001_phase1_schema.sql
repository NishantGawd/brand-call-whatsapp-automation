-- Migration: Phase 1 - Complete Schema Setup
-- This creates all necessary tables and columns from scratch

-- 1. Drop existing tenant_settings if it exists (clean slate)
DROP TABLE IF EXISTS tenant_settings CASCADE;

-- 2. Create tenant_settings table with all required columns
CREATE TABLE IF NOT EXISTS tenant_settings (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,

    -- WhatsApp Configuration
    whatsapp_phone_number_id VARCHAR(255),
    whatsapp_business_account_id VARCHAR(255),
    whatsapp_access_token TEXT,
    whatsapp_webhook_verify_token VARCHAR(255),

    -- Webhook Security
    webhook_secret_key VARCHAR(255),

    -- Message Configuration
    thank_you_message TEXT DEFAULT 'Thank you for calling! Here is our complete catalog with product details.',
    include_catalog BOOLEAN DEFAULT TRUE,

    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Ensure one settings record per tenant
    UNIQUE(tenant_id)
);

-- 3. Create message_logs table for tracking all sent messages
CREATE TABLE IF NOT EXISTS message_logs (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    call_id INTEGER REFERENCES calls(id) ON DELETE SET NULL,

    -- Message Details
    recipient_phone VARCHAR(20) NOT NULL,
    message_type VARCHAR(50) NOT NULL, -- 'text', 'image', 'document', 'template'
    message_content TEXT,
    media_url TEXT,

    -- WhatsApp Response
    whatsapp_message_id VARCHAR(255),
    status VARCHAR(50) DEFAULT 'pending', -- 'pending', 'sent', 'delivered', 'read', 'failed'
    error_message TEXT,

    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Add indexes for better performance
CREATE INDEX IF NOT EXISTS idx_message_logs_tenant ON message_logs(tenant_id);
CREATE INDEX IF NOT EXISTS idx_message_logs_call ON message_logs(call_id);
CREATE INDEX IF NOT EXISTS idx_message_logs_status ON message_logs(status);
CREATE INDEX IF NOT EXISTS idx_message_logs_created ON message_logs(created_at DESC);

-- 5. Create trigger for updating updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_tenant_settings_updated_at BEFORE UPDATE ON tenant_settings
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_message_logs_updated_at BEFORE UPDATE ON message_logs
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- 6. Insert default settings for existing tenants
INSERT INTO tenant_settings (tenant_id, thank_you_message, include_catalog)
SELECT id,
       'Thank you for calling! Here is our complete catalog with product details.',
       TRUE
FROM tenants
WHERE NOT EXISTS (
    SELECT 1 FROM tenant_settings WHERE tenant_settings.tenant_id = tenants.id
);
