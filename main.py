import sys
from dotenv import load_dotenv

from utils.audio_proccessor import process_input
from core.summarize import summarize, generate_title
from core.transcriber import transcribe_all
from core.extractor import (
    extract_action_items,
    extract_key_decisions,
    extract_questions
)
from core.rag_engine import build_rag_chain, ask_question
from core.External_Docs import answer_question
from core.External_vector import build_vector_store

load_dotenv()


def print_banner():
    print("""\033[36m
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║          🤖  AI  ASSISTANT  —  VIDEO  &  DOCS  🤖        ║
║                                                          ║
║   Web-ready backend for URL + Document RAG pipelines     ║
║                                                          ║
║           Powered by Whisper + Mistral AI                ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
\033[0m""")


# -------------------------
# Video Pipeline
# -------------------------
def run_video_pipeline(source: str, question: str, translate: bool = False):
    """
    Web-ready video/URL pipeline.

    Args:
        source: YouTube URL or video file path
        question: User's question about the video
        translate: Whether to translate transcript to English

    Returns:
        dict containing title, transcript preview, summary, extracted items, and answer
    """
    chunks = process_input(source)
    transcript = transcribe_all(chunks, translate=translate)

    title = generate_title(transcript)
    summary = summarize(transcript)
    action_items = extract_action_items(transcript)
    decisions = extract_key_decisions(transcript)
    questions = extract_questions(transcript)

    rag_chain = build_rag_chain(transcript)
    answer = ask_question(rag_chain, question)

    return {
        "title": title,
        "transcript_preview": transcript[:300],
        "summary": summary,
        "action_items": action_items,
        "key_decisions": decisions,
        "open_questions": questions,
        "answer": answer,
    }


# -------------------------
# Document Pipeline
# -------------------------
def run_document_pipeline(file_path: str, question: str):

    vector_store = build_vector_store(file_path)

    answer = answer_question(vector_store, question)

    return {
        "answer": answer
    }


# -------------------------
# Optional CLI testing
# -------------------------
if __name__ == "__main__":
    print_banner()

    print("What would you like to do?")
    print("  1. Process a Video / YouTube URL")
    print("  2. Ask questions from a Document")
    choice = input("\nEnter choice (1 or 2): ").strip()

    if choice == "1":
        source = input("Enter video file path or YouTube URL: ").strip()
        translate_input = input("Translate to English? (y/n): ").strip().lower()
        translate = True if translate_input == "y" else False
        question = input("Enter your question: ").strip()

        result = run_video_pipeline(source, question, translate=translate)

        print("\n" + "=" * 60)
        print("TITLE")
        print("=" * 60)
        print(result["title"])

        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print(result["summary"])

        print("\n" + "=" * 60)
        print("ANSWER")
        print("=" * 60)
        print(result["answer"])

    elif choice == "2":
        file_path = input("Enter document path (PDF/Word/Text/PowerPoint): ").strip().strip('"')
        question = input("Enter your question: ").strip()

        result = run_document_pipeline(file_path, question)

        print("\n" + "=" * 60)
        print("ANSWER")
        print("=" * 60)
        print(result["answer"])

    else:
        print("Invalid choice. Please enter 1 or 2.")