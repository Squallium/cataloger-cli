import logging
import urllib
from typing import Type
from urllib.parse import urljoin

import requests

from cataloger_cli.apis.api_response import ApiResponse


class ApiServer:
    GET = 'get'
    POST = 'post'
    PUT = 'put'
    DELETE = 'delete'
    PATCH = 'patch'

    def __init__(self, host=None, token=None, verify=None, additional_headers=None, response_class=ApiResponse) -> None:
        super().__init__()

        self.host = host
        self.token = token
        self.verify = verify
        self.version = None
        self.default_headers = {
            'Authorization': f'bearer {self.token}'
        }

        if additional_headers:
            self.default_headers.update(additional_headers)

        self.response_class: Type[ApiResponse] = response_class

    def request(self, method, path, params=None, body={}, headers={}, model_class=None) -> ApiResponse:
        # creating the header
        final_headers = self.default_headers.copy()
        final_headers.update(headers)

        url = urljoin(self.host, path)
        logging.debug(f'{url}{"?" + urllib.parse.urlencode(params, doseq=True) if params else ""}')

        if method == self.GET:
            response = requests.get(url,
                                    params=params,
                                    verify=self.verify,
                                    headers=final_headers)
        elif method == self.POST:
            response = requests.post(url,
                                     json=body,
                                     verify=self.verify,
                                     headers=final_headers)
        elif method == self.PUT:
            response = requests.put(url,
                                    json=body,
                                    verify=self.verify,
                                    headers=final_headers)
        elif method == self.DELETE:
            response = requests.delete(url,
                                       verify=self.verify,
                                       headers=final_headers)
        elif method == self.PATCH:
            response = requests.patch(url,
                                      json=body,
                                      verify=self.verify,
                                      headers=final_headers)
        else:
            raise NotImplementedError(f'Request method {method} no implemented')

        return self.response_class.from_request(response, model_class=model_class)
