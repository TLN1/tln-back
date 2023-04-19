from enum import IntEnum


class Status(IntEnum):
    ACCOUNT_DOES_NOT_EXIST = 5
    OK = 0
    ACCOUNT_ALREADY_EXISTS = 1
    ACCOUNT_REGISTER_ERROR = 2
    USER_ALREADY_LOGGED_IN = 4


class Message:
    ACCOUNT_ALREADY_EXISTS = "account already exists"
    ACCOUNT_REGISTER_ERROR = "account registration error"
    USER_ALREADY_LOGGED_IN = "user already logged in"
    ACCOUNT_DOES_NOT_EXIST = "account does not exist"


class HttpResponseCode(IntEnum):
    SUCCESS = 200
    CREATED = 201
    BAD_REQUEST = 400
    SERVER_ERROR = 500


STATUS_HTTP_MAPPING = {
    Status.OK: HttpResponseCode.SUCCESS,
    Status.ACCOUNT_ALREADY_EXISTS: HttpResponseCode.BAD_REQUEST,
    Status.ACCOUNT_REGISTER_ERROR: HttpResponseCode.SERVER_ERROR,
    Status.USER_ALREADY_LOGGED_IN: HttpResponseCode.BAD_REQUEST,
    Status.ACCOUNT_DOES_NOT_EXIST: HttpResponseCode.BAD_REQUEST,
}
