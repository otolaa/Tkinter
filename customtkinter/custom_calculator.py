import tkinter
import tkinter.messagebox
import customtkinter

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

root = customtkinter.CTk()  # create CTk window like you do with the Tk window
root.title('Calculator')
root.geometry("500x310")

for c in range(5): root.columnconfigure(index=c, weight=1)
for r in range(5): root.rowconfigure(index=r, weight=1)

# create main entry and button
font_e = customtkinter.CTkFont(family="Helvetica", size=30, weight='bold')
font_btn = customtkinter.CTkFont(family="Helvetica", size=20, weight='bold')
c_entry = customtkinter.CTkEntry(master=root, placeholder_text="", font=font_e, justify="right")
c_entry.grid(row=0, column=0, columnspan=5, ipadx=6, ipady=6, padx=4, pady=4, sticky="nsew")

btns = ['7',"8","9","+","-",'4',"5","6","*","/",'1',"2","3","**","** 0.5","0",".","C","-/+","="]

b = 0
for r in range(5):
    if r == 0: continue
    for c in range(5):
        fg_color = '#9a2fa5' if btns[b]=='=' else '#2fa572'
        # hover_color
        btn = customtkinter.CTkButton(master=root, text=btns[b], font=font_btn, fg_color=fg_color)
        btn.grid(row=r, column=c, ipadx=6, ipady=6, padx=4, pady=4, sticky="nsew")
        b += 1

if __name__ == '__main__':
    root.mainloop()