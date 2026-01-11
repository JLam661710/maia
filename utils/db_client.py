
import os
import json
from dotenv import load_dotenv
from supabase import create_client, Client

# Load env vars immediately
load_dotenv()
from datetime import datetime

class DBClient:
    def __init__(self):
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        
        if not url or not key:
            print("⚠️ Supabase credentials missing. DB operations will be skipped.")
            self.client = None
        else:
            try:
                self.client: Client = create_client(url, key)
            except Exception as e:
                print(f"❌ Failed to connect to Supabase: {e}")
                self.client = None

    # ==========================================
    # Auth Methods
    # ==========================================
    def sign_up(self, email, password, nickname):
        """Registers a new user."""
        if not self.client: return None, "DB Not Connected"
        try:
            res = self.client.auth.sign_up({
                "email": email, 
                "password": password,
                "options": {
                    "data": {"nickname": nickname}
                }
            })
            return res.user, None
        except Exception as e:
            return None, str(e)

    def sign_in(self, email, password):
        """Logs in an existing user."""
        if not self.client: return None, "DB Not Connected"
        try:
            res = self.client.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            return res.user, None
        except Exception as e:
            return None, str(e)
            
    def sign_out(self):
        """Logs out."""
        if self.client:
            self.client.auth.sign_out()

    # ==========================================
    # Session Methods
    # ==========================================
    def create_session(self, user_id=None):
        """Creates a new session. user_id is Optional (None for Guest)."""
        if not self.client: return None
        try:
            data = self.client.table("sessions").insert({
                "user_id": user_id, # Can be None
                "status": "In Progress"
            }).execute()
            if data.data:
                return data.data[0]['id']
        except Exception as e:
            print(f"Error creating session: {e}")
        return None

    def get_user_sessions(self, user_id):
        """Fetches all sessions for a logged-in user."""
        if not self.client or not user_id: return []
        try:
            # Order by newest first
            res = self.client.table("sessions").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()
            return res.data
        except Exception as e:
            print(f"Error fetching sessions: {e}")
            return []

    def load_session_history(self, session_id):
        """Loads messages and state for a specific session."""
        if not self.client or not session_id: return [], {}
        
        messages = []
        json_state = {}
        
        try:
            # 1. Get Messages
            msg_res = self.client.table("messages").select("*").eq("session_id", session_id).order("created_at").execute()
            messages = msg_res.data
            
            # 2. Get Latest State
            state_res = self.client.table("analysis_states").select("*").eq("session_id", session_id).order("updated_at", desc=True).limit(1).execute()
            if state_res.data:
                json_state = state_res.data[0].get("json_state", {})
                
        except Exception as e:
            print(f"Error loading history: {e}")
            
        return messages, json_state

    # ==========================================
    # Data Saving Methods
    # ==========================================
    def save_message(self, session_id, role, content):
        if not self.client or not session_id: return
        try:
            self.client.table("messages").insert({
                "session_id": session_id,
                "role": role,
                "content": content
            }).execute()
        except Exception as e:
            print(f"Error saving message: {e}")

    def update_analysis_state(self, session_id, json_state, system_notice):
        if not self.client or not session_id: return
        try:
            self.client.table("analysis_states").insert({
                "session_id": session_id,
                "json_state": json_state,
                "system_notice": system_notice
            }).execute()
        except Exception as e:
            print(f"Error updating analysis state: {e}")

    def save_deliverable(self, session_id, content):
        if not self.client or not session_id: return
        try:
            self.client.table("deliverables").insert({
                "session_id": session_id,
                "content": content
            }).execute()
        except Exception as e:
            print(f"Error saving deliverable: {e}")
    
    def update_session_status(self, session_id, status, summary=None, archived_count=None):
        if not self.client or not session_id: return
        try:
            update_data = {"status": status}
            if summary is not None:
                update_data["conversation_summary"] = summary
            if archived_count is not None:
                update_data["archived_count"] = archived_count
                
            self.client.table("sessions").update(update_data).eq("id", session_id).execute()
        except Exception as e:
            print(f"Error updating session status: {e}")

# Global instance
db_client = DBClient()
