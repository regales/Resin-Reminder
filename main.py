from pystray import Icon as icon, Menu as menu, MenuItem as item
from PIL import Image
import PySimpleGUI as sg
from time import sleep
from win10toast import ToastNotifier
from threading import Thread
import os


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


image = Image.open(resource_path('resin.ico'))
sg.theme("systemdefaultforreal")

toaster = ToastNotifier()


def set_reminder(amount, duration, notifyOnSet):
    durationMins = duration * 60

    if notifyOnSet:
        toaster.show_toast("Reminder set", f"Your reminder for {amount} resin has been set.", icon_path=resource_path("resin.ico"))

    sleep(durationMins)

    toaster.show_toast(f"Your {amount} resin has regenerated!", "Enjoy your DEF% artifact!", icon_path=resource_path("resin.ico"),
                       duration=30, threaded=True)


def on_clicked():
    window = sg.Window("Resin Reminder", [
        [sg.Text("Select how much resin you want a reminder when regenerated:"),
         sg.Spin(key='-RESINNUM-', initial_value=1, values=list(range(1, 160)))],
        [sg.Text('Notification when reminder is set:'), sg.Checkbox("", default=True, key='-SETNOTIF-')],
        [sg.Submit("Set reminder"), sg.Exit()]])
    window.set_icon(resource_path('resin.ico'))
    event, values = window.read()
    window.close()
    if event == sg.WIN_CLOSED or event == 'Exit':
        exit()
    reminderMins = values['-RESINNUM-'] * 8
    Thread(name="reminder subprocess", target=set_reminder(values['-RESINNUM-'], reminderMins, values['-SETNOTIF-']))


on_clicked()

while True:
    icon('test', image, menu=menu(item('Open', on_clicked, default=True))).run()
