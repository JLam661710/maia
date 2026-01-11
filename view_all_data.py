
import os
import json
from dotenv import load_dotenv
from supabase import create_client, Client
from rich.console import Console
from rich.table import Table

# Load env vars
load_dotenv()

console = Console()

def view_data():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        console.print("[bold red]❌ Error: SUPABASE_URL or SUPABASE_KEY missing in .env[/bold red]")
        return

    try:
        supabase: Client = create_client(url, key)
        
        console.print("\n[bold cyan]🔍 SUPABASE DATA VIEWER (Admin)[/bold cyan]")
        console.print("Fetching latest data...\n")

        # 1. Sessions Table
        console.print("[bold yellow]1. Latest Sessions (Top 5)[/bold yellow]")
        sessions = supabase.table("sessions").select("*").order("created_at", desc=True).limit(5).execute()
        
        if sessions.data:
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("ID", style="dim", width=12)
            table.add_column("User ID", width=12)
            table.add_column("Status")
            table.add_column("Created At")
            table.add_column("Summary (Truncated)")
            
            for s in sessions.data:
                summ = s.get('conversation_summary', '') or ''
                user_id = s.get('user_id') or "GUEST"
                table.add_row(
                    str(s['id'])[:8] + "...",
                    str(user_id)[:8] + "..." if user_id != "GUEST" else "GUEST",
                    s.get('status'),
                    s['created_at'][:16],
                    summ[:30] + "..." if len(summ) > 30 else summ
                )
            console.print(table)
        else:
            console.print("[italic]No sessions found.[/italic]")

        # 2. Messages Table
        console.print("\n[bold yellow]2. Latest Messages (Top 5)[/bold yellow]")
        msgs = supabase.table("messages").select("*").order("created_at", desc=True).limit(5).execute()
        
        if msgs.data:
            table = Table(show_header=True, header_style="bold green")
            table.add_column("Session ID", style="dim", width=12)
            table.add_column("Role", style="bold")
            table.add_column("Content (Truncated)")
            table.add_column("Time")
            
            for m in msgs.data:
                content = m.get('content', '') or ''
                table.add_row(
                    str(m['session_id'])[:8] + "...",
                    m['role'],
                    content[:50].replace("\n", " ") + "..." if len(content) > 50 else content,
                    m['created_at'][11:19]
                )
            console.print(table)
        else:
            console.print("[italic]No messages found.[/italic]")

    except Exception as e:
        console.print(f"[bold red]❌ Error fetching data: {e}[/bold red]")

if __name__ == "__main__":
    view_data()
