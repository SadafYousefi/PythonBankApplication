"""Form5 is used to :Connecting to mysql database,
                     Updating users data consists of delete,insert and exchange them,
                     Back to form1"""

#Importing libraries and mudouls

import mysql.connector
from tkinter import *
from PIL import Image, ImageTk
import tkinter.messagebox as messagebox
import mysql.connector
from tkinter.ttk import Combobox
import io
from tkinter import filedialog
import traceback
# from tkinter.filedialog import askopenfilename

#connection to database

b_project = mysql.connector.connect(host='localhost',
                                    user='root',
                                    password='root',
                                    database='melli_bank')
print(b_project)
cursor = b_project.cursor()

# able and disable inputs
def disable_enable_edit(i, j):
    if i.get():
        j.config(state="normal")
    else:
        j.config(state="disabled")

#get data from user , set limitation to not to be empty and connect to database then add data to information_t database

def Edit():

    new_name = New_Neme.get()
    new_lastname = New_Lastname.get()
    new_phone = New_Phone.get()
    new_email = New_Email.get()
    new_gender = New_Gender.get()
    new_state = New_state.get()
    new_city = New_City.get()
    new_degree = New_Degree.get()

    # create dictionary
    Dict_qeury = {'firstname': new_name,
                  'lastname': new_lastname,
                  'mobile': new_phone,
                  'email': new_email,
                  'Gender': new_gender,
                  'province': new_state,
                  'city': new_city,
                  'degree': new_degree}

    # change dictionary to string
    edit_items = ', '.join([f"{key}='{value}'" for key, value in Dict_qeury.items() if value != ''])

    Edit_ID = entry1.get()
    c=b_project.cursor()

    c.execute(f"""UPDATE information_t set {edit_items} WHERE national_id LIKE %s""",(Edit_ID,))

    lbl_update=Label(f5,text=f"اطلاعات کاربر با کدملی {Edit_ID} به روزرسانی شد",fg='green',bg='black', font='bold')
    lbl_update.place(x=100,y=600)

    edit_window.destroy()

#to exchange previous user information
def modify_data():

    global edit_window,\
           entry_name, \
           entry_LastName,\
           Edit_Costomer,\
           New_Neme,\
           New_Lastname,\
           New_Phone,\
           New_Email, \
           New_Gender, \
           New_state, \
           New_City, \
           New_Degree,\
           search_results

    New_Neme = StringVar()
    New_Lastname = StringVar()
    New_Phone = StringVar()
    New_Email = StringVar()
    New_Gender = IntVar()
    New_state = StringVar()
    New_City = StringVar()
    New_Degree = StringVar()

    Edit_id = entry1.get()

    #creationg tk visual for exchange user information,set according to national ID

    edit_window = Toplevel()
    edit_window.title('ویرایش کاربر')
    edit_window.geometry('650x650')
    edit_window.config(background='pink')
    edit_window.resizable(width=False,height=False)

    lbl_ask = Label(edit_window, text=f'اطلاعات جدید کاربر با کد ملی {Edit_id} را وارد نمایید',bg='yellow', fg='purple')
    lbl_ask.place(x=180, y=240)

    search_results = Text(edit_window, width=30, height=10, bg='silver')
    search_results.place(x=200, y=30)
    try:
        # make object to run the query
        c = b_project.cursor()

        # make query for search according to national_id
        c.execute("""SELECT national_id,
                                     firstname,
                                     lastname,
                                     mobile, 
                                     email,
                                     Gender,
                                     city, 
                                     province,
                                     degree,
                                     loan,
                                     image FROM information_t WHERE national_id like %s""",(Edit_id,))

        result = c.fetchall()

        # display search result
        search_results.delete(1.0, END)
        for rec in result:
                search_results.insert(END, f"national_id: {rec[0]}\n")
                search_results.insert(END, f"firstname: {rec[1]}\n")
                search_results.insert(END, f"lastname: {rec[2]}\n")
                search_results.insert(END, f"mobile: {rec[3]}\n")
                search_results.insert(END, f"email: {rec[4]}\n")
                search_results.insert(END, f"Gender: {rec[5]}\n")
                search_results.insert(END, f"city: {rec[6]}\n")
                search_results.insert(END, f"province: {rec[7]}\n")
                search_results.insert(END, f"degree: {rec[8]}\n")
                search_results.insert(END, f"balance: {rec[9]}\n")
                search_results.insert(END, f"loan: {rec[9]}\n")
                search_results.insert(END, "\n")


    except:
        print('error edit customer!')

    checkbutton_value_name = BooleanVar()
    checkbutton_name = Checkbutton(edit_window, text="تغییر نام",
                                   variable=checkbutton_value_name,
                                   selectcolor="red",
                                   bg='yellow',
                                   fg='black',
                                   command=lambda: disable_enable_edit(checkbutton_value_name, entry_name))
    checkbutton_name.place(x=520, y=300)

    entry_name = Entry(edit_window, state="disabled",bg='silver', textvariable=New_Neme)
    entry_name.place(x=390, y=300)

    checkbutton_value_last_name = BooleanVar()
    checkbutton_last_name = Checkbutton(edit_window, text="تغییر نام خانوادگی",
                                        variable=checkbutton_value_last_name,
                                        selectcolor="red",
                                        bg='yellow',
                                        fg='black',
                                        command=lambda: disable_enable_edit(checkbutton_value_last_name, entry_last_name))
    checkbutton_last_name.place(x=520, y=330)

    entry_last_name = Entry(edit_window, state="disabled", bg='silver', textvariable=New_Lastname)
    entry_last_name.place(x=390, y=330)

    checkbutton_value_phone = BooleanVar()
    checkbox_phone = Checkbutton(edit_window, text="تغییر شماره تلفن",
                                 variable=checkbutton_value_phone,
                                 selectcolor="red",
                                 bg='yellow',
                                 fg='black',
                                 command=lambda: disable_enable_edit(checkbutton_value_phone, entry_phone))
    checkbox_phone.place(x=520, y=360)

    entry_phone = Entry(edit_window, state="disabled", bg='silver', textvariable=New_Phone)
    entry_phone.place(x=390, y=360)

    checkbutton_value_email = BooleanVar()
    checkbox_email = Checkbutton(edit_window, text="تغییر ایمیل",
                                 variable=checkbutton_value_email,
                                 selectcolor="red",
                                 bg='yellow',
                                 fg='black',
                                 command=lambda: disable_enable_edit(checkbutton_value_email, entry_email))
    checkbox_email.place(x=520, y=390)

    entry_email = Entry(edit_window, state="disabled", bg='silver', textvariable=New_Email)
    entry_email.place(x=390, y=390)


    checkbutton_value_state = BooleanVar()
    checkbox_last_state = Checkbutton(edit_window, text="تغییر استان",
                                      variable=checkbutton_value_state,
                                      selectcolor="red",
                                      bg='yellow',
                                      fg='black',
                                      command=lambda: disable_enable_edit(checkbutton_value_state, entry_state))
    checkbox_last_state.place(x=520, y=420)

    entry_state = Entry(edit_window, state="disabled", bg='silver', textvariable=New_state)
    entry_state.place(x=390, y=420)

    checkbutton_value_city = BooleanVar()
    checkbox_last_city = Checkbutton(edit_window, text="تغییر شهر",
                                     variable=checkbutton_value_city,
                                     selectcolor="red",
                                     bg='yellow',
                                     fg='black',
                                     command=lambda: disable_enable_edit(checkbutton_value_city, entry_city))
    checkbox_last_city.place(x=520, y=450)

    entry_city = Entry(edit_window, state="disabled", bg='silver', textvariable=New_City)
    entry_city.place(x=390, y=450)

    checkbutton_value_degree = BooleanVar()
    checkbox_degree = Checkbutton(edit_window, text="تغییر مدرک تحصیلی",
                                  variable=checkbutton_value_degree,
                                  selectcolor="red",
                                  bg='yellow',
                                  fg='black',
                                  command=lambda: disable_enable_edit(checkbutton_value_degree, entry_degree))
    checkbox_degree.place(x=520, y=480)

    entry_degree = Entry(edit_window, state="disabled", bg='silver', textvariable=New_Degree)
    entry_degree.place(x=390, y=480)

    checkbutton_value_gender = BooleanVar()
    checkbox_degree = Checkbutton(edit_window, text="تغییر جنسیت",
                                  variable=checkbutton_value_gender,
                                  selectcolor="red",
                                  bg='yellow',
                                  fg='black',
                                  command=lambda: disable_enable_edit(checkbutton_value_gender, entry_gender))
    checkbox_degree.place(x=520, y=510)

    entry_gender = Entry(edit_window, state="disabled", bg='silver', textvariable=New_Gender)
    entry_gender.place(x=390, y=510)

    Btn_yes = Button(edit_window, text='اعمال تغییرات',
                     bg='purple',
                     fg='yellow',
                     width=10,
                     font=('arial', 12, 'bold'),
                     command=lambda: Edit() if messagebox.askokcancel("تغییر اطلاعات کاربر",f"تغییر اطلاعات کاربر با کد ملی{Edit_id}انجام شود؟ ") else None)
    Btn_yes.place(x=150, y=350)

    Btn_cancel = Button(edit_window, text="لغو", bg='purple', fg='yellow', width=10,font=('arial', 12, 'bold'), command=edit_window.destroy)
    Btn_cancel.place(x=150, y=420)

    edit_window.mainloop()

#delete data function definition

def Delete():

    Delete_ID = entry1.get()

    try:
        print(b_project)
        c=b_project.cursor()
        messagebox.askquestion("اخطار!","آیا مطمئن به حذف اطلاعات خود هستید؟")
        c.execute("""DELETE FROM information_t WHERE national_id LIKE %s""",(Delete_ID,))

        lbl_delete=Label(f5,text=f"کاربر با شماره ملی {Delete_ID} با موفقیت حذف شد ",
                         fg='white', bg='blue', font='bold')
        lbl_delete.place(x=90,y=600)

        details_window.destroy()
    except:print('Erorr delete function')

def delete_data():
    global details_window, checkbox_value_name, entry_name,frame2,label_img2
    Delete_ID = entry1.get()

    #creating tk visual for delete data from database

    details_window = Toplevel()
    details_window.title('حذف اطلاعات کاربر')
    details_window.geometry('650x650')
    details_window.config(background='light yellow')
    details_window.resizable(width=False,height=False)

    lbl_ask=Label(details_window, text= f'به منظور حذف کامل اطلاعات کاربری با کد ملی {Delete_ID} کلید <حذف> را انتخاب نمایید',
                  bg='blue',fg='yellow',font=('arial', 12, 'bold'))
    lbl_ask.place(x=70,y=70)

    search_results = Text(details_window, width=30, height=14,bg='pink')
    search_results.place(x=220,y=140)
    try:
        # make object to run the query
        print(b_project)
        c = b_project.cursor()

        # make query for search according to national_id
        c.execute("""SELECT * FROM information_t WHERE national_id like %s""",(Delete_ID,))

        result = c.fetchall()

        # display search result
        search_results.delete(1.0, END)
        for rec in result:
            search_results.insert(END, f"national_id: {rec[2]}\n")
            search_results.insert(END, f"firstname: {rec[3]}\n")
            search_results.insert(END, f"lastname: {rec[4]}\n")
            search_results.insert(END, f"mobile: {rec[5]}\n")
            search_results.insert(END, f"email: {rec[6]}\n")
            search_results.insert(END, f"Gender: {rec[7]}\n")
            search_results.insert(END, f"city: {rec[8]}\n")
            search_results.insert(END, f"province: {rec[9]}\n")
            search_results.insert(END, f"degree: {rec[10]}\n")
            search_results.insert(END, f"loan: {rec[11]}\n")
            search_results.insert(END, "\n")

            Btn_yes = Button(details_window, text='حذف', fg='white',bg='red',font='bold', command=Delete)
            Btn_yes.place(x=290,y=400)

            Btn_cancel = Button(details_window, text="لغو", fg='white',bg='blue',font='bold', command=details_window.destroy)
            Btn_cancel.place(x=295,y=450)

            details_window.mainloop()

    except:print('error customer delete')

def upload_image():
    global image_byte_array
    # Open file dialog to select an image file

    filename = filedialog.askopenfilename(initialdir="/", title="Select Image",
                                          filetypes=(("jpeg files", "*.jpg"), ("PNG files", "*.png")))
    # Check if the user selected a file
    if filename:
        try:
            # Load the image

            image = Image.open(filename)

            # resize the image to 200x200 pixels

            image = image.resize((200, 200))

            # Convert the image to bytes
            image_byte_array = io.BytesIO()
            image.save(image_byte_array, format='PNG')
            image_byte_array = image_byte_array.getvalue()
            print(image_byte_array)

            # Display the image in a label
            photo = ImageTk.PhotoImage(image)

            # Set the image in the label

            label_img.config(image=photo)
            label_img.image = photo

            # Return the image byte array
            return image_byte_array
        except (FileNotFoundError, OSError, ValueError) as e:
            # Handle specific exceptions
            print(f'Error: {e}')
            print(traceback.format_exc())
    else:
        # Handle user cancellation
        print('No file selected!')

#get information from user and set as data in database

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

    #connecting to database

    con = mysql.connector.connect(host='localhost',
                                  user='root',
                                  password='root',
                                  database='melli_bank')
    print(b_project)
    c = con.cursor()

    try:
        image = image_byte_array
    except:
        messagebox.showerror('خطا', 'تصویر خود را بارگذاری نمایید')

        #set limitation for user information to not to be empty and add them to database

    if n_id == '' and f_name == '' and l_name == '' and mobile_n == '' and email_a == '' and city_n == '' and province_n == '' and degree_l == '' and selected_option == '':
        messagebox.showerror('خطا', 'لطفا همه فیلد ها را پر کنید')
    else:
        insert_into_db = ("""INSERT INTO information_t(national_id, firstname, lastname, mobile, email, Gender, city, province, 
                                    degree,image) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)""")


        data = (n_id, f_name, l_name, mobile_n, email_a, selected_option, city_n, province_n, degree_l,image)

        try:
            c.execute(insert_into_db, data)
            con.commit()
            Label(insert_data, text='اطلاعات کاربری ذخیره شد', bg='gold', fg='green').place(x=10, y=10)

        except:
            con.rollback()
            labl_not_insert = Label(insert_data, text="اطلاعات شما ذخیره نشد!", fg='red', bg='gold')
            labl_not_insert.place(x=10, y=10)


def insert_datas():
    global gender_r,upload_new_image,entry_id ,label_img, entry1, entry2, entry3, entry4, optionCity, optionProvince, entry8, insert_data

    entry_id = StringVar()
    entry1 = StringVar()
    entry2 = StringVar()
    entry3 = StringVar()
    entry4 = StringVar()
    optionCity = StringVar()
    optionProvince = StringVar()
    entry8 = StringVar()
    gender_r = StringVar()

    #creating add user tk visual

    insert_data = Toplevel()
    insert_data.title('افزودن کاربر')
    insert_data.geometry('650x650')
    insert_data.resizable(False, False)
    insert_data.config(background='grey')

    #definition of button,label and entry in form5

    label0 = Label(insert_data, text='لطفا مشخصات ذیل را وارد کنید',font='bold', fg='grey', bg='yellow')
    label0.place(x=240, y=140)

    label_id = Label(insert_data, text=': کد ملی', fg='blue', bg='light blue')
    label_id.place(x=530, y=200)

    entry_id = Entry(insert_data, bg='light green')
    entry_id.place(x=400, y=200)

    label1 = Label(insert_data, text=': نام', fg='blue', bg='light blue')
    label1.place(x=530, y=230)

    entry1 = Entry(insert_data, bg='light green')
    entry1.place(x=400, y=230)

    label2 = Label(insert_data, text=': نام خانوادگی', fg='blue', bg='light blue')
    label2.place(x=530, y=260)

    entry2 = Entry(insert_data, bg='light green')
    entry2.place(x=400, y=260)

    label3 = Label(insert_data, text=': تلفن', fg='blue', bg='light blue')
    label3.place(x=530, y=290)

    entry3 = Entry(insert_data, bg='light green')
    entry3.place(x=400, y=290)

    label4 = Label(insert_data, text=': ایمیل', fg='blue', bg='light blue')
    label4.place(x=530, y=320)

    entry4 = Entry(insert_data, bg='light green')
    entry4.place(x=400, y=320)

    label5 = Label(insert_data, text=': جنسیت', fg='blue', bg='light blue')
    label5.place(x=530, y=350)

    radio5_1 = Radiobutton(insert_data, text='مرد', value=1, variable=gender_r, bg='light green', width=5)
    radio5_1.place(x=400, y=350)

    radio5_2 = Radiobutton(insert_data, text='زن', value=2, variable=gender_r, bg='light green', width=5)
    radio5_2.place(x=460, y=350)

    label6 = Label(insert_data, text=": شهر", fg='blue', bg='light blue')
    label6.place(x=530, y=380)
    optionCity = Combobox(insert_data, width=16, values=(
    'تهران', 'تبریز', 'شیراز', 'اصفهان', 'اراک', 'مشهد', 'رشت', 'گرگان', 'بندرعباس', 'خرم آباد'))
    optionCity.current()
    optionCity.place(x=400, y=380)

    label7 = Label(insert_data, text=": استان", fg='blue', bg='light blue')
    label7.place(x=530, y=410)
    optionProvince = Combobox(insert_data, width=16, values=(
    'تهران', 'اردبیل', 'شیراز', 'اصفهان', 'مرکزی', 'مشهد', 'گیلان', 'گلستان', 'هرمزگان', 'لرستان'))
    optionProvince.current()
    optionProvince.place(x=400, y=410)

    label8 = Label(insert_data, text=': مدرک تحصیلی', fg='blue', bg='light blue')
    label8.place(x=530, y=440)

    entry8 = Entry(insert_data, bg='light green')
    entry8.place(x=400, y=440)

    lbl_Image = Label(insert_data, text=':آپلود عکس', bg='light blue', fg='blue')
    lbl_Image.place(x=530, y=480)
    btn_upload = Button(insert_data, text='آپلود', width=10, relief='groove', activebackground="black",
                        activeforeground='gold', command=upload_image, bg='blue', fg='pink')
    btn_upload.place(x=400, y=480)

    label_img = Label(insert_data, bg='pink')
    label_img.place(x=150, y=250)

    button1 = Button(insert_data, text='ثبت', width=10, background='green', command=register, activebackground="black",
                     activeforeground='gold')
    button1.place(x=70, y=340)

    insert_data.mainloop()

#function definition for the return command , used in button
def return_mainpage():
    f5.withdraw()
    a = f5_creation
    from form1main import Application
    b=Application()

#creating add user tk visual

def f5_creation():
    global f5,entry_id ,label_img, entry1, entry2, entry3, entry4, optionCity, optionProvince, entry8,gender_r

    f5 = Toplevel()
    f5.title('به روز رسانی داده')
    f5.geometry('650x650')
    f5.resizable(False, False)
    f5.config(background='light green')

    logo_image1 = Image.open('images/melli1.jpg')
    user_IMG = ImageTk.PhotoImage(logo_image1)
    img_label = Label(f5, image=user_IMG)
    img_label.place(x=265, y=20)

    # function definition for the return command , used in button

    label = Label(f5, text="  لطفا کد ملی خود را وارد نمایید", fg='yellow', bg='blue', font=('arial', 14, 'bold'))
    label.place(x=210, y=150)

    label1 = Label(f5, text=': کد ملی ', fg='white', bg='blue', width=7)
    label1.place(x=560, y=190)

    entry1 = Entry(f5, bg='light blue', width=18)
    entry1.place(x=445, y=190)

    button1 = Button(f5, text='حذف اطلاعات', background='brown', command=delete_data)
    button1.place(x=140, y=320)

    button1 = Button(f5, text='درج اطلاعات', background='brown', command=insert_datas)
    button1.place(x=240, y=320)

    button1 = Button(f5, text='تغییر اطلاعات', background='brown', command=modify_data)
    button1.place(x=340, y=320)

    button1 = Button(f5, text='بازگشت به صفحه اصلی', background='brown', command=return_mainpage)
    button1.place(x=440, y=320)

    # display tk visual

    f5.mainloop()

