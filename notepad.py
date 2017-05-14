#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import getpass
import logging
import logging.handlers
import os
import pickle
import OpenReports
import requests
import json as js

import chatexchange.client
import chatexchange.events

hostID = 'stackoverflow.com'
roomID = '111347'
selfID = 7829893
filename = ',notepad'
apiUrl = 'http://reports.socvr.org/api/create-report'

helpmessage = \
        '    o, open:                    Open all reports not on ignore list\n' + \
        '    `number` [b[back]]:         Open up to `number` reports, fetch from the back of the list if b or back is present\n' + \
        '    ir, ignore rest:            Put all unhandled reports from you last querry on your ignore list\n' + \
        '    fa, fetch amount:           Display the number of unhandled reports\n' + \
        '    dil, delete ignorelist:     Delete your ignorelist\n' + \
        '    commands:                   Print this help'

def _parseMessage(msg):
    temp = msg.split()
    return ' '.join(temp[1:]).lower()

def buildReport(notepad):
    ret = {'botName' : 'Notepad'}
    posts = []
    for i, v in enumerate(notepad, start=1):
        posts.append([{'id':'idx', 'name':'Message Index', 'value':i},
            {'id':'msg', 'name':'Message', 'value':v}])
    ret['posts'] = posts
    return ret

def handleCommand(message, command, uID):
    words = command.split()
    try:
        f = open(str(uID) + filename, 'rb')
        currNotepad = pickle.load(f)
    except:
        currNotepad = []
    if words[0] == 'add':
        currNotepad.append(''.join(words[1:]))
    if words[0] == 'rm':
        which = int(words[1])
        if which > len(currNotepad):
            message.message.reply('Item does not exist.')
        del currNotepad[which - 1]
    if words[0] == 'rma':
        currNotepad = []
    if words[0] == 'show':
        if not currNotepad:
            message.message.reply('You have no saved messages.')
            return
        report = buildReport(notepad)
        r = requests.post(apiUrl, data=js.dumps(report))
        r.raise_for_status()
        message.message.reply('Opened your notepad [here](%s).'%r.text)
        return
    f = open(uID + filename, 'wb')
    pickle.dump(currNotepad, f)
        
def onMessage(message, client):
    if isinstance(message, chatexchange.events.MessagePosted) and message.content in ['🚂', '🚆']:
        message.room.send_message('🚃 by notepad')
        return

    amount = None
    fromTheBack = False
    try:
        if message.target_user_id != selfID:
            return
        userID = message.user.id
        command = _parseMessage(message.content)
        if command == 'reboot notepad':
            os._exit(1)
        if command in ['a', 'alive']:
            message.message.reply('[notepad] Yes.')
            return
        if command == 'commands':
            message.room.send_message(helpmessage)
            return
    except:
        return
    
    handleCommand(messagem command, userID)

if 'ChatExchangeU' in os.environ:
    email = os.environ['ChatExchangeU']
else:
    email = input("Email: ")
if 'ChatExchangeP' in os.environ:
    password = os.environ['ChatExchangeP']
else:
    password = input("Password: ")

client = chatexchange.client.Client(hostID)
client.login(email, password)
print('Logged in')

room = client.get_room(roomID)
room.join()
print('Joined room')
room.send_message('[notepad] Hi o/')

watcher = room.watch(onMessage)
watcher.thread.join()


client.logout()

