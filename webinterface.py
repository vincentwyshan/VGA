#/usr/bin/env python
#coding=utf8

import os
import web

#from weibopy.auth import OAuthHandler
#from weibopy.api import API
import oauth

from mako.template import Template
from mako.lookup import TemplateLookup

from weibopy.auth import OAuthHandler
from weibopy.api import API

web.config.debug = False

lookup = TemplateLookup(directories=[os.path.dirname(__file__)])

class sinaindex(object):
    def GET(self):
        web.header('Content-Type', 'text/html')
        template = lookup.get_template('sinaweibo.mako')
        auth_url, session.rtKey[web.ctx.ip], session.rtSec[web.ctx.ip] = oauth.authorization_url('http://localhost:8080/sinaweibo/callback')
        return template.render_unicode(auth_url=auth_url)

class sinacallback:
    def GET(self):
        oauth_token = web.input().oauth_token
        oauth_verifier = web.input().oauth_verifier
        auth = OAuthHandler(oauth.APP_KEY, oauth.APP_SECRET)
        auth.set_request_token(session.rtKey[web.ctx.ip], session.rtSec[web.ctx.ip])
        access_token = auth.get_access_token(oauth_verifier)
        session.atKey[web.ctx.ip] = access_token.key
        session.atSec[web.ctx.ip] = access_token.secret
        raise web.seeother('/sinaweibo/timeline')

class sinatimeline:
    def GET(self):
        auth = OAuthHandler(oauth.APP_KEY, oauth.APP_SECRET)
        auth.setToken(session.atKey[web.ctx.ip], session.atSec[web.ctx.ip])
        api = API(auth)
        unread = api.unread()
        timeline = api.mentions()
        html = '<p>%(id)s. %(user)s created %(created)s: %(text)s -- %(ref)s</p>'
        h_list = []
        for status in timeline:
            weibo = {}
            weibo['id'] = status.id
            weibo['created'] = status.created_at
            weibo['user'] = status.text
            weibo['text'] = status.text
            weibo['source'] = status.source
            weibo['ref'] = ''
            refer = getattr(status, 'retweeted_status', None)
            if refer:
                weibo['ref'] = u'{[%s]%s}'% (refer.user.name, refer.text)
            h_list.append(html % weibo)
        html = ''.join(h_list)
        return html


urls = (
        '/sinaweibo', 'sinaindex',
        '/sinaweibo/callback', 'sinacallback',
        '/sinaweibo/timeline', 'sinatimeline',
    )

app = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore('sessions'),
        initializer={'rtKey': {}, 'rtSec':{},
            'atKey':{},
            'atSec':{},
            })

if __name__ == '__main__':
    app.run()
