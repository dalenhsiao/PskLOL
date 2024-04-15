import os
from _updatedb import DB_connector, fetch_data


# Get the directory of the current script
current_dir = os.path.dirname(__file__)
# Construct the path to the '_db' directory
db_dir = os.path.join(current_dir, "_db")
print("current db path : ", db_dir)
# Ensure the '_db' directory exists
os.makedirs(db_dir, exist_ok=True)
# Specify the path to the 'institute_db.json' file
institute_path = os.path.join(db_dir, "data.csv")

# update local db
db = DB_connector(db_dir + "data.csv")


def category_search(institutions: list, category: list):
    institutions = list(set(institutions))
    keywords = list(set(category))
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

        # with open(institute_path, "r") as file:
        #     data = json.load(file)
        for inst in institutions:
            data = fetch_data(inst)

            db.update_data(data)
            data = db.get_data()
            # import pdb; pdb.set_trace()
            for i, r in data.iterrows():
                # import pdb ; pdb.set_trace()
                entity = r["display_name"]
                all_cats = [
                    name["display_name"].lower() for name in r["x_concepts"]
                    ]
                print("======================================================")
                print("Entity name: ", entity)
                print("------------------------------------------------------")
                print("Selected keywords: ", keywords)
                if not all(keyword in all_cats for keyword in keywords):
                    not_in = [ky for ky in keywords if ky not in all_cats]
                    remain_keywords = [ky for ky in keywords if ky in all_cats]
                    keywords_not_in_entity_str = (
                        "Keywords",
                        f"{', '.join(map(str, not_in))}",
                        "is not in this entity",
                    )

                    print(keywords_not_in_entity_str)
                    print("All categories in the selected entity: ", all_cats)
                    print(
                        "Search for existing keywords:",
                        f"\"{', '.join(map(str, remain_keywords))}\"",
                        "...",
                    )
                else:
                    remain_keywords = keywords
                print("------------------------------------------------------")
                print("Results Found: \n")
                # get paper
                # if save_paper:
                #     institutions_ids.append(r["id"])
                for i, keys in enumerate(remain_keywords):
                    idx = all_cats.index(keys)
                    r["x_concepts"][idx]["score"]
                    print(
                        f"Entity: {entity}, ",
                        f"Category: {keys}, ",
                        f"Score: {r['x_concepts'][idx]['score']}",
                    )

    else:
        raise FileNotFoundError(
            "Database does not exist yet, try update the database first"
        )
    # if save_paper:
    #     papers = get_paper(category, institutions_ids, save_paper)


if __name__ == "__main__":
    category_search(["carnegie mellon university"], ["engineering"])
