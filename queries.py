"""
database/queries.py
All Database Query Functions for AMAS Project
"""

from database.connection import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import psycopg2.extras


# ============================================
# USER QUERIES
# ============================================

def user_register(name, email, password):
    """Register a new user"""
    try:
        query = """
            INSERT INTO users (email, password_hash, first_name, created_at, updated_at, is_active)
            VALUES (%s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, true)
            RETURNING user_id
        """
        password_hash = generate_password_hash(password)
        cursor = db.conn.cursor()
        cursor.execute(query, (email, password_hash, name))
        db.conn.commit()
        
        user_id = cursor.fetchone()[0]
        cursor.close()
        return {"success": True, "user_id": user_id}
    except Exception as e:
        db.conn.rollback()
        return {"success": False, "error": str(e)}


def user_login(email, password):
    """Login user - verify credentials"""
    try:
        query = "SELECT user_id, email, password_hash, first_name FROM users WHERE email = %s AND is_active = true"
        cursor = db.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(query, (email.lower(),))
        user = cursor.fetchone()
        cursor.close()
        
        if not user:
            return {"success": False, "error": "Invalid email or password"}
        
        # Check password
        if check_password_hash(user['password_hash'], password):
            return {
                "success": True,
                "user_id": user['user_id'],
                "email": user['email'],
                "name": user['first_name']
            }
        else:
            return {"success": False, "error": "Invalid email or password"}
            
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_user_by_email(email):
    """Get user details by email"""
    try:
        query = "SELECT user_id, email, first_name FROM users WHERE email = %s AND is_active = true"
        cursor = db.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(query, (email.lower(),))
        user = cursor.fetchone()
        cursor.close()
        return user
    except Exception as e:
        print(f"Error: {e}")
        return None


# ============================================
# CONVERSATION QUERIES
# ============================================

def create_conversation(user_id, conversation_type, title, description=None):
    """Create a new conversation session"""
    try:
        query = """
            INSERT INTO conversations 
            (user_id, conversation_type, title, description, is_deleted, created_at, updated_at)
            VALUES (%s, %s, %s, %s, false, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            RETURNING conversation_id
        """
        cursor = db.conn.cursor()
        cursor.execute(query, (user_id, conversation_type, title, description))
        db.conn.commit()
        
        conv_id = cursor.fetchone()[0]
        cursor.close()
        return {"success": True, "conversation_id": conv_id}
    except Exception as e:
        db.conn.rollback()
        return {"success": False, "error": str(e)}


def get_user_conversations(user_id):
    """Get all conversations for a user (from view)"""
    try:
        query = """
            SELECT conversation_id, user_id, conversation_type, title, created_at, 
                   updated_at, extracted_title, executive_summary, sentiment, message_count
            FROM vw_user_conversations
            WHERE user_id = %s
            ORDER BY created_at DESC
        """
        cursor = db.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(query, (user_id,))
        conversations = cursor.fetchall()
        cursor.close()
        return conversations
    except Exception as e:
        print(f"Error: {e}")
        return []


def delete_conversation(conversation_id, user_id):
    """Soft delete a conversation"""
    try:
        query = """
            UPDATE conversations 
            SET is_deleted = true, updated_at = CURRENT_TIMESTAMP
            WHERE conversation_id = %s AND user_id = %s
        """
        cursor = db.conn.cursor()
        cursor.execute(query, (conversation_id, user_id))
        db.conn.commit()
        cursor.close()
        return {"success": True}
    except Exception as e:
        db.conn.rollback()
        return {"success": False, "error": str(e)}


# ============================================
# MESSAGE QUERIES (Q&A Chat History)
# ============================================

def add_message(conversation_id, role, content):
    """Add a message to conversation (user or assistant)"""
    try:
        query = """
            INSERT INTO messages (conversation_id, role, content, created_at)
            VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
            RETURNING message_id
        """
        cursor = db.conn.cursor()
        cursor.execute(query, (conversation_id, role, content))
        db.conn.commit()
        
        msg_id = cursor.fetchone()[0]
        cursor.close()
        return {"success": True, "message_id": msg_id}
    except Exception as e:
        db.conn.rollback()
        return {"success": False, "error": str(e)}


def get_conversation_messages(conversation_id):
    """Get all messages for a conversation"""
    try:
        query = """
            SELECT message_id, conversation_id, role, content, created_at
            FROM messages
            WHERE conversation_id = %s
            ORDER BY created_at ASC
        """
        cursor = db.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(query, (conversation_id,))
        messages = cursor.fetchall()
        cursor.close()
        return messages
    except Exception as e:
        print(f"Error: {e}")
        return []


# ============================================
# SOURCE DOCUMENTS QUERIES
# ============================================

def save_source_document(conversation_id, source_type, source_url=None, file_name=None, 
                        file_path=None, file_size=None, extracted_title=None, 
                        extracted_preview=None, processed_content=None):
    """Save URL or File metadata"""
    try:
        query = """
            INSERT INTO source_documents
            (conversation_id, source_type, source_url, file_name, file_path, 
             file_size_bytes, extracted_title, extracted_preview, processed_content, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
            RETURNING source_id
        """
        cursor = db.conn.cursor()
        cursor.execute(query, (
            conversation_id, source_type, source_url, file_name, file_path,
            file_size, extracted_title, extracted_preview, processed_content
        ))
        db.conn.commit()
        
        source_id = cursor.fetchone()[0]
        cursor.close()
        return {"success": True, "source_id": source_id}
    except Exception as e:
        db.conn.rollback()
        return {"success": False, "error": str(e)}


def get_source_document(conversation_id):
    """Get source document for a conversation"""
    try:
        query = """
            SELECT source_id, conversation_id, source_type, source_url, file_name,
                   file_path, file_size_bytes, extracted_title, extracted_preview, 
                   processed_content, created_at
            FROM source_documents
            WHERE conversation_id = %s
        """
        cursor = db.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(query, (conversation_id,))
        document = cursor.fetchone()
        cursor.close()
        return document
    except Exception as e:
        print(f"Error: {e}")
        return None


# ============================================
# CONVERSATION SUMMARY QUERIES
# ============================================

def save_conversation_summary(conversation_id, extracted_title, executive_summary, 
                             key_points, sentiment, total_messages, processing_time_ms, 
                             model_version):
    """Save analysis results/summary"""
    try:
        query = """
            INSERT INTO conversation_summary
            (conversation_id, extracted_title, executive_summary, key_points, sentiment,
             total_messages, processing_time_ms, model_version, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
            RETURNING summary_id
        """
        cursor = db.conn.cursor()
        cursor.execute(query, (
            conversation_id, extracted_title, executive_summary, key_points, sentiment,
            total_messages, processing_time_ms, model_version
        ))
        db.conn.commit()
        
        summary_id = cursor.fetchone()[0]
        cursor.close()
        return {"success": True, "summary_id": summary_id}
    except Exception as e:
        db.conn.rollback()
        return {"success": False, "error": str(e)}


def get_conversation_summary(conversation_id):
    """Get summary for a conversation"""
    try:
        query = """
            SELECT summary_id, conversation_id, extracted_title, executive_summary,
                   key_points, sentiment, total_messages, processing_time_ms, 
                   model_version, created_at
            FROM conversation_summary
            WHERE conversation_id = %s
        """
        cursor = db.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(query, (conversation_id,))
        summary = cursor.fetchone()
        cursor.close()
        return summary
    except Exception as e:
        print(f"Error: {e}")
        return None


# ============================================
# FEEDBACK QUERIES
# ============================================

def submit_feedback(user_id, feedback_type, subject, content, rating=None):
    """Submit user feedback (bug, feature request, review, faq, general)"""
    try:
        query = """
            INSERT INTO feedback
            (user_id, feedback_type, subject, content, rating, is_resolved, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, false, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            RETURNING feedback_id
        """
        cursor = db.conn.cursor()
        cursor.execute(query, (user_id, feedback_type, subject, content, rating))
        db.conn.commit()
        
        feedback_id = cursor.fetchone()[0]
        cursor.close()
        return {"success": True, "feedback_id": feedback_id}
    except Exception as e:
        db.conn.rollback()
        return {"success": False, "error": str(e)}


def get_faq_questions():
    """Get all FAQ questions from community"""
    try:
        query = "SELECT * FROM vw_faq_questions ORDER BY created_at DESC"
        cursor = db.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(query)
        faqs = cursor.fetchall()
        cursor.close()
        return faqs
    except Exception as e:
        print(f"Error: {e}")
        return []


def get_unresolved_tickets():
    """Get unresolved support tickets"""
    try:
        query = "SELECT * FROM vw_support_tickets ORDER BY created_at ASC"
        cursor = db.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(query)
        tickets = cursor.fetchall()
        cursor.close()
        return tickets
    except Exception as e:
        print(f"Error: {e}")
        return []


# ============================================
# HELPER FUNCTIONS
# ============================================

def email_exists(email):
    """Check if email already registered"""
    try:
        query = "SELECT user_id FROM users WHERE email = %s"
        cursor = db.conn.cursor()
        cursor.execute(query, (email.lower(),))
        result = cursor.fetchone()
        cursor.close()
        return result is not None
    except Exception as e:
        print(f"Error: {e}")
        return False


def get_user_stats(user_id):
    """Get statistics for user dashboard"""
    try:
        # Count conversations by type
        query = """
            SELECT 
                conversation_type,
                COUNT(*) as count
            FROM conversations
            WHERE user_id = %s AND is_deleted = false
            GROUP BY conversation_type
        """
        cursor = db.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(query, (user_id,))
        stats = cursor.fetchall()
        cursor.close()
        
        # Format results
        result = {
            "total_sessions": 0,
            "total_videos": 0,
            "total_documents": 0,
            "total_messages": 0
        }
        
        for stat in stats:
            if stat['conversation_type'] == 'URL':
                result['total_videos'] = stat['count']
            elif stat['conversation_type'] == 'DOCUMENT':
                result['total_documents'] = stat['count']
            result['total_sessions'] += stat['count']
        
        # Get total messages
        query = """
            SELECT COUNT(*) as count
            FROM messages m
            JOIN conversations c ON m.conversation_id = c.conversation_id
            WHERE c.user_id = %s
        """
        cursor = db.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(query, (user_id,))
        msg_result = cursor.fetchone()
        cursor.close()
        
        result['total_messages'] = msg_result['count'] if msg_result else 0
        return result
        
    except Exception as e:
        print(f"Error: {e}")
        return {}