from tkinter import *
from tkinter import ttk
import customtkinter

root = customtkinter.CTk()

root.geometry("500x400")

# Create A Main Frame
main_frame = customtkinter.CTkFrame(root)
main_frame.pack(side='left', anchor='n')

# Create A Canvas
my_canvas = customtkinter.CTkCanvas(main_frame, height=50, width=350)
my_canvas.pack()

# Add A Scrollbar To The Canvas
my_scrollbar = customtkinter.CTkScrollbar(main_frame, orientation=HORIZONTAL, command=my_canvas.xview, width=350)
my_scrollbar.pack(side=LEFT)

# Configure The Canvas
my_canvas.configure(xscrollcommand=my_scrollbar.set)
my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))

# Create ANOTHER Frame INSIDE the Canvas
second_frame = customtkinter.CTkFrame(my_canvas, fg_color='transparent')

# Add that New frame To a Window In The Canvas
my_canvas.create_window((0,0), window=second_frame, anchor="nw")

for thing in range(100):
	customtkinter.CTkButton(second_frame, text=f'Button {thing} Yo!').grid(row=0, column=thing,padx=10)



root.mainloop()

#code from flatplanet
#modified by me