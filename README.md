# 🚀 AMAS - AI-Powered Media Analysis System

<img width="1360" height="581" alt="Dashboard_page_insights_" src="https://github.com/user-attachments/assets/333d62f6-80db-4227-ae23-be55799de323" />

<img width="1344" height="644" alt="History_page" src="https://github.com/user-attachments/assets/5fb91855-1647-4490-bab5-9d722806904f" />

<img width="1348" height="566" alt="Faq_page_Last" src="https://github.com/user-attachments/assets/2b05772f-8b16-4f4b-9069-6ab21c54ab06" />

<img width="1343" height="645" alt="Faq_page_contact_us_page" src="https://github.com/user-attachments/assets/a92d3c18-5a5a-4c16-8143-b5b0af1a6252" />

<img width="1341" height="639" alt="FAQ+page_part_2" src="https://github.com/user-attachments/assets/f5d81947-cd99-4006-92ed-294bbb9a40db" />

<img width="1360" height="640" alt="Faq_page_middle_division" src="https://github.com/user-attachments/assets/9327441a-8c5a-4b8a-8c7c-b46133c077a4" />

<img width="1343" height="643" alt="Faq_page" src="https://github.com/user-attachments/assets/2de0662b-3a70-4ad5-a634-18cc5718171d" />

<img width="1360" height="642" alt="Url_analysis_questions" src="https://github.com/user-attachments/assets/f557fed8-66e2-4b93-b4db-7d1299107e3e" />

<img width="1353" height="644" alt="Url_analysis_response" src="https://github.com/user-attachments/assets/1d19395a-1032-4780-beaf-a5528063a115" />

<img width="1358" height="642" alt="Url_analysis_loading" src="https://github.com/user-attachments/assets/cd6f47e3-0934-4ef1-b9dc-0f1f0b3de005" />

<img width="1360" height="645" alt="LLm_response" src="https://github.com/user-attachments/assets/e7934573-cb99-474d-bc9a-f01507314c72" />
<img width="1360" height="644" alt="Document_page" src="https://github.com/user-attachments/assets/026327c9-48da-4b19-b5b8-2b947d33f7f8" />

<img width="1360" height="647" alt="Dashboard_page" src="https://github.com/user-attachments/assets/8026bb4c-e8e6-438e-8465-4f5210186408" />

<img width="1352" height="638" alt="Login_page" src="https://github.com/user-attachments/assets/2236a609-e2f1-44fd-a514-bc6fa395fd9c" />

<img width="1347" height="634" alt="Registration_page" src="https://github.com/user-attachments/assets/8863f362-20c3-4b12-9154-d18d9895bb31" />

<img width="1360" height="644" alt="Landing_page_part_3" src="https://github.com/user-attachments/assets/27e3ab45-8e25-46d4-ac40-343bff6a16e8" />

<img width="1360" height="643" alt="Landing_page_part_4" src="https://github.com/user-attachments/assets/8c1c91e4-dfcc-4e0d-89fd-0c31b0fb7afa" />


<img width="1360" height="635" alt="Landing_page_part2" src="https://github.com/user-attachments/assets/68437b4f-4498-4bee-b828-c95163ed1f42" />

<img width="1360" height="645" alt="Landing_page" src="https://github.com/user-attachments/assets/af5a6d19-6027-4862-a5a3-1278b6e46032" />



> **Complete RAG Application for Intelligent Content Analysis**
> Transform any video, document, or URL into actionable insights using advanced AI and machine learning.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-Production%20Ready-brightgreen)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)

---

## 📋 Table of Contents

- [Quick Overview](#-quick-overview)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Quick Start (5 Minutes)](#-quick-start-5-minutes)
- [Installation](#-installation)
- [Project Structure](#-project-structure)
- [API Endpoints](#-api-endpoints)
- [Database Schema](#-database-schema)
- [Bug Fixes & Updates](#-bug-fixes--updates)
- [Usage Examples](#-usage-examples)
- [Configuration](#-configuration)
- [Security](#-security)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Quick Overview

**AMAS** is a sophisticated RAG (Retrieval Augmented Generation) application that enables intelligent analysis of:

- 🎬 **YouTube Videos** - Transcribe and analyze video content
- 📄 **Documents** - Process PDF, DOCX, PPTX, TXT files
- 🔗 **URLs** - Extract and analyze web content

### **What It Does:**
1. User uploads content (URL, file, or text)
2. System extracts and processes the content
3. AI analyzes and generates summaries
4. User can ask questions about the content
5. Complete conversation history is saved
6. User can resume and continue conversations

---

## ✨ Key Features

### **🔐 Authentication & Security**
- User registration and login system
- Secure password hashing with Werkzeug
- Session-based authentication
- User ownership verification
- SQL injection prevention

### **🎯 Content Analysis**
- YouTube video transcription
- Multi-format document processing
- URL content extraction
- Automatic summary generation
- Sentiment analysis

### **💬 Conversation Management**
- Create conversations for each analysis
- Store complete Q&A history
- Resume previous conversations
- Update conversation metadata
- Soft delete functionality

### **🧠 RAG Framework**
- Retrieval Augmented Generation
- Context-aware responses
- Multi-turn conversations
- Document embeddings
- Semantic search

### **📚 Additional Features**
- FAQ/Support system
- User feedback collection
- Dashboard with statistics
- Real-time analysis
- Error handling & logging

---

## 🛠️ Tech Stack

### **Backend**
- **Framework:** Flask (Python)
- **Database:** PostgreSQL 12+
- **ORM:** SQLAlchemy (Query builder)
- **Security:** Werkzeug (Password hashing)
- **Server:** Gunicorn (Production)

### **Frontend**
- **HTML5** - Structure
- **CSS3** - Styling & responsive design
- **JavaScript** - Interactivity & API calls

### **AI & LLM**
- **Mistral AI** - Primary LLM
- **OpenAI/Claude** - Alternative LLMs
- **RAG Framework** - Retrieval system
- **Embeddings** - Vector search

### **Libraries & Tools**
| Library | Purpose |
|---------|---------|
| `python-docx` | Word document processing |
| `PyPDF2` | PDF handling |
| `openpyxl` | Excel file processing |
| `requests` | HTTP client |
| `beautifulsoup4` | Web scraping |
| `python-dotenv` | Environment management |

---

## ⚡ Quick Start (5 Minutes)

### **Prerequisites**
```bash
✅ Python 3.8+
✅ PostgreSQL 12+
✅ Git
```

### **Step 1: Clone Repository**
```bash
git clone https://github.com/yourusername/AMAS.git
cd AMAS
```

### **Step 2: Setup Virtual Environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### **Step 3: Install Dependencies**
```bash
pip install -r requirements.txt
```

### **Step 4: Setup Database**
```bash
# Create database
createdb amas

# Run schema
psql -U postgres -d amas -f database/schema.sql
```

### **Step 5: Configure Environment**
Create `.env` file:
```env
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://postgres:password@localhost:5432/amas
UPLOAD_FOLDER=uploads
MISTRAL_API_KEY=your-key
OPENAI_API_KEY=your-key
```

### **Step 6: Run Application**
```bash
python app.py
```

**✅ Done! Visit: `http://localhost:5000`**

---

## 📥 Installation (Detailed)

### **For Windows Users**

```powershell
# 1. Clone
git clone https://github.com/yourusername/AMAS.git
cd AMAS

# 2. Virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install
pip install --upgrade pip
pip install -r requirements.txt

# 4. Database (ensure PostgreSQL running)
createdb -U postgres amas
psql -U postgres -d amas -f database/schema.sql

# 5. Environment
# Create .env file with settings

# 6. Run
python app.py
```

### **For macOS/Linux Users**

```bash
# 1. Clone
git clone https://github.com/yourusername/AMAS.git
cd AMAS

# 2. Virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install
pip install --upgrade pip
pip install -r requirements.txt

# 4. Database
createdb amas
psql -U postgres -d amas -f database/schema.sql

# 5. Environment
# Create .env file with settings

# 6. Run
python app.py
```

---

## 📁 Project Structure

```
AMAS/
│
├── 📂 static/
│   ├── 📂 css/
│   │   ├── style.css
│   │   ├── dashboard.css
│   │   └── history.css
│   └── 📂 js/
│       ├── dashboard.js
│       ├── chat.js
│       ├── history.js (FIXED ✅)
│       ├── url_analysis.js
│       └── document_analysis.js
│
├── 📂 templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── url_analysis.html
│   ├── document_analysis.html
│   ├── history.html (FIXED ✅)
│   ├── conversation_view.html
│   ├── chat.html
│   └── faq.html
│
├── 📂 database/
│   ├── __init__.py
│   ├── schema.sql (6 tables)
│   └── queries.py (All DB operations)
│
├── 📂 uploads/
│   └── [User uploaded files]
│
├── 📄 app.py (FIXED ✅)
│   └── Main Flask application
│       - 15+ endpoints
│       - All authentication
│       - Analysis routes
│       - Chat management
│       - Error handling
│
├── 📄 main.py
│   └── RAG pipeline logic
│
├── 📄 config.py
│   └── Configuration settings
│
├── 📄 requirements.txt
│   └── Python dependencies (30+)
│
├── 📄 .env.example
│   └── Environment template
│
├── 📄 .gitignore
│   └── Git ignore rules
│
├── 📄 README.md
│   └── This file!
│
└── 📄 LICENSE
    └── MIT License
```

---

## 📡 API Endpoints

### **Authentication (3 endpoints)**

#### **Register User**
```http
POST /register
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword123"
}
```

#### **Login**
```http
POST /login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "securepassword123"
}
```

#### **Logout**
```http
GET /logout
```

---

### **Dashboard (1 endpoint)**

#### **Get Stats**
```http
GET /api/dashboard
Authorization: session_required

Response:
{
  "success": true,
  "stats": {
    "total_conversations": 12,
    "total_documents": 8,
    "total_urls": 4,
    "total_messages": 156
  },
  "conversations": [...]
}
```

---

### **Analysis (2 endpoints)**

#### **Analyze YouTube/URL**
```http
POST /url-analysis
Content-Type: application/json

{
  "url": "https://youtube.com/watch?v=...",
  "question": "What is this video about?",
  "translate": false
}

Response:
{
  "success": true,
  "conversation_id": 1,
  "result": "Analysis results..."
}
```

#### **Analyze Document**
```http
POST /document-analysis
Content-Type: multipart/form-data

file: [PDF/DOCX file]
question: "Summarize this document"

Response:
{
  "success": true,
  "conversation_id": 2,
  "result": "Analysis results..."
}
```

---

### **Conversations (5 endpoints)**

#### **Get All Conversations**
```http
GET /api/history
Authorization: session_required

Response:
{
  "success": true,
  "items": [
    {
      "conversation_id": 1,
      "title": "YouTube Analysis",
      "conversation_type": "URL",
      "created_at": "2024-01-15T10:30:00",
      "message_count": 5,
      "executive_summary": "...",
      "sentiment": "Positive"
    }
  ],
  "total": 1
}
```

#### **Get Conversation Messages** ✅ FIXED
```http
GET /api/conversations/<conversation_id>/messages
Authorization: session_required

Response:
{
  "success": true,
  "messages": [
    {
      "message_id": 1,
      "role": "user",
      "content": "What is this about?",
      "created_at": "2024-01-15T10:30:00"
    },
    {
      "message_id": 2,
      "role": "assistant",
      "content": "This is about...",
      "created_at": "2024-01-15T10:35:00"
    }
  ],
  "total": 2
}
```

#### **Get Conversation Details**
```http
GET /api/conversation/<conversation_id>
Authorization: session_required
```

#### **Add Message & Continue Conversation**
```http
POST /api/conversation/<conversation_id>/message
Content-Type: application/json

{
  "message": "Tell me more about that"
}
```

#### **Delete Conversation**
```http
POST /api/conversation/<conversation_id>/delete
```

---

### **FAQ (2 endpoints)**

#### **Get FAQs**
```http
GET /api/faq
```

#### **Submit FAQ**
```http
POST /api/faq/submit
Content-Type: application/json

{
  "subject": "How does this work?",
  "content": "Detailed question..."
}
```

---

## 🗄️ Database Schema

### **6 Main Tables**

#### **1. users**
```sql
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
```

#### **2. conversations**
```sql
CREATE TABLE conversations (
    conversation_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(user_id),
    conversation_type VARCHAR(20) CHECK (conversation_type IN ('URL', 'DOCUMENT')),
    title VARCHAR(255),
    description VARCHAR(500),
    is_deleted BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### **3. messages**
```sql
CREATE TABLE messages (
    message_id SERIAL PRIMARY KEY,
    conversation_id INT NOT NULL REFERENCES conversations(conversation_id),
    role VARCHAR(20) CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### **4. source_documents**
```sql
CREATE TABLE source_documents (
    source_id SERIAL PRIMARY KEY,
    conversation_id INT NOT NULL UNIQUE REFERENCES conversations(conversation_id),
    source_type VARCHAR(20) CHECK (source_type IN ('URL', 'PDF', 'DOCX', 'PPTX', 'TXT')),
    source_url VARCHAR(2048),
    file_name VARCHAR(255),
    file_path VARCHAR(500),
    file_size_bytes BIGINT,
    extracted_title VARCHAR(500),
    extracted_preview VARCHAR(1000),
    processed_content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### **5. conversation_summary**
```sql
CREATE TABLE conversation_summary (
    summary_id SERIAL PRIMARY KEY,
    conversation_id INT NOT NULL UNIQUE REFERENCES conversations(conversation_id),
    extracted_title VARCHAR(500),
    executive_summary TEXT,
    key_points TEXT,
    sentiment VARCHAR(50) CHECK (sentiment IN ('Positive', 'Neutral', 'Negative', 'Mixed')),
    total_messages INT DEFAULT 0,
    processing_time_ms INT,
    model_version VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### **6. feedback**
```sql
CREATE TABLE feedback (
    feedback_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(user_id),
    feedback_type VARCHAR(50) CHECK (feedback_type IN ('BUG', 'FEATURE_REQUEST', 'REVIEW', 'FAQ', 'GENERAL')),
    subject VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    is_resolved BOOLEAN DEFAULT false,
    admin_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🐛 Bug Fixes & Updates

### **Fix #1: History Modal Message Display** ✅

**Problem:**
- Modal only showed summary, not actual questions & answers
- Users couldn't see previous Q&A pairs

**Solution:**
- Added `/api/conversations/<id>/messages` endpoint
- Updated `history.js` to fetch and display messages
- Messages now show with role (user/assistant) and timestamp

**Files Modified:**
- `app.py` - Added new endpoint
- `static/js/history.js` - Fetch messages logic
- `templates/history.html` - Display Q&A pairs

**Result:** ✅ Users can now see complete conversation history!

---

### **Fix #2: UPDATE CRUD Operations** ✅

**Problem:**
- Database updates not committing to database
- WHERE clause issues
- No proper error handling

**Solution:**
- Added proper transaction handling
- Verified WHERE clause before update
- Implemented try/catch with rollback
- Added proper commit() calls

**Files Modified:**
- `database/queries.py` - Fixed update functions
- `app.py` - Added error handling

**Result:** ✅ All UPDATE operations work perfectly!

---

### **Fix #3: Chat Resume Functionality** ✅

**Problem:**
- Users couldn't resume previous conversations
- Message history lost

**Solution:**
- Implemented message retrieval from database
- Automatic context preservation
- Conversation metadata updates
- Session management improvements

**Result:** ✅ Users can now resume conversations seamlessly!

---

## 💡 Usage Examples

### **Example 1: Analyze YouTube Video**

```
1. Register/Login
2. Go to Dashboard
3. Click "URL Analysis"
4. Paste: https://youtube.com/watch?v=...
5. Ask: "What is this video about?"
6. Get instant analysis!
7. Ask follow-up questions
8. View in History anytime
```

### **Example 2: Analyze Document**

```
1. Go to Dashboard
2. Click "Document Analysis"
3. Upload: research.pdf
4. Ask: "Summarize this document"
5. Get key points and summary
6. Continue asking questions
7. All saved in History
```

### **Example 3: Resume Conversation**

```
1. Go to "History Center"
2. See all previous conversations
3. Click on one
4. View complete Q&A history
5. Click "Continue Conversation"
6. Add new message
7. Get response based on context
```

---

## ⚙️ Configuration

### **Environment Variables (.env)**

```env
# Flask
FLASK_ENV=development
SECRET_KEY=your-secret-key-12345
DEBUG=True

# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/amas

# File Upload
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=52428800  # 50MB

# AI APIs
MISTRAL_API_KEY=your-mistral-key
OPENAI_API_KEY=your-openai-key
```

### **Database Configuration**

| Setting | Value |
|---------|-------|
| Host | localhost |
| Port | 5432 |
| Database | amas |
| User | postgres |
| Password | your-password |

---

## 🔒 Security

### **Authentication**
- ✅ Secure password hashing (Werkzeug)
- ✅ Session-based authentication
- ✅ User verification on every request
- ✅ CSRF protection ready

### **Database**
- ✅ Parameterized queries (SQL injection prevention)
- ✅ User ownership verification
- ✅ Soft deletes (data retention)
- ✅ Indexes for performance

### **File Handling**
- ✅ Filename sanitization
- ✅ Size validation
- ✅ Type checking
- ✅ Secure upload path

### **Best Practices**
- ✅ Error messages don't leak info
- ✅ Rate limiting ready
- ✅ HTTPS ready
- ✅ Environment separation

---

## 🤝 Contributing

### **Ways to Contribute**
- Report bugs
- Suggest features
- Write code
- Improve documentation
- Fix typos
- Add tests

### **Process**
1. Fork repository
2. Create feature branch: `git checkout -b feature/amazing`
3. Commit changes: `git commit -m "feat: add amazing feature"`
4. Push branch: `git push origin feature/amazing`
5. Open Pull Request

### **Code Style**
- Follow PEP 8
- Add docstrings
- Write comments for complex logic
- Test your changes

---

## 📊 Project Statistics

| Metric | Count |
|--------|-------|
| **Backend Endpoints** | 15+ |
| **Database Tables** | 6 |
| **Lines of Code** | 2500+ |
| **Documentation** | 8000+ words |
| **Supported File Types** | 5+ |
| **API Methods** | GET, POST, DELETE |

---

## 🚀 Deployment

### **Production Checklist**
- [ ] Set `FLASK_ENV=production`
- [ ] Configure secure `SECRET_KEY`
- [ ] Setup PostgreSQL with backups
- [ ] Add API keys
- [ ] Enable HTTPS
- [ ] Configure allowed hosts
- [ ] Setup logging
- [ ] Enable error monitoring
- [ ] Configure CDN for static files
- [ ] Test all endpoints

### **Cloud Deployment Options**
- Heroku
- AWS EC2
- Google Cloud Run
- DigitalOcean
- Azure App Service

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | This file (complete guide) |
| `CONTRIBUTING.md` | Developer guidelines |
| `API_DOCUMENTATION.md` | Detailed API reference |
| `QUICKSTART.md` | 5-minute setup guide |
| `PROJECT_SUMMARY.md` | Architecture overview |

---

## 🎓 Learning Resources

- **Flask:** https://flask.palletsprojects.com
- **PostgreSQL:** https://postgresql.org/docs
- **Python:** https://python.org/docs
- **RAG:** https://www.youtube.com/results?search_query=retrieval+augmented+generation
- **LLMs:** https://openai.com/research

---

## 📈 Roadmap

### **v1.0.0** ✅ (Current)
- Core features implemented
- Database schema complete
- API endpoints working
- Documentation complete

### **v1.1.0** (Planned)
- WebSocket support for real-time chat
- Advanced filtering
- Bulk operations
- Export functionality

### **v2.0.0** (Future)
- Mobile app
- Multi-language support
- Team collaboration
- Custom AI model training

---

## 📞 Support

| Channel | Link |
|---------|------|
| **GitHub Issues** | [Report bugs](https://github.com/yourusername/AMAS/issues) |
| **Discussions** | [Ask questions](https://github.com/yourusername/AMAS/discussions) |
| **Email** | support@amas-ai.com |
| **Documentation** | [Docs](README.md) |

---

## 📄 License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 AMAS Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software...
```

---

## 🙏 Acknowledgments

- Built with ❤️ using Flask and PostgreSQL
- AI powered by Mistral AI and OpenAI
- Thanks to all contributors and users
- Open source community support

---

## ⭐ Show Your Support

If this project helped you, please consider:
- ⭐ Starring the repository
- 🔗 Sharing with others
- 💬 Giving feedback
- 🤝 Contributing code

---

## 📅 Changelog

### **v1.0.0** (January 2024)
- ✅ Initial release
- ✅ All core features
- ✅ Complete documentation
- ✅ Bug fixes #1, #2, #3
- ✅ Production ready

---

## 🎉 Ready to Get Started?

1. **Clone:** `git clone https://github.com/yourusername/AMAS.git`
2. **Setup:** Follow the [Quick Start](#-quick-start-5-minutes) section
3. **Explore:** Check out the [API Endpoints](#-api-endpoints) section
4. **Contribute:** Read [Contributing](#-contributing) guidelines
5. **Support:** Open an issue if you have questions

---

**Made with ❤️ by AMAS Team**

⭐ If you find this helpful, please star the repository! 🌟

---

**Last Updated:** January 2024  
**Version:** 1.0.0  
**Status:** ✅ Production Ready  
**License:** MIT
