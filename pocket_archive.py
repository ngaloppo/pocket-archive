import datetime
import time
import copy

from pocketpy.auth import auth
from pocketpy.jsonconfig import JsonConfig
from pocketpy.tags import add_tags
from pocketpy.pocket import modify

import argparse

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


def parse_options():

    parser = argparse.ArgumentParser(description='Auto-archive Pocket items')
    parser.add_argument('json', help='Pocket items JSON (retrieved with pocket_to_json.py')
    parser.add_argument('--archive', action='store_true', default=False,
                        help='Effectively archive old items')
    parser.add_argument('--days', default=100, type=int,
                        help='Number of days to archive')

    args = parser.parse_args()

    return args

if __name__ == "__main__":
    args = parse_options()

    delta = datetime.timedelta(days=args.days)
    last_ts = long(time.mktime((datetime.datetime.now() - delta).timetuple()))

    # get old item ids from json
    jc = JsonConfig(args.json)
    items = jc.read()
    old_item_uids = get_old_items(items, last_ts)

    print "Found {} old items out of {} in the Pocket reading list...".format(len(old_item_uids), len(items))

    if args.archive:
        # tag old items, and archive
        print "Tagging %d articles..." % len(old_item_uids)
        config = auth({})
        credentials = copy.deepcopy(config)
        add_tags(credentials, old_item_uids, ["old-unread"])

        print "Archiving %d articles" % len(old_item_uids)
        credentials = copy.deepcopy(config)
        archive(credentials, old_item_uids)
    else:
        print "Use --archive to effectively archive these items"
