import csv
import pandas as pd
from tkinter import *
from tkinter.ttk import *

attribute_names = []
attributes = csv.reader(open("zoo/attributes.csv"), delimiter=',', quoting=csv.QUOTE_MINIMAL)
attribute_namesv2 = []

for row in attributes:
    attribute_names = row
    dataset = pd.read_csv('zoo/zoo._polskie.csv', names=row)

for sth in attribute_names:
    if sth != 'name':
        attribute_namesv2.append(sth)

question = pd.read_csv('zoo/question.csv', names=attribute_namesv2)

class akinator:
    def __init__(self, node):
        self.window = Tk()
        self.window.geometry("400x400")
        self.var = StringVar()
        self.node = node
        self.makeFrame(node)

    def makeFrame(self, node):
        variable = {}
        if str(type(node)) == "<class 'dict'>":
            for key, value in node.items():
                self.key = key
                count = 0
                for cos in value:
                    if key == 'gromada':
                        variable[cos] = self.nameClass(cos)
                    elif key == 'pletwy' or key == 'nogi':
                        variable[cos] = int(cos)
                    elif cos == 1 or cos == '1':
                        variable[cos] = 'tak'
                    elif cos == 0 or cos == '0':
                        variable[cos] = 'nie'
                    elif cos == '?':
                        variable[cos] = 'nie wiadomo'
                    count += 1
                if count == 1:
                    variable['x'] = 'inna odpowiedz'
            string = self.key
            msg = Message(self.window, textvariable=self.var, relief=RAISED)
            self.var.set(str(question[string][0]))

            msg.pack()
            for (text, value) in variable.items():
                Radiobutton(self.window, text=value, variable=self.var,
                            value=text, command=self.function).pack(side=TOP)
        else:
            string = node
            print("Czy udało się odgadnąć? [" + string + "]")
            odp = input("[tak/nie] ")
            if odp == 'nie':
                self.saveNewAnimal(string)
                msg = Message(self.window, textvariable=self.var, relief=RAISED)
                self.var.set("Przykro nam, że nie udało się znaleźć odpowiedniego zwierzecia...")
                msg.pack()
            else:
                msg = Message(self.window, textvariable=self.var, relief=RAISED)
                self.var.set("ODGADNIĘTE ZWIERZĘ TO: " + string)
                msg.pack()
        mainloop()

    def __del__(self):
        print("")

    def function(self):
        wartosc = self.var.get()
        if wartosc == 'x':
            exit(self)
        elif wartosc == '?' or (wartosc == '0' and self.key != 'domowy') or (wartosc == '1' and self.key != 'domowy'):
            self.node = self.node[self.key][wartosc]
            makeNew(self)
        else:
            self.node = self.node[self.key][float(wartosc)]
            makeNew(self)

    def nameClass(self, val):
        if val == 1:
            return 'ssaki'
        elif val == 2:
            return 'ptaki'
        elif val == 3:
            return 'gady'
        elif val == 4:
            return 'ryby'
        elif val == 5:
            return 'plazy'
        elif val == 6:
            return 'owady'
        elif val == 7:
            return 'zwierzeta morskie'

    def saveNewAnimal(self, string):
        print("O jakim zwierzęciu myślał*ś?")
        zwierze = input("")
        print("Czym się różni " + string + " od " + zwierze + "?")
        cecha = input("nazwa cechy binarnej: ")
        print("Jaką wartość przyjmuje cecha " + cecha + " dla " + string + "?")
        odp1 = input("[0/1] ")
        print("Jaką wartość przyjmuje cecha " + cecha + " dla " + zwierze + "?")
        odp2 = input("[0/1] (różna od " + odp1 + ") ")
        print(cecha + " { " + string + " : " + odp1 + "; " + zwierze + " : " + odp2 + " }")
        # print(attribute_names)
        attribute_names[-1] = cecha
        attribute_names.append('name')
        # print(attribute_names)
        print("Czy mogl*bys sformulowac pytanie dotyczace tej cechy?")
        newQuestion = input("")
        csv.register_dialect('myDialect',
                             delimiter=',',
                             quotechar='"',
                             skipinitialspace=True,
                             quoting=csv.QUOTE_ALL)
        questions = []
        with open('zoo/question.csv', 'r', newline='') as file:
            reader = csv.reader(file, dialect='myDialect')
            for row in reader:
                row.append(newQuestion)
                questions = row
        with open('zoo/question.csv', 'w', newline='') as f:
            writer = csv.writer(f, dialect='myDialect')
            writer.writerow(questions)
        writer = csv.writer(open('zoo/attributes.csv', 'w', newline=''), delimiter=',',
                            quoting=csv.QUOTE_MINIMAL)
        writer.writerow(attribute_names)
        reader = csv.reader(open("zoo/zoo._polskie.csv"), delimiter=',', quoting=csv.QUOTE_MINIMAL)
        rows = []
        for row in reader:
            # print(row[-1])
            name = row[-1]
            if name == string:
                row[-1] = odp1
            elif name == zwierze:
                row[-1] = odp2
            else:
                row[-1] = '?'
            row.append(name)
            rows.append(row)
        with open('zoo/zoo._polskie.csv', 'w', newline='') as file:
                writerRows = csv.writer(file, quoting=csv.QUOTE_MINIMAL,
                                    delimiter=',')
                writerRows.writerows(rows)
        print("Nowe dane zostaly zapisane.")


def exit(window1: akinator):
    window1.window.destroy()
    print("przykro nam, nie ma takiego zwierzecia")


def makeNew(window1: akinator):
    node = window1.node
    window1.window.destroy()
    del window1
    akinator(node)