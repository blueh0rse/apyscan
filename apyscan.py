#!/usr/bin/env python3

import argparse
import datetime
import logging
import requests
import time
from urllib.parse import urlparse


def main():
    VERSION = "v0.3"
    logger = create_logger()
    logger.info("APYSCAN %s", VERSION)

    DEFAULT_CODES = [200, 201, 301]

    parser = argparse.ArgumentParser(description="Python API Tester")
    parser.add_argument("-u", "--url", help="target url", required=True)
    parser.add_argument("-w", "--wordlist", help="wordlist path", required=True)
    parser.add_argument(
        "-c",
        "--codes",
        help="status codes to look for",
        type=int,
        default=DEFAULT_CODES,
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
    print("[+] Codes:", args.codes)

    # parse target url
    parsed_target = urlparse(target)

    # extract parameter
    url_param = parsed_target.query.split("=")[0]
    print("[*] Detected parameter:", url_param)

    # read wordlist
    line_count = 0
    if args.wordlist:
        payloads = []
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
    print("[*] Starting fuzzing...")
    success = 0
    match = 0
    fail = 0
    start = time.time()
    for payload in payloads:
        try:
            url = target.split("?")[0] + "?" + url_param + "=" + payload
            r = requests.get(url)
            if r.status_code in args.codes:
                print(f"{r.status_code} -> {url_param}={payload}")
                match += 1
            success += 1
        except:
            fail += 1
    end = time.time()
    elapsed_time = str(datetime.timedelta(seconds=end - start))[:-3]
    print("[-] Total:", line_count, "/ OK:", success, "/ NOK:", fail, "/ MATCH:", match)
    print("[+] Fuzzing finished in", elapsed_time)


def create_logger():
    """Create logger with file handler and custom format"""
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
