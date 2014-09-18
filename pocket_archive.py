import datetime
import os
import time
import copy

from pocketpy.auth import auth
from pocketpy.jsonconfig import JsonConfig
from pocketpy.pocket import retrieve
from pocketpy.tags import add_tags
from pocketpy.pocket import modify


JSON_FILE = "pocket_json/1375544032.json"

def is_old(item, last_ts):
    return int(item['time_updated']) < last_ts


def get_old_items(items, last_ts):
    uids = []

    for uid, item in items.iteritems():
        if is_old(item, last_ts):
            uids.append(uid)
        # get a word count from each item
        #word_count = item.get('word_count', None)
        #if not word_count:
            #continue
        #word_count = long(word_count)

    return uids

def archive_action(creds, item_ids, action):
    if len(item_ids) <= 0:
        return
    actions = []

    for item_id in item_ids:
        action_obj = {"action": action, "item_id": item_id}
        actions.append(action_obj)

    config["actions"] = actions
    response = modify(config)
    body = response.json()
    assert(body["status"] == 1)

def archive(credentials, uids):
    archive_action(credentials, uids, "archive")
    return

if __name__ == "__main__":
    delta = datetime.timedelta(days=100)
    last_ts = long(time.mktime((datetime.datetime.now() - delta).timetuple()))

    # get old item ids from json
    jc = JsonConfig(JSON_FILE)
    items = jc.read()
    old_item_uids = get_old_items(items, last_ts)

    # tag old items, and archive
    config = auth({})
    credentials = copy.deepcopy(config)
    add_tags(credentials, old_item_uids, ["old-unread"])
    print "Tagged %d articles" % len(old_item_uids)

    credentials = copy.deepcopy(config)
    archive(credentials, old_item_uids)

