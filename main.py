import os
from dotenv import load_dotenv

# Wajib load_dotenv paling atas agar API Key tersedia untuk modul lain
load_dotenv()

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

# Import komponen yang sudah dipisah
from src.state.state import State
from src.tools.time_tool import tools
from src.nodes.agent_node import call_model

# 1. Setup Nodes
tool_node = ToolNode(tools)

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

# 4. Interface Chat (CLI)
if __name__ == "__main__":
    print("\n--- 🤖 Baals_Agent Mu Aktif ---")
    print("Ketik 'exit' untuk keluar.\n")
    
    while True:
        try:
            user_input = input("Baal: ")
            if user_input.lower() in ["exit", "quit", "keluar"]:
                break

            events = app.stream(
                {"messages": [("user", user_input)]},
                stream_mode="values"
            )

            for event in events:
                if "messages" in event:
                    last_message = event["messages"][-1]
                    if hasattr(last_message, "type") and last_message.type == "ai" and last_message.content:
                        print(f"Agent: {last_message.content}\n")

        except Exception as e:
            print(f"Error: {e}")
            break