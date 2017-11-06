# -*- coding: utf-8 -*-
'''
© 2012-2013 eBay Software Foundation
Authored by: Tim Keefer
Licensed under CDDL 1.0
'''

import os
import sys
from optparse import OptionParser

sys.path.insert(0, '%s/../' % os.path.dirname(__file__))

from common import dump

import ebaysdk
from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError


def init_options():
    usage = "usage: %prog [options]"
    parser = OptionParser(usage=usage)

    parser.add_option("-d", "--debug",
                      action="store_true", dest="debug", default=False,
                      help="Enabled debugging [default: %default]")
    parser.add_option("-y", "--yaml",
                      dest="yaml", default='ebay.yaml',
                      help="Specifies the name of the YAML defaults file. [default: %default]")
    parser.add_option("-a", "--appid",
                      dest="appid", default=None,
                      help="Specifies the eBay application id to use.")
    parser.add_option("-c", "--consumer_id",
                      dest="consumer_id", default=None,
                      help="Specifies the eBay consumer_id id to use.")

    (opts, args) = parser.parse_args()
    return opts, args


def getIds(itemList):
    for x in itemList:
        yield x.itemId

def run(opts):

    try:

        shopping = Finding(debug=opts.debug, appid=opts.appid,
                            config_file=opts.yaml, warnings=False)

        response = shopping.execute('findItemsByKeywords',
                                    {'keywords': 'Python'})

        nodes = response.reply.searchResult.item
#        itemIds = list(getIds(response.reply.searchResult.item))

        for r in nodes:
            print ("ID(%s) TITLE(%s)" % (r.itemId, r.title))

    except ConnectionError as e:
        print(e)
        print(e.response.dict())


if __name__ == "__main__":
    print("FindItem samples for SDK version %s" % ebaysdk.get_version())
    (opts, args) = init_options()
    run(opts)
