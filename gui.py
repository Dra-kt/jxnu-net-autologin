import tkinter as tk
from tkinter import ttk
from utils.config import config
from utils.apis import do_request

domain_dict = {
    "电信": "ctcc",
    "移动": "cucc",
    "联通": "cmcc",
    "校园宽带": "jxnu"
}

domain_name = {
    "ctcc": "电信",
    "cucc": "移动",
    "cmcc": "联通",
    "jxnu": "校园宽带"
}

global username_entry, password_entry, type_combobox, root


def save_config():
    config.username = username_entry.get()
    config.password = password_entry.get()
    config.domain = domain_dict.get(type_combobox.get()) or type_combobox.get()
    config.record_config()


def confirm():
    save_config()
    root.destroy()


def read_config():
    if config.init_getconf():
        username_entry.insert(0, config.username)
        password_entry.insert(0, config.password)
        type_combobox.set(domain_name.get(config.domain) or config.domain)


def login_h():
    save_config()
    do_request(0)


def logout_h():
    save_config()
    do_request(1)


def gui_main():
    global username_entry, password_entry, type_combobox, root
    root = tk.Tk()
    root.title("账户设置")

    # 用户名输入框
    username_label = tk.Label(root, text="用户名")
    username_label.grid(row=0, column=0, sticky="w")
    username_entry = tk.Entry(root)
    username_entry.grid(row=0, column=1, sticky="w")

    # 密码输入框
    password_label = tk.Label(root, text="密码")
    password_label.grid(row=1, column=0, sticky="w")
    password_entry = tk.Entry(root)
    password_entry.grid(row=1, column=1, sticky="w")

    # 网络类型选择
    type_label = tk.Label(root, text="网络类型")
    type_label.grid(row=2, column=0, sticky="w")
    type_combobox = ttk.Combobox(root, values=["电信", "移动", "联通", "校园宽带"], width=10)
    type_combobox.grid(row=2, column=1, sticky="w")

    # 相连的三个按钮
    confirm_button = tk.Button(root, text="确认", command=confirm)
    confirm_button.grid(row=3, column=0, sticky="w")
    login_button = tk.Button(root, text="登录", command=login_h)
    login_button.grid(row=3, column=1, sticky="w")
    logout_button = tk.Button(root, text="注销", command=logout_h)
    logout_button.grid(row=3, column=2, sticky="w")

    read_config()

    root.mainloop()


if __name__ == '__main__':
    gui_main()
