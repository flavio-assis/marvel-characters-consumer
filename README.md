# Project: Marvel Characters Consumer

---
languages:
  - python 3.9
  
Products:
  - Python 3.9
  - Docker 20.10.8
---

## Description
This application implements an extraction from Marvel's Characters API and loads it into a DataFrame.

## How does it works?

It works by fetching the API and getting the responses in configurable batch sizes. After the extraction is done, the results are loaded into a DataFrame. 

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
In order to use this application you must first set your Marvel credentials and then:

__Linux ou MacOS__
```
export MARVEL_PUBLIC_API_KEY=<< Marvel's public API key >>
export MARVEL_PRIVATE_API_KEY=<< Marvel's private API key >>
```
__Windows (CommandPrompt)__ 

```
setx MARVEL_PUBLIC_API_KEY=<< Marvel's public API key >>
setx MARVEL_PRIVATE_API_KEY=<< Marvel's private API key >>
```
__Windows (PowerShell)__ 
```
$Env:MARVEL_PUBLIC_API_KEY=<< Marvel's public API key >>
$Env:MARVEL_PRIVATE_API_KEY=<< Marvel's private API key >>
```

### Using Docker
To use the application using docker you must build the image. To do that, you can use the make command:
```
make docker-build IMAGE_NAME=<my_image_name> VERSION=<my_image_tag>
```
_Note: The default values for IMAGE_NAME and VERSION are respectively `marvel-character-consumer` and `0.0.1`_

After the image is built you can use it by using the make command:
```
make load-characters-df MARVEL_PUBLIC_API_KEY=$MARVEL_PUBLIC_API_KEY MARVEL_PRIVATE_API_KEY=$MARVEL_PRIVATE_API_KEY
```
This command will run the extraction and outputs the DataFrame.

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

## Project structure
```
               
```