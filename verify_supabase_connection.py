
import os
import sys
from dotenv import load_dotenv
from supabase import create_client, Client

# Load Env
load_dotenv(override=True)

def verify_connection():
    print("="*50)
    print("🔍 VERIFYING SUPABASE CONNECTION")
    print("="*50)
    
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    # 1. Check Env Vars
    if not url or "your_supabase_project_url" in url:
        print("❌ Error: SUPABASE_URL is not configured in .env")
        return False
    if not key or "your_supabase_anon_key" in key:
        print("❌ Error: SUPABASE_KEY is not configured in .env")
        return False
        
    print(f"✅ Credentials found.")
    print(f"   URL: {url[:20]}...")
    
    # 2. Connect
    try:
        supabase: Client = create_client(url, key)
        print("✅ Client initialized.")
    except Exception as e:
        print(f"❌ Client initialization failed: {e}")
        return False
        
    # 3. Test Read (Public Table)
    print("\n[Test 1] Reading 'sessions' table...")
    try:
        res = supabase.table("sessions").select("*").limit(1).execute()
        print("✅ Read successful.")
    except Exception as e:
        print(f"❌ Read failed. Did you run the SQL script? Error: {e}")
        return False

    # 4. Test Write (Guest Session)
    print("\n[Test 2] Writing test session...")
    try:
        data = supabase.table("sessions").insert({
            "status": "Connection Test",
            "user_id": None
        }).execute()
        
        if data.data:
            sid = data.data[0]['id']
            print(f"✅ Write successful. Test Session ID: {sid}")
            
            # Cleanup
            print("   Cleaning up test data...")
            supabase.table("sessions").delete().eq("id", sid).execute()
            print("   Cleanup done.")
        else:
            print("❌ Write returned no data.")
            return False
    except Exception as e:
        print(f"❌ Write failed. Error: {e}")
        return False
        
    print("\n" + "="*50)
    print("🎉 SUCCESS! SUPABASE IS READY.")
    print("="*50)
    return True

if __name__ == "__main__":
    verify_connection()
