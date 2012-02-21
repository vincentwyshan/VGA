#coding=utf8

import logging

def singleton(getlogger):
    _calllog = dict()
    def _warper(*kargs, **kwarg):
        name = kargs[0]
        if name not in _calllog:
            _calllog[name] = getlogger(name)
        return _calllog[name]
    return _warper

@singleton
def getlogger(name):
    import logging
    logger = logging.getLogger('simple_example')
    logger.setLevel(logging.DEBUG)
    hdr = logging.StreamHandler()
    hdr.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(levelname)s @ %(asctime)s]%(module)s.%(funcName)s: %(message)s')
    hdr.setFormatter(formatter)
    while logger.handlers:
        logger.handlers.pop()
    logger.addHandler(hdr)
    return logger
