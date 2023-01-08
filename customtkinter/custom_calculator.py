import tkinter
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
        cmd = lambda x = btns[b]: calcul(x)
        btn = customtkinter.CTkButton(master=root, text=btns[b], font=font_btn, command=cmd)
        if btns[b]=='=':
            btn.configure(fg_color='#9a2fa5', hover_color='#671f6f')
        btn.grid(row=r, column=c, ipadx=6, ipady=6, padx=4, pady=4, sticky="nsew")
        b += 1

# the calculator
def calcul(x):
    if "=" in c_entry.get():
        c_entry.delete(0,"end")
        return

    if x == "=":
        try:
            result = eval(c_entry.get())
            c_entry.insert("end","="+str(result))
        except:
            mw = customtkinter.CTkToplevel(root)
            mw.title('Error')
            mw.geometry("300x100")
            customtkinter.CTkLabel(mw, text="Check the data...").pack(side="top", fill="both", expand=True, padx=40, pady=40)
        return

    if x == "C":
        c_entry.delete(0, "end")
        return  

    if x == "-/+":
        if c_entry.get()[0] == "-":
            c_entry.delete(0)
        else:
            c_entry.insert(0,"-")
        return

    c_entry.insert("end", x)
    return

if __name__ == '__main__':
    root.mainloop()