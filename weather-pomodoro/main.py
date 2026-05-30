import customtkinter as ctk
from ui.home_page import HomePage

ctk.set_appearance_mode("light")

root = ctk.CTk()
root.geometry("600x1000")
root.title("일기예뽀")
root.minsize(600, 900)

HomePage(root)

root.mainloop()