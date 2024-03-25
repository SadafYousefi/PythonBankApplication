"""form4 is used to :connecting to mysql database,
                     visualize users information in charts"""

#Importing libraries and mudouls

import matplotlib.pyplot as plt
from tkinter import *
from PIL import ImageTk,Image
from tkinter.ttk import Combobox
import mysql.connector
from datetime import date
from dateutil.relativedelta import relativedelta
import tkinter.messagebox as messagebox

#connection to database
def create_table_balance():
    con=mysql.connector.connect(host='localhost',
                                user='root',
                                password='root',
                                database='melli_bank')
    c=con.cursor()

    #t_AccountBalance table creation

    try:
        quary_Accuntinfo='''CREATE TABLE IF NOT EXISTS t_AccountBalance (
            Account_Number VARCHAR(15) PRIMARY KEY,
            Final_Balance VARCHAR(10) NOT NULL,
            Loan VARCHAR(10),
            Months VARCHAR(10),
            StartDate VARCHAR(10),
            FinalDate VARCHAR(10))'''
    #error managemant

        c.execute(quary_Accuntinfo)
        con.commit()

        print("Table t_AccountBalance created")
    except:
        print('Error,Table t_AccountBalance info not created!')
        con.rollback()

    query_relation='''ALTER TABLE information_t 
                    ADD Account_Number VARCHAR(15)'''
    try:
        c.execute(query_relation)
    except:
        print('Error new fields not added!')


    c.close()

create_table_balance()

#serch and find user information according to national ID
def search_user():
    global entry_search
    entry_search = StringVar()

    #creating a tk visual environment

    search = Toplevel()
    search.title('نمودار')
    search.geometry('650x650')
    search.resizable(False, False)
    search.config(background='light yellow')

    #set bank logo picture

    logo_image1 = Image.open('images/melli1.jpg')
    user_IMG = ImageTk.PhotoImage(logo_image1)
    img_label = Label(search, image=user_IMG)
    img_label.place(x=265, y=20)

    # definition of button,label and entry in form4 in search part

    label_search = Label(search,text=' لطفا کد ملی را وارد کنید: ',fg='white',bg='blue')
    label_search.place(x=250, y=170)

    label_id = Label(search, text=': کد ملی', fg='purple', bg='light blue')
    label_id.place(x=530, y=220)

    entry_search = Entry(search,bg="light blue")
    entry_search.place(x=400, y=220)

    submit_button = Button(search, text='جستجو', command=f4_creation)
    submit_button.place(x=260, y=320)


    search.mainloop()
def tranaction():
    national_id = entry_search.get()
    Accunt_Number = f"000-{national_id}"

    Loanvalue = entry_loan_value.get()

    amount =  entry_balance.get()
    if amount == '':
        amount = 0
    if Loanvalue == '':
        Loanvalue = 0
    Final_Balance = int(amount) + int(Loanvalue)

    Months = DateValue.get()



    # تاریخ تراکنش
    date_start_loan = date.today()
    date_loan_end= date_start_loan + relativedelta(months=Months)

 # ایجاد شیی cursor برای اجرای کوئری
    con = mysql.connector.connect(host='localhost',
                                  user='root',
                                  password='root',
                                  database='melli_bank')
    c = con.cursor()

    # اجرای کوئری برای جستجوی فرد با شماره ملی
    if Months !='' and Loanvalue != '':
        try:
            c.execute(
                '''INSERT INTO t_AccountBalance(Account_Number, Final_Balance, Loan, Months ,StartDate ,FinalDate) VALUES (%s, %s, %s, %s, %s, %s)''',
                (Accunt_Number, Final_Balance,Loanvalue, Months, date_start_loan, date_loan_end)
            )

            con.commit()

            c.execute('''UPDATE information_t SET Account_Number = %s WHERE national_id = %s''', (Accunt_Number, national_id))
            con.commit()

            Label(f4, text='submited successfully on "Loan" table', bg='gold', fg='green').pack()

            # اتصال به پایگاه داده برای دریافت میزان موجودی حساب

            c.execute(
                '''SELECT Final_Balance ,Loan,StartDate, FinalDate , Months FROM t_AccountBalance WHERE 
                Account_Number = %s''',
                (Accunt_Number,))

            result1 = c.fetchone()

            # نمایش موجودی فعلی
            if result1:
                current_balance2 = result1[0]
                Loan2 =  result1[1]
                startdate = result1[2]
                finaldate = result1 [3]
                month2 = result1[4]


                label_balance = Label(f4,text=f"{current_balance2}:موجودی جدید")
                label_balance.place(x=100,y=320)

                label_loan2 = Label(f4, text=f"{Loan2}:مقدار وام")
                label_loan2.place(x=400, y=320)

                label_startdate = Label(f4, text=f"{startdate}:تاریخ شروع وام")
                label_startdate.place(x=100, y=340)

                label_finaldate = Label(f4, text=f"{finaldate}:تاریخ پایان وام")
                label_finaldate.place(x=400, y=340)

                label_month2 = Label(f4, text=f"{month2}:تعداد اقساط")
                label_month2.place(x=100, y=360)


                print("موجودی فعلی: ", current_balance2)
            else:

                print("موجودی فعلی وجود ندارد")



            con.commit()



            Label(f4, text='submited successfully on "AccountBalance" table', bg='gold', fg='green').pack()



        except:
            con.rollback()
            labl_not_insert = Label(f4, text="کاربر قبلا وام گرفته", fg='red', bg='gold')
            labl_not_insert.place(x=250,y=320)
            con = mysql.connector.connect(host='localhost',
                                          user='root',
                                          password='root',
                                          database='melli_bank')
            c = con.cursor()

            c.execute(
                '''SELECT Final_Balance ,Loan,StartDate, FinalDate , Months FROM t_AccountBalance WHERE 
                Account_Number = %s''',
                (Accunt_Number,))

            result1 = c.fetchone()

            # نمایش موجودی فعلی
            if result1:
                current_balance2 = result1[0]
                Loan2 =  result1[1]
                startdate = result1[2]
                finaldate = result1 [3]
                month2 = result1[4]


                label_balance = Label(f4,text=f"{current_balance2}:موجودی جدید")
                label_balance.place(x=100,y=320)

                label_loan2 = Label(f4, text=f"{Loan2}:مقدار وام")
                label_loan2.place(x=400, y=320)

                label_startdate = Label(f4, text=f"{startdate}:تاریخ شروع وام")
                label_startdate.place(x=100, y=340)

                label_finaldate = Label(f4, text=f"{finaldate}:تاریخ پایان وام")
                label_finaldate.place(x=400, y=340)

                label_month2 = Label(f4, text=f"{month2}:تعداد اقساط")
                label_month2.place(x=100, y=360)
                con.commit()
            else:
                print("موجودی فعلی وجود ندارد")


    else:messagebox.showerror('Error','Enter Data !')

def chart_func():
    national_id = entry_search.get()
    Accunt_Number = f"000-{national_id}"

    con = mysql.connector.connect(host='localhost',
                                  user='root',
                                  password='root',
                                  database='melli_bank')
    c = con.cursor()

    c.execute(
        '''SELECT Final_Balance ,Loan FROM t_AccountBalance WHERE 
        Account_Number = %s''',
        (Accunt_Number,))

    result = c.fetchone()

    # نمایش موجودی فعلی
    if result:
        money = result[0]
        loan = result[1]

        # بررسی ابعاد داده‌ها
        if money and loan:
            plt.title("Balance:")
            plt.pie([float(money) - float(loan), float(loan)], labels=['ماو', 'ماو ریغ یدوجوم '],
                    autopct='%1.1f%%')
            plt.legend()
            plt.show()

        else:
            print("Invalid data format.")

    else:
            print("موجودی فعلی وجود ندارد")

#displaying user finantional informatioan also add new finantional information to database then visualize them on a pie chart
def f4_creation():
    global entry_balance, entry_loan_value, DateValue, f4

    entry_balance = IntVar()
    entry_loan_value = IntVar()
    DateValue = IntVar()

    #main page definition

    f4 = Toplevel()
    f4.title('وام')
    f4.geometry('650x650')
    f4.resizable(False, False)
    f4.config(background='light yellow')

    #set bank logo picture

    logo_image1 = Image.open('images/melli1.jpg')
    user_IMG = ImageTk.PhotoImage(logo_image1)
    img_label = Label(f4, image=user_IMG)
    img_label.place(x=265, y=20)

    label1 = Label(f4,text=' لطفا همه فیلد ها را پر کنید و پس از فشردن کلید "بررسی تقاضا" منتظر بمانید ',fg='white',bg='blue')
    label1.place(x=125,y=125)

    loan_mounth = Label(f4, text=' طرح/وام مورد نظر من(بازپرداخت چند ماه:): ',fg='yellow', bg='black')
    loan_mounth.place(x=30, y=170)
    option_l2 = Combobox(f4, width=10 ,values=('12','24', '36', '48', '60'),textvariable=DateValue)
    option_l2.current()
    option_l2.place(x=360, y=170)

    balance = Label(f4, text=' موجودی فعلی حساب من: ', fg='yellow', bg='black')
    balance.place(x=30, y=220)
    entry_balance = Entry(f4,bg='lightblue')
    entry_balance.place(x=360, y=270)

    loan_value = Label(f4, text=' مقدار وام من: ', fg='yellow', bg='black')
    loan_value.place(x=30, y=270)
    entry_loan_value = Entry(f4, bg='lightblue')
    entry_loan_value.place(x=360, y=220)

    submit_button = Button(f4, text='ثبت  یا بازیابی', command=tranaction)
    submit_button.place(x=230,y=400)

    butten_chart = Button(f4,text='نمودار' , command=chart_func)
    butten_chart.place(x=350 ,y=400)

    #display tk visual

    f4.mainloop()

