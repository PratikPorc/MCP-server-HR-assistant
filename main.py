from mcp.server.fastmcp import FastMCP 

# Create the MCP server
mcp = FastMCP("HR_Leave_Meeting_Manager")

# --------------------
# Mock Databases
# --------------------
employees = {
    "e001": {"name": "Alice", "role": "Manager", "leave_balance": 12},
    "e002": {"name": "Bob", "role": "Developer", "leave_balance": 8},
    "e003": {"name": "Charlie", "role": "Sales Executive", "leave_balance": 10},
    "e004": {"name": "Diana", "role": "HR Associate", "leave_balance": 15},
    "e005": {"name": "Ethan", "role": "DevOps Engineer", "leave_balance": 7},
    "e006": {"name": "Fiona", "role": "QA Tester", "leave_balance": 9},
    "e007": {"name": "George", "role": "Business Analyst", "leave_balance": 11},
    "e008": {"name": "Hannah", "role": "Content Writer", "leave_balance": 13},
    "e009": {"name": "Ivan", "role": "Finance Manager", "leave_balance": 6},
    "e010": {"name": "Jasmine", "role": "UI/UX Designer", "leave_balance": 12},
    "e011": {"name": "Kunal", "role": "Intern", "leave_balance": 5},
    "e012": {"name": "Lara", "role": "Tech Support", "leave_balance": 14},
}

leave_requests = []
meetings = []

# --------------------
# Leave Management Tools
# --------------------

@mcp.tool()
def submit_leave_request(emp_id: str, days: int, reason: str) -> str:
    """Create new leave requests"""
    if emp_id not in employees:
        return "Employee not found."
    if employees[emp_id]['leave_balance'] < days:
        return "Insufficient leave balance."
    
    leave_id = f"L{len(leave_requests) + 1:03d}"
    leave_requests.append({
        "leave_id": leave_id,
        "emp_id": emp_id,
        "days": days,
        "reason": reason,
        "status": "Pending"
    })
    return f"Leave request {leave_id} submitted successfully."

@mcp.tool()
def approve_leave_request(leave_id: str, manager_id: str) -> str:
    """Manager approval workflow"""
    for leave in leave_requests:
        if leave["leave_id"] == leave_id and leave["status"] == "Pending":
            leave["status"] = "Approved"
            employees[leave["emp_id"]]["leave_balance"] -= leave["days"]
            return f"Leave request {leave_id} approved by {manager_id}."
    return "Leave request not found or already processed."

@mcp.tool()
def get_leave_balance(emp_id: str) -> str:
    """Check remaining days"""
    if emp_id in employees:
        return f"{employees[emp_id]['name']} has {employees[emp_id]['leave_balance']} leave days remaining."
    return "Employee not found."

@mcp.tool()
def list_leave_requests(emp_id: str = None, status: str = None) -> list:
    """View pending/approved requests"""
    results = leave_requests
    if emp_id:
        results = [r for r in results if r["emp_id"] == emp_id]
    if status:
        results = [r for r in results if r["status"].lower() == status.lower()]
    return results

@mcp.tool()
def cancel_leave_request(leave_id: str) -> str:
    """Cancel existing requests"""
    for leave in leave_requests:
        if leave["leave_id"] == leave_id:
            if leave["status"] == "Pending":
                leave["status"] = "Cancelled"
                return f"Leave request {leave_id} cancelled."
            return "Cannot cancel a processed leave request."
    return "Leave request not found."


# --------------------
# Meeting Scheduler Tools
# --------------------

@mcp.tool()
def schedule_client_meeting(emp_id: str, date: str, time: str, client: str) -> str:
    """Create new meetings"""
    meeting_id = f"M{len(meetings) + 1:03d}"
    meetings.append({
        "meeting_id": meeting_id,
        "emp_id": emp_id,
        "date": date,
        "time": time,
        "client": client,
        "status": "Scheduled"
    })
    return f"Meeting {meeting_id} scheduled with {client} on {date} at {time}."

@mcp.tool()
def get_available_slots(emp_id: str, date: str) -> list:
    """Check calendar availability"""
    booked = [m['time'] for m in meetings if m['emp_id'] == emp_id and m['date'] == date and m['status'] == "Scheduled"]
    all_slots = [f"{hour}:00" for hour in range(9, 18)]
    return [slot for slot in all_slots if slot not in booked]

@mcp.tool()
def list_upcoming_meetings(emp_id: str) -> list:
    """View scheduled meetings"""
    return [m for m in meetings if m["emp_id"] == emp_id and m["status"] == "Scheduled"]

@mcp.tool()
def cancel_meeting(meeting_id: str) -> str:
    """Cancel/reschedule meetings"""
    for meeting in meetings:
        if meeting["meeting_id"] == meeting_id:
            meeting["status"] = "Cancelled"
            return f"Meeting {meeting_id} cancelled."
    return "Meeting not found."

@mcp.tool()
def send_meeting_invite(meeting_id: str, email: str) -> str:
    """Email invitations"""
    for meeting in meetings:
        if meeting["meeting_id"] == meeting_id:
            return f"Invite sent to {email} for meeting {meeting_id} with {meeting['client']}."
    return "Meeting not found."


# --------------------
# Shared / Utility Tools
# --------------------

@mcp.tool()
def get_employee_info(emp_id: str) -> dict:
    """Shared employee data"""
    return employees.get(emp_id, {"error": "Employee not found."})

@mcp.tool()
def generate_report(emp_id: str = None) -> dict:
    """Combined reporting"""
    report = {
        "total_leave_requests": len([r for r in leave_requests if not emp_id or r["emp_id"] == emp_id]),
        "upcoming_meetings": len([m for m in meetings if not emp_id or m["emp_id"] == emp_id and m["status"] == "Scheduled"]),
    }
    return report


# --------------------
# Dynamic Resources & Prompts
# --------------------

@mcp.resource("employee://{emp_id}")
def employee_resource(emp_id: str) -> str:
    """Dynamic employee greeting"""
    emp = employees.get(emp_id)
    return f"Hello, {emp['name']}!" if emp else "Employee not found."


@mcp.prompt()
def leave_summary_prompt(emp_id: str) -> str:
    """Prompt for summarizing leave"""
    emp = employees.get(emp_id)
    if not emp:
        return "Employee not found."
    balance = emp['leave_balance']
    return f"Please summarize the leave record for {emp['name']} who has {balance} days remaining."

if __name__ == "__main__":
    mcp.run()