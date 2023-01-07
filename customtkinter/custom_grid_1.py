from tkinter import *
import customtkinter

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

root = customtkinter.CTk()  # create CTk window like you do with the Tk window
root.title('Grid_1')
root.geometry("400x240")

for c in range(2): root.columnconfigure(index=c, weight=1)
for r in range(2): root.rowconfigure(index=r, weight=1)

btn1 = customtkinter.CTkButton(master=root, text="button 1")
# columnspan=2 - expand into two columns
btn1.grid(row=0, column=0, columnspan=2, ipadx=6, ipady=6, padx=4, pady=4, sticky=NSEW)

btn3 = customtkinter.CTkButton(master=root, text="button 3")
btn3.grid(row=1, column=0, ipadx=6, ipady=6, padx=5, pady=4, sticky=NSEW)
 
btn4 = customtkinter.CTkButton(master=root, text="button 4")
btn4.grid(row=1, column=1, ipadx=6,  ipady=6, padx=5, pady=4, sticky=NSEW)

if __name__ == '__main__':
    root.mainloop()