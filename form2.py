"""form2 is used to :rejister to my sql database,
                     create and save users information,
                     connection to other forms(3-5)"""

#Importing libraries and mudouls

import tkinter
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import io
import tkinter.messagebox as messagebox
import mysql.connector
from tkinter.ttk import Combobox

#Connect to mysql database

b_project = mysql.connector.connect(host='localhost',
                                    user='root',
                                    password='root',
                                    database='melli_bank')

print(b_project)
mycursor = b_project.cursor()

#Create new TABLE for the project

TableName=("""CREATE TABLE  IF NOT EXISTS information_t(username varchar(100),
                                                        password varchar(100),
                                                        national_id varchar(10) PRIMARY KEY,
                                                        firstname varchar(50) ,
                                                        lastname varchar(100),
                                                        mobile varchar(11),
                                                        email varchar(255),
                                                        Gender varchar(255),
                                                        city varchar(100),
                                                        province varchar(255),
                                                        degree varchar(255),
                                                        loan varchar(255),
                                                        Image MEDIUMBLOB)""")
mycursor.execute(TableName)
b_project.commit()
b_project.close()

#importing to transfer user to other apllicatin pages

from form5 import f5_creation

from form4 import search_user

from form3 import f3_creation

#Ask users before closing form2
def destroy_f2():
    if messagebox.showinfo('توجه', 'می خواهید خارج شوید؟'):
        form2.destroy()
        import form1
        form1

#To warning users from blank fields

def emptyError():
    messagebox.showinfo('توجه', 'لطفا همه فیلد ها را پر کنید')

#To catch recieved information from user add to database , warn to the user if there are blank fields
def upload_image():
    global image_byte_array
    try:
        # Open file dialog to select an image file
        filename = filedialog.askopenfilename(initialdir="/", title="Select Image",
                                              filetypes=(("jpeg files", "*.jpg"), ("PNG files", "*.png")))
        # Load the image
        image = Image.open(filename)
        image = image.resize((200, 200))

        # Convert the image to bytes
        image_byte_array = io.BytesIO()
        image.save(image_byte_array, format='PNG')
        image_byte_array = image_byte_array.getvalue()
        print(image_byte_array)

        # Display the image in a label
        photo = ImageTk.PhotoImage(image)
        label_img.config(image=photo)  # Set the image in the label
        label_img.image = photo

        return image_byte_array
    except:
        print('can not upload img!')

#get data from user , set limitation to not to be empty and connect to database then add data to information_t database

def register():
    n_id=entry_id.get()
    f_name = entry1.get()
    l_name = entry2.get()
    mobile_n = entry3.get()
    email_a = entry4.get()
    city_n = optionCity.get()
    province_n = optionProvince.get()
    degree_l = entry8.get()
    selected_option = gender_r.get()

    con = mysql.connector.connect(host='localhost',
                                  user='root',
                                  password='root',
                                  database='melli_bank')

    print(b_project)
    c = con.cursor()

    try:
        image = image_byte_array
    except:
        messagebox.showerror('Error', 'لطفا عکس خود را بارگذاری نمایید')

    if n_id == '' or f_name == '' or l_name == '' or mobile_n == '' or email_a == '' or city_n == '' or province_n == '' or  degree_l== '' or selected_option== '':
        messagebox.showerror('Error', 'لطفا همه فیلد ها را پر کنید')
    else:

        insert_into_db = '''INSERT INTO information_t(national_id, firstname, lastname, mobile, email, Gender, city, province, 
                                    degree,image) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''


        data = (n_id, f_name, l_name, mobile_n, email_a, selected_option, city_n, province_n, degree_l, image)

        try:
            c.execute(insert_into_db, data)
            con.commit()
            Label(form2, text='ورود موفق', bg='gold', fg='green').grid(row=10, column=3)



        except:
            con.rollback()
            labl_not_insert = Label(form2, text="Error,ورود ناموفق!", fg='red', bg='gold')
            labl_not_insert.grid(row=10, column=3)


#Create labels and blank areas to fill by user and buttomns for doing actions
def Form2():
    global entry_id ,label_img, entry1, entry2, entry3, entry4, optionCity, optionProvince, entry8
    global gender_r, form2

    form2 = Toplevel()
    form2.title('بانک ملی')
    form2.geometry('650x650')
    form2.resizable(False, False)
    form2.config(background='pink')

    entry_id = StringVar()
    entry1 = StringVar()
    entry2 = StringVar()
    entry3 = StringVar()
    entry4 = StringVar()
    optionCity = StringVar()
    optionProvince = StringVar()
    entry8 = StringVar()
    gender_r = StringVar()

    #definition of button,label and entry in form2

    label0 = Label(form2, text='لطفا مشخصات ذیل را وارد کنید', fg='brown', bg='yellow')
    label0.place(x=250, y=170)

    label_id = Label(form2, text=': کد ملی', fg='purple', bg='light blue')
    label_id.place(x=530, y=220)

    entry_id = Entry(form2, bg='lightgreen')
    entry_id.place(x=400, y=220)

    label1 = Label(form2, text=': نام', fg='purple', bg='light blue')
    label1.place(x=530, y=250)

    entry1 = Entry(form2, bg='lightgreen')
    entry1.place(x=400, y=250)

    label2 = Label(form2, text=': نام خانوادگی', fg='purple', bg='light blue')
    label2.place(x=530, y=280)

    entry2 = Entry(form2, bg='lightgreen')
    entry2.place(x=400, y=280)

    label3 = Label(form2, text=': تلفن', fg='purple', bg='light blue')
    label3.place(x=530, y=310)

    entry3 = Entry(form2, bg='lightgreen')
    entry3.place(x=400, y=310)

    label4 = Label(form2, text=': ایمیل', fg='purple', bg='light blue')
    label4.place(x=530, y=340)

    entry4 = Entry(form2, bg='lightgreen')
    entry4.place(x=400, y=340)

    label5 = Label(form2, text=': جنسیت', fg='purple', bg='light blue')
    label5.place(x=530, y=370)

    radio5_1 = Radiobutton(form2, text='مرد', value=1, variable=gender_r, bg='lightgreen',width=5)
    radio5_1.place(x=400, y=370)

    radio5_2 = Radiobutton(form2, text='زن', value=2, variable=gender_r, bg='lightgreen',width=5)
    radio5_2.place(x=460, y=370)

    label6 = Label(form2, text=": شهر", fg='purple', bg='light blue')
    label6.place(x=530, y=400)
    optionCity = Combobox(form2, width=16,values=('تهران', 'تبریز', 'شیراز', 'اصفهان','اراک', 'مشهد', 'رشت', 'گرگان','بندرعباس', 'خرم آباد'))
    optionCity.current()
    optionCity.place(x=400, y=400)

    label7 = Label(form2, text=": استان", fg='purple', bg='light blue')
    label7.place(x=530, y=430)
    optionProvince = Combobox(form2, width=16,values=('تهران', 'اردبیل', 'شیراز', 'اصفهان','مرکزی', 'مشهد', 'گیلان', 'گلستان','هرمزگان', 'لرستان'))
    optionProvince.current()
    optionProvince.place(x=400, y=430)

    label8 = Label(form2, text=': مدرک تحصیلی', fg='purple', bg='light blue')
    label8.place(x=530, y=460)

    entry8 = Entry(form2, bg='lightgreen')
    entry8.place(x=400, y=460)

    lbl_Image=Label(form2,text=':آپلود عکس',bg='light blue',fg='purple')
    lbl_Image.place(x=530, y=550)
    btn_upload=Button(form2, text='آپلود', width=10,relief='groove', activebackground="silver", activeforeground='gold', command=upload_image, bg='purple',fg='pink')
    btn_upload.place(x=400, y=550)

    label_img=Label(form2,bg='pink')
    label_img.place(x=150, y=250)

    button1 = Button(form2, text='ثبت', width=10, background='green',command=register)
    button1.place(x=170, y=575)

    button2 = Button(form2, text='بستن فرم ثبت نام', command=destroy_f2, background='blue', fg='white')
    button2.place(x=280, y=575)

    button3 = Button(form2, text='بازیابی داده', command=f3_creation, bg='purple', fg='pink',font=('arial', 16, 'bold'))
    button3.place(x=230, y=65)

    button4 = Button(form2, text='وام', command=search_user, bg='purple', fg='pink',font=('arial', 16, 'bold'))
    button4.place(x=130, y=65)

    button5 = Button(form2, text='به روز رسانی داده', command=f5_creation, bg='purple', fg='pink',font=('arial', 16, 'bold'))
    button5.place(x=370, y=65)

    # Set menu in form2

    menubar = Menu(form2)
    filemenu = Menu(menubar, title='File', tearoff=0, fg='black', bg='light blue', bd=5, font=('Arial', 10))
    menubar.add_cascade(label='فایل', menu=filemenu)
    filemenu.add_command(label='خروج', command=lambda: [form2.destroy()])

    editmenu = Menu(menubar, title='Edit', tearoff=0, fg='black', bg='light blue', bd=5, font=('Arial', 10))
    menubar.add_cascade(label='ویرایش', command=Edit)

    helpmenu = Menu(menubar, title='Help', tearoff=0, fg='black', bg='light blue', bd=5, font=('Arial', 10))
    menubar.add_cascade(label='راهنما', menu=helpmenu)
    helpmenu.add_command(label='اطلاعات', command=About)

    # Show the menu

    form2.config(menu=menubar)
    # Show form2

    form2.mainloop()

#menu functions
def About():
    messagebox.showinfo('ارتباط با ما', 'تهران منطقه 12 تقاطع خیابان جمهوری و خیابان فردوسی\nشماره تماس :021-64140')
    print('The Menu')

#menu functions
def Edit():
    messagebox.showinfo('ویرایش اطلاعات', 'جهت ویرایش اطلاعات کلید به روزرسانی داده را بفشارید  ')





