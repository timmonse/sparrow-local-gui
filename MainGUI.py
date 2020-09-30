#!/usr/bin/env Python3
import PySimpleGUI as sg
import cv2

# Use this to preview themes
# sg.preview_all_look_and_feel_themes()

# FIXME | Test with DarkGrey9
sg.ChangeLookAndFeel('Default')

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
    [sg.Image(filename='', key='_IMAGE_', size=(40, 40)),
     sg.Frame('Display Controls', [[
         sg.Button('Hide', button_color=('white', 'Black')),sg.Button('Show', button_color=('white', 'Gray'))
     ]]),
     sg.Frame('Camera Controls', [[
         sg.Button('Record', button_color=('white', 'red')), sg.Button('Pause', button_color=('black', 'yellow')),
         sg.Button('Stop', button_color=('white', 'black'))
     ], [sg.Text('Put the next row here')]])
     ],
    [sg.Submit(tooltip='Click to submit this window'), sg.Cancel()]
]

# Keep no_titlebar == True to disable title bar
# Dimensions hardcoded to screen values
# Add element_justification='c' to center the elements
window = sg.Window('Sparrow v1', layout, no_titlebar=False, default_element_size=(40, 1), grab_anywhere=False,
                   location=(0, 0), size=(1024, 600), keep_on_top=True).Finalize()

# Maximize the window automatically
# window.Maximize()

# event, values = window.read()
cap = cv2.VideoCapture(0)  # Setup the OpenCV capture device (webcam)
timeout = 20
while True:
    event, values = window.read(timeout=timeout, timeout_key='timeout')
    if event in (sg.WIN_CLOSED, 'Cancel'):
        break
    ret, frame = cap.read()  # Read image from capture device (camera)
    imgbytes = cv2.imencode('.png', frame)[1].tobytes()  # Convert the image to PNG Bytes
    window.FindElement('_IMAGE_').Update(data=imgbytes)  # Change the Image Element to show the new image
    if event == "Pause" or event == "Stop":
        # window.FindElement('_IMAGE_').Update(visible=False)
        # Pause and stop logic to go here
        timeout = 10000000
    if event == "Record":
        timeout = 20
    if event == "Hide":
        window.FindElement('_IMAGE_').Update(visible=False)
    if event == "Show":
        window.FindElement('_IMAGE_').Update(visible=True)

window.close()

sg.popup('Title',
         'The results of the window.',
         'The button clicked was "{}"'.format(event),
         'The values are', values)
