import json
import os, sys
import os.path as ospath

global file_path
config_name = "userinfo.json"
if getattr(sys, 'frozen', False):
    file_path = ospath.join(os.path.dirname(sys.executable), config_name)
else:
    file_path = ospath.join(ospath.dirname(__file__), '..', config_name)


def change_config_path(path: str):
    global file_path
    file_path = path


class Config:
    """
    配置类
    """

    def __init__(self):
        self.username = ""  # 学号
        self.password = ""  # 密码
        self.domain = ""  # 网络类型

    def record_config(self, path: str = file_path):
        """
        写入配置文件
        """
        with open(path, 'w', encoding='utf8') as conf:
            json.dump(self.__dict__, conf, indent=2)

    def init_getconf(self, path: str = file_path) -> bool:
        """
        读取配置文件
        """
        if not ospath.isfile(path):  # 配置文件不存在时自动生成配置文件
            self.record_config(path)
            return False
        with open(path, 'r', encoding='utf8') as conf:
            try:
                self.__dict__ = json.load(conf)
            except Exception:
                return False
        return True

    def get_dict(self):
        return self.__dict__


config = Config()
