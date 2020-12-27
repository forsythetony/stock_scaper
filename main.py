#!/usr/bin/env python3

import argparse
import logging as log

def setup():
    setup_logging()
    setup_argument_parsing()

def setup_logging():
    logging_format = "%(asctime)s: %(message)s"
    log.basicConfig(
        format=logging_format,
        level=log.DEBUG,
        datefmt="%H:%M:%S"
    )

def setup_argument_parsing():
    parser = argparse.ArgumentParser(
        description='A sample description of the application'
    )

    """
    Example of a positional style argument
    
    parser.add_argument(
        'integers',
        dest='integers'
    )
    """

    """
    Example of a named 'non-positional' style argument
    
    parser.add_argument(
        '-o', '--output',
        dest='output_directory',
        required=False,
        default='output'
    )
    """

    """
    Example of a boolean 'store_true' style argument
    
    
    parser.add_argument(
        '--skipBack',
        dest='skip_copy_back',
        action='store_true',
        required=False,
        default=False
    )
    """

    args = parser.parse_args()

    configure_globals()    

def configure_globals():

    """
    Configuration settings should be passed in as arguments to this
    function and set in the following form

    global SAMPLE_ARGUMENT

    SAMPLE_ARGUMENT = sample_argument
    """
    pass

def main():
    setup()

if __name__ == "__main__":
    main()