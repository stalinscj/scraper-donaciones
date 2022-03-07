# Scrape and filter data


## Requisites

- python >= 3.9
- pip >= 22.0.3
- chromedriver (the version must match the version of your Chrome and should be [able to run](https://chromedriver.chromium.org/getting-started#h.p_ID_36) from anywhere)


## Installation

```sh
git clone https://github.com/stalinscj/scraper-donaciones.git
```

```sh
cd scraper-donaciones
```

```sh
pip install -r requirements.txt
```

```sh
python -m pip install pytest
```


## Running tests

```sh
pytest
```


## Running scripts

```sh
python scraper.py -ct CONTENT_TYPE -c CATEGORY -f FORMAT -r REPORT_NAME [-q]
```

```sh
python filter.py filename [-q]
```


## Examples

```sh
python scraper.py -ct Dataset -c 'Economía y Finanzas' -f csv -r donaciones
```

```sh
python filter.py pcm_donaciones.csv
```
