#Avem hardcodat punctele prin care algoritmul detecteaza forma obiectului

myVar = {
    '1': {'Points': 3, 'Form': 'Triunghi'},
    '2': {'Points': 4, 'Form': ['Patrat', 'Dreptunghi']},
    '3': {'Points': 5, 'Form': 'Pentagon'},
    '4': {'Points': 6, 'Form': 'Hexagon'},
    '5': {'Points': 7, 'Form': 'Heptagon'},
    '6': {'Points': 8, 'Form': 'Cerc'},
    '7': {'Points': 12, 'Form': 'Patrat'},
    '8': {'Points': 10, 'Form': 'Stea'}
    
}

#Declaram o functie care returneaza numele obiectului
def getNameOfShape(pointNumber, w, h):
    for var in myVar:
        #Se verifica daca variabila pointNumber este egala cu 4
        if pointNumber == myVar[var]['Points'] and pointNumber == 4:
            #In cazul in care rezultatul if-ului este unul pozitiv se va verifica daca obiectul este un patrat sau un dreptunghi
            if  ((float(w)/h) >= 0.95 and (float(w)/h) <= 1.05):
                return myVar[var]['Form'][0]
            else:
                return myVar[var]['Form'][1]
        #In cazul in care pointNumber-ul este diferit de 4 dar este egal cu alta forma din array, se ve returna valoarea formei
        elif pointNumber == myVar[var]['Points']:
            return myVar[var]['Form']
    return 0





