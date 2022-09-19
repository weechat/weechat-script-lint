#!/usr/bin/env python3
#
# Author: Sébastien Helleu
#

"""A WeeChat script."""

import sys

try:
	    import weechat
except ImportError:
	    print("This script must be run under WeeChat: http://www.weechat.org")

if __name__ == "__main__":
    if weechat.register("script", "author", "0.1", "GPL3", "desc", "", ""):
        infolist = weechat.infolist_get("buffer", "", "")
        python2_bin = weechat.info_get("python2_bin", "")
        weechat.hook_completion_get_string("0x123abc", "base_command")
        weechat.hook_completion_list_add("0x123abc", "word", 0,
                                         weechat.WEECHAT_LIST_POS_SORT)
        color_code = weechat.info_get("irc_nick_color", "nick")
        color_name = weechat.info_get("irc_nick_color_name", "nick")
        weechat.hook_modifier("irc_in_privmsg", "callback", "")
        weechat.hook_signal("*,irc_out_privmsg", "callback", "")
        weechat.hook_signal("*,irc_outtags_privmsg", "callback", "")
        sys.exit(1)
