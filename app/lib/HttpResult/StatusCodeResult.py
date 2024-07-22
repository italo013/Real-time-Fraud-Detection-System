from flask import jsonify
from abc import ABC, abstractmethod


class _HttpResult(ABC):
    def __init__(self, response=None):
        if response is None:
            response = {}
        self.response = response

    @abstractmethod
    def __call__(self, *args, **kwargs):
        return


# 2xx
class OkObjectResult(_HttpResult):
    def __init__(self, response=None):
        super(OkObjectResult, self).__init__(response)

    def __call__(self, *args, **kwargs):
        return jsonify(self.response), 200


class CreateObjectResult(_HttpResult):
    def __init__(self, response=None):
        super(CreateObjectResult, self).__init__(response)

    def __call__(self, *args, **kwargs):
        return jsonify(self.response), 201


class NoContentResult(_HttpResult):
    def __call__(self, *args, **kwargs):
        return jsonify(self.response), 204


# 4xx
class BadRequestObjectResult(_HttpResult):
    def __init__(self, response=None):
        super(BadRequestObjectResult, self).__init__(response)

    def __call__(self, *args, **kwargs):
        return jsonify(self.response), 400


class UnauthorizedObjectResult(_HttpResult):
    def __init__(self, response=None):
        super(UnauthorizedObjectResult, self).__init__(response)

    def __call__(self, *args, **kwargs):
        return jsonify(self.response), 401


class ForbiddenObjectResult(_HttpResult):
    def __init__(self, response=None):
        super(ForbiddenObjectResult, self).__init__(response)

    def __call__(self, *args, **kwargs):
        return jsonify(self.response), 403


class NotFoundResult(_HttpResult):
    def __call__(self, *args, **kwargs):
        return jsonify(self.response), 404


# 5xx
class InternalServerErrorObjectResult(_HttpResult):
    def __init__(self, response=None):
        super(InternalServerErrorObjectResult, self).__init__(response)

    def __call__(self, *args, **kwargs):
        return jsonify(self.response), 500
