#!/usr/bin/env python3

import argparse
import datetime
import requests
import time
from urllib.parse import urlparse
from logger import create_logger

logger = create_logger()


def main():
    VERSION = "v0.4"
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
    logger.info("URL: %s", target)

    # check wordlist
    wordlist = args.wordlist
    logger.info("Wordlist: %s", wordlist)

    # check status codes
    logger.info("Codes: %s", args.codes)

    # parse target url
    parsed_target = urlparse(target)

    # extract parameter
    url_param = parsed_target.query.split("=")[0]
    logger.info("Detected parameter: %s", url_param)

    # read wordlist
    line_count = 0
    if args.wordlist:
        payloads = []
        with open(args.wordlist, "r", encoding="UTF-8") as wordlist:
            while line := wordlist.readline():
                payloads.append(line.rstrip())
                line_count += 1
        logger.info("Wordlist length: %s", line_count)

    # check if host is reachable
    try:
        response = requests.get(target, timeout=3)
        if response.status_code == 200:
            logger.info("Host is online")
        else:
            logger.info(
                "Host is reachable but returned status: %s", response.status_code
            )
            return False
    except requests.exceptions.RequestException as err:
        logger.info("Host is unreachable: %s", target)
        return False

    # start fuzzing
    logger.info("Starting fuzzing...")
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
    logger.info(
        "Total: %s / OK: %s / NOK: %s / MATCH: %s", line_count, success, fail, match
    )
    logger.info("Fuzzing finished in %s", elapsed_time)


if __name__ == "__main__":
    main()
