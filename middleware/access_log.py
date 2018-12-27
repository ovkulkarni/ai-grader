# -*- coding: utf-8 -*-
import logging
from datetime import datetime
from ipware import get_client_ip

logger = logging.getLogger("grader_access")


class AccessLogMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if not request.user:
            username = "unknown_user"
        elif request.user.is_anonymous:
            username = "anonymous_user"
        else:
            username = request.user.username

        ip, routable = get_client_ip(request)

        log_line = "{} - {} - [{}] \"{}\" \"{}\"".format(ip,
                                                         username,
                                                         datetime.now(),
                                                         request.get_full_path(),
                                                         request.META.get("HTTP_USER_AGENT", ""))

        logger.info(log_line)

        return response
