import customtkinter as ctk
import socket
import uuid
import psutil
import platform
import pyperclip
from tkinter import messagebox


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
app.title("本地网络信息查询器")
app.geometry("420x270")

# 界面元素
title_label = ctk.CTkLabel(app, text="📡 本地网络信息", font=("Arial", 20))
title_label.pack(pady=12)

os_label = ctk.CTkLabel(app, text="")
os_label.pack(pady=4)

ip_label = ctk.CTkLabel(app, text="")
ip_label.pack(pady=4)

mac_label = ctk.CTkLabel(app, text="")
mac_label.pack(pady=4)

# 按钮区域
button_frame = ctk.CTkFrame(app)
button_frame.pack(pady=20)

refresh_button = ctk.CTkButton(button_frame, text="🔄 刷新", command=refresh_info)
refresh_button.grid(row=0, column=0, padx=10)

copy_mac_button = ctk.CTkButton(button_frame, text="📋 复制 MAC", command=copy_mac)
copy_mac_button.grid(row=0, column=1, padx=10)

# 初始化变量 & 显示内容
current_ip = None
current_mac = None
refresh_info()

app.mainloop()
