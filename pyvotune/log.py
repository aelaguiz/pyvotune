# -*- coding: utf-8 -*-

from logging import getLogger, StreamHandler, Formatter, getLoggerClass, DEBUG

logger_name = 'pyvotune'
debug_log_format = (
    '-' * 80 + '\n' +
    '%(levelname)s in %(module)s [%(pathname)s:%(lineno)d]:\n' +
    '%(message)s\n' +
    '-' * 80
)


global_debug = False
global_logobj = None


def set_debug(debug=True):
    global global_logobj
    global global_debug

    global_debug = debug

    # If we are toggling global_debug flag and
    # a logger is already created, must replace it
    if global_logobj:
        global_logobj = create_logger()


def logger():
    global global_logobj

    if not global_logobj:
        global_logobj = create_logger()

    return global_logobj


def create_logger():
    Logger = getLoggerClass()

    class DebugLogger(Logger):
        def getEffectiveLevel(x):
            if x.level == 0 and global_debug:
                return DEBUG
            return Logger.getEffectiveLevel(x)

    class DebugHandler(StreamHandler):
        def emit(x, record):
            StreamHandler.emit(x, record) if global_debug else None

    handler = DebugHandler()
    handler.setLevel(DEBUG)
    handler.setFormatter(Formatter(debug_log_format))
    logger = getLogger(logger_name)

    # just in case that was not a new logger, get rid of all the handlers
    # already attached to it.
    del logger.handlers[:]
    logger.__class__ = DebugLogger
    logger.addHandler(handler)
    return logger
