#! /usr/bin/python
# -*- coding: utf-8 -*-
#'''
#reference   :   http://zys-free.com/wordpress/?p=244
#'''
#
#from urllib import quote, urlencode
#import urllib
#import urllib2
#import time
#import uuid
#import hmac, hashlib
#
#APP_KEY = '2622175870' #写自己的
#APP_SECRET = 'da083eeca1f6aef7bc2381f20a9b2a3b'
#
#def get_token():
#    'get request token and request secret'
#    #visit here:
#    #http://api.t.sina.com.cn/oauth/authorize?oauth_token={token}&oauth_callback={callback}
#    URL = 'http://api.t.sina.com.cn/oauth/request_token'
#
#    params = [
#        ('oauth_consumer_key', APP_KEY),
#        ('oauth_nonce', uuid.uuid4().hex),
#        ('oauth_signature_method', 'HMAC-SHA1'),
#        ('oauth_timestamp', int(time.time())),
#        ('oauth_version', '1.0'),
#    ]
#
#    params.sort()
#
#    p = 'GET&%s&%s' % (quote(URL, safe=''), quote(urlencode(params)))
#    signature = hmac.new(APP_SECRET + '&', p, hashlib.sha1).digest().encode('base64').rstrip()
#
#    params.append(('oauth_signature', quote(signature)))
#
#    h = ', '.join(['%s="%s"' % (k, v) for (k, v) in params])
#
#    r = urllib2.Request(URL, headers={'Authorization': 'OAuth realm="", %s' % h})
#
#    data = urllib2.urlopen(r).read()
#    token, secret = [pair.split('=')[1] for pair in data.split('&')]
#
#    return token, secret
#
#
#def get_access_token(token, secret, verifier):
#    URI = 'http://api.t.sina.com.cn/oauth/access_token'
#
#    headers = [
#        ('oauth_consumer_key', APP_KEY),
#        ('oauth_nonce', uuid.uuid4().hex),
#        ('oauth_signature_method', 'HMAC-SHA1'),
#        ('oauth_timestamp', int(time.time())),
#        ('oauth_version', '1.0'),
#        ('oauth_token', token),
#        ('oauth_verifier', verifier),
#        ('oauth_token_secret', secret),
#    ]
#
#    headers.sort()
#
#    p = 'POST&%s&%s' % (quote(URI, safe=''), quote(urlencode(headers)))
#    signature = hmac.new(APP_SECRET + '&' + secret, p, hashlib.sha1).digest().encode('base64').rstrip()
#
#    headers.append(('oauth_signature', quote(signature)))
#
#    h = ', '.join(['%s="%s"' % (k, v) for (k, v) in headers])
#
#    r = urllib2.Request(URI, headers={'Authorization': 'OAuth realm="", %s' % h})
#
#    data = urllib2.urlopen(r, data='').read()
#    token, secret, user_id = [pair.split('=')[1] for pair in data.split('&')]
#
#    return token, secret, user_id
#
#
#def get_info(token, secret):
#    URI = 'http://api.t.sina.com.cn/account/verify_credentials.json'
#
#    headers = [
#        ('oauth_consumer_key', APP_KEY),
#        ('oauth_nonce', uuid.uuid4().hex),
#        ('oauth_signature_method', 'HMAC-SHA1'),
#        ('oauth_timestamp', int(time.time())),
#        ('oauth_version', '1.0'),
#        ('oauth_token', token)
#    ]
#
#    headers.sort()
#
#    p = 'POST&%s&%s' % (quote(URI, safe=''), quote(urlencode(headers)))
#    signature = hmac.new(APP_SECRET + '&' + secret, p, hashlib.sha1).digest().encode('base64').rstrip()
#
#    headers.append(('oauth_signature', quote(signature)))
#
#    h = ', '.join(['%s="%s"' % (k, v) for (k, v) in headers])
#
#    r = urllib2.Request(URI, data='', headers={'Authorization': 'OAuth realm="", %s' % h})
#
#    data = urllib2.urlopen(r).read()
#    return data
#
#def get_timeline(access_token, count, page):
#    URI = 'https://api.weibo.com/2/statuses/public_timeline.json'
#
#    request = urllib2.Request(URI, data=urllib.urlencode({'access_token':access_token}))
#
#    data = urllib2.urlopen(request).read()
#    print data
#    return data
#
#
#
##if __name__ == '__main__':
##    print get_access_token('0a426d1b8695df7888c0b79d77c2071c',
##                           '77764447cbdd856463b3198c935bad41',
##                           '601738')
##
##if __name__ == '__main__':
##    print get_token()



from weibopy.auth import OAuthHandler
from weibopy.api import API

APP_KEY = '2622175870' 
APP_SECRET = 'da083eeca1f6aef7bc2381f20a9b2a3b'

BACK_URL = "http://localhost:8080/";

def authorization_url(callback_url=BACK_URL):
    auth = OAuthHandler( APP_KEY, APP_SECRET, callback_url);
    auth_url = auth.get_authorization_url()
    return auth_url, auth.request_token.key, auth.request_token.secret

