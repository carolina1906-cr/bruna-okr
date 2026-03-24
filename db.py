import streamlit as st
from config import get_supabase

@st.cache_data(ttl=300)
def get_departments():
    sb = get_supabase()
    res = sb.table("departments").select("*").order("code").execute()
    return res.data

@st.cache_data(ttl=300)
def get_key_results(department_code=None):
    sb = get_supabase()
    q = sb.table("key_results").select("*").order("sort_order")
    if department_code:
        q = q.eq("department_code", department_code)
    return q.execute().data

def get_monthly_values(key_result_id, year):
    sb = get_supabase()
    res = sb.table("monthly_values")\
        .select("*")\
        .eq("key_result_id", key_result_id)\
        .eq("year", year)\
        .execute()
    return {row["month"]: row["value"] for row in res.data}

def upsert_monthly_value(key_result_id, year, month, value, notes=""):
    sb = get_supabase()
    sb.table("monthly_values").upsert({
        "key_result_id": key_result_id,
        "year": year,
        "month": month,
        "value": value,
        "notes": notes
    }, on_conflict="key_result_id,year,month").execute()

def get_setting(key, default=None):
    sb = get_supabase()
    res = sb.table("app_settings").select("value").eq("key", key).execute()
    if res.data:
        return res.data[0]["value"]
    return default

def set_setting(key, value):
    sb = get_supabase()
    sb.table("app_settings").upsert({"key": key, "value": str(value)}, on_conflict="key").execute()
