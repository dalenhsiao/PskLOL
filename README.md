# PskLOL: Package for Scientific Keyword Search on Local Database from OpenAlex Library 

## Introduction
In scientific research, access to scientific literature is a crucial component because the most advanced research builds upon previous studies. In this project, I aim to design an API that provides users with more convenient access to scientific research related to their chosen topics. Users simply need to input a keyword related to their area of interest (e.g., Engineering, Computer Science, Business, etc.), and the proposed utility package will conduct a search based on the database obtained from OpenAlex. OpenAlex includes a feature score to estimate the impact of an entity within a specific scientific area. For instance, when searching for Carnegie Mellon University, we can find the following information: 

```
Carnegie Mellon University
[{'id': 'https://openalex.org/C41008148', 'wikidata': 'https://www.wikidata.org/wiki/Q21198', 'display_name': 'Computer science', 'level': 0, 'score': 74.3}
```

Using the score as a criterion to measure research brilliance allows us to gain an understanding of the direction in searching for scientific literature. In this scenario, knowing that CMU has a score of 74.3 in Computer Science research enables us to determine that starting the search for related research work from CMU can help users narrow down their search scope.





## Functions 
- **category_search(institutions:list, category:list)**: Search specific scientific category by institutions and return category scores. 
- **update(institution:list)**: update the intitution information on local data base from OpenAlex API. 
- ****




## Installation
- Git clone the repository 

```bash
# zsh, bash  
git clone https://github.com/dalenhsiao/PskLOL.git

```

- cd to the package root directory 

```bash 
cd ./project

```

- pip install 

```bash 
pip install . 

```