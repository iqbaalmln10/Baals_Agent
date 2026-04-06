import os
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage
from src.tools.time_tool import tools # Import list tools

# Inisialisasi LLM di sini agar terisolasi
api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.7,
    groq_api_key=api_key
)

# Bind tools ke LLM
llm_with_tools = llm.bind_tools(tools)

def call_model(state):
    """Node yang menangani logika berpikir Agen."""
    system_prompt = SystemMessage(content=(
        "Nama kamu adalah Baals_Agent. Kamu adalah AI Agent "
        "yang dikembangkan oleh The Raid Dev"
        "Kamu diciptakan untuk membantu pekerjaan saya"
        "to-the-point, dan cerdas."
        "Pakai Bahasa santai dan gaul seperti anak muda"
        "Nama Pengembangmu Adalah Ball"
    ))
    
    messages = [system_prompt] + state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}