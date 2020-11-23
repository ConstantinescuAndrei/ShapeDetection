import cv2
import imutils
import numpy as np
import shapeList as sl

def getContours(img, imgContour):
    #Metoda findContours ne va returna conturile
    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    for cnt in contours:
        #Pentru fiecare contur vom afla zona
        area = cv2.contourArea(cnt)
        if area > 1000:
            #Daca zona este mai mare de 1000 vom desena un contur in jurul obiectului
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 255), 8)
            #In variabila per vom afla lungimea arcului
            per = cv2.arcLength(cnt, True)
            #Returneaza o lista de puncte
            approx = cv2.approxPolyDP(cnt, 0.02 * per, True)

            #Se va desena in jurul obiectului patratul verde
            x, y, w, h = cv2.boundingRect(approx)
            cv2.rectangle(imgContour, (x, y), (x + w, y + h), (0, 255, 0), 5)

            #Apelam functia pentru a gasi obiectul
            shapeName = sl.getNameOfShape(len(approx), w, h)

            # return shapeName

def findShape(fullImagePath):
    #Din path-ul absolut primit prin variabila fullImagePath extragem doar numele imaginii si extensia acestuia
    imagePath = ''
    for i in range((len(fullImagePath) - 1), 0, -1):
        if fullImagePath[i] == '/':
            break
        imagePath = imagePath + fullImagePath[i]
    imagePath = imagePath[::-1]

    #Cream path-ul pentru citirea ei in variabila img cu ajutorul methodei imread() din biblioteca OpenCV
    path = "images/"
    path += imagePath
    img = cv2.imread(path)

    #Tranformam imaginea in 400x400
    img = imutils.resize(img, width=400, height=400)

    #In imgContour copiem variabila img
    imgContour = img.copy()

    #Bluram poza folosindu-ne de metoda GaussianBlur care ia ca parametrii: imaginea, o matrice "kernel" de 7 pe 7 si o deviatie de 1
    imgBlur = cv2.GaussianBlur(img, (7, 7), 1)
    #Apoi ea este transformata in imagine gri
    imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)

    #Declaram cele doua threshold-uri
    threshold1 = 94
    threshold2 = 80

    #Detectam marginile obiectului folosindu-ne de metoda lui Canny care are ca parametri o imagine gri si cele doua threshold-uri
    imgCanny = cv2.Canny(imgGray, threshold1, threshold2)
    #Aplicam o dilatare peste imaginea Canny
    kernel = np.ones((5, 5))
    imgDil = cv2.dilate(imgCanny, kernel, iterations=1)

    #Apoi apelam functia getContours pe langa desenarea obiectului ne va returna si numele formei
    shapeName = getContours(imgDil, imgContour)

    return img, imgGray, imgBlur, imgCanny, imgContour, shapeName