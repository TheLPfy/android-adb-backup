import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ppadb.client import Client as AdbClient
import datetime as date


adb = None


def create_year_dropdown(window):
    now = date.datetime.now()

    years = []

    # Combobox creation
    yearschoosen = ttk.Combobox(window, width=27, textvariable=tk.StringVar())

    for year in range(now.year - 5, now.year + 5, 1):
        years.append(' ' + str(year))

    # label
    ttk.Label(window, text="Select the Year :",
              font=("Times New Roman", 10)).grid(column=0, row=4, padx=10, pady=25)

    yearschoosen['values'] = years

    yearschoosen.grid(column=1, row=4)
    yearschoosen.current()

    return yearschoosen


def create_month_dropdown(window):
    # label
    ttk.Label(window, text="Select the Month :",
              font=("Times New Roman", 10)).grid(column=0, row=5, padx=10, pady=25)

    # Combobox creation
    monthchoosen = ttk.Combobox(window, width=27, textvariable=tk.StringVar())

    # Adding combobox drop down list
    monthchoosen['values'] = (' 01',
                              ' 02',
                              ' 03',
                              ' 04',
                              ' 05',
                              ' 06',
                              ' 07',
                              ' 08',
                              ' 09',
                              ' 10',
                              ' 11',
                              ' 12')

    monthchoosen.grid(column=1, row=5)
    monthchoosen.current()

    return monthchoosen


def get_files(path):
    ls = adb.shell('ls -p '+ path +' 2>&1 | grep -v "Permission denied"')
    for listing in str.splitlines(ls):
        if str.endswith(listing, '/'):
            print(path+listing)
            get_files(path+listing)


def backup(year, month):
    if year == '' or month == '':
        alert("Bitte Jahr und Monat auswählen")
        return
    global adb
    adb = connect()

    get_files("/sdcard/")


def create_button(window, year, month):
    # label
    ttk.Label(window, text="Starte Backup :",
              font=("Times New Roman", 10)).grid(column=0, row=6, padx=10, pady=25)

    # Button creation
    btn = ttk.Button(window, width=10, text="Backup", command=(lambda: backup(year.get(), month.get())))

    btn.grid(column=1, row=6)


def alert(msg):
    messagebox.showwarning(title="Problem", message=msg)


def connect():
    client = AdbClient(host="127.0.0.1", port=5037)

    devices = client.devices()

    device = devices[0]

    if len(devices) == 0:
        alert("Gerät nicht gefunden.")
        return
    return device


def main():
    # Creating tkinter window
    window = tk.Tk()
    window.title('@Tobias Etzenberger')
    window.geometry('500x250')

    # label text for title
    ttk.Label(window, text="Android Backup",
              background='green', foreground="white",
              font=("Times New Roman", 15)).grid(row=0, column=1)

    # Combobox years
    yearD = create_year_dropdown(window)

    monthD = create_month_dropdown(window)

    create_button(window, yearD, monthD)

    window.mainloop()


if __name__ == '__main__':
    main()
