import os
import sys
import json
import hashlib
import base64

import gi
gi.require_version('Notify', '0.7')
from gi.repository import Notify

import mjs
import mapper


class PrioAndroid:
    MIN = -2
    LOW = -1
    DEFAULT = 0
    HIGH = 1
    MAX = 2


urgency_mapping = {
    PrioAndroid.MIN     : Notify.Urgency.LOW,
    PrioAndroid.LOW     : Notify.Urgency.LOW,
    PrioAndroid.DEFAULT : Notify.Urgency.LOW,
    PrioAndroid.HIGH    : Notify.Urgency.NORMAL,
    PrioAndroid.MAX     : Notify.Urgency.CRITICAL
}

NOTIFY_DEFAULT_PORT = 8022
NOTIFY_CACHE_DIR   = os.path.expanduser('~/.cache/notify-libnotify/')
NOTIFY_CONFIG_FILE = os.path.expanduser('~/.config/notify-libnotify.conf')

Notify.init('notify-droid')
notifications = {}

mpr = mapper.Mapper()


def notify(uid, summary, body, icon='', urgency=None):
    if uid in notifications:
        notifications[uid].close()

    noti = Notify.Notification.new(summary, body, icon)

    if urgency is not None:
        noti.set_urgency(urgency)
    
    noti.show()

    notifications[uid] = noti
    print('Added notification to stack. New size is: %i' % len(notifications))


@mpr.s_url('/notification/posted/', 'POST')
def notification_posted(payload):
    notification = payload

    uid = notification['packageName'] + str(notification['id'])

    # Get an icon to display
    large_icon_data = notification['largeIcon']['data']
    app_icon_data   = notification['appIcon']['data']
    small_icon_data = notification['smallIcon']['data']

    icon = None
    icon_path = None
    if large_icon_data:
        icon = large_icon_data

    elif app_icon_data:
        icon = app_icon_data

    elif small_icon_data:
        icon = small_icon_data

    icon_path = os.path.join(NOTIFY_CACHE_DIR,
                             hashlib.md5(icon.encode()).hexdigest())

    if not os.path.exists(icon_path):
        with open(icon_path, 'wb') as f:
            f.write(base64.b64decode(icon))

    priority = notification['priority']
    urgancy  = urgency_mapping[priority]

    notify(uid, notification['title'], notification['text'], icon_path, urgancy)

    return {'status_code' : 200}

@mpr.s_url('/notification/removed/', 'POST')
def notification_removed(payload):
    notification = payload

    uid = notification['packageName'] + str(notification['id'])
    if uid in notifications:
        notifications[uid].close()
        del notifications[uid]
        print('Removed notification from stack. New size is: %i' % len(notifications))

    return {'status_code' : 200}

@mpr.s_url('/call/started/', 'POST')
def call_started(payload):
    return {'status_code' : 200}

@mpr.s_url('/call/ended/', 'POST')
def call_ended(payload):
    return {'status_code' : 200}

@mpr.s_url('/call/missed/', 'POST')
def call_missed(payload):
    return {'status_code' : 200}


def _get_cli_port():
    try:
        port = int(sys.argv[1])
    except:
        port = None

    return port

def _get_conf_port():
    user_conf = None
    if os.path.exists(NOTIFY_CONFIG_FILE):
        with open(NOTIFY_CONFIG_FILE, 'r') as f:
            try:
                user_conf = json.loads(f.read())
            except:
                print('Failed parsing config at "%s"' % NOTIFY_CONFIG_FILE)
                pass

    port = None
    if user_conf and 'port' in user_conf:
        try:
            port = int(user_conf['port'])
        except:
            pass

    return port

def main():
    port = _get_cli_port()

    if not port:
        port = _get_conf_port()
    
    if not port:
        print('No port provided, reverting to default "%i"'
              % NOTIFY_DEFAULT_PORT)
        port = NOTIFY_DEFAULT_PORT

    if not os.path.exists(NOTIFY_CACHE_DIR):
        os.makedirs(NOTIFY_CACHE_DIR)

    conf = mjs.Config()
    conf.address = '0.0.0.0'
    conf.port = port

    server = mjs.ThreadedServer(conf)

    # Start the server
    print('Server running: %s:%s' % (conf.address, conf.port))
    print('use ctrl+c to exit')
    try:
        server.serve_forever()

    except KeyboardInterrupt:
        print('Server closed...')

if __name__ == '__main__':
    main()
