#!/usr/bin/env python3

import argparse
import logging as log
import random
import time

from util import build_directory_path_for_yaml, read_tuples_from_file
from microcenter import MicrocenterBuddy

PRODUCTS = []
MINNESOTA_STORE_ID = "045"
CHROME_DRIVER_LOCATION = ""

MICROCENTER_BUDDY = None

MAX_SLEEP_SECONDS = 60 * 2

def setup():
    setup_logging()
    setup_argument_parsing()
    setup_product_data()

    global MICROCENTER_BUDDY

    MICROCENTER_BUDDY = MicrocenterBuddy(CHROME_DRIVER_LOCATION)

def setup_logging():
    logging_format = "[%(name)s] %(asctime)s: %(message)s"
    log.basicConfig(
        format=logging_format,
        level=log.DEBUG,
        datefmt="%H:%M:%S"
    )

    #   Suppress loggers I don't really care about
    for logger in [log.getLogger(name) for name in log.root.manager.loggerDict]:
        logger.setLevel(log.WARN)

def setup_argument_parsing():
    parser = argparse.ArgumentParser(
        description='A sample description of the application'
    )

    parser.add_argument(
        '-cd', '--chrome_driver',
        dest='chrome_driver',
        required=True
    )

    args = parser.parse_args()

    configure_globals(args.chrome_driver)

def configure_globals(chrome_driver_directory: str):

    global CHROME_DRIVER_LOCATION

    CHROME_DRIVER_LOCATION = chrome_driver_directory

def setup_product_data():

    global PRODUCTS

    file_name = 'product_info.yml'

    with open(build_directory_path_for_yaml(file_name), 'r') as file:
        PRODUCTS = read_tuples_from_file(file)

def search_for_stock():

    curr_index = 0

    while True:
        product_index = curr_index % len(PRODUCTS)
        product = PRODUCTS[product_index]
        product_count = MICROCENTER_BUDDY.total_product_count(product)

        log.info(f"Found {product_count} for product {product.simple_name}")

        product_index += 1
        
        seconds_to_sleep = random.randint(0, MAX_SLEEP_SECONDS)
        seconds_to_sleep = 2
        log.info(f"Going to go to sleep for {seconds_to_sleep} seconds")
        time.sleep(seconds_to_sleep)

        
def main():
    setup()
    search_for_stock()

if __name__ == "__main__":
    main()