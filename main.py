import os
from dotenv import load_dotenv

# Wajib load_dotenv paling atas agar API Key tersedia untuk modul lain
load_dotenv()

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

# Import komponen yang sudah dipisah
from src.state.state import State
from src.tools import all_tools
from src.nodes.agent_node import call_model

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.text import Text
from rich import box

# 1. Setup Nodes
tool_node = ToolNode(all_tools)

# 2. Build Graph
workflow = StateGraph(State)

workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

workflow.set_entry_point("agent")

# 3. Conditional Logic
def should_continue(state: State):
    last_message = state['messages'][-1]
    if last_message.tool_calls:
        return "tools"
    return END

workflow.add_conditional_edges("agent", should_continue)
workflow.add_edge("tools", "agent")

# Compile Aplikasi
app = workflow.compile()

console = Console()

# TARUH ASCII ART KAMU DI SINI
# Gunakan r""" agar karakter backslash (\) tidak error
LOGO_ASCII = r"""
  ____             _        
 | __ )  __ _  ___| |___    
 |  _ \ / _` |/ _ \ / __|   
 | |_) | (_| |  __/ \__ \   
 |____/ \__,_|\___|_|___/   
"""

def display_welcome():
    console.clear()
    
    # Menyiapkan konten di dalam kotak
    welcome_content = Text(justify="center")
    
    # Baris 1: ASCII ART
    welcome_content.append(LOGO_ASCII, style="bold cyan")
    
    # Baris 2: Nama & Versi
    welcome_content.append("\nBaals_Agent", style="bold cyan" )
    welcome_content.append(" v1.0.0\n", style="white dim")
    
    # Baris 3: Credit
    welcome_content.append("developed by Iqbal", style="white dim")

    # Panel Utama dengan garis putus-putus (dashed)
    console.print(Panel(
        welcome_content,
        box=box.ASCII2, 
        border_style="blue",
        title="[bold white]System Active[/bold white]",
        title_align="center",
        padding=(1, 2),
        expand=False
    ))
    console.print("[dim]Ketik 'exit' untuk keluar atau 'clear' untuk reset layar.[/dim]\n")

chat_history = []
if __name__ == "__main__":
    display_welcome()
    
    while True:
        try:
            # Input Prompt profesional
            user_input = Prompt.ask("[bold green]Baal[/bold green]")

            if user_input.lower() in ["exit", "quit", "keluar"]:
                console.print("[yellow]Shutting down... Sampai jumpa, Iqbal![/yellow]")
                break
            
            if user_input.lower() == "clear":
                chat_history=[]
                display_welcome()
                continue

            chat_history.append(("user", user_input))

            if not user_input.strip():
                continue

            # Spinner/Loading Animation
            with console.status("[bold blue]Baals_Agent sedang berpikir...", spinner="dots"):
                events = app.stream(
                    {"messages": chat_history},
                    stream_mode="values"
                )
                
                final_event = None
                for event in events:
                    final_event = event
                    

            if final_event and "messages" in final_event:
                last_message = final_event["messages"][-1]
                
                if hasattr(last_message, "type") and last_message.type == "ai" and last_message.content:
                    # 5. SIMPAN respon AI ke dalam riwayat agar dia ingat apa yang dia katakan sendiri
                    chat_history.append(("ai", last_message.content))
                    # Render Response dalam Panel Markdown
                    console.print(Panel(
                        Markdown(last_message.content),
                        title="[bold blue]Agent Response[/bold blue]",
                        box=box.ASCII2, 
                        title_align="left",
                        border_style="blue",
                        padding=(1, 2)
                    ))
                    print() # Spasi antar chat

        except Exception as e:
            console.print(f"[bold red]System Error:[/bold red] {e}")
            continue