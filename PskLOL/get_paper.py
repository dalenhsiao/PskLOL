import requests
import json


def get_paper(category:list, institutions_ids:list= [], save_path = False, per_page=1):
        # Define the API endpoint with the search query
    papers = dict()
    cat_ids = []
    param = {'per_page':per_page}

    for cat in category:

        concept_name = cat

        # API endpoint for searching concepts
        concept_search_url = f"https://api.openalex.org/concepts?search={concept_name}"

        # Send the request
        concept_response = requests.get(concept_search_url, params=param)
        concept_data = concept_response.json()

        # Print the concept ID
        for concept in concept_data['results']:
            cat_ids.append(concept['id'])
    if len(institutions_ids)==0: 
        for cat in category:    
                
            url = "https://api.openalex.org/works?search=abstract:(" + cat + ")"
            # url = "https://api.openalex.org/works"
            # filter = 
            # params = {
            #     # 'search': cat,
            #     'filter': f'abstract.search:{cat}',  # Replace <institution-id> with the actual institution ID
            #     'per_page': per_page  # Modify as needed
            # }
            
            # Send the GET request
            response = requests.get(url, params=param)
            # Parse the response JSON
            data = response.json()

            # Print the titles and abstracts of the first few works
            for work in data['results']:
                print(f"Title: {work['display_name']}")
                print(f"DOI: {work['doi']}")
                print(f"Citation counts: {work['cited_by_count']}")
                papers[work['display_name']] = {"Category":cat, "DOI": work['doi'], "Citation count":work['cited_by_count']}
            
    else: 
        
        for i, id in enumerate(institutions_ids):
            for j, cid in enumerate(cat_ids):       
                
                # Define the API endpoint to get works associated with the institution
                # url = f"https://api.openalex.org/works?filter=institutions.id:{id}"
                url = f"https://api.openalex.org/works?filter=institutions.id:{id}+AND+concepts.id:{cid}"

                # Send the GET request
                response = requests.get(url, params=param)
                results = response.json()

                # Print the titles and other relevant details of the works
                for work in results['results']:
                    print(f"Title: {work['display_name']}")
                    print(f"DOI: {work['doi']}")
                    print(f"Citation counts: {work['cited_by_count']}")
                    papers[work['display_name']] = {"Category":category[j], "DOI": work['doi'], "Citation count":work['cited_by_count']}
        
    if save_path is not False:
        with open(save_path, 'w') as f: 
            json.dump(papers, f,indent=4)
            print(f"paper saved! path -> {save_path}")

            
    
        
        