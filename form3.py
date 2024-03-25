"""form3 is used to :connecting to my sql database,
                     displaying users account,
                     by reffering to form 2"""

#Importing libraries and mudouls

import tkinter as tk
from tkinter import *
from PIL import ImageTk,Image
import mysql.connector

#Connect to mysql database

connection= mysql.connector.connect(
                                host='localhost',
                                user='root',
                                password='root',
                                database='melli_bank')
cursor = connection.cursor()

#Create labels and blank areas to fill by user and buttomns for doing actions
def f3_creation():
    f3 = tk.Toplevel()
    f3.title("بازیابی اطلاعات")
    f3.geometry('650x650')
    f3.resizable(False, False)
    f3.config(background='light blue')

    def show_data():
        employee_id = entry1.get()
        cursor.execute("SELECT * FROM information_t WHERE national_id=%s", [employee_id])
        result = cursor.fetchall()  # Fetch all rows
        if result:
            details_text.delete(1.0, tk.END)  # Clear previous details
            for row in result:
                details_text.insert(tk.END,f"کدملی: {row[2]}\n نام: {row[3]}\nنام خانوادگی: {row[4]}\nشماره تماس:\n {row[5]}\nایمیل: {row[6]}\nمدرک تحصیلی: {row[10]}\nشهر: {row[8]}\nاستان: {row[9]}\n\n")
        else:
            details_text.delete(1.0, tk.END)
            details_text.insert(tk.END, "Employee not found")

    #set bank logo

    logo_image= Image.open('images/melli1.jpg')
    user_IMG = ImageTk.PhotoImage(logo_image)
    img_label = Label(f3, image=user_IMG)
    img_label.place(x=270, y=20)

    #definition of button,label and entry in form3

    label0 = Label(f3, text='لطفا مشخصات ذیل را وارد کنید', fg='brown', bg='yellow')
    label0.place(x=240, y=170)

    label_id = Label(f3, text=': کد ملی', fg='purple', bg='light blue')
    label_id.place(x=530, y=220)

    entry1 = tk.Entry(f3, width=20)
    entry1.place(x=400, y=220)

    details_text = tk.Text(f3, height=10, width=40)
    details_text.place(x=170, y=350)

    button1 = Button(f3, text='نمایش اطلاعات', background='brown',command=show_data)
    button1.place(x=270, y=220)

    # Show form3

    f3.mainloop()

    #close connection to mysql database

    cursor.close()
    connection.close()