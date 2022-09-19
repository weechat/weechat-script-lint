#
# Author: Sébastien Helleu <flashcode@flashtux.org>
#

"""A WeeChat script."""

import weechat

if __name__ == "__main__":
    if weechat.register("script", "author", "0.1", "GPL3", "desc", "", ""):
        infolist = weechat.infolist_get("buffer", "", "")
