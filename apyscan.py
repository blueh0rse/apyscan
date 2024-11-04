import argparse
import requests
from urllib.parse import urlparse


def main():
    parser = argparse.ArgumentParser(description="Python API Tester")
    parser.add_argument("-u", "--url", help="target url", required=True)
    parser.add_argument("-w", "--wordlist", help="wordlist path")
    args = parser.parse_args()

    # parse target url
    target = args.url
    print("[ ] Target URL:", target)
    parsed_target = urlparse(target)

    # extract parameter
    url_param = parsed_target.query.split("=")[0]
    print("[ ] Detected parameter:", url_param)

    # read wordlist
    if args.wordlist:
        payloads = []
        print("[ ] Wordlist:", args.wordlist)
        with open(args.wordlist, "r", encoding="UTF-8") as wordlist:
            while line := wordlist.readline():
                payloads.append(line.rstrip())

    # start fuzzing
    for payload in payloads:
        url = target.split("?")[0] + "?" + url_param + "=" + payload
        r = requests.get(url)
        print(f"{r.status_code} -> {url_param}={payload}")


if __name__ == "__main__":
    main()
