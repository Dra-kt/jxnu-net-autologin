import sys

import requests
import time
import re
import json
import os.path as ospath
import argparse
from encryption.srun_md5 import *
from encryption.srun_sha1 import *
from encryption.srun_base64 import *
from encryption.srun_xencode import *

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
}
init_url = "http://172.16.8.8/srun_portal_pc?ac_id=1&theme=pro"
get_challenge_api = "http://172.16.8.8/cgi-bin/get_challenge"

srun_portal_api = "http://172.16.8.8/cgi-bin/srun_portal"
n = '200'
type = '1'
ac_id = '1'
enc = "srun_bx1"
config = {
    'username': '',
    'password': '',
    'domain': ''
}


def get_chksum():
    chkstr = token + username
    chkstr += token + hmd5
    chkstr += token + ac_id
    chkstr += token + ip
    chkstr += token + n
    chkstr += token + type
    chkstr += token + i
    return chkstr


def get_info():
    info_temp = {
        "username": username,
        "password": password,
        "ip": ip,
        "acid": ac_id,
        "enc_ver": enc
    }
    i = re.sub("'", '"', str(info_temp))
    i = re.sub(" ", '', i)
    return i


def init_getip():
    global ip
    init_res = requests.get(init_url, headers=header)
    print("初始化获取ip")
    ip = re.search('ip +: "(.*?)",', init_res.text).group(1)
    print("ip:" + ip)


# 写入配置文件
def record_config(path: str):
    global config
    with open(path, 'w', encoding='utf8') as conf:
        json.dump(config, conf, indent=2)


# 读取配置文件
def init_getconf(path: str) -> bool:
    global config, username, password, args
    # 配置文件不存在时自动生成配置文件
    if not ospath.isfile(path):
        record_config(path)
        print("已生成配置文件")
        return False
    with open(path, 'r', encoding='utf8') as conf:
        config = json.load(conf)

    # 命令行覆盖数据
    username = (config['username'] if args.username is None else args.username) + '@' + (
        config['domain'] if args.domain is None else args.domain)
    password = config['password'] if args.password is None else args.password
    return True


def get_token():
    # print("获取token")
    global token
    get_challenge_params = {
        "callback": "jQuery112404953340710317169_" + str(int(time.time() * 1000)),
        "username": username,
        "ip": ip,
        "_": int(time.time() * 1000),
    }
    get_challenge_res = requests.get(get_challenge_api, params=get_challenge_params, headers=header)
    token = re.search('"challenge":"(.*?)"', get_challenge_res.text).group(1)
    print(get_challenge_res.text)
    print("token为:" + token)


def do_complex_work():
    global i, hmd5, chksum
    i = get_info()
    i = "{SRBX1}" + get_base64(get_xencode(i, token))
    hmd5 = get_md5(password, token)
    chksum = get_sha1(get_chksum())
    print("所有加密工作已完成")


def login():
    srun_portal_params = {
        'callback': 'jQuery11240645308969735664_' + str(int(time.time() * 1000)),
        'action': 'login',
        'username': username,
        'password': '{MD5}' + hmd5,
        'ac_id': ac_id,
        'ip': ip,
        'chksum': chksum,
        'info': i,
        'n': n,
        'type': type,
        'os': 'windows+10',
        'name': 'windows',
        'double_stack': '0',
        '_': int(time.time() * 1000)
    }
    # print(srun_portal_params)
    srun_portal_res = requests.get(srun_portal_api, params=srun_portal_params, headers=header)
    print(srun_portal_res.text)


def logout():
    srun_portal_params = {
        'callback': 'jQuery112405732556458913045_' + str(int(time.time() * 1000)),
        'action': 'logout',
        'username': username,
        'ip': ip,
        'ac_id': ac_id,
        '_': int(time.time() * 1000)
    }
    srun_portal_res = requests.get(srun_portal_api, params=srun_portal_params, headers=header)
    print(srun_portal_res.text)


def parseArg():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", type=str, default="./userinfo.json", help="配置文件路径")
    parser.add_argument("-m", "--mode", type=str, default="login", help="运行模式")
    parser.add_argument("-u", "--username", type=str, help="用户名")
    parser.add_argument("-p", "--password", type=str, help="密码")
    parser.add_argument("-d", "--domain", type=str, help="登录域")
    args = parser.parse_args()


if __name__ == '__main__':
    global args
    parseArg()
    if init_getconf(args.config) is False:
        sys.exit(0)
    init_getip()
    if args.mode == "login":
        get_token()
        do_complex_work()
        login()
    elif args.mode == 'logout':
        logout()
    elif args.mode == 'relogin':
        logout()
        time.sleep(3)
        get_token()
        do_complex_work()
        login()
    else:
        raise Exception('不支持的运行模式')
    record_config(args.config)
