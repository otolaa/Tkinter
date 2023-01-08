from tkinter import *
 
def NewWindow():
    window = Toplevel()
    window.title('250 x 70')
    window.geometry('250x70')
    newlabel = Label(window, text = "Settings Window")
    newlabel.pack(pady = 10)
 
 
root = Tk()
root.title("280 x 172")
root.geometry('280x172')
 
myframe = Frame(root)
myframe.pack(pady = 10)

mainLabel0 = Label(myframe, text='Example for pop up input box')
mainLabel0.pack()

mybutton = Button(myframe, text = "Settings", command = NewWindow)
mybutton.pack()
 
root.mainloop()