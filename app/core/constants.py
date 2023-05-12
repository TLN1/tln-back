from enum import Enum, IntEnum


class Status(Enum):
    OK = "ok"
    ACCOUNT_ALREADY_EXISTS = "account already exists"
    ACCOUNT_REGISTER_ERROR = "account registration error"
    USER_ALREADY_LOGGED_IN = "user already logged in"
    ACCOUNT_DOES_NOT_EXIST = "account does not exist"
    USER_NOT_LOGGED_IN = "user not logged in"
    CREATE_APPLICATION_ERROR = "application creation error"
    APPLICATION_DOES_NOT_EXIST = "application does not exist"


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
    Status.USER_NOT_LOGGED_IN: HttpResponseCode.BAD_REQUEST,
    Status.CREATE_APPLICATION_ERROR: HttpResponseCode.SERVER_ERROR,
    Status.APPLICATION_DOES_NOT_EXIST: HttpResponseCode.BAD_REQUEST,
}
