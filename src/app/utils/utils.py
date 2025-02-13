# -*- coding: utf-8 -*-

import logging
from flask import g

_logger = logging.getLogger(__name__)


def get_user():
    return g.user