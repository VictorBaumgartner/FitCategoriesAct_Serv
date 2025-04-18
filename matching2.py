import json
import requests

# Config Supabase
SUPABASE_URL = "https://zqiftxlcvsfbxbsxwytc.supabase.co"
SUPABASE_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpxaWZ0eGxjdnNmYnhic3h3eXRjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQ2MjA1NjAsImV4cCI6MjA2MDE5NjU2MH0.Yfato4huGnjvWIluyX3aJwmt3NemZUo2fsODn80WieI"
SUPABASE_TABLE = "demo"

headers = {
    "apikey": SUPABASE_API_KEY,
    "Authorization": f"Bearer {SUPABASE_API_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

# Charger les correspondances
with open(r"C:\Users\victo\Desktop\categ\categories_to_activities.json", "r", encoding="utf-8") as f:
    activities_mapping = json.load(f)

with open(r"C:\Users\victo\Desktop\categ\categories_to_services.json", "r", encoding="utf-8") as f:
    services_mapping = json.load(f)

# Fusionner les données
all_categories = set(activities_mapping.keys()) | set(services_mapping.keys())

for cat in all_categories:
    payload = {
        "meta_category": cat,
        "activities": activities_mapping.get(cat, []),
        "services": services_mapping.get(cat, [])
    }

    response = requests.post(
        f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}",
        headers=headers,
        json=payload
    )

    if response.status_code in [201, 200, 204]:
        print(f"✅ Insertion réussie pour la catégorie : {cat}")
    else:
        print(f"❌ Erreur ({response.status_code}) pour {cat} : {response.text}")
