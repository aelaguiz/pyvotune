# -*- coding: utf-8 -*-

from logging import getLogger, StreamHandler, Formatter, getLoggerClass, DEBUG

logger_name = 'pyvotune'
debug_log_format = (
    '-' * 80 + '\n' +
    '%(levelname)s in %(module)s [%(pathname)s:%(lineno)d]:\n' +
    '%(message)s\n' +
    '-' * 80
)


def create_logger(obj):
    """Creates a logger for the given objlication.  This logger works
    similar to a regular Python logger but changes the effective logging
    level based on the objlication's debug flag.  Furthermore this
    function also removes all attached handlers in case there was a
    logger with the log name before.
    """
    Logger = getLoggerClass()

    if not hasattr(obj, 'debug'):
        obj.debug = False

    if not hasattr(obj, 'debug_log_format'):
        obj.debug_log_format = debug_log_format

    if not hasattr(obj, 'logger_name'):
        obj.logger_name = logger_name

    class DebugLogger(Logger):
        def getEffectiveLevel(x):
            if x.level == 0 and obj.debug:
                return DEBUG
            return Logger.getEffectiveLevel(x)

    class DebugHandler(StreamHandler):
        def emit(x, record):
            StreamHandler.emit(x, record) if obj.debug else None

    handler = DebugHandler()
    handler.setLevel(DEBUG)
    handler.setFormatter(Formatter(obj.debug_log_format))
    logger = getLogger(obj.logger_name)

    # just in case that was not a new logger, get rid of all the handlers
    # already attached to it.
    del logger.handlers[:]
    logger.__class__ = DebugLogger
    logger.addHandler(handler)
    return logger
