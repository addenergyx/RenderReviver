import requests

def make_request(url, timeout, max_retries):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=timeout)
            return response.status_code
        except requests.Timeout:
            print(f"Timeout occurred. Attempt {attempt + 1} of {max_retries}.")
        except Exception as e:
            return f"An error occurred: {e}"

    return "Request failed after maximum retries."

# Usage
urls = ['https://indel-app.onrender.com/', 'https://fixed-loan-calculator.onrender.com/']
timeout = 120  # seconds
max_retries = 2  # number of attempts, including the first one


for url in urls:
    status = make_request(url, timeout, max_retries)
print(status)