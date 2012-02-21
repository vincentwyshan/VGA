#coding=utf8
'''
reference: yahoo weather 
'''

import user
import datetime
import time

from lxml import etree

import basis
log = basis.getlogger(__name__)


class Weather(object):
    data = {}
    def __init__(self, email):
        self.email = email

    def switch(self, sig, city=None):
        if sig == 'on':
            user.update_app('weather', self.email, city=city)
            return 'Turn on succed'
        elif sig == 'off':
            user.delete_app('weather', self.email)
            return 'Turn off succed'
        else:
            return "unknown option [%s]" % sig

    def forecast(self):
        info = user.get_app('weather', self.email)
        if not info:
            return
        recently_send = info.get('recently_send')
        log.debug('recently send: %s' % str(recently_send))
        if recently_send and type(recently_send) in (str, unicode):
            r = time.strptime(recently_send, '%Y-%m-%d')
            recently_send = datetime.date(r.tm_year, r.tm_mon, r.tm_mday)
        if recently_send == datetime.date.today():
            return
        city = info.get('city')
        forecast = self._get_weather(city)
        result = ''
        if not forecast:
            return result
        for f in forecast:
            result += u'%(day_of_week)s: High[%(high)s], Low[%(low)s], Condition[%(condition)s]\n' % f
        user.update_app('weather', self.email, recently_send=datetime.date.today())
        return result

    def __call__(self, opt, args, message):
        return self.switch(opt.switch, opt.city)

    @classmethod
    def _get_weather(cls, city):
        '''
        >>> Weather._get_weather('shanghai') is not None
        True
        '''
        import datetime
        today = datetime.date.today()
        for k in list(cls.data.keys()):
            if not k == today:
                cls.data.pop(k)
        if not today in cls.data:
            cls.data[today] = dict()
        if not cls.data[today].get(city):
            cls.data[today][city] = []
            api_uri = 'http://www.google.com/ig/api?weather=%s' % city
            response = etree.parse(api_uri)
            forecasts = response.findall('//forecast_conditions')
            for ele in forecasts:
                cls.data[today][city].append( dict(
                        day_of_week = ele.find('day_of_week').attrib.get('data'),
                        condition = ele.find('condition').attrib.get('data'),
                        low = ele.find('low').attrib.get('data'),
                        high = ele.find('high').attrib.get('data')
                    ) )
        return cls.data[today].get(city)

    @classmethod
    def sendall(cls, conn):
        now = datetime.datetime.now()
        if now.hour != 8:
            return
        cursor = user.db.cursor()
        cursor.execute("select email from weather")
        import xmpp
        from xmpp.protocol import JID
        for row in cursor.fetchall():
            result = Weather(row[0]).forecast()
            conn.send(xmpp.Message(JID(row[0]), result))
