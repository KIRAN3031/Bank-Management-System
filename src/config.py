# src/config.py
import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load .env only for local dev
load_dotenv()

def _read_supabase_creds():
    # Prefer Streamlit secrets in Cloud; fall back to env for local dev
    try:
        import streamlit as st
        url = st.secrets.get("SUPABASE_URL", None)
        key = st.secrets.get("SUPABASE_KEY", None)
    except Exception:
        url = None
        key = None

    if not url:
        url = os.getenv("SUPABASE_URL")
    if not key:
        key = os.getenv("SUPABASE_KEY")
    return (url.strip() if url else None, key.strip() if key else None)

def get_supabase() -> Client:
    url, key = _read_supabase_creds()
    if not url or not key:
        # Log booleans for diagnostics without leaking values
        print("Supabase creds present? URL:", bool(url), "KEY:", bool(key))
        raise RuntimeError("Missing Supabase credentials via secrets or environment")
    try:
        print("Creating Supabase client for host:", url.split("//")[-1])
        return create_client(url, key)
    except Exception as e:
        raise RuntimeError(f"Failed to create Supabase client: {e}")