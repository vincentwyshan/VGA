#coding=utf8

from sina import SinaWeibo

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

CMDS = {
        'sina':(sina, SinaWeibo),
        'weather':weather,
        'qq':qq,
       }
