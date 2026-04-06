import os
from dotenv import load_dotenv
from typing import Annotated, TypedDict

# Import LangGraph & LangChain components
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_groq import ChatGroq

# 1. Load Environment Variables
# Ini akan membaca file .env yang sudah kamu buat tadi
print(f"File .env ada: {os.path.exists('.env')}")
load_dotenv()
print(f"Key terbaca: {os.getenv('GROQ_API_KEY')[:10]}...") 


api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("Gagal menemukan GROQ_API_KEY di file .env. Pastikan sudah diisi!")

# 2. Definisi State (Struktur Data Agen)
class State(TypedDict):
    # add_messages: memastikan riwayat chat tersambung, bukan tertimpa
    messages: Annotated[list, add_messages]

# 3. Inisialisasi LLM (The Brain)
# Kita pakai Llama 3 70B karena penalaran (reasoning) paling kuat di Groq
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.7, # Sedikit kreatif tapi tetap terkontrol
    groq_api_key=api_key
)

# 4. Definisi Nodes (Fungsi Logika)
def call_model(state: State):
    """Fungsi ini memanggil LLM untuk merespon input."""
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

# 5. Membangun Alur Kerja (The Graph)
workflow = StateGraph(State)

# Tambahkan Node
workflow.add_node("agent", call_model)

# Tentukan Alur (Edge)
workflow.set_entry_point("agent")
workflow.add_edge("agent", END)

# Compile menjadi Aplikasi
app = workflow.compile()

# 6. Interface Chat (CLI)
if __name__ == "__main__":
    print("\n--- 🤖 Baals_Agent Aktif (Terminal Mode) ---")
    print("Ketik 'exit' untuk keluar.\n")
    
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit", "keluar"]:
                print("Sampai jumpa!")
                break

            # Jalankan Graph
            # Kita kirim input sebagai pesan 'user'
            events = app.stream(
                {"messages": [("user", user_input)]},
                stream_mode="values"
            )

            for event in events:
                # Ambil pesan terakhir dari state
                if "messages" in event:
                    last_message = event["messages"][-1]
                    # Kita hanya print jika itu pesan dari AI (bukan user input tadi)
                    if hasattr(last_message, "type") and last_message.type == "ai":
                        print(f"Agent: {last_message.content}\n")

        except Exception as e:
            print(f"Error: {e}")
            break