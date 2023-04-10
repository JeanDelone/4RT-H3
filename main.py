import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import random
import PySimpleGUI as sg

sg.LOOK_AND_FEEL_TABLE['MyCreatedTheme'] = {'BACKGROUND': '#202124',
                                        'TEXT': '#fafafa',
                                        'INPUT': '#3c4042',
                                        'TEXT_INPUT': '#fafafa',
                                        'SCROLL': '#ea80fc',
                                        'BUTTON': ('#202124', '#ea80fc'),
                                        'PROGRESS': ('#202124', '#ea80fc'),
                                        'BORDER': 1, 'SLIDER_DEPTH': 0, 
'PROGRESS_DEPTH': 0, }
sg.theme("MyCreatedTheme")
sg.set_options(font = "Lato 14")

titlebar = [[sg.Column([[sg.Text('A4T H3', grab=True, font="Lato 11")]], pad=(0, 0)),
             sg.Column([[sg.Text(sg.SYMBOL_X, enable_events=True, key='-X-', font="Lato 11")]],  # '❎'
                    element_justification='r', grab=True, pad=(0, 0), expand_x=True)],
            [sg.HorizontalSeparator()]
            ]

image_col = sg.Column([[sg.Image("Images/skull.png", key = "-IMAGE-")]])
control_col = sg.Column([[sg.Slider(range=(0, 255), default_value=154, expand_x=True, enable_events=True, orientation='horizontal', key='-SL-')]],
)

layout = [
    titlebar + 
    [image_col, control_col]

]

WIN = sg.Window("W/E",
                layout,
                size = (1600,900),
                enable_close_attempted_event=True,
                no_titlebar=True,
                # grab_anywhere=True,
                finalize = True,

                )
WIN.bind("<Escape>", "-ESCAPE-")

def make_new_img(thresh):
    img = cv.imread("Images/skull.png")
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    ret, threshold = cv.threshold(gray, thresh, 255, cv.THRESH_BINARY)
    imgbytes = cv.imencode(".png", threshold)[1].tobytes()
    WIN["-IMAGE-"].update(data = imgbytes)


while True:
    event, values = WIN.read()
    make_new_img(values["-SL-"])

    if event in (sg.WIN_CLOSED, "-ESCAPE-", "-X-"):
        break    



WIN.close()

