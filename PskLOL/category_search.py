import json
import os
from .get_paper import get_paper

# Get the directory of the current script
current_dir = os.path.dirname(__file__)
# Construct the path to the '_db' directory
db_dir = os.path.join(current_dir, '_db')
print("current db path : ", db_dir)
# Ensure the '_db' directory exists
os.makedirs(db_dir, exist_ok=True)
# Specify the path to the 'institute_db.json' file
institute_path = os.path.join(db_dir, 'institute_db.json')



def category_search(institutions:list,category:list, save_paper=False):
    institutions = list(set(institutions))
    keywords = list(set(category))
    institutions_ids = []
    # for inst in institutions: # update local database
    #     _updatedb(inst)
    
    """
        dict_keys(['id', 'ror', 'display_name', 'relevance_score', 
        'country_code', 'type', 'type_id', 'lineage', 'homepage_url', 
        'image_url', 'image_thumbnail_url', 'display_name_acronyms', 
        'display_name_alternatives', 'repositories', 'works_count', 
        'cited_by_count', 'summary_stats', 'ids', 'geo', 'international', 
        'associated_institutions', 'counts_by_year', 'roles', 'x_concepts', 
        'works_api_url', 'updated_date', 'created_date'])
    """
    # print(school_name, categories, scores)
    if os.path.exists(path=institute_path):
        with open(institute_path, "r") as file:
            data = json.load(file)
        for inst in institutions:
            inst_data = data[inst]
            for r in inst_data['results']:
                entity = r['display_name']  
                # print(r['display_name'])
                # print(r["x_concepts"]) # the domain is arraged in a orderly fashion 
                all_categories = [name['display_name'].lower() for name in r['x_concepts']]
                print("======================================================")
                print("Entity name: ", entity)
                print("------------------------------------------------------")
                print("Selected keywords: ", keywords)
                if not all(keyword in all_categories for keyword in keywords):
                    not_in = [keyword for keyword in keywords if keyword not in all_categories]
                    remain_keywords = [keyword for keyword in keywords if keyword in all_categories]
                    print(f"Keywords \"{', '.join(map(str, not_in))}\" is not in this entity")
                    print("All categories in the selected entity: ", all_categories)
                    print(f"Search for existing keywords: \"{', '.join(map(str, remain_keywords))}\"...")
                # print("All keryword is in the searched entity: ", all(keyword in all_categories for keyword in keywords))
                
                print("------------------------------------------------------")
                print("Results Found: \n")
                # get paper
                
                if save_paper:
                    institutions_ids.append(r["id"])

                    
                
                for i, keys in enumerate(remain_keywords):
                    idx = all_categories.index(keys)
                    r["x_concepts"][idx]["score"]
                    print(f"Entity: {entity}, Category: {keys}, Score: {r['x_concepts'][idx]['score']}")
    else:
        raise FileNotFoundError("Database does not exist yet, try update the database first")
    
    if save_paper:
        get_paper(category, institutions_ids, save_paper)
        
        
        
                