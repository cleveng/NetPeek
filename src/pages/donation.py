import customtkinter as ctk
import webbrowser
from PIL import Image
import os


class DonationPage(ctk.CTkFrame):
  def __init__(self, parent, controller):
    super().__init__(parent)
    self.default_font = ctk.CTkFont(family=("PingFang SC", "Microsoft YaHei", "SimHei"), size=14)
    self.controller = controller

    ctk.CTkLabel(self, text="🙏 感谢您的支持", font=self.default_font).pack(pady=12)
    ctk.CTkLabel(self, text="🔗 如果觉得好用，请考虑赞助支持或给个 Star～", font=self.default_font).pack(pady=4)

    image_dir = os.path.join(os.path.dirname(__file__), "../assets")
    wechat_img = ctk.CTkImage(Image.open(os.path.join(image_dir, "wechat_pay.png")), size=(240, 240))

    image_frame = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
    image_frame.pack(pady=10)

    wechat_label = ctk.CTkLabel(image_frame, text="", image=wechat_img)
    wechat_label.grid(row=0, column=0)

    # 按钮区域

    button_frame = ctk.CTkFrame(self)
    button_frame.pack(side="bottom", fill="x", pady=10, padx=10)

    back_btn = ctk.CTkButton(button_frame, text="← 返回首页", font=self.default_font, command=lambda: controller.show_page("HomePage"))
    back_btn.pack(side="left", expand=True, fill="x", padx=(0, 5))

    github_btn = ctk.CTkButton(button_frame, text="⭐ GitHub 项目地址", font=self.default_font, command=lambda: webbrowser.open("https://github.com/cleveng/NetPeek"))
    github_btn.pack(side="left", expand=True, fill="x", padx=(0, 5))
