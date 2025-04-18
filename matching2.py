import json
from supabase import create_client
import unicodedata

# Supabase Config
SUPABASE_URL = "https://zqiftxlcvsfbxbsxwytc.supabase.co"
SUPABASE_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpxaWZ0eGxjdnNmYnhic3h3eXRjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQ2MjA1NjAsImV4cCI6MjA2MDE5NjU2MH0.Yfato4huGnjvWIluyX3aJwmt3NemZUo2fsODn80WieI"
SUPABASE_TABLE = "demo"

# Initialize Supabase Client
supabase = create_client(SUPABASE_URL, SUPABASE_API_KEY)

def normalize_text(text):
    return unicodedata.normalize('NFKC', str(text)).strip()

# Load and normalize JSON keys in advance
with open(r"C:\Users\victo\Desktop\CS\Job\categ\categories_to_activities.json", "r", encoding='utf-8') as f:
    activities_mapping = {
        normalize_text(k): v 
        for k, v in json.load(f).items()
    }

with open(r"C:\Users\victo\Desktop\CS\Job\categ\categories_to_services.json", "r", encoding='utf-8') as f:
    services_mapping = {
        normalize_text(k): v 
        for k, v in json.load(f).items()
    }

# Get all categories from DB (normalized)
db_categories = supabase.table(SUPABASE_TABLE)\
    .select("meta_category")\
    .execute()
    
all_categories = {
    normalize_text(item['meta_category']) 
    for item in db_categories.data
}

for db_category in all_categories:
    # Find matching normalized key
    activity = next(
        (v[0] for k, v in activities_mapping.items() 
         if normalize_text(k) == db_category),
        ""
    )
    
    service = next(
        (v[0] for k, v in services_mapping.items()
         if normalize_text(k) == db_category),
        ""
    )
    
    data = {
        "meta_category": db_category,  # Original DB value
        "activities": activity,
        "services": service
    }

