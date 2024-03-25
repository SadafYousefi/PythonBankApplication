"""form1 is used to :Log in or register to mysql database,
                     create and save account,
                     connection to other forms(2-5)"""

#Importing libraries and mudouls

from tkinter import *
import tkinter.messagebox as msgbox
import mysql
import mysql.connector
from PIL import Image, ImageTk

HOST = "localhost"
USER = "root"
PASSWORD = "root"
DATABASE = "melli_bank"

def is_not_empty(text):
    return bool(text) and text.strip()

class LogoLabel:
    def __init__(self, image_file, form, x, y):
        self.image_file = image_file
        self.form = form
        self.x = x
        self.y = y

    def create_label(self):
        logo_image = Image.open(self.image_file)
        user_IMG = ImageTk.PhotoImage(logo_image)
        img_label = Label(self.form, image=user_IMG)
        img_label.image = user_IMG
        img_label.place(x=self.x, y=self.y)

class ExitButton:
    def __init__(self, form, text, command, background, x, y):
        self.form = form
        self.text = text
        self.command = command
        self.background = background
        self.x = x
        self.y = y

    def create_button(self):
        button_exit = Button(self.form, text=self.text, command=self.command, background=self.background)
        button_exit.place(x=self.x, y=self.y)

#creating main page
class Application:
    def __init__(self) -> None:
        self.window = Tk()
        self.window.geometry("650x650")
        self.window.title("به بانک ملی خوشامدید")
        self.window.resizable(False,False)

        logo = LogoLabel('images/melli1.jpg',self.window, 265, 20)  # create an instance of the class
        logo.create_label()
        self.login_frame = Frame(self.window)
        self.login_frame.grid(row=1,column=1)
        self.create_login_form()

        self.register_frame = Frame(self.window)
        self.register_frame.grid(row=1,column=3)
        self.create_register_form()

        self.create_database()

        def destroy_f1():
            self.window.destroy()

        exit_button = ExitButton(self.window, 'خروج', destroy_f1, 'brown', 300, 580)
        exit_button.create_button()

        try:
            self.DBconnection = mysql.connector.connect(
                host=HOST,
                user=USER,
                password=PASSWORD,
                database=DATABASE
            )
            self.cursor = self.DBconnection.cursor()

        except mysql.connector.Error as err:
            msgbox.showerror("Error connecting to MySQL database:", err)
            raise

    #creating database and profile table
    def create_database(self):
        with mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
        ) as connection:
            cursor = connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE}")
            connection.commit()
            cursor.execute(f"USE {DATABASE}")
            cursor.execute(f"""CREATE TABLE IF NOT EXISTS profile(
                                    national_id varchar(10) PRIMARY KEY,
                                    username varchar(100),
                                    password varchar(100),
                                    firstname varchar(50) ,
                                    lastname varchar(100))""")
            connection.commit()
            msgbox.showinfo(self.window,f"Database {DATABASE} created or exists successfully!")

    def execute_query(self, query, params=None,commit=False):
        try:
            self.cursor.execute(query, params=params)
            if self.cursor.description:
                return self.cursor.fetchall()
            else:
                self.DBconnection.commit()
                return None
        except mysql.connector.Error as err:
            msgbox.showerror("Error executing query:", err)
            raise

    #set message to user in log in situation
    def login(self,uname,pwd):
        user = self.execute_query(f"SELECT username,password FROM profile WHERE username='{uname}' and password='{pwd}'")
        if len(user)<1:
            msgbox.showerror(self.window,f"نام کاربری یا رمز عبور تعریف نشده است\nدر صورت نداشتن حساب کاربری، ابتدا آن را ایجاد نمایید")
        else:
            msgbox.showinfo(self.window,f"ورود با نام کاربری{pwd}با موفقیت {uname} و رمز عبور ")
            global form1main
            from form2 import Form2
            Form2()

    #set limitation for registration to not to be empty

    def register(self,nid,fname,lname,uname,pwd,pwdr):
        if (is_not_empty(nid)
            and is_not_empty(fname)
            and is_not_empty(lname)
            and is_not_empty(uname)
            and is_not_empty(pwd)
            and is_not_empty(pwdr)
            and pwd==pwdr):

            self.execute_query(f"INSERT INTO profile (national_id,username,password,firstname,lastname) VALUES ('{nid}','{uname}','{pwd}','{fname}','{lname}')",commit=True)
            msgbox.showinfo(self.window,f"ثبت نام با نام کاربری {uname} و رمز عبور {pwd} با موفقیت انجام شد")
        else:
            msgbox.showerror(self.window,"لطفا همه فیلد ها را پر کنید")

    # button,label and entry definition for log in form
    def create_login_form(self):

        # Add login form widgets

        self.username_label = Label(self.login_frame, text=":نام کاربری")
        self.username_label.grid()
        self.username_entry = Entry(self.login_frame)
        self.username_entry.grid()

        self.password_label = Label(self.login_frame, text="رمز عبور")
        self.password_label.grid()
        self.password_entry = Entry(self.login_frame)
        self.password_entry.grid()

        self.login_button = Button(self.login_frame, text="ورود",
                                   command=lambda : self.login(self.username_entry.get(),
                                                               self.password_entry.get()))
        self.login_button.grid()

    #button,label and entry definition for registration
    def create_register_form(self):

        fname_label = Label(self.register_frame,text=":نام")
        fname_label.grid()
        fname_entry = Entry(self.register_frame)
        fname_entry.grid()

        lname_label = Label(self.register_frame, text=":نام خانوادگی")
        lname_label.grid()
        lname_entry = Entry(self.register_frame)
        lname_entry.grid()

        username_label = Label(self.register_frame, text=":نام کاربری")
        username_label.grid()
        username_entry = Entry(self.register_frame)
        username_entry.grid()

        password_label = Label(self.register_frame, text=":رمز عبور")
        password_label.grid()
        password_entry = Entry(self.register_frame)
        password_entry.grid()

        passwordr_label = Label(self.register_frame, text=":تکرار رمز عبور")
        passwordr_label.grid()
        passwordr_entry = Entry(self.register_frame)
        passwordr_entry.grid()

        nationalid_label = Label(self.register_frame, text=":کد ملی")
        nationalid_label.grid()
        nationalid_entry = Entry(self.register_frame)
        nationalid_entry.grid()

        register_button = Button(self.register_frame, text="ثبت نام",
                                 command=lambda : self.register(nid=nationalid_entry.get(),
                                                                fname=fname_entry.get(),
                                                                lname=lname_entry.get(),
                                                                uname=username_entry.get(),
                                                                pwd=password_entry.get(),
                                                                pwdr=passwordr_entry.get()))
        register_button.grid()

    def run(self):
        self.window.mainloop()

app = Application()
app.run()
