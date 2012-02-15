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
sina.add_option('-n', help='''new microblog''', dest='newmessage')

#sina.print_help()

weather = OptionParser(usage='weather options')
weather.add_option('-o', help='''turn on''', dest='turnon')
weather.add_option('-f', help='''turn off''', dest='turnoff')

qq = OptionParser(usage='qq options')
qq.add_option('-i', help='''initialize tencent weibo...''', dest='init')

gmail = OptionParser(usage='gmail options')
gmail.add_option('-i', help="initialize gmail...", dest='init')

toall = OptionParser(usage='toall options')
toall.add_option('-n', help="new message to all microblog", dest='newmessage')

CMDS = {
        'sina':(sina, SinaWeibo),
        'weather':(weather, Weather),
        'qq':qq,
        'gmail':gmail,
        'toall':toall,
       }
