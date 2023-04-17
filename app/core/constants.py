from enum import IntEnum


class Status(IntEnum):
    OK = 0


class HttpResponseCode(IntEnum):
    HTTP_RESPONSE_SUCCESS = 200
    HTTP_RESPONSE_CREATED = 201
    HTTP_RESPONSE_SERVER_ERROR = 500


STATUS_HTTP_MAPPING = {
    Status.OK: HttpResponseCode.HTTP_RESPONSE_SUCCESS,
}
