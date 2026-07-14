-- =====================================================
-- AMAS PROJECT - COMPLETE SQL QUERIES
-- PostgreSQL Database Creation Script
-- =====================================================
-- COPY ALL OF THIS → PASTE IN pgAdmin → EXECUTE (Ctrl+Enter)
-- =====================================================

-- =====================================================
-- TABLE 1: users (User Authentication & Profiles)
-- =====================================================
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT true
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at);

-- =====================================================
-- TABLE 2: conversations (Chat Sessions Container)
-- =====================================================
CREATE TABLE conversations (
    conversation_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    conversation_type VARCHAR(20) NOT NULL CHECK (conversation_type IN ('URL', 'DOCUMENT')),
    title VARCHAR(255),
    description VARCHAR(500),
    is_deleted BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_conversations_users FOREIGN KEY (user_id) 
        REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_conversations_is_deleted ON conversations(is_deleted);
CREATE INDEX idx_conversations_created_at ON conversations(created_at);

-- =====================================================
-- TABLE 3: messages (Q&A Chat History - READ ONLY)
-- =====================================================
CREATE TABLE messages (
    message_id SERIAL PRIMARY KEY,
    conversation_id INT NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_messages_conversations FOREIGN KEY (conversation_id) 
        REFERENCES conversations(conversation_id) ON DELETE CASCADE
);

CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_role ON messages(role);
CREATE INDEX idx_messages_created_at ON messages(created_at);

-- =====================================================
-- TABLE 4: source_documents (URLs & Files Metadata)
-- =====================================================
CREATE TABLE source_documents (
    source_id SERIAL PRIMARY KEY,
    conversation_id INT NOT NULL UNIQUE,
    source_type VARCHAR(20) NOT NULL CHECK (source_type IN ('URL', 'PDF', 'DOCX', 'PPTX', 'TXT')),
    source_url VARCHAR(2048),
    file_name VARCHAR(255),
    file_path VARCHAR(500),
    file_size_bytes BIGINT,
    extracted_title VARCHAR(500),
    extracted_preview VARCHAR(1000),
    processed_content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_sourcedocuments_conversations FOREIGN KEY (conversation_id) 
        REFERENCES conversations(conversation_id) ON DELETE CASCADE
);

CREATE INDEX idx_source_documents_conversation_id ON source_documents(conversation_id);
CREATE INDEX idx_source_documents_source_type ON source_documents(source_type);

-- =====================================================
-- TABLE 5: conversation_summary (Analysis Results)
-- =====================================================
CREATE TABLE conversation_summary (
    summary_id SERIAL PRIMARY KEY,
    conversation_id INT NOT NULL UNIQUE,
    extracted_title VARCHAR(500),
    executive_summary TEXT,
    key_points TEXT,
    sentiment VARCHAR(50) CHECK (sentiment IN ('Positive', 'Neutral', 'Negative', 'Mixed')),
    total_messages INT DEFAULT 0,
    processing_time_ms INT,
    model_version VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_conversationsummary_conversations FOREIGN KEY (conversation_id) 
        REFERENCES conversations(conversation_id) ON DELETE CASCADE
);

CREATE INDEX idx_conversation_summary_conversation_id ON conversation_summary(conversation_id);
CREATE INDEX idx_conversation_summary_sentiment ON conversation_summary(sentiment);

-- =====================================================
-- TABLE 6: feedback (Reviews, FAQ, Support)
-- =====================================================
CREATE TABLE feedback (
    feedback_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    feedback_type VARCHAR(50) NOT NULL CHECK (feedback_type IN ('BUG', 'FEATURE_REQUEST', 'REVIEW', 'FAQ', 'GENERAL')),
    subject VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    is_resolved BOOLEAN DEFAULT false,
    admin_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_feedback_users FOREIGN KEY (user_id) 
        REFERENCES users(user_id) ON DELETE NO ACTION
);

CREATE INDEX idx_feedback_user_id ON feedback(user_id);
CREATE INDEX idx_feedback_feedback_type ON feedback(feedback_type);
CREATE INDEX idx_feedback_is_resolved ON feedback(is_resolved);

-- =====================================================
-- VIEWS FOR COMMON QUERIES
-- =====================================================

-- View 1: User's All Conversations with Summary
CREATE VIEW vw_user_conversations AS
SELECT 
    c.conversation_id,
    c.user_id,
    c.conversation_type,
    c.title,
    c.created_at,
    c.updated_at,
    cs.extracted_title,
    cs.executive_summary,
    cs.sentiment,
    (SELECT COUNT(*) FROM messages m WHERE m.conversation_id = c.conversation_id) AS message_count
FROM conversations c
LEFT JOIN conversation_summary cs ON c.conversation_id = cs.conversation_id
WHERE c.is_deleted = false
ORDER BY c.created_at DESC;

-- View 2: FAQ Questions from Community
CREATE VIEW vw_faq_questions AS
SELECT 
    feedback_id,
    user_id,
    subject,
    content,
    created_at
FROM feedback
WHERE feedback_type = 'FAQ'
ORDER BY created_at DESC;

-- View 3: Unresolved Support Tickets
CREATE VIEW vw_support_tickets AS
SELECT 
    feedback_id,
    user_id,
    feedback_type,
    subject,
    rating,
    is_resolved,
    created_at
FROM feedback
WHERE is_resolved = false
ORDER BY created_at ASC;

-- =====================================================
-- TRIGGERS FOR AUTOMATION
-- =====================================================

-- Trigger 1: Auto-update conversations.updated_at
CREATE OR REPLACE FUNCTION update_conversations_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tr_conversations_update
BEFORE UPDATE ON conversations
FOR EACH ROW
EXECUTE FUNCTION update_conversations_timestamp();

-- Trigger 2: Auto-update feedback.updated_at
CREATE OR REPLACE FUNCTION update_feedback_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tr_feedback_update
BEFORE UPDATE ON feedback
FOR EACH ROW
EXECUTE FUNCTION update_feedback_timestamp();

-- Trigger 3: Auto-update users.updated_at
CREATE OR REPLACE FUNCTION update_users_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tr_users_update
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION update_users_timestamp();

-- =====================================================
-- STORED PROCEDURES
-- =====================================================

-- Stored Procedure 1: Get User Dashboard Stats
CREATE OR REPLACE FUNCTION sp_get_user_dashboard_stats(p_user_id INT)
RETURNS TABLE (
    total_sessions INT,
    total_videos INT,
    total_documents INT,
    total_messages INT,
    total_feedback INT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        COUNT(DISTINCT c.conversation_id)::INT AS total_sessions,
        COUNT(DISTINCT CASE WHEN c.conversation_type = 'URL' THEN c.conversation_id END)::INT AS total_videos,
        COUNT(DISTINCT CASE WHEN c.conversation_type = 'DOCUMENT' THEN c.conversation_id END)::INT AS total_documents,
        COUNT(m.message_id)::INT AS total_messages,
        (SELECT COUNT(*) FROM feedback WHERE user_id = p_user_id)::INT AS total_feedback
    FROM conversations c
    LEFT JOIN messages m ON c.conversation_id = m.conversation_id
    WHERE c.user_id = p_user_id AND c.is_deleted = false;
END;
$$ LANGUAGE plpgsql;

-- Stored Procedure 2: Archive Old Conversations
CREATE OR REPLACE FUNCTION sp_archive_old_conversations(p_days_old INT DEFAULT 30)
RETURNS TABLE (
    archived_count INT
) AS $$
BEGIN
    UPDATE conversations
    SET is_deleted = true
    WHERE created_at < CURRENT_TIMESTAMP - INTERVAL '1 day' * p_days_old
    AND is_deleted = false;
    
    RETURN QUERY
    SELECT COUNT(*)::INT FROM conversations 
    WHERE created_at < CURRENT_TIMESTAMP - INTERVAL '1 day' * p_days_old
    AND is_deleted = true;
END;
$$ LANGUAGE plpgsql;

-- Stored Procedure 3: Get Conversation Details
CREATE OR REPLACE FUNCTION sp_get_conversation_details(p_conversation_id INT)
RETURNS TABLE (
    conversation_id INT,
    user_id INT,
    title VARCHAR,
    conversation_type VARCHAR,
    message_count INT,
    source_type VARCHAR,
    source_url VARCHAR,
    summary TEXT,
    sentiment VARCHAR,
    created_at TIMESTAMP
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.conversation_id,
        c.user_id,
        c.title,
        c.conversation_type,
        COUNT(m.message_id)::INT AS message_count,
        sd.source_type,
        sd.source_url,
        cs.executive_summary,
        cs.sentiment,
        c.created_at
    FROM conversations c
    LEFT JOIN messages m ON c.conversation_id = m.conversation_id
    LEFT JOIN source_documents sd ON c.conversation_id = sd.conversation_id
    LEFT JOIN conversation_summary cs ON c.conversation_id = cs.conversation_id
    WHERE c.conversation_id = p_conversation_id
    GROUP BY c.conversation_id, c.user_id, c.title, c.conversation_type, 
             sd.source_type, sd.source_url, cs.executive_summary, cs.sentiment, c.created_at;
END;
$$ LANGUAGE plpgsql;

-- Stored Procedure 4: Get User Conversations with Pagination
CREATE OR REPLACE FUNCTION sp_get_user_conversations(
    p_user_id INT,
    p_limit INT DEFAULT 20,
    p_offset INT DEFAULT 0
)
RETURNS TABLE (
    conversation_id INT,
    title VARCHAR,
    conversation_type VARCHAR,
    message_count INT,
    sentiment VARCHAR,
    created_at TIMESTAMP
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.conversation_id,
        c.title,
        c.conversation_type,
        COUNT(m.message_id)::INT AS message_count,
        cs.sentiment,
        c.created_at
    FROM conversations c
    LEFT JOIN messages m ON c.conversation_id = m.conversation_id
    LEFT JOIN conversation_summary cs ON c.conversation_id = cs.conversation_id
    WHERE c.user_id = p_user_id AND c.is_deleted = false
    GROUP BY c.conversation_id, c.title, c.conversation_type, cs.sentiment, c.created_at
    ORDER BY c.created_at DESC
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;

-- Stored Procedure 5: Delete User Data (GDPR Compliance)
CREATE OR REPLACE FUNCTION sp_delete_user_data(p_user_id INT)
RETURNS TABLE (
    status VARCHAR,
    deleted_count INT
) AS $$
DECLARE
    v_deleted_count INT;
BEGIN
    -- Mark all conversations as deleted
    UPDATE conversations SET is_deleted = true WHERE user_id = p_user_id;
    
    -- Count deleted records
    SELECT COUNT(*) INTO v_deleted_count FROM conversations WHERE user_id = p_user_id;
    
    -- Mark user as inactive
    UPDATE users SET is_active = false WHERE user_id = p_user_id;
    
    RETURN QUERY
    SELECT 'User data marked for deletion'::VARCHAR AS status, v_deleted_count AS deleted_count;
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- VERIFICATION QUERIES (RUN THESE TO VERIFY)
-- =====================================================

-- Check all tables created:
SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';

-- Check all views created:
SELECT table_name FROM information_schema.views WHERE table_schema = 'public';

-- Check all triggers:
SELECT trigger_name FROM information_schema.triggers WHERE trigger_schema = 'public';

-- Count tables (should be 6):
SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE';

-- =====================================================
-- ALL DONE! ✅
-- 6 Tables Created
-- 3 Views Created
-- 3 Triggers Created
-- 5 Stored Procedures Created
-- =====================================================