#!/usr/bin/env python3

import argparse
import requests
from urllib.parse import urlparse


def main():
    default_codes = [200, 201, 301]

    parser = argparse.ArgumentParser(description="Python API Tester")
    parser.add_argument("-u", "--url", help="target url", required=True)
    parser.add_argument("-w", "--wordlist", help="wordlist path", required=True)
    parser.add_argument(
        "-c",
        "--codes",
        help="status codes to look for",
        type=int,
        default=default_codes,
        nargs="+",
    )
    args = parser.parse_args()

    # check url
    target = args.url
    print("[+] Target URL:", target)

    # check wordlist
    wordlist = args.wordlist
    print("[+] Wordlist:", wordlist)

    # check status codes
    status_codes = args.codes

    print("[+] Codes:", status_codes)

    # parse target url
    parsed_target = urlparse(target)

    # extract parameter
    url_param = parsed_target.query.split("=")[0]
    print("[*] Detected parameter:", url_param)

    # read wordlist
    if args.wordlist:
        payloads = []
        with open(args.wordlist, "r", encoding="UTF-8") as wordlist:
            while line := wordlist.readline():
                payloads.append(line.rstrip())

    # start fuzzing
    for payload in payloads:
        url = target.split("?")[0] + "?" + url_param + "=" + payload
        r = requests.get(url)
        if r.status_code in status_codes:
            print(f"{r.status_code} -> {url_param}={payload}")


if __name__ == "__main__":
    main()
