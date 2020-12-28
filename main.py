#!/usr/bin/env python3

import argparse
import logging as log
import random
import time
from datetime import datetime

from util import (
    ProductData, build_directory_path_for_yaml, construct_url_for_product, 
    read_tuples_from_file, 
    Config, 
    load_config, 
    build_local_path,
    simple_timestamp,
    current_datetime_cst
)
from microcenter import MicrocenterBuddy

from sns import SnsWrapper

PRODUCTS = []
CHROME_DRIVER_LOCATION = ""
IS_TESTING = False

MICROCENTER_BUDDY = None

CONFIG : Config = None
SNS : SnsWrapper = None

def setup():
    setup_logging()
    setup_argument_parsing()
    setup_product_data()
    setup_config()
    setup_sns()

    global MICROCENTER_BUDDY

    MICROCENTER_BUDDY = MicrocenterBuddy(CHROME_DRIVER_LOCATION)

def setup_sns():
    global SNS

    SNS = SnsWrapper(CONFIG.aws_topic_arn, CONFIG.aws_region)

    log.info(SNS)

def setup_config():
    global CONFIG

    config_path = build_local_path('config.yml')

    with open(config_path, 'r') as file:
        CONFIG = load_config(file)
    
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

    parser.add_argument(
        '-t',
        dest='is_testing',
        action='store_true'
    )

    args = parser.parse_args()

    configure_globals(args.chrome_driver, args.is_testing)

def configure_globals(chrome_driver_directory: str, is_testing: str):

    global CHROME_DRIVER_LOCATION
    global IS_TESTING

    CHROME_DRIVER_LOCATION = chrome_driver_directory
    IS_TESTING = is_testing

def setup_product_data():

    global PRODUCTS

    file_name = 'product_info.yml'

    with open(build_directory_path_for_yaml(file_name), 'r') as file:
        PRODUCTS = read_tuples_from_file(file)

def should_search():
    now = datetime.now()

    return now.hour >= 6

def send_in_stock_message(product: ProductData, stock_count: int):
    
    message = f"{product.simple_name} is in stock! [{stock_count}]"
    message += "\n\n"
    message += construct_url_for_product(product)

    SNS.publish_message(
        'In stock!',
        message
    )

def search_for_stock():

    curr_index = 0

    while True:
        product_index = curr_index % len(PRODUCTS)
        log.info(f"Build a proudct index of {product_index}")
        product = PRODUCTS[product_index]
        
        if should_search():
            log.info(f"Will attempt to search for stock of {product.simple_name}")
            product_count = MICROCENTER_BUDDY.total_product_count(product)
            curr_index += 1
            log.info(f"Found {product_count} for product {product.simple_name}")

            log.info(f"Type of product count is {type(product_count)}")

            if product_count > 0:
                log.info("Product count was greater than 0")
                send_in_stock_message(product, product_count)
        else:
            log.info("Not search for product because it's not the right time")
        
        seconds_to_sleep = random.randint(CONFIG.min_sleep_seconds, CONFIG.max_sleep_seconds)
        log.info(f"Going to go to sleep for {seconds_to_sleep} seconds")
        time.sleep(seconds_to_sleep)

def test():
    current_datetime = current_datetime_cst()
    log.info(f"The current time in CST is {simple_timestamp(current_datetime)}")

    log.info(f"The current hour is {current_datetime.hour}")

def main():
    SNS.publish_message(
        'Starting up',
        f"Started searching for {len(PRODUCTS)} products at {simple_timestamp()}"
    )
    search_for_stock()

if __name__ == "__main__":
    setup()

    if IS_TESTING:
        test()
    else:
        main()
