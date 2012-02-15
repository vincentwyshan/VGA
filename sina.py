#coding=utf8

from weibopy.auth import OAuthHandler
from weibopy.api import API

import ConfigParser

import user
import basis

log = basis.getlogger(__name__)

cfg = ConfigParser.ConfigParser()
cfg.read('config.ini')

APP_KEY = cfg.get('sina', 'APP_KEY')
APP_SECRET = cfg.get('sina', 'APP_SECRET')

del cfg

def authorization_url(callback_url=''):
    auth = OAuthHandler( APP_KEY, APP_SECRET, callback_url);
    auth_url = auth.get_authorization_url()
    return auth_url, auth.request_token.key, auth.request_token.secret


class SinaWeibo(object):
    user = None
    email = None
    def __init__(self, email):
        self.email = email
        user.add(email)

    def init(self, verifier_num=None):
        log.debug('init %s' % verifier_num)
        info = user.get_app('sina', self.email)
        log.debug(info.get('request_token'))
        if not info.get('request_token') or not verifier_num:
            return self.init_1st_step()
        else:
            return self.init_2nd_step(verifier_num)

    def init_1st_step(self):
        auth = OAuthHandler(APP_KEY, APP_SECRET, '')
        auth_url = auth.get_authorization_url()
        user.update_app('sina', self.email, request_token=auth.request_token.key,
                request_secret=auth.request_token.secret)
        log.debug(repr(user.get(self.email)))
        return auth_url

    def init_2nd_step(self, verifier_num):
        info = user.get_app('sina', self.email)
        auth = OAuthHandler(APP_KEY, APP_SECRET)
        auth.set_request_token(info.get('request_token'), info.get('request_secret'))
        access = auth.get_access_token(verifier_num)
        user.update_app('sina', self.email, access_token=access.key, access_secret=access.secret)
        return True

    def newmessage(self, message, lat=None, long=None):
        log.debug('new message: %s' % message)
        auth = OAuthHandler(APP_KEY, APP_SECRET)
        info = user.get_app('sina', self.email)
        auth.setToken(info['access_token'], info['access_secret'])
        api = API(auth)
        api.update_status(message)
        log.debug('new message done.')
        return True

    def __call__(self, opt, args, message):
        if hasattr(opt, 'init') and opt.init != None:
            response = self.init(opt.init)
            return str(response)
        elif hasattr(opt, 'newmessage') and opt.newmessage != None:
            response = self.newmessage(message)
            return str(response)
