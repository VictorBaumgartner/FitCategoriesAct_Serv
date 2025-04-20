# import pandas as pd
# from collections import defaultdict
# import json

# # Charger les fichiers CSV
# activities_df = pd.read_csv("activities.csv")
# services_df = pd.read_csv("services.csv")

# # Charger les lignes du fichier categ.txt
# with open("categ.txt", "r", encoding="utf-8") as f:
#     lines = f.readlines()

# # Préparer les noms d'activités et services en minuscules pour le matching
# activity_names = set(activities_df["Name"].dropna())
# service_names = set(services_df["Name"].dropna())

# activity_names_lower = {name.lower(): name for name in activity_names}
# service_names_lower = {name.lower(): name for name in service_names}

# # Dictionnaires pour stocker les correspondances
# category_to_activities = defaultdict(set)
# category_to_services = defaultdict(set)

# # Matching souple basé sur sous-chaîne (insensible à la casse)
# for line in lines:
#     clean_line = line.strip()
#     if not clean_line:
#         continue
#     lower_line = clean_line.lower()
#     found = False

#     # Recherche dans les activités
#     for act_key, act_val in activity_names_lower.items():
#         if act_key in lower_line:
#             idx = lower_line.find(act_key)
#             category = clean_line[:idx].strip()
#             category_to_activities[category].add(act_val)
#             found = True
#             break

#     # Si pas trouvé dans les activités, chercher dans les services
#     if not found:
#         for serv_key, serv_val in service_names_lower.items():
#             if serv_key in lower_line:
#                 idx = lower_line.find(serv_key)
#                 category = clean_line[:idx].strip()
#                 category_to_services[category].add(serv_val)
#                 break

# # Conversion en JSON
# category_activity_map = {
#     cat: sorted(list(acts)) for cat, acts in category_to_activities.items()
# }
# category_service_map = {
#     cat: sorted(list(servs)) for cat, servs in category_to_services.items()
# }

# # Sauvegarde dans des fichiers JSON
# with open("categories_to_activities.json", "w", encoding="utf-8") as f:
#     json.dump(category_activity_map, f, ensure_ascii=False, indent=2)

# with open("categories_to_services.json", "w", encoding="utf-8") as f:
#     json.dump(category_service_map, f, ensure_ascii=False, indent=2)

# print("✅ JSON générés avec succès !")






import csv
import json
from collections import defaultdict

# Charger les activités sans pandas
with open(r"C:\Users\victo\Desktop\CS\Job\categ\activities.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    activity_names = set(row["Name"].strip() for row in reader if row["meta_category"].strip())

# Charger les services sans pandas
with open(r"C:\Users\victo\Desktop\CS\Job\categ\services.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    service_names = set(row["Name"].strip() for row in reader if row["meta_category"].strip())

# Mise en minuscules pour matching
activity_names_lower = {name.lower(): name for name in activity_names}
service_names_lower = {name.lower(): name for name in service_names}

# Lire le fichier categ.txt
with open(r"C:\Users\victo\Desktop\CS\Job\categ\snippet_event.csv", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Dictionnaires de mapping
category_to_activities = defaultdict(set)
category_to_services = defaultdict(set)

# Matching amélioré
for line in lines:
    clean_line = line.strip()
    if not clean_line:
        continue
    lower_line = clean_line.lower()

    matched = False

    for act_key, act_val in activity_names_lower.items():
        if act_key in lower_line:
            category_to_activities[clean_line].add(act_val)
            matched = True
            break

    if not matched:
        for serv_key, serv_val in service_names_lower.items():
            if serv_key in lower_line:
                category_to_services[clean_line].add(serv_val)
                break

# Sauvegarde JSON propre
with open("categories4activities.json", "w", encoding="utf-8") as f:
    json.dump({k: sorted(v) for k, v in category_to_activities.items()}, f, ensure_ascii=False, indent=2)

with open("categories4services.json", "w", encoding="utf-8") as f:
    json.dump({k: sorted(v) for k, v in category_to_services.items()}, f, ensure_ascii=False, indent=2)

print("✅ JSON générés avec les catégories complètes !")
