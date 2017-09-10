from tkinter import *
from tkinter import messagebox
from random import randint

slovar_tem = {"Harry Potter osebe": ["Albus Dumbledore", "Hermione Granger", "Lord Voldemort", "Hagrid", "Bellatrix Lestrange", "Draco Malfoy", "Minerva McGonagall", "Severus Snape", "Dolores Jane Umbridge", "Fred Weasley", "Ronald Weasley"],
              "Evropske države": ["Nemčija", "Avstrija", "Italija", "Francija", "Španija", "Slovenija", "Belgija", "Nizozemska", "Portugalska", "Švedska", "Norveška", "Finska", "Poljska", "Estonija","Madžarska", "Češka"],
              "Matematične veje": ["Analiza", "Linearna Algebra", "Diskretna Matematika", "Topologija", "Didaktika", "Logika in Množice", "Numerične Metode", "Verjetnost in statistika"],
              "Evropski nogometni veleklubi": ["Barcelona", "Real Madrid", "Manchester United", "Juventus", "Paris Saint Germain", "Athletico Madrid", "Liverpool", "Borrusia Dortmund", "Bayern Munchen", "Monaco", "Chelsea"]
              }


def center_window(height=750, width=750):

    screen_width = okno.winfo_screenwidth()
    screen_height = okno.winfo_screenheight()

    center_width = screen_width/2 - width/2
    center_height = screen_height/2 - height/2
    okno.geometry('{}x{}+{}+{}'.format(width, height, int(center_width), int(center_height)))

    okno.minsize(height, width)
    okno.maxsize(height, width)


def nakljucna_beseda(slovar, izbrana_tema):
    i = randint(0, len(slovar[izbrana_tema])-1)
    return slovar[izbrana_tema][i]


class Hangman:
    def __init__(self, word, okno):
        self.root = okno
        self.word = word.upper()
        self.ugotovitve = [True if e == ' ' else False for e in self.word]
        self.st_napak = 0
        self.napacne_crke = set()
        self.gumbi = {}
        self.abeceda = "abcčdefghijklmnopqrsštuvwxyzž"
        self.root.focus_force()

        self.zgoraj = Frame(okno)
        self.zgoraj.pack(pady=30)

        self.spodaj = Frame(okno)
        self.spodaj.pack()

        self.slika = PhotoImage(file="vislice.gif", format="gif -index {}".format(self.st_napak))
        self.label = Label(self.zgoraj, image=self.slika)
        self.label.pack()

        self.vislice = Message(self.zgoraj, text=self.izpis_besede(), font=('times', 20, ''), aspect=9000, pady=30)
        self.vislice.pack()

        self.narobe = Message(self.zgoraj, font=('times', 12, 'italic'), aspect=9000)
        self.narobe.pack()

        self.root.bind('<Key>', self.pritisk_crke)

        for e, f in enumerate(self.abeceda.upper()):
            gumb = Button(self.spodaj, text=f)
            gumb.config(command=lambda j=f, o=gumb: (self.klik(j), o.grid_remove()), bg="#ffffff", height=4, width=6)
            row_value = self.vrstica(e)
            self.gumbi[f] = gumb
            gumb.bind("<Enter>", lambda event, h=gumb: h.config(bg="#716687"))
            gumb.bind("<Leave>", lambda event, h=gumb: h.config(bg="#ffffff"))
            gumb.grid(row=row_value[0], column=row_value[1])

    def klik(self, crka):
        self.ugibam(crka)
        self.vislice.configure(text=self.izpis_besede())

    def pritisk_crke(self, event):
        crka = event.keysym
        if crka in self.abeceda:
            self.gumbi[crka.upper()].destroy()
            if crka.upper() not in self.napacne_crke:
                self.ugibam(crka)
            self.vislice.configure(text=self.izpis_besede())

    def vrstica(self, i):
        a = int(i / 10)
        if i > 9:
            i -= a * 10
        return a, i

    def beseda(self):
        return self.word

    def vrni_ugotovitve(self):
        return self.ugotovitve

    def izpis_besede(self):
        return ' '.join([e if f is True else '_' for e, f in zip(self.word, self.ugotovitve)])

    def ugibam(self, crka):
        crka = crka.upper()
        if crka in self.word:
            for i in range(len(self.word)):
                if self.word[i] == crka:
                    self.ugotovitve[i] = True
            if len(self.ugotovitve) == self.ugotovitve.count(True):
                self.vislice.configure(text=self.izpis_besede())
                self.konec('Z')
        else:
            self.st_napak += 1
            self.napacne_crke.add(crka)
            try:
                self.slika.configure(format="gif -index {}".format(self.st_napak))
                self.narobe.configure(text="Napačne črke: " + ', '.join(self.napacne_crke))
            except:
                pass
            if self.st_napak == 10:
                self.konec('P')

    def konec(self, condition):
        if condition is 'Z':
            messagebox.showinfo("Zmaga!", "Zmagali ste!")
        if condition is 'P':
            messagebox.showinfo("Poraz... ", "Izgubili ste. \nFraza, ki ste jo iskali, je bila: " + self.word)

class Settings:
    def __init__(self):
        self.izpis = Message(text="Izberite kategorijo:", font=('times', 18, 'bold'), width=350)
        self.izpis.pack(pady=30)
        self.spremenljivka = StringVar(okno)
        self.spremenljivka.set("Evropske države")
        self.meni = OptionMenu(okno, self.spremenljivka, "Evropske države", "Harry Potter osebe", "Matematične veje", "Evropski nogometni klubi")
        self.meni.pack()

        self.gumb = Button(text="Potrdi izbiro", command=self.vrni_temo)
        self.gumb.pack(pady=15)

    def vrni_temo(self):
        global tema
        tema = self.spremenljivka.get()
        okno.destroy()


if __name__ == "__main__":

    okno = Tk()
    okno.wm_title("Nastavitve")
    tema = ""
    c = Settings()
    center_window(height=300, width=200)
    okno.mainloop()

    okno = Tk()
    okno.wm_title("Vislice")
    a = Hangman(nakljucna_beseda(slovar_tem, tema), okno)
    center_window()
    okno.mainloop()
