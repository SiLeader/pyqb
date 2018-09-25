#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from logging import getLogger
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime, timedelta, timezone

LOCAL_TIMEZONE = timezone(timedelta(hours=datetime.now().hour-datetime.utcnow().hour))


__logger = getLogger("qb_incubator")
__logger.setLevel(10)

sh = logging.StreamHandler()
__logger.addHandler(sh)


def init(file: str):
    fh = TimedRotatingFileHandler("/var/log/pyqb/" + file, when="D")
    __logger.addHandler(fh)


def __message(level, tag, msg):
    now = datetime.now(LOCAL_TIMEZONE)
    return "{0} {1}/{2:<10}: {3}".format(now.strftime("%Y/%m/%d %H:%M:%S%z"), level, tag, msg)


def i(tag, msg):
    __logger.info(__message("I", tag, msg))


def w(tag, msg):
    __logger.warning(__message("W", tag, msg))


def e(tag, msg):
    __logger.error(__message("E", tag, msg))


def d(tag, msg):
    __logger.debug(__message("D", tag, msg))
