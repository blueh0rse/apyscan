# APYSCAN

Another Python API

## Quick Run

```bash
python3 apyscan.py -u "http://127.0.0.1:80/api?id=123" -w wordlists/ids/id100.txt
```

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
$ python3 apyscan.py -u http://127.0.0.1:5000/api/v1/users?id=1 -w wordlists/ids/id10.txt
[+] APYSCAN v0.5
[+] url: http://127.0.0.1:5000/api/v1/users?id=1
[+] wordlist: wordlists/ids/id10.txt
[+] codes: [200, 201, 301]
[+] Detected parameter: id
[+] Wordlist length: 10
[+] Host is online
[+] Starting fuzzing...
200 -> id=1
200 -> id=9
[+] Total: 10 / OK: 10 / NOK: 0 / MATCH: 2
[+] Fuzzing finished in 0:00:00.050
```

## Options

```text
Usage:
python3 apyscan.py [flags]

Flags:
 -u, --url       string    The target url
 -w, --wordlist  string    Path to the wordlist
 -c, --codes     string    Status codes to look for (default: 200,201,301)
 -p, --param     string    Parameter to select
```

### `-c`

Some examples of `-c`:

```bash
python3 apyscan.py -u <url> -w <wordlist> -c 200
```

```bash
python3 apyscan.py -u <url> -w <wordlist> -c 200,301,403
```

### `-p`

Some examples of `-p`:

```bash
python3 apyscan.py -u <url> -w <wordlist> -p id
```

```bash
python3 apyscan.py -u <url> -w <wordlist> -p test
```

## Tests

To run the tests use:

```bash
pytest [-v]
```

## Testing APIs

### Single Get Parameter

Start the test API

```bash
python3 APIs/SingleGETParam/api.py
```

Run the tool

```bash
python3 apyscan.py -u http://127.0.0.1:5000/api/v1/users?id=1 -w wordlists/ids/id1000.txt
```

## Changelog

### v0.7

- New argument `-p` to specify the url parameter to fuzz
  - if not specified takes the first parameter detected
  - added user input verification via regex
  - added test cases into `tests/test_validate_argument.py`
- Moved parameter detection into dedicated function
  - Added test cases into `tests/test_extract_parameter.py`
- Updated readme according to changes
- Updated `.gitignore`

### v0.6

- Unit tests under `tests/` using `pytest` for the `validate_argument()` function

### v0.5

- User input validation using regex via `validate_argument()` for 'url', 'wordlist' and 'codes' arguments
- Modified the `-c` format from ints to string

### v0.4

- Improved logger with dual handler (file + console) in a dedicated file
- Added logging information
- Test if target is reachable before fuzzing
- Fuzzing stats: total requests, success, fails, code matching, elapsed time
- Performance:
  - 10,000 GET requests **<35s**

### v0.3

- Add a logger sending logs to `logs/app.log` by default

### v0.2

- `-c` to specify response status codes to look for

### v0.1

- `-u` to specify a url
- `-w` to specify a wordlist path
- Test API 1: `SingleGETParam` handling a single `id` parameter
- `apyscan` can fuzz the first GET parameter of the provided url
