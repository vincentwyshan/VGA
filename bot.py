#!/usr/bin/python
#coding=utf8

import sys
import StringIO
import xmpp
import datetime

import commands

import basis
log = basis.getlogger(__name__)

def messageCB(conn,mess):
    text=mess.getBody()
    print 'Got Message:', text
    user=mess.getFrom()
    message = mess.getBody()
    email = '%s@%s' % (user.node, user.domain)
    cmd = message.split('||', 1)[0]
    message = message.replace(cmd, '', 1).strip().strip('||').strip()
    app = cmd.split(' ')[0]
    result = None
    if not hasattr(commands, app):
        reply = StringIO.StringIO()
        for name,parser in commands.CMDS.items():
            print >>reply, '%s -h' % name
        result = reply.getvalue()
    else:
        try:
            appparser, apprunner = commands.CMDS[app]
        except:
            import traceback
            conn.send(xmpp.Message(mess.getFrom(), traceback.format_exc()))
            return
        try:
            cmd += ' ' # send blank cmd
            appopt, apparg = appparser.parse_args(cmd.encode('utf8').split(' '))
            result = apprunner(email)(appopt, apparg, message)
        except SystemExit:
            result = appparser.format_help()
    conn.send(xmpp.Message(mess.getFrom(), result or 'None'))

def presenceCB(conn, msg):
    print unicode(msg)
    prs_type=msg.getType()
    who=msg.getFrom()
    if prs_type == "subscribe":
        conn.send(xmpp.Presence(to=who, typ='subscribed'))
        conn.send(xmpp.Presence(to=who, typ='subscribe'))


def StepOn(conn):
    try:
        conn.Process(1) # block 1 second
    except KeyboardInterrupt: return 0
    now = datetime.datetime.now()
    if now.hour == 8:
        log.debug("send weather...")
        from weather import Weather
        Weather.sendall(conn)
    return 1

def GoOn(conn):
    while StepOn(conn): pass

if len(sys.argv)<3:
    print "Usage: bot.py username@server.net password"
else:
    jid=xmpp.JID(sys.argv[1])
    user,server,password=jid.getNode(),jid.getDomain(),sys.argv[2]

    conn=xmpp.Client(server)#,debug=[])
    conres=conn.connect(server=('talk.google.com',5222) )
    if not conres:
        print "Unable to connect to server %s!"%server
        sys.exit(1)
    if conres<>'tls':
        print "Warning: unable to estabilish secure connection - TLS failed!"
    print user, password
    authres=conn.auth(user,password)
    if not authres:
        print "Unable to authorize on %s - check login/password."%server
        sys.exit(1)
    if authres<>'sasl':
        print "Warning: unable to perform SASL auth os %s. Old authentication method used!"%server
    conn.RegisterHandler('message',messageCB)
    conn.RegisterHandler('presence',presenceCB)
    conn.sendInitPresence()
    print "Bot started."
    GoOn(conn)

    
