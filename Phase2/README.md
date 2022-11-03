
# Search Engine for Wikipedia



## Running Tests

To run tests, run the following command

#### To Create Index 
```bash
  sudo bash index.sh <path_to_wiki_dump> <path_to_inverted_index>
```
#### To Search Query
```bash
  python3 search.py <path_to_query_file>
```


## Prerequisites


```bash
  Python3
  Pip
  nltk
  PyStemmer
```
    
## Author

- Gagan Agarwal


## Features

```bash
All the Field queries and normal queries are supported. 
2 level indexing is used for ensuring faster results.
The inverted index is at first sorted into a single file and then splitted again to ensure that all files are sorted.

```
