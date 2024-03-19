import requests
import time
import re
from encryption import *
from utils.config import config
from utils.notify import send_notification

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
}

# 请求地址
init_url = "http://172.16.8.8/srun_portal_pc?ac_id=1&theme=pro"
get_challenge_api = "http://172.16.8.8/cgi-bin/get_challenge"
srun_portal_api = "http://172.16.8.8/cgi-bin/srun_portal"

n = '200'
type = '1'
ac_id = '1'
enc = "srun_bx1"


def get_chksum():
    chkstr = token + config.username
    chkstr += token + hmd5
    chkstr += token + ac_id
    chkstr += token + ip
    chkstr += token + n
    chkstr += token + type
    chkstr += token + i
    return chkstr


def get_info():
    info_temp = {
        "username": config.username,
        "password": config.password,
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


def get_token():
    print("获取token")
    global token
    get_challenge_params = {
        "callback": "jQuery112404953340710317169_" + str(int(time.time() * 1000)),
        "username": config.username,
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
    hmd5 = get_md5(config.password, token)
    chksum = get_sha1(get_chksum())
    print("所有加密工作已完成")


def login():
    srun_portal_params = {
        'callback': 'jQuery11240645308969735664_' + str(int(time.time() * 1000)),
        'action': 'login',
        'username': config.username,
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
    print("登录操作完成")
    send_notification("登录成功", f"{config.username}已登录")
    return True


def logout():
    srun_portal_params = {
        'callback': 'jQuery112405732556458913045_' + str(int(time.time() * 1000)),
        'action': 'logout',
        'username': config.username,
        'ip': ip,
        'ac_id': ac_id,
        '_': int(time.time() * 1000)
    }
    srun_portal_res = requests.get(srun_portal_api, params=srun_portal_params, headers=header)
    print(srun_portal_res.text)
    print("注销操作完成")
    send_notification("注销成功", f"{config.username}已注销")
    return True


def init():
    init_getip()
    get_token()
    do_complex_work()


def do_request(op: int = 0) -> bool:
    """
    执行网络请求
    :param op: 0为登录，1为注销
    :return: 是否成功
    """
    try:
        init()
        if op == 1:
            return logout()
        else:
            return login()
    except Exception as e:
        send_notification("网络请求失败", "请检查网络连接")
