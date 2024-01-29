import requests
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def lambda_handler(event, context):
    urls = ['https://indel-app.onrender.com/', 'https://fixed-loan-calculator.onrender.com/']
    timeout = 120  # seconds
    max_retries = 5  # number of attempts, including the first one

    status = None
    for url in urls:
        status = make_request(url, timeout, max_retries)
        logger.info(status)

    return {
        'statusCode': 200,
        'body': status
    }

def make_request(url, timeout, max_retries):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=timeout)
            logger.info(f"Request to {url} returned with status code {response.status_code}.")
            return response.status_code
        except requests.Timeout:
            logger.warning(f"Timeout occurred for {url}. Attempt {attempt + 1} of {max_retries}.")
        except Exception as e:
            logger.error(f"An error occurred for {url}: {e}")
            return f"An error occurred: {e}"

    logger.error(f"Request failed after {max_retries} retries for {url}.")
    return "Request failed after maximum retries."

# The following is to test locally and should not be executed in the AWS Lambda environment
if __name__ == '__main__' and not os.getenv('AWS_LAMBDA_FUNCTION_NAME'):
    lambda_handler(None, None)
