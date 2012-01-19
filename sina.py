#coding=utf8

from weibopy.auth import OAuthHandler
from weibopy.api import API

import user

APP_KEY = '2622175870' 
APP_SECRET = 'da083eeca1f6aef7bc2381f20a9b2a3b'

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
        print 'init', verifier_num
        info = user.get(self.email)
        print info.get('request_token')
        if not info.get('request_token'):
            return self.init_1st_step()
        else:
            return self.init_2nd_step(verifier_num)

    def init_1st_step(self):
        auth = OAuthHandler(APP_KEY, APP_SECRET, '')
        auth_url = auth.get_authorization_url()
        user.update_app('sina', self.email, request_token=auth.request_token.key,
                request_secret=auth.request_token.secret)
        return auth_url

    def init_2nd_step(self, verifier_num):
        info = user.get_app('sina', self.email)
        auth = OAuthHandler(APP_KEY, APP_SECRET)
        auth.set_request_token(info.get('request_token'), info.get('request_secret'))
        access = auth.get_access_token(verifier_num)
        user.update_app('sina', self.email, access_token=access.key, access_secret=access.secret)
        return True

    def newmessage(self, message):
        auth = OAuthHandler(oauth.APP_KEY, oauth.APP_SECRET)
        auth.setToken(session.atKey[web.ctx.ip], session.atSec[web.ctx.ip])
        api = API(auth)
        api.update_status(message)
        return True

    def __call__(self, opt, args, message):
        if hasattr(opt, 'init'):
            response = self.init(opt.init)
            if type(response) in (str, unicode):
                print response
            else:
                print ''
