#!/usr/bin/python
#coding=utf8

import sys
import StringIO
import xmpp

import commands

def messageCB(conn,mess):
    text=mess.getBody()
    print 'Got Message:', text
    user=mess.getFrom()
    reply = StringIO.StringIO()
    message = mess.getBody()
    email = '%s@%s' % (user.node, user.domain)
    cmd = message.split('||', 1)[0]
    message = message.replace(cmd, '', 1)
    app = cmd.split(' ')[0]
    if not hasattr(commands, app):
        for name,parser in commands.CMDS.items():
            print >>reply, '%s -h' % name
    else:
        appparser, apprunner = commands.CMDS[app]
        bakup = sys.stdout
        sys.stdout = reply
        try:
            cmd += ' '
            appopt, apparg = appparser.parse_args(cmd.encode('utf8').split(' '))
            apprunner(email)(appopt, apparg, message)
        except SystemExit:
            pass
        finally:
            sys.stdout = bakup
    if reply: conn.send(xmpp.Message(mess.getFrom(),reply.getvalue()))

def presenceCB(conn, msg):
    print unicode(msg)
    prs_type=msg.getType()
    who=msg.getFrom()
    if prs_type == "subscribe":
        conn.send(xmpp.Presence(to=who, typ='subscribed'))
        conn.send(xmpp.Presence(to=who, typ='subscribe'))


def StepOn(conn):
    try:
        conn.Process(1)
    except KeyboardInterrupt: return 0
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

    
