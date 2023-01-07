import tkinter
import customtkinter

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

root = customtkinter.CTk()  # create CTk window like you do with the Tk window
root.title('')
root.geometry("500x350")

def login():
    print("Test")

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=20, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="Login system", font=customtkinter.CTkFont(size=24, weight="normal"))
label.pack(pady=12, padx=10)

entry_1 = customtkinter.CTkEntry(master=frame, placeholder_text="Username")
entry_1.pack(pady=12, padx=10)

entry_2 = customtkinter.CTkEntry(master=frame, placeholder_text="Password", show='*')
entry_2.pack(pady=12, padx=10)

# Use CTkButton instead of tkinter Button
button = customtkinter.CTkButton(master=frame, text="Login", command=login)
button.pack(pady=12, padx=10)

chessbox = customtkinter.CTkCheckBox(master=frame, text="Remember me")
chessbox.pack(pady=12, padx=10)

if __name__ == '__main__':
    root.mainloop()