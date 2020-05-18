import concurrent.futures
from requests_futures.sessions import FuturesSession
import requests
from typing import Optional

from async_caller_app import APP_PORT, ROUTE

DOMAIN = 'http://localhost:{}'.format(APP_PORT)

class ApiCall:
    def __init__(
        self,
        method: str,
        url: str,
        body: Optional[str] = None
    ):
        self.method = method
        self.url = url
        self.body = body

    @classmethod
    def call(self):
        return ApiCall(
            'GET',
            DOMAIN + ROUTE,
            None
        )



def make_api_call(api_call: ApiCall):
    if api_call.method:
        if api_call.method == 'GET':
            return requests.get(url=api_call.url)
        elif api_call.method == 'POST':
            return requests.post(url=api_call.url, data=api_call.body)
        elif api_call.method == 'PUT':
            return requests.put(url=api_call.url, data=api_call.body)
        elif api_call.method == 'DELETE':
            return requests.delete(url=api_call.url)
        else:
            raise ValueError('Invalid method type: {}'.format(api_call.method))
    else:
        raise ValueError('No API method defined')


def get_api_call_future(api_call: ApiCall):
    if api_call.method:
        session = FuturesSession()
        if api_call.method == 'GET':
            return session.get(url=api_call.url)
        elif api_call.method == 'POST':
            return session.post(url=api_call.url, data=api_call.body)
        elif api_call.method == 'PUT':
            return session.put(url=api_call.url, data=api_call.body)
        elif api_call.method == 'DELETE':
            return session.delete(url=api_call.url)
        else:
            raise ValueError('Invalid method type: {}'.format(api_call.method))
    else:
        raise ValueError('No API method defined')


def call_and_print_response():
    response = make_api_call(ApiCall.call())
    print('response :: status_code={} content={}'.format(response.status_code,
                                                         response.content))


def run_futures_for_count(count: int = 1):
    check_count_value(count)
    return (get_api_call_future(ApiCall.call()) for _i in range(count))


def run_for_count(count: int = 1):
    check_count_value(count)
    return (make_api_call(ApiCall.call()) for _i in range(count))


def check_count_value(count: int):
    if count < 0:
        raise ValueError('Count cannot be less than 0, provided={}'.format(count))


def async_runner(count: int):
    while True:
        # print('waiting...')
        calls = run_futures_for_count(count)
        for response in concurrent.futures.as_completed(calls):
            print('response :: status_code={} content={}'.format(response.result().status_code,
                                                                 response.result().content))


def sync_runner(count: int):
    while True:
        responses = run_for_count(count)
        for response in responses:
            print('response :: status_code={} content={}'.format(response.status_code,
                                                                 response.content))


def threaded_runner(count: int):
    check_count_value(count)
    with concurrent.futures.ThreadPoolExecutor(max_workers=count) as executor:
        for _i in range(count):
            executor.submit(call_and_print_response())



if __name__ == '__main__':
    COUNT = 10

    async_runner(COUNT)
    # sync_runner(COUNT)
    # threaded_runner(COUNT)
