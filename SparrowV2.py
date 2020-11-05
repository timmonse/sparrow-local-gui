#!/usr/bin/env Python3
import PySimpleGUI as sg
import cv2
import imutils
import signal
import subprocess
import os

sg.ChangeLookAndFeel('DefaultNoMoreNagging')


# ------ Menu Definition ------ #
menu_def = [['File', ['Open', 'Save', 'Exit', 'Properties']],
            ['Edit', ['Paste', ['Special', 'Normal', ], 'Undo'], ],
            ['Help', 'About...'], ]

# ------ Main Layout ------ #
layout = [
    [sg.Menu(menu_def, tearoff=True)],
    [sg.Text('Sparrow', size=(55, 1), justification='center', font=("Helvetica", 25), relief=sg.RELIEF_RIDGE)],
    [sg.Image(filename='', key='_IMAGE_', size=(10, 10)),
     sg.Frame('Display Video Feed', [[
         sg.Button('Hide/Show', button_color=('white', 'Black'))
     ]]),
     sg.Frame('Control Panel', [[
         sg.Button('Record', button_color=('white', 'red')),
         sg.Button('Stop', button_color=('white', 'black'))
     ], [sg.Button('Upload', button_color=('white', 'green'))]])
     ],
    [sg.Submit(tooltip='Click to submit this window'), sg.Cancel()]
]

# Keep no_titlebar == True to disable title bar
# Dimensions hardcoded to screen values
# Add element_justification='c' to center the elements
window = sg.Window('Sparrow v2', layout, no_titlebar=False, default_element_size=(40, 1), grab_anywhere=False,
                   location=(0, 0), size=(1024, 600), keep_on_top=False, element_justification='c').Finalize()

# Maximize the window automatically
window.Maximize()

# event, values = window.read()
cap = cv2.VideoCapture(2)# Setup the OpenCV capture device (webcam)

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
    if event == "Stop":
        # window.FindElement('_IMAGE_').Update(visible=False)
        # Pause and stop logic to go here
        for child in children:
            os.killpg(os.getpgid(child.pid), signal.SIGTERM)
        timeout = 10000000
    if event == "Hide/Show":
        window.FindElement('_IMAGE_').Update(visible=isVisible)
        isVisible = not isVisible
    if event == "Record":
        timeout = 20
        p = subprocess.Popen('~/recordWebcam.sh', stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
        p2 = subprocess.Popen('alpr /dev/video2 -j > ~/Sparrow_Master/output/JSON.txt', stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
        children.append(p)
        children.append(p2)

window.close()

sg.popup('Title',
         'The results of the window.',
         'The button clicked was "{}"'.format(event),
         'The values are', values)
