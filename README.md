# HR Leave Manager & Client Meeting Scheduler (MCP-Powered)

This project implements a robust **HR Leave Management System** and **Client Meeting Scheduler** using `FastMCP`, the Python framework for building context-aware LLM-powered applications. It includes dynamic tools, prompt handling, and resources for interacting with a mock employee database.

---

## 🚀 Features

### ✅ Leave Management Tools
- `submit_leave_request`: Submit a new leave request
- `approve_leave_request`: Manager approval workflow
- `get_leave_balance`: View remaining leave days
- `list_leave_requests`: See pending/approved requests
- `cancel_leave_request`: Withdraw pending requests

### ✅ Meeting Scheduler Tools
- `schedule_client_meeting`: Book client meetings
- `get_available_slots`: Check open time slots
- `list_upcoming_meetings`: View scheduled meetings
- `cancel_meeting`: Cancel or reschedule
- `send_meeting_invite`: Email invitation handler

### ✅ Shared Utility Tools
- `get_employee_info`: Lookup employee data
- `generate_report`: Get summary of leave & meetings

---

## 🛠 Installation Guide

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/hr-meeting-mcp.git
   cd hr-meeting-mcp
   ```

2. **Set Up a Virtual Environment (Optional but Recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Server**

   ```bash
   python main.py
   ```

   This will start the MCP server and register all tools and resources.

---

## 🧪 Testing (Optional)

You can test tool functionality using the MCP-compatible client or build a FastAPI/CLI layer to call tools interactively.

---

## 📦 Requirements

Below is the `requirements.txt`:

```
fastapi
uvicorn
mcp
```

You can install them via:

```bash
pip install -r requirements.txt
```

---

## 🤝 License

MIT License – Use freely with attribution.

---

## 🙋‍♂️ Support or Contributions

Feel free to open an issue or pull request. For feature requests or integration help, reach out to [pratikguharoystads@gmail.com](mailto:pratikguharoystads@gmail.com).

```