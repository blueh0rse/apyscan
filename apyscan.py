#!/usr/bin/env python3

import re
import argparse
import datetime
import sys
import requests
import time
from urllib.parse import urlparse
from logger import create_logger

logger = create_logger()


def main():
    VERSION = "v0.5"
    logger.info("APYSCAN %s", VERSION)

    parser = argparse.ArgumentParser(description="Python API Tester")
    parser.add_argument("-u", "--url", help="target url", required=True)
    parser.add_argument("-w", "--wordlist", help="wordlist path", required=True)
    parser.add_argument("-c", "--codes", help="status codes to look for")
    args = parser.parse_args()

    target = validate_argument("url", args.url)
    wordlist = validate_argument("wordlist", args.wordlist)
    codes = validate_argument("codes", args.codes)

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
            if r.status_code in codes:
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


def validate_argument(argument, value):
    """Perform regex validation on arguments"""
    logger.debug("Checking argument '%s' with value '%s'", argument, value)

    success_message = f"{argument}: {value}"
    error_message = f"For the argument '{argument}' this value is not valid: {value}"

    match argument:
        case "url":
            url_regex = "^https?:\/\/(?:\d{1,3}(?:\.\d{1,3}){3}|(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,})(?::\d{1,5})?(\/[^\s]*)?$"

            if not re.fullmatch(url_regex, value):
                logger.error(error_message)
                sys.exit(1)
            else:
                logger.info(success_message)
                return value

        case "wordlist":
            file_path_regex = "^(?:[^\s\\/]+[\\/])*[^\s\\/]+\.[a-zA-Z0-9]+$"

            if not re.fullmatch(file_path_regex, value):
                logger.error(error_message)
                sys.exit(1)
            else:
                logger.info(success_message)
                return value

        case "codes":
            codes_regex = "^(\d{3})(,\d{3})*$"
            if value is None:
                value = [200, 201, 301]
                logger.info("%s: %s", argument, value)
                return value
            elif not re.fullmatch(codes_regex, value):
                logger.error(error_message)
                sys.exit(1)
            else:
                logger.info(success_message)
                return [int(code) for code in value.split(",")]


if __name__ == "__main__":
    main()
