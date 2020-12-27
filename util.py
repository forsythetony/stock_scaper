from collections import namedtuple
from io import TextIOWrapper
from typing import Sequence
import logging as log
import yaml
import os

ASSET_FOLDER_NAME = 'assets'
MICROCENTER_BASE_URL = "https://www.microcenter.com/product/"

ProductData = namedtuple('ProductData', 'store_id, product_id, simple_name, full_name')

def build_directory_path_for_yaml(yaml_file_name: str):
    return os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        ASSET_FOLDER_NAME,
        yaml_file_name
    )

def print_product_info_list(productInfoList: Sequence[ProductData]):
    print_str = '\n'.join(str(x) for x in productInfoList)
    log.info(print_str)

def write_tuples_to_file(productInfoList: Sequence[ProductData], file: TextIOWrapper):    
    yaml.dump([x._asdict() for x in productInfoList], file)

def read_tuples_from_file(file: TextIOWrapper) -> Sequence[ProductData]:
    
    loaded_yaml = yaml.safe_load(file)

    return [ProductData(**x) for x in loaded_yaml]

def construct_url_for_product(product: ProductData) -> str:
    return f"{MICROCENTER_BASE_URL}/{product.product_id}/{product.full_name}?storeid={product.store_id}"

def remove_non_digits(string: str) -> str:
    BAD_STR = [ '+', '-', 'in stock']

    return_string = string

    for s in BAD_STR:
        return_string = return_string.replace(s, '')
    
    return return_string.strip()
 
def clean_stock_string(stock_str: str) -> str:
    
    return remove_non_digits(stock_str.strip().lower())
