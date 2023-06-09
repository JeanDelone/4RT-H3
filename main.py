import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import random
import PySimpleGUI as sg

# Custom dark-pink theme

sg.LOOK_AND_FEEL_TABLE['MyCreatedTheme'] = {'BACKGROUND': '#202124',
                                        'TEXT': '#fafafa',
                                        'INPUT': '#3c4042',
                                        'TEXT_INPUT': '#fafafa',
                                        'SCROLL': '#ffb2ff',
                                        'BUTTON': ('#202124', '#ea80fc'),
                                        'PROGRESS': ('#202124', '#ea80fc'),
                                        'BORDER': 1, 'SLIDER_DEPTH': 0, 
'PROGRESS_DEPTH': 0, }
sg.theme("MyCreatedTheme")
sg.set_options(font = "Lato 14")

# Title
titlebar = [[sg.Column([[sg.Text('A4T H3', grab=True, font="Lato 11")]], pad=(0, 0)),
             sg.Column([[sg.Text(sg.SYMBOL_X, enable_events=True, key='-X-', font="Lato 11")]],  # '❎'
                    element_justification='r', grab=True, pad=(0, 0), expand_x=True)],
            [sg.HorizontalSeparator()]
            ]

# Left column
image_col = sg.Column([[sg.Image("Images/skull.png", key = "-IMAGE-")],
                       [sg.Image("Images/skull.png", key = "-IMAGE2-")]],scrollable=True,  vertical_scroll_only=True, pad = (0,0), expand_y = True
                      )

# Right column
image_col2 = sg.Column([
                       [sg.Image("Images/skull.png", key = "-IMAGE3-")]],scrollable=True,  vertical_scroll_only=True, pad = (0,0), expand_y = True
                      )

# Column with control panel
control_col = sg.Column([
                        [sg.Slider(range=(0, 255), default_value=154, expand_x=True, enable_events=True, orientation='horizontal', key='-SL-')],
                        [sg.Slider(range=(1, 100), default_value=50, expand_x=True, enable_events=True, orientation='horizontal', key='-SL2-')],
],
)

layout = [
    [titlebar],
    [image_col, control_col, image_col2]

]

WIN = sg.Window("W/E",
                layout,
                size = (1600,900),
                enable_close_attempted_event=True,
                no_titlebar=True,
                # grab_anywhere=True,
                finalize = True,
                margins = (0,0)

                )
WIN.bind("<Escape>", "-ESCAPE-")

"""
This function is responsible for analyzing image, takes threshold and cont_values that are used in analyzing image
Those values are taken from slider in a main loop.

"""
def make_new_img(thresh, cont_value):
    img = cv.imread("Images/skull.png")
    blank = np.zeros((img.shape[1], img.shape[0],3), dtype="uint8")
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    ret, threshold = cv.threshold(gray, thresh, 255, cv.THRESH_BINARY)
    contours , hierarchy = cv.findContours(threshold, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

    for contour in contours:
        approx = cv.approxPolyDP(contour, cont_value * 1/5000 * cv.arcLength(contour, True), True)

        x = approx.ravel()[0]
        y = approx.ravel()[1] - 5
        if len(approx) == 3:
            # cv.putText( img, "Triangle", (x, y), cv.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0) )
            pass
        elif len(approx) == 4 :
            x, y , w, h = cv.boundingRect(approx)
            aspectRatio = float(w)/h
            print(aspectRatio)
            if aspectRatio >= 0.95 and aspectRatio < 1.05:
                # cv.putText(img, "square", (x, y), cv.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0))
                pass
            else:
                # cv.putText(img, "rectangle", (x, y), cv.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0))
                pass
        elif len(approx) == 5 :
            # cv.putText(img, "pentagon", (x, y), cv.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0))
            pass
        elif len(approx) == 10 :
            # cv.putText(img, "star", (x, y), cv.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0))
            pass
        else:
            cv.putText(img, "circle", (x, y), cv.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 255))
            cv.drawContours(img, [approx], 0, (0, 0, 0), 5)
            cv.drawContours(blank, [approx], 0, (255, 0, 255), 5)
    imgbytes = cv.imencode(".png", threshold)[1].tobytes()
    WIN["-IMAGE2-"].update(data = imgbytes)
    imgbytes = cv.imencode(".png", img)[1].tobytes()
    WIN["-IMAGE-"].update(data = imgbytes)
    imgbytes = cv.imencode(".png", blank)[1].tobytes()
    WIN["-IMAGE3-"].update(data = imgbytes)

# Main loop
while True:
    event, values = WIN.read()
    make_new_img(values["-SL-"], values["-SL2-"])
    if event in (sg.WIN_CLOSED, "-ESCAPE-", "-X-"):
        break    
WIN.close()

