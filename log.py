#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Create log process
"""
import logging


def createLog(log_name) :
    # create logger with 'spam_application'
    logger = logging.getLogger(log_name)
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler('%s.log'%log_name)
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


class LogC(object):
    @property
    def logger(self):
        name = '.'.join([__name__, self.__class__.__name__])
        return logging.getLogger(name)


# This class could be imported from a utility module
class LogMixin(object):
    @property
    def logger(self):
        name = '.'.join([__name__, self.__class__.__name__])
        return logging.getLogger(name)

## create logger
#logger = logging.getLogger(__name__)
#logger.setLevel(logging.DEBUG)
#
## create console handler and set level to debug
#ch = logging.StreamHandler()
#ch.setLevel(logging.DEBUG)
#
## create formatter
#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#
## add formatter to ch
#ch.setFormatter(formatter)
#
## add ch to logger
#logger.addHandler(ch)



# 'application' code
# logger.debug('debug message')
# logger.info('info message')
# logger.warning('warn message')
# logger.error('error message')
# logger.critical('critical message')

