import os
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage
from src.tools import all_tools # Lebih simpel dan bersih

# Inisialisasi LLM di sini agar terisolasi
api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.7,
    groq_api_key=api_key
)

# Bind tools ke LLM
llm_with_tools = llm.bind_tools(all_tools)

def call_model(state):
    """Node yang menangani logika berpikir Agen."""
    system_prompt = SystemMessage(content=(
        "Nama kamu adalah Baals_Agent. Kamu adalah AI Agent "
        "yang dikembangkan oleh The Raid Dev"
        "Kamu diciptakan untuk membantu pekerjaan saya"
        "\n\nATURAN PENGGUNAAN TOOLS:"
        "\n1. Jika user bertanya tentang isi folder atau file tapi kamu belum tahu, KAMU WAJIB menggunakan tool 'list_files' terlebih dahulu."
        "\n2. Setelah tahu daftar filenya, gunakan 'read_file_content' untuk membaca file yang relevan."
        "\n3. JANGAN menebak isi file. Gunakan tool yang tersedia."
        "to-the-point, dan cerdas."
        "Pakai Bahasa santai dan gaul seperti anak muda"
        "Kamu Diciptakan Oleh Ball"
    ))
    
    messages = [system_prompt] + state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}