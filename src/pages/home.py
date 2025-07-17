import customtkinter as ctk
import socket
import uuid
import psutil
import platform
import pyperclip
import threading
import os
import requests
import ipaddress
from tkinter import messagebox


def get_public_ip() -> str:
  proxies = {
    "http": os.environ.get("HTTP_PROXY"),
    "https": os.environ.get("HTTPS_PROXY")
  }
  try:
    r = requests.get("https://api.ipify.org", proxies=proxies, timeout=5)
    r.raise_for_status()
    return r.text
  except Exception as e:
    print(f"获取公网 IP 失败: {e}")
    return "获取失败"


def get_os_info() -> str:
  if platform.system() == "Windows":
    version, _, build, _ = platform.win32_ver()
    return f"Windows {version} (Build {build})"
  else:
    return f"{platform.system()} {platform.release()}"


def get_mac_address() -> str:
  mac = uuid.getnode()
  if (mac >> 40) % 2:
    return "MAC 地址可能是虚拟的或无效"
  return ':'.join(f'{(mac >> i) & 0xff:02x}' for i in range(40, -1, -8)).upper()


def get_local_ipv6() -> str:
  for _, snics in psutil.net_if_addrs().items():
    for snic in snics:
      if snic.family == socket.AF_INET6 and not snic.address.startswith("::1"):
        return snic.address.split('%')[0]
  return "-"

def is_trusted_private_ip(ip: str) -> bool:
  try:
    addr = ipaddress.ip_address(ip)
    # 只允许 192.168.x.x 或 10.x.x.x
    return (
      addr.is_private and
      (ip.startswith("192.168.") or ip.startswith("10."))
    )
  except ValueError:
    return False

def get_local_ip() -> str:
  for iface_name, snics in psutil.net_if_addrs().items():
    for snic in snics:
      if snic.family == socket.AF_INET:
        ip = snic.address
        if is_trusted_private_ip(ip):
          return ip
  return "无法获取 IP"

class HomePage(ctk.CTkFrame):
  def __init__(self, parent, controller):
    super().__init__(parent)
    self.default_font = ctk.CTkFont(family=("PingFang SC", "Microsoft YaHei", "SimHei"), size=14)

    self.controller = controller
    self.current_ip = None
    self.current_mac = None

    # 主布局
    title_label = ctk.CTkLabel(self, text="📡 本地网络信息", font=self.default_font)
    title_label.pack(pady=12)

    self.os_label = ctk.CTkLabel(self, text="", font=self.default_font)
    self.os_label.pack(pady=4)

    self.public_label = ctk.CTkLabel(self, text="", font=self.default_font)
    self.public_label.pack(pady=4)

    self.ip_label = ctk.CTkLabel(self, text="", font=self.default_font)
    self.ip_label.pack(pady=4)

    self.ipv6_label = ctk.CTkLabel(self, text="", font=self.default_font)
    self.ipv6_label.pack(pady=4)

    self.mac_label = ctk.CTkLabel(self, text="", font=self.default_font)
    self.mac_label.pack(pady=4)

    self.memory_label = ctk.CTkLabel(self, text="", font=self.default_font)
    self.memory_label.pack(pady=4)

    self.disk_label = ctk.CTkLabel(self, text="", justify="left", font=self.default_font)
    self.disk_label.pack(pady=4)

    # 按钮区域
    button_frame = ctk.CTkFrame(self)
    button_frame.pack(side="bottom", fill="x", pady=10, padx=10)

    refresh_button = ctk.CTkButton(button_frame, text="🔄 刷新", font=self.default_font, command=self.refresh_info)
    refresh_button.pack(side="left", expand=True, fill="x", padx=(0, 5))

    copy_mac_button = ctk.CTkButton(button_frame, text="📋 复制 MAC", font=self.default_font, command=self.copy_mac)
    copy_mac_button.pack(side="left", expand=True, fill="x", padx=(5, 0))

    donate_button = ctk.CTkButton(button_frame, text="❤️ 捐助支持", font=self.default_font, command=lambda: self.controller.show_page("DonationPage"))
    donate_button.pack(side="left", expand=True, fill="x", padx=(5, 0))

    self.refresh_info()

  def copy_mac(self):
    if self.current_mac and "无效" not in self.current_mac:
      pyperclip.copy(self.current_mac)
      messagebox.showinfo("已复制", f"已复制 MAC 地址：{self.current_mac}")
    else:
      messagebox.showwarning("复制失败", "当前 MAC 地址不可用")

  def refresh_info(self):
    self.public_label.configure(text="📡 公网 IP: 正在获取...")

    def worker():
      ip = get_public_ip()
      self.public_label.after(0, lambda: self.public_label.configure(text=f"📡 公网 IP: {ip}"))

    threading.Thread(target=worker, daemon=True).start()

    self.current_ip = get_local_ip()
    self.current_mac = get_mac_address()
    current_ipv6 = get_local_ipv6()
    os_info = get_os_info()

    self.ip_label.configure(text=f"🌐 内网 IP: {self.current_ip}")
    self.ipv6_label.configure(text=f"🌀 内网 IPv6: {current_ipv6}")
    self.mac_label.configure(text=f"🔑 MAC 地址: {self.current_mac}")
    self.os_label.configure(text=f"🖥️ 操作系统: {os_info}")

    total_mem = round(psutil.virtual_memory().total / (1024 ** 3))
    self.memory_label.configure(text=f"🧠 内存容量: {total_mem} GB")

    disk_lines = []
    for part in psutil.disk_partitions():
      try:
        usage = psutil.disk_usage(part.mountpoint)
        total = usage.total / (1024 ** 3)
        free = usage.free / (1024 ** 3)
        disk_lines.append(f"💾 {part.device}  {total:.1f} GB / 空闲 {free:.1f} GB")
      except PermissionError:
        continue

    self.disk_label.configure(text="\n".join(disk_lines))
