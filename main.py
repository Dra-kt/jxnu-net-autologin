from utils.config import config
from utils.apis import do_request
from gui import gui_main

if __name__ == '__main__':
    if config.init_getconf() is False or config.username == "":
        gui_main()
        exit(0)
    do_request()
