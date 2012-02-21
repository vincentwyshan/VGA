#coding=utf8

from sina import SinaWeibo
from weather import Weather

from optparse import *

sina = OptionParser(usage='sina options')
sina.add_option('-i', help='''initialize sina weibo...''', dest='init', default=None)
#sina.add_option('-r', help='''reply @someone''', dest='reply')
#sina.add_option('-m', help='''mentions''', dest='mentions')
#sina.add_option('-c', help='''comments''', dest='comments')
#sina.add_option('-u', help='''unread messages''', dest='unread')
sina_newmessage = OptionGroup(sina, 'Sina newmessage')
sina_newmessage.add_option('-n', help='''new microblog''', dest='newmessage')
sina_newmessage.add_option('-o', '--longitude', help='longitude, number', dest='longitude', default=None)
sina_newmessage.add_option('-a', '--latitude', help='latitude, number', dest='latitude', default=None)
sina.add_option_group(sina_newmessage)

#sina.print_help()

weather = OptionParser(usage='weather options')
weather.add_option('-t', help='''turn [on/off]''', dest='switch')
weather.add_option('-c', help='''city [shanghai/beijing]''', dest='city')

qq = OptionParser(usage='qq options')
qq.add_option('-i', help='''initialize tencent weibo...''', dest='init')

gmail = OptionParser(usage='gmail options')
gmail.add_option('-i', help="initialize gmail...", dest='init')

broadcast = OptionParser(usage='broadcast options')
broadcast.add_option('-n', help="new message to all microblog", dest='newmessage')

CMDS = {
        'sina':(sina, SinaWeibo),
        'weather':(weather, Weather),
        'qq':qq,
        'gmail':gmail,
        'bc':broadcast,
       }
