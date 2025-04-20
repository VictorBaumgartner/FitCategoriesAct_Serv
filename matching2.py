import json
from supabase import create_client

# Supabase Config
SUPABASE_URL = "https://zqiftxlcvsfbxbsxwytc.supabase.co"
SUPABASE_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpxaWZ0eGxjdnNmYnhic3h3eXRjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQ2MjA1NjAsImV4cCI6MjA2MDE5NjU2MH0.Yfato4huGnjvWIluyX3aJwmt3NemZUo2fsODn80WieI"
SUPABASE_TABLE = "demo"

# Initialize Supabase Client
supabase = create_client(SUPABASE_URL, SUPABASE_API_KEY)

# Load JSON Data
with open(r"C:\Users\victo\Desktop\CS\Job\categ\categories_to_activities.json", "r") as f:
    activities_mapping = json.load(f)  # Format: {"category": ["activity1", "activity2"]}

with open(r"C:\Users\victo\Desktop\CS\Job\categ\categories_to_services.json", "r") as f:
    services_mapping = json.load(f)  # Format: {"category": ["service1", "service2"]}

# Get all unique categories from both mappings
all_categories = set(activities_mapping.keys()).union(services_mapping.keys())

for cat in all_categories:
    # Initialize empty warnings
    activity_warning = ""
    service_warning = ""
    
    # Get activity (or mark as missing)
    if cat in activities_mapping:
        activity = activities_mapping[cat][0] if activities_mapping[cat] else ""
    else:
        activity = ""
        activity_warning = "⚠️ No activity mapping found"
    
    # Get service (or mark as missing)
    if cat in services_mapping:
        service = services_mapping[cat][0] if services_mapping[cat] else ""
    else:
        service = ""
        service_warning = "⚠️ No service mapping found"
    
    data = {
        "meta_category": cat,
        "activities": activity,
        "services": service
    }
    
    try:
        response = supabase.table(SUPABASE_TABLE).insert(data).execute()
        print(f" Inserted: {cat}")
        if activity_warning:
            print(f"   {activity_warning}")
        if service_warning:
            print(f"   {service_warning}")
    except Exception as e:
        print(f" Failed to insert {cat}: {str(e)}")



