# -*- coding: utf-8 -*-

"""Open ssh connection to site from ansible-server."""

from albertv0 import *
import json
import urllib.request
import os

__iid__ = "PythonInterface/v0.1"
__prettyname__ = "AnsibleServerSites"
__version__ = "1.0"
__trigger__ = "a "
__author__ = "Stanislav Popov"
__dependencies__ = []

iconPath = os.path.dirname(__file__)+"/gnome-terminal.svg"

sites_json_url = 'https://dev.viasite.ru/sites.json'
r = urllib.request.urlopen(sites_json_url)
sites_json = json.loads(r.read())

def handleQuery(query):
    if query.isTriggered:
        item = Item(id=__prettyname__, icon=iconPath, completion=query.rawString)
        stripped = query.string.strip()

        if stripped == '':
            item.text = "Enter site domain or host name"
            return item
        else:
            items = getSitesItems(query)
            if len(items) == 0:
                item.text = "Site not found"
                return item
            return items

def getSitesItems(query):
    q = query.string

    matched = [s for s in sites_json['sites'] if q in s['domain'] or q in s['host']]

    items = []

    for site in matched:
        user_host = '%s@%s' % (site['user'], site['host'])
        items.append(
            Item(
                id = __prettyname__,
                icon = iconPath,
                text = site['domain'],
                subtext = site['host'],
                actions = [
                    ProcAction(
                        text="Open terminal",
                        commandline=['gnome-terminal', '--', 'ssh', user_host] #.extend(site['ssh_command'].split(' '))
                    )
                ]
            )
        )

    return items
