from tkinter import *
import customtkinter

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

root = customtkinter.CTk()  # create CTk window like you do with the Tk window
root.title('Grid')
root.geometry("400x240")

for c in range(3): root.columnconfigure(index=c, weight=1)
for r in range(4): root.rowconfigure(index=r, weight=1)

for r in range(4):
    for c in range(3):
        btn = customtkinter.CTkButton(master=root, text=f"({r},{c})")
        btn.grid(row=r, column=c, ipadx=6, ipady=6, padx=4, pady=4, sticky=NSEW)

if __name__ == '__main__':
    root.mainloop()