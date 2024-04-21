# V1版本已弃用，推荐使用V2及以后版本

适用于**江西师范大学**校园网的登录程序

即深澜科技`v2.00`认证系统，修改`main.py`中的请求地址即可切换兼容，但此项目不保证兼容性

算法原作者：[huxiaofan1223/jxnu_srun](https://github.com/huxiaofan1223/jxnu_srun)

## 使用说明

### 首次使用

运行程序时，若配置文件不存在，程序会在所在目录下生成`userinfo.json`文件，用于存储配置信息，其默认结构如下

```json
{
    "username": "登录用户名",
    "password": "登录密码",
    "domain": "登录域"
}
```

需要填写其中的`username`，`password`和`domain`字段，其中`domain`字段可为以下四种，根据账户实际情况填写：

- `cucc`：中国联通
- `cmcc`：中国移动
- `ctcc`：中国电信
- `jxnu`：校园宽带

### 正常使用

正确填写配置文件后直接运行程序即可

### 命令行操作

- `-h`：显示命令行参数帮助
- `-c`,`--config`：配置文件路径，默认路径为`./userinfo.json`
- `-u`,`--username`：覆盖配置文件中的用户名
- `-p`,`--password`：覆盖配置文件中的密码
- `-d`,`--domain`：覆盖配置文件中的登录域
- `-m`,`--mode`：运行模式，默认为`login`
    - `login`：常规登录流程
    - `logout`：注销账户（**只能注销经由此程序登录的账户**）

