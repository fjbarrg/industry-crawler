# Industry Crawler

This application contains a web-crawler that downloads industry information from an [official/public government page](https://www.osha.gov/pls/imis/sic_manual.html). The implementation relies on nested-structures (tree-like data), string operations, and recursive search using python.

Objectives: 

* Real world data extraction using a custom web-crawler. 
* Understanding of data modeling by using object-oriented programming. 
* Usage of list/dict comprehension, recursion, and other pythonic-patterns. 


## Setup 

Clone this repository and do the following:

1. Create and activate a virtualenv
    * `virtualenv --python=python3 venv`
    * `source venv/bin/activate`
1. Install requirements
    * `pip install -r requirements.txt`

## Usage

Once `venv` in active, the usage is fairly simple:

* Download the data with the following command:

```commandline
$ python main.py download --filename industries.json
```

* Search for industries:

```commandline
$ python main.py search --title 'Nonclassifiable Establishments' --exact 
```

The python application will search within the nested-structure using a "contains" constraints. You can drop the `--exact` flag to specify similarity search.

## Examples

Search for any industry title that contains the word "Establishments": 

```text
$ python main.py search --title 'aquaculture' --exact
[
    {
        "title": "Division A: Agriculture, Forestry, And Fishing",
        "children": [
            {
                "title": "Major Group 02: Agriculture production livestock and animal specialties",
                "children": [
                    {
                        "title": "Industry Group 027: Animal Specialties",
                        "children": [
                            {
                                "title": "0273 Animal Aquaculture",
                                "children": []
                            }
                        ]
                    }
                ]
            }
        ]
    }
]
```

Search for any industries that resemble the following: "nonclassifiable est"


```text
$ python main.py search --title 'no classifiable'        
[
    {
        "title": "Division J: Public Administration ",
        "children": [
            {
                "title": "Major Group 99: Nonclassifiable Establishments",
                "children": [
                    {
                        "title": "Industry Group 999: Nonclassifiable Establishments",
                        "children": [
                            {
                                "title": "9999 Nonclassifiable Establishments",
                                "children": []
                            }
                        ]
                    }
                ]
            }
        ]
    }
]
```
