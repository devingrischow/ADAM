from tkinter import *
from tkinter import ttk
import customtkinter

root = customtkinter.CTk()
root.title('Learn To Code at Codemy.com')
root.iconbitmap('c:/gui/codemy.ico')
root.geometry("500x400")

# Create A Main Frame
main_frame = customtkinter.CTkFrame(root)
main_frame.pack(fill='both', expand=1)

# Create A Canvas
my_canvas = customtkinter.CTkCanvas(main_frame)
my_canvas.pack(side='right', fill='both', expand=1)

# Add A Scrollbar To The Canvas
my_scrollbar = customtkinter.CTkScrollbar(main_frame, orientation='VERTICAL', command=my_canvas.yview)
my_scrollbar.pack(side='right', fill='y')

# Configure The Canvas
my_canvas.configure(yscrollcommand=my_scrollbar.set)
my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))

# Create ANOTHER Frame INSIDE the Canvas
second_frame = customtkinter.CTkFrame(my_canvas)

# Add that New frame To a Window In The Canvas
my_canvas.create_window((0,0), window=second_frame, anchor="nw")

for thing in range(100):
	customtkinter.CTkButton(second_frame, text=f'Button {thing} Yo!').grid(row=thing, column=0, pady=10, padx=10)

my_label = customtkinter.CTkLabel(second_frame, text="It's Friday Yo!").grid(row=3, column=2)


root.mainloop()