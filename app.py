"""
app.py - AMAS Project
Flask Application with PostgreSQL Database Integration
COMPLETE CORRECTED VERSION - All fixes applied
"""

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import uuid
import traceback
from dotenv import load_dotenv

# Import database functions
from database.queries import (
    user_register, user_login, get_user_by_email, email_exists,
    create_conversation, get_user_conversations, delete_conversation,
    add_message, get_conversation_messages,
    save_source_document, get_source_document,
    save_conversation_summary, get_conversation_summary,
    submit_feedback, get_faq_questions, get_unresolved_tickets,
    get_user_stats
)

from main import run_video_pipeline, run_document_pipeline

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "videagent_secret")

# Configuration
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = int(os.getenv("MAX_CONTENT_LENGTH", 52428800))


def get_payload():
    """Get data from JSON or form"""
    data = request.get_json(silent=True)
    if data:
        return data
    return request.form.to_dict()


def require_login(f):
    """Decorator to require login"""
    def decorated_function(*args, **kwargs):
        if "user_email" not in session:
            if request.method == "POST":
                return jsonify({"success": False, "message": "Please login first."}), 401
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function


# ============================================
# AUTHENTICATION ROUTES
# ============================================

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = get_payload()
        name = (data.get("name") or "").strip()
        email = (data.get("email") or "").strip().lower()
        password = data.get("password") or ""

        # Validation
        if not name or not email or not password:
            return jsonify({"success": False, "message": "All fields are required."}), 400

        if len(password) < 8:
            return jsonify({"success": False, "message": "Password must be at least 8 characters."}), 400

        if email_exists(email):
            return jsonify({"success": False, "message": "An account with this email already exists."}), 400

        # Register in database
        result = user_register(name, email, password)
        
        if result["success"]:
            return jsonify({"success": True, "redirect": url_for("login")})
        else:
            return jsonify({"success": False, "message": result.get("error", "Registration failed")}), 400

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = get_payload()
        email = (data.get("email") or "").strip().lower()
        password = data.get("password") or ""

        # Login with database
        result = user_login(email, password)
        
        if result["success"]:
            session["user_email"] = result["email"]
            session["user_name"] = result["name"]
            session["user_id"] = result["user_id"]
            return jsonify({"success": True, "redirect": url_for("dashboard")})
        else:
            return jsonify({"success": False, "message": result["error"]}), 401

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


# ============================================
# DASHBOARD ROUTES
# ============================================

@app.route("/dashboard")
@require_login
def dashboard():
    user_name = session.get("user_name", "User")
    return render_template("dashboard.html", user_name=user_name)


@app.route("/api/dashboard")
@require_login
def api_dashboard():
    """Get dashboard stats and recent conversations"""
    try:
        user_id = session.get("user_id")
        
        # Get user statistics
        stats = get_user_stats(user_id)
        
        # Get recent conversations
        conversations = get_user_conversations(user_id)
        
        return jsonify({
            "success": True,
            "stats": stats,
            "conversations": conversations
        }), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"success": False, "message": str(e)}), 500
    


# ============================================
# ANALYSIS ROUTES
# ============================================

@app.route("/url-analysis", methods=["GET", "POST"])
@require_login
def url_analysis():
    if request.method == "GET":
        return render_template("url_analysis.html", user_name=session.get("user_name", "Admin"))

    data = get_payload()
    source = (data.get("url") or data.get("source") or "").strip()
    question = (data.get("question") or "").strip()
    translate_raw = (data.get("translate") or "").strip().lower()
    translate = translate_raw in ["1", "true", "yes", "y", "on"]

    if not source:
        return jsonify({"success": False, "message": "URL is required."}), 400

    if not question:
        return jsonify({"success": False, "message": "Question is required."}), 400

    try:
        user_id = session.get("user_id")
        
        # Create conversation session
        conv_result = create_conversation(
            user_id=user_id,
            conversation_type="URL",
            title=f"YouTube Analysis - {source[:50]}",
            description=question
        )
        
        if not conv_result["success"]:
            return jsonify({"success": False, "message": "Failed to create conversation"}), 500
        
        conversation_id = conv_result["conversation_id"]
        
        # Save source document
        save_source_document(
            conversation_id=conversation_id,
            source_type="URL",
            source_url=source,
            extracted_title=f"YouTube Analysis"
        )
        
        # Add user question to messages
        add_message(conversation_id, "user", question)
        
        # Run analysis pipeline
        result = run_video_pipeline(source=source, question=question, translate=translate)
        
        # Add AI response to messages
        ai_response = result.get("result", "Analysis complete")
        add_message(conversation_id, "assistant", str(ai_response))
        
        # Save summary
        save_conversation_summary(
            conversation_id=conversation_id,
            extracted_title=f"YouTube - {source[:100]}",
            executive_summary=str(ai_response)[:500],
            key_points="",
            sentiment="Neutral",
            total_messages=2,
            processing_time_ms=0,
            model_version="mistral-ai"
        )
        
        return jsonify({
            "success": True,
            "conversation_id": conversation_id,
            "result": result
        }), 200
        
    except Exception as e:
        traceback.print_exc()
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/document-analysis", methods=["GET", "POST"])
@require_login
def document_analysis():
    if request.method == "GET":
        return render_template("document_analysis.html", user_name=session.get("user_name", "Admin"))

    question = (request.form.get("question") or "").strip()
    uploaded_file = request.files.get("file")

    if not uploaded_file or uploaded_file.filename == "":
        return jsonify({"success": False, "message": "Please upload a document file."}), 400

    if not question:
        return jsonify({"success": False, "message": "Question is required."}), 400

    try:
        user_id = session.get("user_id")
        
        # Save uploaded file
        filename = secure_filename(uploaded_file.filename)
        unique_name = f"{uuid.uuid4().hex}_{filename}"
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], unique_name)
        uploaded_file.save(file_path)
        
        # Create conversation session
        conv_result = create_conversation(
            user_id=user_id,
            conversation_type="DOCUMENT",
            title=f"Document Analysis - {filename}",
            description=question
        )
        
        if not conv_result["success"]:
            return jsonify({"success": False, "message": "Failed to create conversation"}), 500
        
        conversation_id = conv_result["conversation_id"]
        
        # Save source document metadata
        file_size = os.path.getsize(file_path)
        save_source_document(
            conversation_id=conversation_id,
            source_type=filename.split('.')[-1].upper(),
            file_name=filename,
            file_path=file_path,
            file_size=file_size,
            extracted_title=filename
        )
        
        # Add user question
        add_message(conversation_id, "user", question)
        
        # Run document pipeline
        result = run_document_pipeline(file_path=file_path, question=question)
        
        # Add AI response
        ai_response = result.get("result", "Analysis complete")
        add_message(conversation_id, "assistant", str(ai_response))
        
        # Save summary
        save_conversation_summary(
            conversation_id=conversation_id,
            extracted_title=filename,
            executive_summary=str(ai_response)[:500],
            key_points="",
            sentiment="Neutral",
            total_messages=2,
            processing_time_ms=0,
            model_version="mistral-ai"
        )
        
        return jsonify({
            "success": True,
            "conversation_id": conversation_id,
            "result": result
        }), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({"success": False, "message": str(e)}), 500


# ============================================
# HISTORY & CHAT ROUTES
# ============================================

@app.route("/history")
@require_login
def history():
    return render_template("history.html", user_name=session.get("user_name", "Admin"))


@app.route("/api/history")
@require_login
def api_history():
    """Get all conversations for user"""
    try:
        user_id = session.get("user_id")
        conversations = get_user_conversations(user_id)
        
        return jsonify({
            "success": True,
            "items": conversations
        }), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/api/conversation/<int:conversation_id>")
@require_login
def view_conversation(conversation_id):
    """Get conversation details and messages"""
    try:
        user_id = session.get("user_id")
        
        # Verify user owns this conversation
        user_conversations = get_user_conversations(user_id)
        conv_exists = any(c['conversation_id'] == conversation_id for c in user_conversations)
        
        if not conv_exists:
            return jsonify({"success": False, "message": "Conversation not found"}), 404
        
        # Get messages
        messages = get_conversation_messages(conversation_id)
        source = get_source_document(conversation_id)
        summary = get_conversation_summary(conversation_id)
        
        return jsonify({
            "success": True,
            "messages": messages,
            "source": source,
            "summary": summary
        }), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/api/conversation/<int:conversation_id>/message", methods=["POST"])
@require_login
def add_conversation_message(conversation_id):
    """Add a new message to existing conversation and get AI response"""
    try:
        user_id = session.get("user_id")
        data = request.get_json()
        message = (data.get("message") or "").strip()
        
        if not message:
            return jsonify({"success": False, "message": "Message cannot be empty"}), 400
        
        # Verify user owns this conversation
        user_conversations = get_user_conversations(user_id)
        conv_exists = any(c['conversation_id'] == conversation_id for c in user_conversations)
        
        if not conv_exists:
            return jsonify({"success": False, "message": "Conversation not found"}), 404
        
        # Add user message
        add_message(conversation_id, "user", message)
        
        # Get source document to run RAG
        source = get_source_document(conversation_id)
        
        if not source:
            return jsonify({"success": False, "message": "Source document not found"}), 404
        
        # Run RAG pipeline based on source type
        try:
            if source['source_type'] == 'URL':
                result = run_video_pipeline(
                    source=source['source_url'],
                    question=message,
                    translate=False
                )
            else:
                result = run_document_pipeline(
                    file_path=source['file_path'],
                    question=message
                )
            
            ai_response = result.get("result", "Unable to generate response")
            
        except Exception as e:
            print(f"Pipeline error: {e}")
            ai_response = f"Error processing request: {str(e)}"
        
        # Add AI response to messages
        add_message(conversation_id, "assistant", str(ai_response))
        
        return jsonify({
            "success": True,
            "response": str(ai_response)
        }), 200
        
    except Exception as e:
        traceback.print_exc()
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/api/conversation/<int:conversation_id>/delete", methods=["POST"])
@require_login
def delete_conv(conversation_id):
    """Delete a conversation (soft delete)"""
    try:
        user_id = session.get("user_id")
        result = delete_conversation(conversation_id, user_id)
        
        if result["success"]:
            return jsonify({"success": True, "message": "Conversation deleted"}), 200
        else:
            return jsonify({"success": False, "message": result.get("error")}), 500
    except Exception as e:
        traceback.print_exc()
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/chat")
@require_login
def view_chat():
    """Load chat interface for existing conversation"""
    conversation_id = request.args.get('id')
    if not conversation_id:
        return redirect(url_for('history'))
    try:
        # Verify conversation belongs to user
        user_id = session.get("user_id")
        user_conversations = get_user_conversations(user_id)
        conv_exists = any(c['conversation_id'] == int(conversation_id) for c in user_conversations)
        
        if not conv_exists:
            return redirect(url_for('history'))
        
        return render_template("conversation_view.html")
    except:
        return redirect(url_for('history'))


# ============================================
# FAQ ROUTES
# ============================================

@app.route("/faq")
@require_login
def faq():
    return render_template("faq.html", user_name=session.get("user_name", "Admin"))


@app.route("/api/faq")
@require_login
def api_faq():
    """Get all FAQ questions"""
    try:
        faqs = get_faq_questions()
        return jsonify({
            "success": True,
            "faqs": faqs
        }), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"success": False, "message": str(e)}), 500



@app.route("/api/faq/submit", methods=["POST"])
@require_login
def submit_faq():
    """Submit a FAQ question"""
    try:
        user_id = session.get("user_id")
        data = request.get_json()
        
        subject = (data.get("subject") or "").strip()
        content = (data.get("content") or "").strip()
        
        if not subject or not content:
            return jsonify({"success": False, "message": "Subject and content required"}), 400
        
        result = submit_feedback(
            user_id=user_id,
            feedback_type="FAQ",
            subject=subject,
            content=content
        )
        
        if result["success"]:
            return jsonify({"success": True, "message": "FAQ submitted"}), 200
        else:
            return jsonify({"success": False, "message": result.get("error")}), 500
    except Exception as e:
        traceback.print_exc()
        return jsonify({"success": False, "message": str(e)}), 500


# ============================================
# ERROR HANDLERS
# ============================================

@app.errorhandler(404)
def not_found(e):
    return jsonify({"success": False, "message": "Route not found"}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({"success": False, "message": "Internal server error"}), 500



# ============================================
# APP STARTUP
# ============================================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
        use_reloader=False
    )