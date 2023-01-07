# Calculator form tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

root = Tk()
root.title("Калькулятор")
root.geometry("500x310")

def calc(key): # логика калькулятора
    global memory
    if key == "=":
        # исключение написание букв
        strl = "-+0123456789.*/"
        if calc_entry.get()[0] not in strl:
            calc_entry.insert(END, " Первый символ не число")
            messagebox.showerror("Ошибка","Вы ввели не число!")
        # счет
        try:
            result = eval(calc_entry.get())
            calc_entry.insert(END,"="+str(result))
        except:
            calc_entry.insert(END," Ошибка")
            messagebox.showerror("Ошибка","Проверте данные нельза делить на ноль!")
    elif key == "C":
        calc_entry.delete(0, END)
    elif key == "-/+":
        if "=" in calc_entry.get():
            calc_entry.delete(0,END)
        try:
            if calc_entry.get()[0] == "-":
                calc_entry.delete(0)
            else:
                calc_entry.insert(0,"-")
        except IndexError:
            pass    
    else:
        if "=" in calc_entry.get():
            calc_entry.delete(0,END)
        calc_entry.insert(END, key)
        
for c in range(5): root.columnconfigure(index=c, weight=1)
for r in range(5): root.rowconfigure(index=r, weight=1)

# Создание всех кнопок
bttn_list = ['7',"8","9","+","-",'4',"5","6","*","/",'1',"2","3","**","** 0.5","0",".","C","-/+","="]

btn = 0
for r in range(5):
    if r == 0: continue
    for c in range(5):
        if bttn_list[btn] is None: continue
        cmd = lambda x = bttn_list[btn]: calc(x)
        ttk.Button(root, text=bttn_list[btn], command=cmd).grid(row=r, column=c, sticky=NSEW)
        # print(f"({r},{c}, {btn}, {bttn_list[btn]})")
        btn += 1

calc_entry = Entry(root, width=20, bd=2, font="Helvetica 30 normal", justify="center")
calc_entry.grid(row=0, column=0, columnspan=5, sticky=NSEW)

if __name__ == '__main__':
    root.mainloop()