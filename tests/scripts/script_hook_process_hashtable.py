#
# Author: Sébastien Helleu <flashcode@flashtux.org>
#

"""A WeeChat script."""

import weechat

if __name__ == "__main__":
    if weechat.register("script", "author", "0.1", "GPL3", "desc", "", ""):
        weechat.hook_process_hashtable("url:http://localhost:1234", {}, 1000, "callback", "")
