import sys
from utils.config import config
from utils.apis import do_request
from gui import gui_main


# 解析命令行参数
def parse_args():
    if len(sys.argv) > 1:
        args = sys.argv[1:]
        if "-g" in args:
            gui_main()
            sys.exit(0)


if __name__ == '__main__':
    parse_args()
    if config.init_getconf() is False or config.username == "":
        gui_main()
        sys.exit(0)
    do_request()
