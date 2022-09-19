#
# Author: Sébastien Helleu <flashcode@flashtux.org>
#

"""A WeeChat script."""

import weechat

if __name__ == "__main__":
    if weechat.register("script", "author", "0.1", "GPL3", "desc", "", ""):
        if True:
            weechat.hook_completion_get_string("0x123abc", "base_command")
        else:
            weechat.completion_get_string("0x123abc", "base_command")
