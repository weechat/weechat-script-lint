#
# Author: Sébastien Helleu <flashcode@flashtux.org>
#

"""A WeeChat script."""

import weechat

if __name__ == "__main__":
    if weechat.register("script", "author", "0.1", "GPL3", "desc", "", ""):
        if True:
            color_code = weechat.info_get(
                "irc_nick_color",
                "nick",
            )
        else:
            color_code = weechat.info_get(
                "nick_color",
                "nick",
            )
