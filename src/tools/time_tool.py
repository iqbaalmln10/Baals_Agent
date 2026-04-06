import datetime
from langchain_core.tools import tool

@tool
def get_system_time():
    """Gunakan ini untuk mengetahui waktu dan tanggal sistem saat ini."""
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

# List ini akan memudahkan kita saat melakukan binding di node
tools = [get_system_time]