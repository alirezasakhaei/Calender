import json
from tkinter import *
import datetime
from calendar import monthrange
import calendar
import Day

today = datetime.date.today()
directory = 'data.txt'
FONT = 'Times New Romans'
root = Tk()
root.title('Calender')


def obj_to_json(day_obj):
    D = dict()
    D['date'] = str(day_obj.date)
    D['learnt_something'] = day_obj.learnt_something
    D['note'] = day_obj.note
    return json.dumps(D)


def make_days_and_save_them_in_txt():
    with open(directory, 'w') as f:
        for i in range(-500, 500):
            delta = datetime.timedelta(i)
            date = today.__add__(delta)
            day_obj = Day.Day(date)
            D = obj_to_json(day_obj)
            f.write(D + '\n')


make_days_and_save_them_in_txt()


def load_from_txt_into_objects():
    with open(directory, 'r') as file:
        all_data = file.readlines()
        objects_dict = dict()
        for line in all_data:
            D = json.loads(line)
            obj = Day.Day(D['date'])
            obj.learnt_something = D['learnt_something']
            obj.note = D['note']
            objects_dict[D['date']] = obj
    return objects_dict


###########
objs_dict = load_from_txt_into_objects()
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
year, month = datetime.date.today().year, datetime.date.today().month
###########

def update_the_txt_file():
    # global objs_dict
    with open(directory, 'w') as file:
        for key, value in objs_dict.items():
            D = obj_to_json(value)
            file.write(D + '\n')


def do_the_day_updating_func(date, ls_var, note_var):
    def do_the_day_updating():
        global objs_dict
        objs_dict[str(date)].learnt_something = bool(ls_var.get())
        objs_dict[str(date)].note = note_var.get()
        update_the_txt_file()

    return do_the_day_updating


def update_day_func(year, month, day):
    def update_day():
        day_view = Toplevel(root)
        date = datetime.date(year, month, day + 1)
        day_view.title(str(date))

        ls_var = IntVar()

        Checkbutton(day_view,
                    text='Learnt Something',
                    variable=ls_var,
                    width=30,
                    font=('Times New Romans', 20)).pack()

        if objs_dict[str(date)].learnt_something:
            ls_var.set(1)

        note_var = StringVar()
        Entry(day_view,
              textvariable= note_var,
              font=('Times New Romans', 20)).pack()
        note_var.set(objs_dict[str(date)].note)

        Button(day_view,
               text='Update',
               padx=30,
               font=('Times New Romans', 15),
               command=do_the_day_updating_func(date, ls_var, note_var)).pack(pady=10)

    return update_day


def show_month_func(year, month):
    def show_month():
        firstday, range_of_month = monthrange(year, month)
        month_view = Toplevel(root, bg='white')
        month_name = calendar.month_name[month]
        month_name_frame = LabelFrame(month_view)
        month_name_frame.grid(row=0, column=0, columnspan=6, pady=10, padx=30)
        month_name_label = Label(month_name_frame,
                                 text=month_name,
                                 font=("Times New Romans", 30),
                                 width=40,
                                 fg='black')
        month_name_label.pack()
        ###########
        month_names_days_frame = LabelFrame(month_view)
        month_names_days_frame.grid(row=1, column=0, columnspan=7, pady=10)
        for i, name in enumerate(days):
            Label(month_names_days_frame,
                  text=name,
                  font=("Times New Romans", 15),
                  fg='black').grid(row=0, column=i)

        def find_row_col(num, w):
            d = num + w
            row = d // 7
            column = d % 7
            return row, column

        for day in range(range_of_month):
            row, column = find_row_col(day, firstday)
            text = f'{day + 1:02d}'
            BUTTON_SIZE: int = 25
            Button(month_names_days_frame,
                   text=text,
                   padx=BUTTON_SIZE,
                   pady=BUTTON_SIZE,
                   command=update_day_func(year, month, day),
                   bg='black',
                   fg='cyan',
                   font=('Times New Romans', 7)).grid(row=row + 1, column=column, padx=10, pady=5)

    return show_month


# year, month = datetime.date.today().year, datetime.date.today().month


def big_picture():
    big_picture_view = Toplevel(root)
    for i in range(1, 13):
        month_name = calendar.month_name[i]
        Button(big_picture_view,
               text=month_name,
               command=show_month_func(year, i),
               pady=25,
               padx=25,
               width=10,
               height=5).grid(row=(i - 1) // 4, column=(i - 1) % 4, padx=10, pady=5)

Button(root,
       text= 'month view',
       command=big_picture,
       pady=25,
       padx=25,
       width=10,
       height=5).grid(row=0, column=0, padx=10, pady=5)


def go_to_today():
    year, month, day = datetime.date.today().year, datetime.date.today().month, datetime.date.today().day
    update_day_func(year, month, day)()


Button(root,
       text= 'go to today',
       command=go_to_today,
       pady=25,
       padx=25,
       width=10,
       height=5).grid(row=0, column=1, padx=10, pady=5)

root.mainloop()
