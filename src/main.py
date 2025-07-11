import customtkinter as ctk
import os
import sys
import tomllib
from pages.home import HomePage
from pages.donation import DonationPage

def get_app_metadata():
  try:
    base_path = sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.dirname(__file__)
    pyproject_path = os.path.join(base_path, "pyproject.toml")
    with open(pyproject_path, "rb") as f:
      data = tomllib.load(f)
      return f"{data['project']['name']} v{data['project']['version']}"
  except Exception:
    return "本地网络信息查询器"

class App(ctk.CTk):
  def __init__(self):
    super().__init__()

    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    self.title(get_app_metadata())
    self.geometry("420x400")
    self.minsize(420, 400)
    self.resizable(True, True)

    container = ctk.CTkFrame(self, fg_color="transparent")
    container.pack(fill="both", expand=True)
    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)

    self.pages = {}

    for PageClass in (HomePage, DonationPage):  # 未来可以加更多页面
      frame = PageClass(container, self)
      self.pages[PageClass.__name__] = frame
      frame.grid(row=0, column=0, sticky="nsew")

    self.show_page("HomePage")

  def show_page(self, name):
    self.pages[name].tkraise()


if __name__ == "__main__":
  App().mainloop()
