"""
Main script for the scraper, consisting of a functional handler to interface with AWS Lambda and the function itself
"""

import requests
from bs4 import BeautifulSoup


def aws_scraper_handle(event, context):
    """
    Function handle required to interface with AWS Lambda

    :param event: a dict like object containing event trigger related information
    :param context: a dict like object containing context information
    :return: None
    """
    pass


def aws_scraper(credential):
    """
    Queries and saves information from the target website

    :param credential: a dict like object with username and password
    :return: None
    """
    pass

