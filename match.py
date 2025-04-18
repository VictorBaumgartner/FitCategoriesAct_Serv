import json
import google.generativeai as genai # Import the Google Generative AI library
from supabase import create_client, Client
import csv

# Configure the Gemini API key
# Option 1: Directly insert your key (less secure, okay for quick tests)
GOOGLE_API_KEY = "AIzaSyDv6RKa7WLoegUfoxNurhWSH4PmGLdFfwA"

if not GOOGLE_API_KEY:
    raise ValueError("Gemini API key not found. Please set the GOOGLE_API_KEY environment variable.")

# Configure the library with your API key
genai.configure(api_key=GOOGLE_API_KEY)

# --- Initialize your OpenAI and Supabase clients here ---
# Make sure to replace with your actual keys and URLs
supabase_url = "https://zqiftxlcvsfbxbsxwytc.supabase.co"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpxaWZ0eGxjdnNmYnhic3h3eXRjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQ2MjA1NjAsImV4cCI6MjA2MDE5NjU2MH0.Yfato4huGnjvWIluyX3aJwmt3NemZUo2fsODn80WieI"
supabase: Client = create_client(supabase_url, supabase_key)
# ------------------------------------------------------

gemini_model = genai.GenerativeModel('gemini-2.5-pro-preview-03-25')

# Load categories from a text file (one category per line)
with open(r'C:\Users\victo\Desktop\categ\categ.txt', 'r') as f:
    categories = [line.strip() for line in f.readlines()]

# Load activities from a CSV file
activities_data = []
with open(r'C:\Users\victo\Desktop\categ\activities.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        activities_data.append(row)

# Function to ask the LLM for the best match between categories and activities
def ask_llm_for_match(category):
    prompt = f"""
You are an assistant that matches categories to activities based on context and relevance.
Given the category "{category}", suggest the most relevant activities from the following list:
{json.dumps([activity['Name'] for activity in activities_data], indent=2)}

Return a JSON object with the category as the key and the list of activity names as the value.
For example:
{{
    "{category}": ["Activity Name 1", "Activity Name 2", "Activity Name 3"]
}}
"""
    response = gemini_model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(temperature=0)
    )
    try:
        content = response.parts[0].text.strip()
        return json.loads(content)
    except json.JSONDecodeError:
        print(f"Error decoding JSON response for category {category}: {content}")
        return {category: []}
    except Exception as e:
        print(f"Error generating content for category {category}: {e}")
        return {category: []}

# Create a dictionary to map activity IDs to their categories (using Name as category for now)
activity_id_to_category = {
    activity.get('ID'): activity.get('Name')
    for activity in activities_data
    if 'ID' in activity and 'Name' in activity
}

# Update the Supabase table with the new activities column
for activity_id, category in activity_id_to_category.items():
    # Ask the LLM for the best match
    match_result = ask_llm_for_match(category)
    activities = match_result.get(category, [])

    # Print the correspondence here
    print(f"Category: {category} -> Suggested Activities: {activities}")

    # Update the row with the new activities column
    try:
        supabase.table("demo").update({"activities": activities}).eq("id", activity_id).execute()
        print(f"Updated row {activity_id} with activities: {activities}")
    except Exception as e:
        print(f"Error updating row {activity_id}: {e}")

print("All rows have been processed.")



