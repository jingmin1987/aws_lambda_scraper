"""
Main script for the scraper, consisting of a functional handler to interface with AWS Lambda and the function itself
"""

import requests, logging, time, random
from bs4 import BeautifulSoup
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

LOGIN_URL = 'https://www.optionstrategist.com/user/'
TARGET_URL = 'https://www.optionstrategist.com/subscriber-content/put-call-ratios'
QUERY_URL = 'https://www.optionstrategist.com/pcharts/put_call_chart.php?s='
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'}


def aws_scraper_handle(event, context):
    """
    Function handle required to interface with AWS Lambda

    :param event: A dict like object containing event trigger related information
    :param context: A dict like object containing context information
    :return: None
    """
    pass


def aws_scraper(credential):
    """
    Queries and saves information from the target website

    :param credential: A dict like object with username and password
    :return: None
    """

    payload = {
        'form_id': 'user_login',
        'op': 'Log in'
    }
    payload.update(credential)

    s = requests.Session()
    r = s.get(LOGIN_URL, headers=HEADERS)
    soup = BeautifulSoup(r.content, 'html5lib')
    payload['form_build_id'] = soup.find('input')
    r = s.post(LOGIN_URL, data=payload, headers=HEADERS)

    if r.text.find(payload['name']) == -1:
        logger.warning(f'{now()}: Logging in failed for account {payload["name"]}. Script terminating.')
        return
    else:
        logger.info(f'{now()}: Logging in successful for account {payload["name"]}')

    r = s.get(TARGET_URL, headers=HEADERS)
    if r.status_code != 200:
        logger.warning(f'{now()}: Failed to get content from {TARGET_URL}. Script terminating')
        return
    else:
        logger.info(f'{now()}: Successfully connected to {TARGET_URL}.')

    try:
        scrape_all_ticker_charts(s)
    except Exception as e:
        logger.warning(f'{now()}: Exception occurred during scraping. Message: {repr(e)}')
        return

    try:
        write_to_s3()
    except Exception as e:
        logger.warning(f'{now()}: Exception occurred during writing to S3 bucket. Message: {repr(e)}')
        return

    try:
        recommendations = scrape_all_recommendations(s)
    except Exception as e:
        logger.warning(f'{now()}: Exception occurred during scraping recommendations. Message: {repr(e)}')
        return

    try:
        write_to_dynamodb(recommendations)
    except Exception as e:
        logger.warning(f'{now()}: Exception occurred during writing to DynamoDB. Message: {repr(e)}')
        return

def scrape_all_ticker_charts(session):
    """

    :param session: An authenticated session
    :return: None
    """

    r = session.get(TARGET_URL, headers=HEADERS)
    soup = BeautifulSoup(r.content, 'html5lib')
    tickers = soup.find_all('td')
    logger.info(f'{now()}: Starting to scraping charts of {len(tickers)} tickers ...')
    for t in tickers:
        t_cleaned = t.text.split('.txt')[0].strip()
        r = session.get(f'{QUERY_URL}{t_cleaned}')
        with open(f'tmp/{t_cleaned}.png', 'wb') as f:
            f.write(r.content)
        time.sleep(random.random() / 1e2)
    logger.info(f'{now()}: Charts scraping completed')


def write_to_s3():
    pass


def scrape_all_recommendations(session):
    r = session.get(TARGET_URL, headers=HEADERS)
    soup = BeautifulSoup(r.content, 'html5lib')
    txt = soup.find('pre')
    recommend = {}
    for t in txt:
        if t.find('NOW ON') > -1:
            ticker, *rest = t.split()
            recommend[ticker] = ' '.join(rest)
    return recommend


def write_to_dynamodb(recommendations):
    pass


def now():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
