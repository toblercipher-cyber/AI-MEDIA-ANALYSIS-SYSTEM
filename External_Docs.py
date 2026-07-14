import os
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel
from core.External_vector import build_vector_store, get_retriever

load_dotenv()

# -------------------------
# LLM
# -------------------------
llm = ChatMistralAI(
    model="open-mistral-7b",
    mistral_api_key=os.getenv("MISTRAL_API_KEY")
)

# -------------------------
# Parallel Runnable One — Brief Introduction (1–4 lines)
# -------------------------
intro_prompt = ChatPromptTemplate.from_messages([
    ("system",
     """You are a helpful assistant.
Based on the context provided, give a brief introduction to the topic in 1 to 4 lines only.
Do not go beyond 4 lines. Answer ONLY from the context."""),
    ("human", "Context:\n{context}\n\nQuestion:\n{question}")
])

intro_chain = intro_prompt | llm | StrOutputParser()

# -------------------------
# Parallel Runnable Two — Bullet Points + Summary
# -------------------------
detail_prompt = ChatPromptTemplate.from_messages([
    ("system",
     """You are a helpful assistant.
- Explain each topic from the context in clear bullet points.
- After the bullet points, provide a short summary of the topic.
Answer ONLY from the provided context.
If the answer is not available, say: 'I could not find any relevant information.'"""),
    ("human", "Context:\n{context}\n\nQuestion:\n{question}")
])

detail_chain = detail_prompt | llm | StrOutputParser()

# -------------------------
# Parallel Runnable
# -------------------------
parallel_chain = RunnableParallel(
    introduction=intro_chain,
    detailed_response=detail_chain
)

# -------------------------
# Answer Question
# -------------------------
def answer_question(vector_store, question: str):
    retriever = get_retriever(vector_store)
    relevant_chunks = retriever.invoke(question)

    context = "\n\n".join(
        [c.page_content for c in relevant_chunks]
    )

    result = parallel_chain.invoke({
        "context": context,
        "question": question
    })

    return {
        "introduction": result["introduction"],
        "detailed_response": result["detailed_response"]
    }

# -------------------------
# Banner
# -------------------------
def print_banner():
    print("""\033[36m
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║         📄  DOCUMENT  RAG  ASSISTANT  📄                 ║
║                                                          ║
║     Supports: PDF • Word • Text • PowerPoint             ║
║                                                          ║
║              Powered by Mistral AI                       ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
\033[0m""")

# -------------------------
# Main
# -------------------------
if __name__ == "__main__":
    print_banner()

    file_path = input("Enter document path: ").strip().strip('"')

    print("\nLoading and building vector store...")
    vector_store = build_vector_store(file_path)
    print("Document ready!\n")

    print("=" * 60)
    print("ASK QUESTIONS ABOUT YOUR DOCUMENT (type 'exit' to quit)")
    print("=" * 60)

    while True:
        question = input("\nYour Question: ").strip()
        if question.lower() in ["exit", "quit", "q"]:
            print("Goodbye!")
            break
        if not question:
            continue
        answer_question(vector_store, question)