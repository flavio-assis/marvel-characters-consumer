# Project: Marvel Characters Consumer

---
languages:
  - python 3.9
  
Products:
  - Python 3.9
  - Docker 20.10.8
---

## Description
This application implements an extraction from Marvel's Characters API and loads it into a DataFrame. All records gotten from the API will
be downloaded in a local path and the data after the cleaning process will also be stored as json files.

## How does it works?

It works by fetching the API and getting the responses in configurable batch sizes. After the extraction is done, the results are loaded into a DataFrame. 

### The Results folder:
All data will be stored in order to be accessible even after the execution is done.
By default, the records gotten from the API will be downloaded to the folder `${APP_HOME}/results/raw/<<execution_time_in_isoformat>>` and after the cleaning process,
the results will be written in `${APP_HOME}/results/cleaned/<<execution_time_in_isoformat>>`. 
These paths are configurable by passing the arguments `--raw-path` and `--cleaned-path` respectively.


### Cleaning Process:

Not all the API fields are required for the analysis so the following columns must be dropped:

- `modified`
- `thumbnail`
- `resourceURI`
- `urls`

For other columns, they must have the "available" value extracted from the raw data. These columns are:
- `comics`
- `series`
- `stories`
- `events`

## Using the application
In order to use this application you must first set your Marvel credentials:

```
export MARVEL_PUBLIC_API_KEY=<< Marvel's public API key >>
export MARVEL_PRIVATE_API_KEY=<< Marvel's private API key >>
```


### Using Docker
To use the application using docker you must build the image. To do that, you can use the make command:
```
make docker-build IMAGE_NAME=<my_image_name> VERSION=<my_image_tag>
```
_Note: The default values for IMAGE_NAME and VERSION are respectively `marvel-character-consumer` and `0.0.1`_

After the image is built you can use it by using the make command:
```
make load-characters-df \
 MARVEL_PUBLIC_API_KEY=$MARVEL_PUBLIC_API_KEY \
 MARVEL_PRIVATE_API_KEY=$MARVEL_PRIVATE_API_KEY
```

Or if you want to customize the batch size that will be extracted on each API call:
```
make load-characters-df BATCH=<<Your custom batch size>> \
 MARVEL_PUBLIC_API_KEY=$MARVEL_PUBLIC_API_KEY \
 MARVEL_PRIVATE_API_KEY=$MARVEL_PRIVATE_API_KEY
```

This command will run the extraction and outputs the DataFrame.
This will also extract the results and sink the files in `${PWD}/results` path. 

### Using virtual environment
Another approach to use the application is to run it inside a virtual environment. To do that, you can use another make command:
```
make virtualenv
```

Then 
```
source venv/bin/activate
```
Finally
```
load-characters-df
```

## Running the tests 
To run the tests you can use the make command:
```
make test
```
They are unit and integration tests built with the python package `unittest`

Note: You have to use the virtual environment to run the tests

## Project structure
```
├── Dockerfile
├── LICENSE
├── Makefile
├── README.md
├── THEROADSOFAR.md
├── requirements.txt
├── requirements-dev.txt
├── setup.py
├── src
│   ├── __init__.py
│   ├── api
│   │   ├── __init__.py
│   │   └── hook.py
│   ├── data_processing
│   │   ├── __init__.py
│   │   └── cleaning.py
│   ├── main.py
│   ├── models
│   │   ├── __init__.py
│   │   └── connection.py
│   └── utils
│       ├── __init__.py
│       ├── logger.py
│       └── path_manager.py
└── tests
    ├── __init__.py
    ├── integration
    │   ├── __init__.py
    │   ├── files
    │   │   ├── cleaned
    │   │   │   └── characters-cleaned.json
    │   │   └── raw
    │   │       └── characters-0-4.json
    │   ├── test_clean_dataframe.py
    │   └── test_get_raw_results.py
    ├── unit
    │   ├── api
    │   │   ├── __init__.py
    │   │   └── test_hook_marvel_character.py
    │   ├── data_processing
    │   │   ├── __init__.py
    │   │   └── test_data_processing_cleaning.py
    │   ├── models
    │   │   ├── __init__.py
    │   │   └── test_model_connection.py
    │   └── utils
    │       ├── __init__.py
    │       ├── test_logger.py
    │       └── test_path_manager.py
    └── utils
        ├── __init__.py
        └── response_mocker.py
           
```