#!/usr/bin/env Python3
import PySimpleGUI as sg
import cv2
import imutils
import signal

import subprocess
import os

from subprocess import Popen, PIPE

# Use this to preview themes
# sg.preview_all_look_and_feel_themes()

# FIXME | Test with DarkGrey9
sg.ChangeLookAndFeel('DefaultNoMoreNagging')


# ------ Menu Definition ------ #
menu_def = [['File', ['Open', 'Save', 'Exit', 'Properties']],
            ['Edit', ['Paste', ['Special', 'Normal', ], 'Undo'], ],
            ['Help', 'About...'], ]

# ------ Main Layout ------ #
layout = [
    [sg.Menu(menu_def, tearoff=True)],
    [sg.Text('Sparrow', size=(55, 1), justification='center', font=("Helvetica", 25), relief=sg.RELIEF_RIDGE)],
    [sg.Text('Video Storage Location', size=(17, 1), auto_size_text=False, justification='left'),
     sg.InputText('Default Folder'), sg.FolderBrowse()],
    [sg.Image(filename='', key='_IMAGE_', size=(10, 10)),
     sg.Frame('Display Video Feed', [[
         sg.Button('Hide/Show', button_color=('white', 'Black'))
     ]]),
     sg.Frame('Camera Controls', [[
         sg.Button('Record', button_color=('white', 'red')), sg.Button('Pause', button_color=('black', 'yellow')),
         sg.Button('Resume', button_color=('white', 'green')), sg.Button('Stop', button_color=('white', 'black'))
     ], [sg.Text('Put the next row here')]])
     ],
    [sg.Submit(tooltip='Click to submit this window'), sg.Cancel()]
]

# Keep no_titlebar == True to disable title bar
# Dimensions hardcoded to screen values
# Add element_justification='c' to center the elements
window = sg.Window('Sparrow v1', layout, no_titlebar=False, default_element_size=(40, 1), grab_anywhere=False,
                   location=(0, 0), size=(1024, 600), keep_on_top=False).Finalize()

# Maximize the window automatically
window.Maximize()

# Terminal command tests
# list_files = subprocess.run(["ls", "-l"])
# print("The exit code was: %d" % list_files.returncode)

# event, values = window.read()
cap = cv2.VideoCapture(1)  # Setup the OpenCV capture device (webcam)

#Set above to 2 when testing split camera, 1 when testing other

timeout = 20
isVisible = False
output = "none"
errors = "no errors"
children = []
while True:
    event, values = window.read(timeout=timeout, timeout_key='timeout')
    if event in (sg.WIN_CLOSED, 'Cancel'):
        break
    ret, frame = cap.read()  # Read image from capture device (camera)

    frame = imutils.resize(frame, width=520)
    imgbytes = cv2.imencode('.png', frame)[1].tobytes()  # Convert the image to PNG Bytes
    window.FindElement('_IMAGE_').Update(data=imgbytes)  # Change the Image Element to show the new image
    if event == "Pause" or event == "Stop":
        # window.FindElement('_IMAGE_').Update(visible=False)
        # Pause and stop logic to go here
        for child in children:
            os.killpg(os.getpgid(child.pid), signal.SIGTERM)
            # child.kill()
        timeout = 10000000
    if event == "Resume":
        timeout = 20
        # subprocess.call(['gnome-terminal', '-x', 'ls -l'])
        # subprocess.call(['gnome-terminal', '-x', 'ls -l'])
        # Subprogram = subprocess.Popen(['gnome-terminal', '-e', 'ls -l'])
        # os.system("gnome-terminal -x ls -l")
        # subprocess.call(['/bin/bash', '-i', '-c', "~/recordWebcam.sh"])
        # os.popen('sh ~/recordWebcam.sh')
    if event == "Hide/Show":
        window.FindElement('_IMAGE_').Update(visible=isVisible)
        isVisible = not isVisible
    if event == "Record":
        timeout = 20
        # print(os.listdir()) # This example will work on windows
        # output = os.system("alpr webcam")
        # output = subprocess.call(["alpr", "webcam"], shell=True)
        # subprocess.call(["echo", "hello"], shell=True)
        # print("hello")
        # list_dir = subprocess.Popen(["ls", "-l"]) # This example will work on linux
        # list_dir.wait()

        # testOut = subprocess.Popen(["alpr", "webcam"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        #                                     stderr=subprocess.PIPE, text=True)
        # output, errors = testOut.communicate()
        # testOut.wait()
        p = subprocess.Popen('~/recordWebcam.sh', stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
        p2 = subprocess.Popen('alpr /dev/video2 -j > ~/Sparrow_Master/output/JSON.txt', stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
        children.append(p)
        children.append(p2)
    # print(output)
    # print(errors)

window.close()

sg.popup('Title',
         'The results of the window.',
         'The button clicked was "{}"'.format(event),
         'The values are', values)
