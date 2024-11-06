#!/usr/bin/env python3

import argparse
import requests
from urllib.parse import urlparse
import logging


def main():
    VERSION = "v0.3"
    logger = create_logger()
    logger.info("apyscan %s", VERSION)

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
        line_count = 0
        with open(args.wordlist, "r", encoding="UTF-8") as wordlist:
            while line := wordlist.readline():
                payloads.append(line.rstrip())
                line_count += 1
        print("[*] Wordlist length:", line_count)

    # check if host is reachable
    try:
        response = requests.get(target, timeout=3)
        if response.status_code == 200:
            print("[+] Host is online")
        else:
            print("[!] Host is reachable but returned status:", response.status_code)
            return False
    except requests.exceptions.RequestException as err:
        print("[!] Host is unreachable:", target)
        return False

    # start fuzzing
    for payload in payloads:
        url = target.split("?")[0] + "?" + url_param + "=" + payload
        r = requests.get(url)
        if r.status_code in status_codes:
            print(f"{r.status_code} -> {url_param}={payload}")


def create_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(10)
    file_handler = logging.FileHandler("logs/app.log", mode="a", encoding="utf-8")
    logger.addHandler(file_handler)

    formatter = logging.Formatter(
        "{asctime} - {levelname} - {message}",
        style="{",
        datefmt="%d-%m-%Y %H:%M",
    )

    file_handler.setFormatter(formatter)
    return logger


if __name__ == "__main__":
    main()
