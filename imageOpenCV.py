import cv2
import numpy as np
import PySimpleGUI as sg
import os
import detectShapes as detectShapes

#Declaram variabilele globale in care vom stoca imaginiile

global imgOriginal, imgGray, imgBlur, imgCanny, imgContour, shapeName

#Fereastra va fi impartita in doua coloane

#Prima coloana care contine cautarea foldarului cu imagini, a listei si a butoanelor
fileListColumn = [
    [
        sg.Text("Image Folder"),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),        
    ],
    
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
        )
    ],
    [
        sg.Button('Normal image', key="-ORIGINAL-"),
        sg.Button('Gray image', key="-GRAY-"),
        sg.Button('Blur image', key="-BLUR-"),
    ],
    [
        sg.Button('Canny image', key="-CANNY-"),
        sg.Button('Detect shape', key="-SHAPE-"),
    ],
    [
        sg.Button('Exit', key="-EXIT-")
    ]
]

#A doua coloana in care se afiseaza imaginiile
imageViewerColumn = [
    
    [sg.Text("Numele formei este: ")],
    [sg.Text(size=(40, 1), key="-TOUT-")],
    [sg.Image(key="-IMAGE-")],
]

layout = [
    [
        sg.Column(fileListColumn),
        sg.VSeparator(),
        sg.Column(imageViewerColumn),
    ]
]

#Cream fereastra
sg.theme("LightGreen")
window = sg.Window("Img", layout)

while True:
    #Pentru fiecare iteratie a bucle infinite salvam datele primite de la GUI
    event, values = window.read()

    #Prima conditie verifica daca am citit un folder din computer-ul nostru
    if event == "-FOLDER-":
        folder = values["-FOLDER-"]

        #Se va verifica daca in variabila folder avem directoare, iar daca aplicatia gaseste acestea se vor stoca in fileList
        try:
            fileList = os.listdir(folder)
        except:
            fileList = []

        #Variabila fnames va retine toate fisierele care se vor termina cu extensia .png sau .gif
        fnames = [
            f
            for f in fileList
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith((".png", ".gif"))
        ]

        #Se va updata fereastra cu lista de poze salvata in fnames
        window["-FILE LIST-"].update(fnames)
    #Se verifica daca a fost aleasa o poza din noua lista
    elif event == "-FILE LIST-":
        try:
            #Daca s-a ales o noua poza, variabila filename va retine path-ul absolut pentru gasirea pozei
            filename = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
            )
            
            #Metoda findShape va returna imaginea originala, gry, blurata, detectia Canny,cu obiectul conturat si numele figurii
            global imgOriginal, imgGray, imgBlur, imgCanny, imgContour, shapeName
            imgOriginal, imgGray, imgBlur, imgCanny, imgContour, shapeName = detectShapes.findShape(filename)

            #Convertim imaginea intr-un vector de biti
            imgBytes = cv2.imencode(".png", imgOriginal)[1].tobytes()

            #Actualizam numele formei si imaginea
            window['-TOUT-'].update(shapeName)
            window["-IMAGE-"].update(data=imgBytes)
        except:
            pass
    #Se verifica daca a fost apasat butonul pentru afisarea imaginii originale
    elif event == "-ORIGINAL-":
        #Convertim imaginea intr-un vector de biti
        imgBytes = cv2.imencode(".png", imgOriginal)[1].tobytes()

        #Actualizam imaginea
        window['-TOUT-'].update(shapeName)
    #Se verifica daca a fost apasat butonul pentru afisarea imaginii gri
    elif event == "-GRAY-":
        #Convertim imaginea intr-un vector de biti
        imgBytes = cv2.imencode(".png", imgGray)[1].tobytes()

        #Actualizam imaginea
        window["-IMAGE-"].update(data=imgBytes)
    #Se verifica daca a fost apasat butonul pentru afisarea imaginii blurate
    elif event == "-BLUR-":
        #Convertim imaginea intr-un vector de biti
        imgBytes = cv2.imencode(".png", imgBlur)[1].tobytes()

        #Actualizam imaginea
        window["-IMAGE-"].update(data=imgBytes)
    #Se verifica daca a fost apasat butonul pentru afisarea imaginii dupa detectia Canny
    elif event == "-CANNY-":
        #Convertim imaginea intr-un vector de biti
        imgBytes = cv2.imencode(".png", imgCanny)[1].tobytes()

        #Actualizam imaginea
        window["-IMAGE-"].update(data=imgBytes)
    #Se verigica daca a fost apasat butonul pentru afisarea imaginii unde obiectul este conturat
    elif event == "-SHAPE-":
        #Convertim imaginea intr-un vector de biti
        imgBytes = cv2.imencode(".png", imgContour)[1].tobytes()

        #Actualizam imaginea
        window["-IMAGE-"].update(data=imgBytes)
              
    #In cazul in care se apasa butonul exit sau x-ul ferestrei aplicatia va inchide
    if event == "-EXIT-" or event == sg.WIN_CLOSED:
        break

window.close()