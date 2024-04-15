# PskLOL: Package for Scientific Keyword search on Local database from OpenAlex Library 

## Introduction
PskLOL is designed to provide users with a more convenient access to scientific research related to their chosen topics, using data fetched from OpenAlex and stored in a local database. Users simply need to input keywords related to their areas of interest (e.g., Engineering, Computer Science, Business, etc.). PskLOL will then update and search the local database to provide the desired information, thereby facilitating their scientific search.


## Version 0.0.1

PskLOL search engine is empowered by our `DB_connector` which connect the local database to OpenAlex API and provide user specified information directly without any further effort. For instance, when searching for Carnegie Mellon University, we may find the following information: 

```
Carnegie Mellon University
[{'id': 'https://openalex.org/C41008148', 'wikidata': 'https://www.wikidata.org/wiki/Q21198', 'display_name': 'Computer science', 'level': 0, 'score': 74.3}
```

### Traditional OpenAlex search
When using only the OpenAlex API, in Python, we must access the data by making a request with a URL and then manually query the obtained JSON file, which is not particularly intuitive for users. 

```python
params = {"search": query}
url = "https://api.openalex.org/institutions"
response = requests.get(url, params=params)
response = response.json()
       
```

In the response JSON file, there is much information that users may not require. This complexity can make it difficult for users to sift through all the keys and items in the dictionary.

```python
#  all the keys inside the request json file
"""
    dict_keys(['id', 'ror', 'display_name', 'relevance_score', 
    'country_code', 'type', 'type_id', 'lineage', 'homepage_url', 
    'image_url', 'image_thumbnail_url', 'display_name_acronyms', 
    'display_name_alternatives', 'repositories', 'works_count', 
    'cited_by_count', 'summary_stats', 'ids', 'geo', 'international', 
    'associated_institutions', 'counts_by_year', 'roles', 'x_concepts', 
    'works_api_url', 'updated_date', 'created_date'])
"""
```

### PskLOL search
With PskLOL, users only need to provide the name of the institution and the categories they are interested in with just one line of code. The category search command will first update or initiate the local database if there is none. The search engine will then search through the local database to extract the target information and print out the result.

```python
import PskLOL as lol 

lol.category_search(['carnegie mellon university'], ["engineering", "computer science", "neural science"])

```

**Ouput:**
```
======================================================
Entity name:  Carnegie Mellon University
------------------------------------------------------
Selected keywords:  ['neural science', 'engineering', 'computer science']
('Keywords', 'neural science', 'is not in this entity')
All categories in the selected entity:  ['computer science', 'mathematics', 'physics', 'engineering', 'biology', 'quantum mechanics', 'artificial intelligence', 'programming language', 'chemistry', 'philosophy', 'economics', 'operating system', 'psychology', 'materials science', 'statistics', 'political science', 'medicine']
Search for existing keywords: "engineering, computer science" ...
------------------------------------------------------
Results Found: 

Entity: Carnegie Mellon University,  Category: engineering,  Score: 48.8
Entity: Carnegie Mellon University,  Category: computer science,  Score: 74.7
```



### Limitations
- At this point we only support category search for Canegie Mellon University, hopefully in the next version we will start improving our update search engine and allow user to input desired searched institutions and other entities. 

- The function get_paper, which enables users to fetch research paper titles and their DOI information by category and institution, is still under development. Hopefully, we will see that in future versions. :) 

- Since the data source relies on the OpenAlex library, the information we can access is also restricted by OpenAlex.

## Functions 
- **category_search(institutions: list, category: list)**: Search specific scientific categories by institutions and print categories and category scores. (In version 0.0.1 we only support institution = carnegie mellon university)



## Installation
- Git clone the repository 

```bash
# zsh, bash  
git clone https://github.com/dalenhsiao/PskLOL.git

```

- cd to the package root directory 

```bash 
cd root

```

- pip install 

```bash 
pip install . 

```

## Package Tree
```
PskLOL
├── __init__.py
├── __pycache__
│   ├── __init__.cpython-311.pyc
│   ├── __init__.cpython-39.pyc
│   ├── _updatedb.cpython-311.pyc
│   ├── _updatedb.cpython-39.pyc
│   ├── category_search.cpython-311.pyc
│   ├── category_search.cpython-39.pyc
│   ├── get_paper.cpython-311.pyc
│   └── update.cpython-311.pyc
├── _db
│   ├── data.csv
│   └── institute_db.json
├── _updatedb.py
├── category_search.py
├── get_paper.py
└── update.py

3 directories, 15 files
```


