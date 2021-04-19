#!/usr/bin/env python3
#
# Author: Sébastien Helleu
#

"""A WeeChat script."""

import sys

try:
    import weechat
except ImportError:
    print('This script must be run under WeeChat: http://www.weechat.org')

if __name__ == '__main__':
    if weechat.register('script', 'author', '0.1', 'GPL3', 'desc', '', ''):
        infolist = weechat.infolist_get('buffer', '', '')
        python2_bin = weechat.info_get('python2_bin', '')
        sys.exit(1)
