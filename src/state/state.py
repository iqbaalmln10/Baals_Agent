from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages

class State(TypedDict):
    # add_messages bertugas menggabungkan pesan baru ke pesan lama secara otomatis
    messages: Annotated[list, add_messages]