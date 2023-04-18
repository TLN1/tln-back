from enum import IntEnum


class Status(IntEnum):
    OK = 0
    ACCOUNT_ALREADY_EXISTS = 1
    ACCOUNT_REGISTER_ERROR = 2


class Message:
    ACCOUNT_ALREADY_EXISTS = "account already exists"
    ACCOUNT_REGISTER_ERROR = "account registration error"


class HttpResponseCode(IntEnum):
    SUCCESS = 200
    CREATED = 201
    BAD_REQUEST = 400
    SERVER_ERROR = 500


STATUS_HTTP_MAPPING = {
    Status.OK: HttpResponseCode.SUCCESS,
    Status.ACCOUNT_ALREADY_EXISTS: HttpResponseCode.BAD_REQUEST,
    Status.ACCOUNT_REGISTER_ERROR: HttpResponseCode.SERVER_ERROR,
}
