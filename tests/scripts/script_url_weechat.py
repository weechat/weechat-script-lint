#
# Author: Sébastien Helleu <flashcode@flashtux.org>
#

"""A WeeChat script."""

try:
    import weechat
except ImportError:
    print('This script must be run under WeeChat: http://www.weechat.org')

if __name__ == '__main__':
    if weechat.register('script', 'author', '0.1', 'GPL3', 'desc', '', ''):
        pass
