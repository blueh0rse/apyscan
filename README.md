# APYSCAN

Another Python API Scanner

## Setup

Create virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
(.venv)$ pip install -r requirements.txt
```

## Run

```bash
python3 apyscan.py -u <url> -w <wordlist>
```

Example:

```bash
$ python3 apyscan.py -u https://example.com/api/v1/users?id=1 -w wordlists/test.txt
[ ] Target URL: https://example.com/api/v1/users?id=1
[ ] Detected parameter: id
[ ] Wordlist: wordlists/test.txt
404 -> id=abc
404 -> id=def
404 -> id=ghi
404 -> id=jkl
```

## Testing APIs

### Single Get Parameter

Start the test API

```bash
python3 tests/APIs/SingleGETParam/api.py
```

Run the tool

```bash
python3 apyscan.py -u https://127.0.0.1:5000/api/v1/users?id=1 -w wordlists/test.txt
```

## Changelog

### v0.1

- `-u` to specify a url
- `-w` to specify a wordlist path
- Test API 1: `SingleGETParam` handling a single `id` parameter
