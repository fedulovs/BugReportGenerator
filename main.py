import PySimpleGUI as sg
import pyperclip

sg.theme('dark grey 8')

devices_conf = "devices.conf"
android_v_conf = "android_v.conf"

devices = {}
android_versions = {}
branches = {"Dev": False,"Release": False}
dev_ver = {}

device = ""
android_version = ""
branch = ""

with open(devices_conf, "r") as f:
    for line in f:
        line = line.replace("\n", "")
        if not (line == " " or line == ""):
            if not line[0] == "#":
                devices.update({line: False})

with open(android_v_conf, "r") as f:
    for line in f:
        line = line.replace("\n", "")
        if not (line == " " or line == ""):
            if not line[0] == "#":
                android_versions.update({line: False})

def get_devices_list():
    list = ""
    for device in dev_ver:
        list += device + "\n"
    return list

def generate_layout():
    layout = [[
        sg.Frame('Parameters',
                 [[sg.Text("Release version:", font=('Arial', 15))],
                  [sg.Input(key="release_version", size=(5, None))],
                  [sg.Text("Build version:", font=('Arial', 15))],
                  [sg.Input(key="build_version", size=(5, None))],
                  [sg.Text("Device: ", size=(5, 1), font=('Arial', 15))],
                  [sg.Combo(list(devices.keys()), key='device', size=(15, 1))],
                  [sg.Text("Android version: ", size=(15, 1), font=('Arial', 15))],
                  [sg.Combo(list(android_versions.keys()), key='android')],
                  [sg.Text("Branch:", font=('Arial', 15))],
                  [sg.Checkbox("Dev", key="Dev", enable_events=True, font=('Arial', 12))],
                  [sg.Checkbox("Release", key="Release", enable_events=True, font=('Arial', 12))]], font=('Arial', 15), vertical_alignment='top', size=(19, 19)
                 ),

        sg.Frame('Devices added', [[sg.Text(get_devices_list(), key="device_list", font=('Arial', 12), size=(19, 19))]],
                 font=('Arial', 15), vertical_alignment='top', size=(19, 18))
    ],
        [sg.Frame('Report', [[sg.Multiline(generate_message(), key="report", size=(40, 10), font=('Arial', 12))]],
                  font=('Arial', 15))],
        [sg.OK(button_text="Commit", font=('Arial', 15)), sg.Cancel(font=('Arial', 15))]]

    return layout

def parse_window_data(values):
    device = ""
    android_v = ""
    if "device" in values:
        device = values["device"]
    if "android" in values:
        android_v = values["android"]
    if "release_version" in values:
        release_v = values["release_version"]
    if "build_version" in values:
        build_v = values["build_version"]

    if not (device == "" and android_v == ""):
        if device in dev_ver:
            if not android_v in dev_ver[device]:
                dev_ver[device].append(android_v)
        else:
            dev_ver.update({device: [android_v]})
    for branch in branches:
        branches[branch] = values[branch]
    return release_v, build_v


def generate_message():
    device = ""
    for device_item in dev_ver:
        for version in dev_ver[device_item]:
            device += " %s / Android %s," % (device_item, version)
    device = device[:-1]
    branch = ""
    for branch_item in branches:
        if branches[branch_item]:
            branch += branch_item + ", "
    branch = branch[:-2]
    message = "h3. Номер сборки приложения: %s (%s)\nh3. Устройство с версией Android:%s\nh3. Ветка: %s\nh3. Шаги:\n\n# \n# \n\nh3. Фактический результат:\nh3. Ожидаемый результат:  " % (
        release_v, build_v, device, branch)
    return message


if __name__ == '__main__':
    release_v = ""
    build_v = ""
    layout = generate_layout()
    window = sg.Window('Bug Report Generator', layout, finalize=True)
    while True:
        event, values = window.read()
        if event in (sg.OK(), "Commit"):
            release_v, build_v = parse_window_data(values)
            window["device_list"].update(get_devices_list())
            window["report"].update(generate_message())
        if event in (sg.WIN_CLOSED, 'Cancel'):
            break
    report = generate_message()
    print(report)
    window.close()
    pyperclip.copy(report)