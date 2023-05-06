import os

from cataloger_cli.apis.api_response import ApiResponse
from cataloger_cli.apis.api_server import ApiServer


class ApiEndpoint:
    base_path = None
    server: ApiServer = None

    # for building parametric url paths
    _base_path = None

    def _get(self, path=None, params=None, model_class=None) -> ApiResponse:
        return self.server.request(ApiServer.GET,
                                   os.path.join(self.__get_base_path, path) if path else self.__get_base_path,
                                   params=params, model_class=model_class)

    def _post(self, path=None, body={}, headers={}, model_class=None) -> ApiResponse:
        return self.server.request(ApiServer.POST,
                                   os.path.join(self.__get_base_path, path) if path else self.__get_base_path,
                                   body=body, headers=headers, model_class=model_class)

    def _put(self, path=None, body={}, headers={}, model_class=None) -> ApiResponse:
        return self.server.request(ApiServer.PUT,
                                   os.path.join(self.__get_base_path, path) if path else self.__get_base_path,
                                   body=body, headers=headers, model_class=model_class)

    def _delete(self, path=None, body={}, headers={}) -> ApiResponse:
        return self.server.request(ApiServer.DELETE,
                                   os.path.join(self.__get_base_path, path) if path else self.__get_base_path,
                                   body=body, headers=headers)

    def _patch(self, path=None, body={}, headers={}, model_class=None) -> ApiResponse:
        return self.server.request(ApiServer.PATCH,
                                   os.path.join(self.__get_base_path, path) if path else self.__get_base_path,
                                   body=body, headers=headers, model_class=model_class)

    @property
    def __get_base_path(self):
        if getattr(self, 'base_path', None) is None:
            raise NotImplementedError('Base path is not set for this request')

        if not self._base_path:
            self._base_path = self.base_path

        return self._base_path
