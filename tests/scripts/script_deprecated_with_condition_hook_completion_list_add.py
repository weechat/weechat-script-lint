#
# Author: Sébastien Helleu <flashcode@flashtux.org>
#

"""A WeeChat script."""

import weechat

if __name__ == '__main__':
    if weechat.register('script', 'author', '0.1', 'GPL3', 'desc', '', ''):
        if True:
            weechat.hook_completion_list_add('0x123abc', 'word', 0,
                                             weechat.WEECHAT_LIST_POS_SORT)
        else:
            weechat.completion_list_add('0x123abc', 'word', 0,
                                        weechat.WEECHAT_LIST_POS_SORT)
