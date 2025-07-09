import os
import sys

import customtkinter as ctk
import socket
import uuid
import psutil
import platform
import pyperclip
import tomli as tomllib
from tkinter import messagebox

def get_app_metadata():
  try:
    # 获取当前文件所在目录（兼容 .exe）
    if getattr(sys, 'frozen', False):  # 打包后
      base_path = sys._MEIPASS
    else:  # 脚本执行
      base_path = os.path.dirname(__file__)

    pyproject_path = os.path.join(base_path, "pyproject.toml")

    with open(pyproject_path, "rb") as f:
      data = tomllib.load(f)
      name = data["project"]["name"]
      version = data["project"]["version"]
      return f"{name} v{version}"
  except Exception as e:
    from tkinter import messagebox
    messagebox.showwarning("读取失败", f"读取 pyproject.toml 失败：\n{e}")
    return "本地网络信息查询器"

def get_local_ip():
    for interface, snics in psutil.net_if_addrs().items():
        for snic in snics:
            if snic.family == socket.AF_INET and not snic.address.startswith("127."):
                return snic.address
    return "无法获取 IP"

def get_mac_address():
    mac = uuid.getnode()
    if (mac >> 40) % 2:
        return "MAC 地址可能是虚拟的或无效"
    return ':'.join(f'{(mac >> i) & 0xff:02x}' for i in range(40, -1, -8)).upper()

def refresh_info():
    global current_ip, current_mac
    current_ip = get_local_ip()
    current_mac = get_mac_address()
    os = platform.system()

    ip_label.configure(text=f"🌐 内网 IP: {current_ip}")
    mac_label.configure(text=f"🔑 MAC 地址: {current_mac}")
    os_label.configure(text=f"🖥️ 操作系统: {os}")

def copy_mac():
    if current_mac and "无效" not in current_mac:
        pyperclip.copy(current_mac)
        messagebox.showinfo("已复制", f"已复制 MAC 地址：{current_mac}")
    else:
        messagebox.showwarning("复制失败", "当前 MAC 地址不可用")

# 设置 UI 风格
ctk.set_appearance_mode("System")  # 可选: "Dark" / "Light"
ctk.set_default_color_theme("blue")

# 主窗口
app = ctk.CTk()
app.title(get_app_metadata())
app.geometry("420x400")

# 界面元素
title_label = ctk.CTkLabel(app, text="📡 本地网络信息", font=("Arial", 20))
title_label.pack(pady=12)

# 操作系统
os_label = ctk.CTkLabel(app, text="")
os_label.pack(pady=4)

# 局域网地址
ip_label = ctk.CTkLabel(app, text="")
ip_label.pack(pady=4)

# mac地址
mac_label = ctk.CTkLabel(app, text="")
mac_label.pack(pady=4)

# 内存大小
memory_label = ctk.CTkLabel(app, text="")
memory_label.pack(pady=4)

# 磁盘大小
disk_label = ctk.CTkLabel(app, text="", justify="left")
disk_label.pack(pady=4)

# 获取内存信息
virtual_mem = psutil.virtual_memory()
total_memory_gb = virtual_mem.total / (1024 ** 3)
memory_label.configure(text=f"🧠 内存容量: {total_memory_gb:.2f} GB")

# 获取磁盘信息
disk_text_lines = []
for part in psutil.disk_partitions():
  try:
    usage = psutil.disk_usage(part.mountpoint)
    total_gb = usage.total / (1024 ** 3)
    free_gb = usage.free / (1024 ** 3)
    disk_text_lines.append(f"💾 {part.device}  {total_gb:.1f} GB / 空闲 {free_gb:.1f} GB")
  except PermissionError:
    continue  # 某些系统分区会拒绝访问

disk_label.configure(text="\n".join(disk_text_lines))

# 按钮区域
button_frame = ctk.CTkFrame(app)
button_frame.pack(side="bottom", fill="x", pady=10, padx=10)

# 刷新按钮
refresh_button = ctk.CTkButton(button_frame, text="🔄 刷新", command=refresh_info)
refresh_button.pack(side="left", expand=True, fill="x", padx=(0, 5))

# 复制按钮
copy_mac_button = ctk.CTkButton(button_frame, text="📋 复制 MAC", command=copy_mac)
copy_mac_button.pack(side="left", expand=True, fill="x", padx=(5, 0))

# 初始化变量 & 显示内容
current_ip = None
current_mac = None
refresh_info()

app.mainloop()
