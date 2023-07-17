from rest_framework.exceptions import APIException


class FollowError(APIException):
    status_code = 400
    default_detail = "Ошибка подписки"
