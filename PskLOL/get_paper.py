import requests
import json


def _get_category_ids(categories: list, req_param: dict) -> list:
    cat_ids = []
    for cat in categories:
        concept_name = cat

        # API endpoint for searching concepts
        concept_search_url = (
            "https://api.openalex.org/concepts?search=",
            f"{concept_name}",
        )

        # Send the request
        concept_response = requests.get(concept_search_url, params=req_param)
        concept_data = concept_response.json()

        # Print the concept ID
        for concept in concept_data["results"]:
            cat_ids.append(concept["id"])
    return cat_ids


def _save_search_results(data: dict, category: str) -> bool:
    papers = []
    for work in data["results"]:
        print(f"Title: {work['display_name']}")
        print(f"DOI: {work['doi']}")
        print(f"Citation counts: {work['cited_by_count']}")
        papers[work["display_name"]] = {
            "Category": category,
            "DOI": work["doi"],
            "Citation count": work["cited_by_count"],
        }
    return papers


def _fetch_from_url(url: str, req_param: dict) -> dict:
    response = requests.get(url, params=req_param)
    return response.json()


def _get_paper_by_category(category: str, req_param: dict) -> dict:
    papers = dict()
    url = ("https://api.openalex.org/works?search=abstract:(", category, ")")
    data = _fetch_from_url(url, req_param)
    # Print the titles and abstracts of the first few works
    papers = _save_search_results(data, category)

    if papers:
        return papers
    else:
        return -1


def _get_paper_by_institute_id(
    inst_id: str, cat_id: str, category: str, req_param: dict
) -> dict:
    url = (
        "https://api.openalex.org/works",
        "?filter=institutions.id:",
        f"{inst_id}+AND+concepts.id:",
        f"{cat_id}",
    )
    data = _fetch_from_url(url, req_param)
    # Print the titles and abstracts of the first few works
    papers = _save_search_results(data, category)
    if papers:
        return papers
    else:
        return -1


def get_paper(
    category: list,
    institutions_ids: list = [],
    save_path=False,
    per_page=1
):
    # Define the API endpoint with the search query
    papers = dict()
    param = {"per_page": per_page}

    if len(institutions_ids) == 0:
        for cat in category:
            papers[cat] = _get_paper_by_category(cat, param)

    else:
        cat_ids = _get_category_ids(category, param)
        for i, id in enumerate(institutions_ids):
            for j, cid in enumerate(cat_ids):
                papers[(id, cid)] = _get_paper_by_institute_id(
                    id,
                    cid, category[j],
                    param
                )

    if save_path is not False:
        if papers:
            with open(save_path, "w") as f:
                json.dump(papers, f, indent=4)
                print(f"paper saved! path -> {save_path}")
            return papers
        else:
            return -1
    if papers:
        return papers
    else:
        return -1
