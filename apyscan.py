#!/usr/bin/env python3

import asyncio
from pathlib import Path
import re
import argparse
import datetime
import sys
import httpx
import requests
import time
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse
from logger import create_logger

logger = create_logger()


async def main():
    VERSION = "v0.9.1"
    logger.info("APYSCAN %s", VERSION)

    parser = argparse.ArgumentParser(description="Python API Tester")
    parser.add_argument("-u", "--url", help="target url", required=True)
    parser.add_argument("-w", "--wordlist", help="wordlist path", required=True)
    parser.add_argument("-c", "--codes", help="status codes to look for")
    parser.add_argument("-p", "--param", help="parameter to fuzz")
    args = parser.parse_args()

    # check argument's value
    target = validate_argument("url", args.url)
    wordlist = validate_argument("wordlist", args.wordlist)
    validate_wordlist(wordlist)
    codes = validate_argument("codes", args.codes)
    param = validate_argument("param", args.param)

    url_param = extract_parameter(target, param)

    if is_host_reachable(target):
        logger.info("Starting fuzzing...")
        responses = await fuzz(target, wordlist, url_param)
    else:
        raise httpx.ConnectError("Host seems to be offline. Exiting.")

    display_result(responses, codes)


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

        case "param":
            param_regex = "^[a-zA-Z0-9_-]*$"
            if value is None:
                return ""
            elif not re.fullmatch(param_regex, value):
                logger.error(error_message)
                sys.exit(1)
            else:
                logger.info(success_message)
                return value


def extract_parameter(url, param):
    parsed_target = urlparse(url)
    query_params = parse_qs(parsed_target.query)
    url_param = ""

    if param:
        if param in query_params:
            url_param = param
            logger.info("Found specified parameter: %s", url_param)
        else:
            logger.error("Parameter '%s' not found in URL: %s", param, url)
            raise ValueError(f"Parameter '{param}' not found in the URL.")
    else:
        if query_params:
            url_param = list(query_params.keys())[0]
            logger.info("Detected parameter: %s", url_param)
        else:
            logger.error("No parameter found for url: %s", url)
            raise ValueError("No query parameter found in the URL")
    return url_param


def validate_wordlist(wordlist):
    logger.debug("Validating provided wordlist: %s", wordlist)
    user_file = Path(wordlist)
    if user_file.is_file():
        logger.debug("File exists!")
        logger.debug("Is it readable?")
        try:
            with open(user_file) as temp:
                logger.debug("It is readable!")
        except Exception as err:
            logger.error("Unexpected error occured: %s", err)
    else:
        logger.error("File not found!")
        raise FileNotFoundError


def is_host_reachable(target):
    try:
        res = requests.get(target, timeout=3)
        if res.status_code == 200:
            logger.info("Host is online !")
            return True
        else:
            logger.info("Host is reachable but returned status: %s", res.status_code)
            return False
    except requests.exceptions.RequestException as err:
        logger.info("Host is unreachable: %s", target)
        return False


async def fuzz(url, wordlist, param):
    start = time.time()
    results = {}
    semaphore = asyncio.Semaphore(200)
    async with httpx.AsyncClient(
        limits=httpx.Limits(max_connections=200, max_keepalive_connections=20)
    ) as client:
        tasks = {}
        logger.info("Opening wordlist...")
        with open(wordlist) as wordlist:
            for line in wordlist:
                payload = line.strip()

                # Ignore empty lines
                if not payload:
                    continue

                target = generate_target(url, param, payload)
                results[target] = None

                tasks[target] = asyncio.create_task(
                    send_request(semaphore, client, target)
                )

        logger.info("Gathering responses...")
        responses = await asyncio.gather(*tasks.values())

        for target, response in zip(tasks.keys(), responses):
            results[target] = response.status_code

        logger.info("Got all responses!")

    end = time.time()
    elapsed_time = str(datetime.timedelta(seconds=end - start))[:-3]
    logger.info("Fuzzing finished in %s", elapsed_time)

    return results


async def send_request(semaphore, client, target):
    try:
        async with semaphore:
            return await client.get(target)
    except httpx.RequestError as e:
        print(f"Request to {target} failed: {e}")


def display_result(responses, codes):
    for url, res_code in responses.items():
        if res_code in codes:
            logger.info("%s -> %s", url, res_code)


def generate_target(url, param, payload):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    if param in query_params:
        query_params[param] = payload
    else:
        logger.warning("Parameter '%s' not found in the URL, adding it.", param)
        query_params[param] = payload

    new_query = urlencode(query_params, doseq=True)
    return urlunparse(parsed_url._replace(query=new_query))


if __name__ == "__main__":
    asyncio.run(main())
