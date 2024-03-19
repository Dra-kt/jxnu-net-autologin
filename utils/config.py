import json
import os
import os.path as ospath

os.chdir(os.path.join(os.path.dirname(__file__), ".."))

file_path = "userinfo.json"


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
