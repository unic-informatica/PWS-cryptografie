from Desalg import ECB, des, tripledes, PAD_PKCS5, CBC
import tkinter as tk
from tkinter import ttk
from tkinter import font as fo
from tkinter.filedialog import askopenfilename
from binascii import unhexlify as unhex
#Eerst worden alle libaries geimport die nodig zijn.
#Hieronder is de basis van de app beschreven.
class mainframes(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
#Hier staan lettertypes beschreven zodat die niet altijd ingetypt moeten worden.
        self.titlefont = fo.Font(family="Arial", size=20, weight="bold")
        self.smalltitlefont = fo.Font(family="Arial", size=14, weight="bold")
        self.normalfont = fo.Font(family="Arial", size=11)
#Hier wordt gezegd welk frame er als eerst moet staan.
        self.frame = None
        self.show_frame(Menu)
#Hieronder wordt beschreven hoe het veranderen van frames werkt.
    def show_frame(self, frame_class):
#Eerst wordt de oude frame vernietigd, een daarna wordt de nieuwe laten zien.
        new_frame = frame_class(self)
        if self.frame is not None:
            self.frame.destroy()
        self.frame = new_frame
#Onder show_frame moeten ook alle frame eigenschappen staan.
#Dit is in dit geval alleen hoe het grid inelkaar zit en hoe ver alles van elkaar af staat.
        self.frame.grid(column=0, row=0, sticky=("N, W, E, S,"))
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        for child in self.frame.winfo_children():
            child.grid_configure(padx=50, pady=50, ipadx=5, ipady=5)
#Elke class waar Tk.Frame in staat is een ander frame.
#De meeste van deze frames zijn menu's.
#Dit frame is de eerste die te zien is.    
class Menu(tk.Frame):
    def __init__(self, parent):
#De bovenste line is nodig om het frame te laten zien.
        tk.Frame.__init__(self, parent)
#Op dit frame staan 5 knoppen en een label.
#De label gebruikt een van de lettertiepes die is beschreven aan het begin.
#Achter elk onderdeel staan waar ze moeten staan in het grid.
#Column is de x-as en row de y-as en sticky is waar ze aan vast plakken.
#Alle knoppen zijn voor andere frames laten zien die command moet met lambda want anders werkt het niet.
        tk.ttk.Label(self, text="Main menu", font=parent.titlefont).grid(column=1, row=1, columnspan=2)
        tk.ttk.Button(self, text="DES", command=lambda: parent.show_frame(Desp), width=30).grid(column=1, row=2, sticky=("W, E"))
        tk.ttk.Button(self, text="DES File", command=lambda: parent.show_frame(Desfile), width=30).grid(column=2, row=2, sticky=("W, E"))
        tk.ttk.Button(self, text="Triple DES", command=lambda: parent.show_frame(tr)).grid(column=1, row=3, sticky=("W, E"))
        tk.ttk.Button(self, text="Triple DES File", command=lambda: parent.show_frame(trfile)).grid(column=2, row=3, sticky=("W, E"))
        tk.ttk.Button(self, text="Instruction manual", command=lambda: parent.show_frame(menig)).grid(column=1, row=4, columnspan=2, sticky=("W, E"))
#Hieronder staat nog een menu
class Desp(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        tk.ttk.Label(self, text="DES Menu", font=parent.titlefont).grid(column=1, row=1, columnspan=3)
        tk.ttk.Button(self, text="DES Encryption", command=lambda: parent.show_frame(Despen), width=30).grid(column=1, row=2, sticky=("W, E"))
        tk.ttk.Button(self, text="DES Decryption", command=lambda: parent.show_frame(Despde), width=30).grid(column=2, row=2, sticky=("W, E"))
        tk.ttk.Button(self, text="Go back to main menu", command=lambda: parent.show_frame(Menu), width=30).grid(column=3, row=2, sticky=("W, E"))
#Hieronder staat het encrypt frame van DES.
class Despen(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
#Er is voor gekozen om variablen boven aan te zetten.
#De rest van de onderdelen zijn gesorteerd op grid plaats.
#De variable zorgt er voor dat de app weet of de checkbox is aangevinkt.
        self.trueorfalse = tk.IntVar()
        tk.ttk.Label(self, text="DES Encryption", font=parent.titlefont).grid(column=1, row=1, columnspan=3)
#Hieronder wordt een textbox beschreven. De tekstbox moet self.___ = ervoor hebben
#want met self kan de text terug gehaald worden en het moet self.___ = zijn
#omdat anders grid en configure niet gebruikt kunnen worden.
#De hoogte en breedte van de textbox worden ook aan gegeven en bd is hoe dik de rand is.
        self.cel = tk.Text(self, width=40, height=5, bd=1)
        self.cel.grid(column=1, row=2, sticky=("W, E"))
        tk.ttk.Label(self, text="Message").grid(column=2, row=2, sticky=("W"))
        tk.ttk.Button(self, text="Go back to DES menu", command=lambda: parent.show_frame(Desp), width=30).grid(column=3, row=2, sticky=("W, E"))
#Bij deze textbox wordt ook achtergrond (bg) gegeven. #F0F0F0 is de achtergrond van de app zelf.
#Ook wordt hiet configure gebruikt met state="disabled".
#Dit zorgt ervoor dat er niet in geschreven kan worden, ook niet door code.
        self.txd = tk.Text(self, width=40, height=5, bg="#F0F0F0", bd=0)
        self.txd.configure(state="disabled")
        self.txd.grid(column=1, row=3, sticky=("W, E"))
        tk.ttk.Label(self, text="Encrypted message").grid(column=2, row=3, sticky=("W"))
        tk.ttk.Button(self, text="Encrypt", command=self.encryptbutt, width=30).grid(column=3, row=3, sticky=("W"))
#Hieronder is de checkbox beschreven. Het is grotendeels het zelfde als een knop
#alleen is hier geen command maar een variable. Deze is 1 of 0.
        tk.ttk.Checkbutton(self, text="Use ECB instead of CBC", variable=self.trueorfalse).grid(column=1, row=4, sticky=("W"))
#Dit is de command voor het encrypten.
    def encryptbutt(self, *args):
#Eerst wordt de textbox geleegd waar de encrypted data in komt.
        self.txd.configure(state="normal")
        self.txd.delete("1.0", "end")
        self.txd.configure(state="disabled")
        self.trueorfalse.get()
#Hier wordt gekeken of er CBC of ECB gebruikt wordt
        if self.trueorfalse.get() == 0:            
            try:
#Eerst wordt de data uit de textbox gehaald. Deze data wordt geëncode.
#Bij het eruit halen van de text moet er 1 character af want de textbox maakt automatisch een niewe regel aan.
#Daarna wordt de key beschreven. Waarmee daarna de encryptie plaatsvind.
#Bij deze key is het echte key "standard", mode CBC, IV "\0\0\0\0\0\0\0\0"
#pad none en padmode PAD_PKCS5.
                data = self.cel.get("1.0", "end-1c")
                data = str(data).encode("utf-8")
                key = des(b"standard", CBC, b"\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
                d = key.encrypt(data)
#Hier wordt de encrypted string in de textbox gezet.
                self.txd.configure(state="normal")
                self.txd.insert("1.0", d)
                self.txd.configure(state="disabled")
#Als er iets fout gaat in dit process wordt deze ValueError gegeven.
#In Desalg staan er nog veel meer dus het maakt niet uit dat deze niet specefiek is.
            except ValueError:
                raise ValueError("Data cannot be used")
#Als de mode ECB is gebeurd er hetzelfde als met CBC maar dan met een andere mode.
        else:
            try:
                data = self.cel.get("1.0", "end-1c")
                data = str(data).encode("utf-8")
                key = des(b"standard", ECB, b"\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
                d = key.encrypt(data)
                self.txd.configure(state="normal")
                self.txd.insert("1.0", d)
                self.txd.configure(state="disabled")
            except ValueError:
                raise ValueError("Data cannot be used")
#Dit is frame voor het decrypten van DES.
#Deze lijkt heel erg op het encryptie frame.
#Alleen is de command (en de text op knoppen/labels)iets anders.
class Despde(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.trueorfalse = tk.IntVar()
        tk.ttk.Label(self, text="DES Decryption", font=parent.titlefont).grid(column=1, row=1, columnspan=3)
        self.celde = tk.Text(self, height=5, width=40, bd=1)
        self.celde.grid(column=1, row=2, sticky=("W, E"))
        tk.ttk.Label(self, text="Encrypted message").grid(column=2, row=2, sticky=("W"))
        tk.ttk.Button(self, text="Go back to DES menu", command=lambda: parent.show_frame(Desp), width=30).grid(column=3, row=2, sticky=("W, E"))
        self.txe = tk.Text(self, width=40, height=5, bg="#F0F0F0", bd=0)
        self.txe.configure(state="disabled")
        self.txe.grid(column=1, row=3, sticky=("W, E"))
        tk.ttk.Label(self, text="Decrypted message").grid(column=2, row=3, sticky=("W"))
        tk.ttk.Button(self, text="Decrypt", command=self.decryptbutt, width=30).grid(column=3, row=3, sticky=("W, E"))
        tk.ttk.Checkbutton(self, text="Use ECB instead of CBC", variable=self.trueorfalse).grid(column=1, row=4, sticky=("W"))

    def decryptbutt(self, *args):
        self.txe.configure(state="normal")
        self.txe.delete("1.0", "end")
        self.txe.configure(state="disabled")
        self.trueorfalse.get()
        if self.trueorfalse.get() == 0:
            try:
#Het enige echte verschil met encryptie is dat de data niet meer wordt geëncode.
#raw_unicode_escape geeft het zelfde effect als een b voor de sting te zetten.
#En inplaats van key.encrypt is het key.decrypt.
                data = self.celde.get("1.0", "end-1c")
                data = bytes(data, "raw_unicode_escape")
                key = des(b"standard", CBC, b"\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
                d = key.decrypt(data)
                self.txe.configure(state="normal")
                self.txe.insert("1.0", d)
                self.txe.configure(state="disabled")
            except ValueError:
                raise ValueError("Data cannot be used")
        else:
            try:
                data = self.celde.get("1.0", "end-1c")
                data = bytes(data, "raw_unicode_escape")
                key = des(b"standard", ECB, b"\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
                d = key.decrypt(data)
                self.txe.configure(state="normal")
                self.txe.insert("1.0", d)
                self.txe.configure(state="disabled")
            except ValueError:
                raise ValueError("Data cannot be used")
#Dit is weer een menu.
class Desfile(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        tk.ttk.Label(self, text="DES file menu", font=parent.titlefont).grid(column=1, row=1, columnspan=3)
        tk.ttk.Button(self, text="Go to DES encryption", command=lambda: parent.show_frame(dfen), width=30).grid(column=1, row=2, sticky=("W, E"))
        tk.ttk.Button(self, text="Go to DES decryption", command=lambda: parent.show_frame(dfde), width=30).grid(column=2, row=2, sticky=("W, E"))
        tk.ttk.Button(self, text="Go back to menu", command=lambda: parent.show_frame(Menu), width=30).grid(column=3, row=2, sticky=("W, E"))
#Dit is de frame waar bestanden encrypted worden.
class dfen(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        tk.ttk.Label(self, text="DES file encryption", font=parent.titlefont).grid(column=1, row=1, columnspan=2)
        tk.ttk.Button(self, text="Encrypt file", command=self.enfiled, width=30).grid(column=1, row=2, sticky=("W, E"))
        tk.ttk.Button(self, text="Go back to DES file menu", command=lambda: parent.show_frame(Desfile), width=30).grid(column=2, row=2, sticky=("W, E"))
#Dit is de functie die bestanden encrypt    
    def enfiled(self):
#Eerst wordt er gevraagd welk bestand er encrypt moet worden.
#Daarna wordt het bestand gelezen in bit vorm(rb+) en wordt het bestand gesloten
#Daarna wordt het bestand encrypted.
#Als laast wordt een nieuw bestand aangemaakt dat het encrypted bestand is wat gekozen is.
        filename = askopenfilename()
        f = open(filename, "rb+")
        data = f.read()
        f.close()
        key = des("standard")
        data = key.encrypt(data, " ")
        f = open("Encyptedfile.enc", "wb+")
        f.write(data)
        f.close()
#Dit is de frame waar bestanden decrypted worden.
class dfde(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        tk.ttk.Label(self, text="DES file decryption", font=parent.titlefont).grid(column=1, row=1, columnspan=2)
        tk.ttk.Button(self, text="Decrypt file", command=self.defiled, width=30).grid(column=1, row=2, sticky=("W, E"))
        tk.ttk.Button(self, text="Go back to DES file menu", command=lambda: parent.show_frame(Desfile), width=30).grid(column=2, row=2, sticky=("W, E"))
#Dit is de functie die bestanden decrypt      
    def defiled(self):
#De functie is bijna hetzelfde als het encrypted.
#Alleen nu wordt er key.decrypt gebruikt.
        filename = askopenfilename()
        f = open(filename, "rb+")
        data = f.read()
        f.close()
        key = des("standard")
        data = key.decrypt(data, " ")
        f = open("Decryptedfile.dec", "wb+")
        f.write(data)
        f.close()
#Dit is weer een menu.
class tr(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        tk.ttk.Label(self, text="Triple DES", font=parent.titlefont).grid(column=1, row=1, columnspan=3)
        tk.ttk.Button(self, text="Go to triple DES encryption", command=lambda: parent.show_frame(tren), width=30).grid(column=1, row=2, sticky=("W, E"))
        tk.ttk.Button(self, text="Go to triple DES encryption", command=lambda: parent.show_frame(trde), width=30).grid(column=2, row=2, sticky=("W, E"))
        tk.ttk.Button(self, text="Go back to menu", command=lambda: parent.show_frame(Menu), width=30).grid(column=3, row=2, sticky=("W, E"))
#Dit is het frame met encryptie voor triple DES.
#Dit frame lijkt heel erg op het frame van DES encryptie.
class tren(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.trueorfalse = tk.IntVar()
        tk.ttk.Label(self, text="Triple DES encryption", font=parent.titlefont).grid(column=1, row=1, columnspan=3)
        self.txt1 = tk.Text(self, width=40, height=5, bd=1)
        self.txt1.grid(column=1, row=2, sticky=("W, E"))
        tk.ttk.Label(self, text="Message").grid(column=2, row=2, sticky=("W"))
        tk.ttk.Button(self, text="Go back to DES menu", command=lambda: parent.show_frame(tr), width=30).grid(column=3, row=2, sticky=("W, E"))
        self.txt12 = tk.Text(self, width=40, height=5, bd=0, bg="#F0F0F0")
        self.txt12.configure(state="disabled")
        self.txt12.grid(column=1, row=3, sticky=("W, E"))
        tk.ttk.Label(self, text="Encrypted message").grid(column=2, row=3, sticky=("W"))
        tk.ttk.Button(self, text="Encrypt", command=self.enbutttr, width=30).grid(column=3, row=3, sticky=("W, E"))
        checkbox = tk.ttk.Checkbutton(self, text="Use ECB instead of CBC", variable=self.trueorfalse)
        checkbox.grid(column=1, row=4, sticky=("W"))
    
    def enbutttr(self):
        self.txt12.configure(state="normal")
        self.txt12.delete("1.0", "end")
        self.txt12.configure(state="disabled")
        self.trueorfalse.get()
        data = self.txt1.get("1.0", "end-1c")
#Triple DES werkt alleen als de data een lengte heeft van 8 of een meerdere daarvan characters.
#Dus als er de data dat niet heeft worden er puntkomma's achter geplakt.
        print(len(data))
        if len(data) % 8 != 0:
            n = 8 - (len(data) % 8)
            s = ";"
            i = 0
            while i < n:
                data += s
                i += 1
        else:
            pass
        if self.trueorfalse.get() == 0:
            try:
#Bijna alles is het zelfde als bij normale DES alleen moet de key nu geschreven worden in hexadecimals.
#Voor de hexadecimals moet wel unhex zodat de sleutel niet meer in hexadecimals staat.
#Met hexadecimals zijn er veel meer mogelijkheden voor de sleutel. 
#Ook kan er dan voor worden gekozen om 3 keer DES te gebruiken.
                key = tripledes(unhex("1231231231234567FACEAABBCCDDFACE5E1001005E890098"), CBC)
                ed = key.encrypt(data)
                print(ed)
                self.txt12.configure(state="normal")
                self.txt12.insert("1.0", ed)
                self.txt12.configure(state="disabled")
            except ValueError:
                raise ValueError("Data cannot be used")
        else:
            try:
                key = tripledes(unhex("1231231231234567FACEAABBCCDDFACE5E1001005E890098"), ECB)
                ed = key.encrypt(data)
                self.txt12.configure(state="normal")
                self.txt12.insert("1.0", ed)
                self.txt12.configure(state="disabled")
            except ValueError:
                raise ValueError("Data cannot be used")
#Dit is het frame met decryptie voor triple DES.
#Dit frame lijkt heel erg op het frame van DES decryptie.
#Er is dan ook niks nieuws vergeleken met de andere frames
class trde(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.trueorfalse = tk.IntVar()
        tk.ttk.Label(self, text="Triple DES decryption", font=parent.titlefont).grid(column=1, row=1, columnspan=3)
        self.txt2 = tk.Text(self, width=40, height=5, bd=1)
        self.txt2.grid(column=1, row=2, sticky=("W, E"))
        tk.ttk.Label(self, text="Encrypted message").grid(column=2, row=2, sticky=("W"))
        tk.ttk.Button(self, text="Go back to DES menu", command=lambda: parent.show_frame(tr), width=30).grid(column=3, row=2, sticky=("W, E"))
        self.txt22 = tk.Text(self, width=40, height=5, bd=0, bg="#F0F0F0")
        self.txt22.configure(state="disabled")
        self.txt22.grid(column=1, row=3, sticky=("W, E"))
        tk.ttk.Label(self, text="Decrypted message").grid(column=2, row=3, sticky=("W"))
        tk.ttk.Button(self, text="Decrypt", command=self.debutttr, width=30).grid(column=3, row=3, sticky=("W, E"))
        checkbox = tk.ttk.Checkbutton(self, text="Use ECB instead of CBC", variable=self.trueorfalse)
        checkbox.grid(column=1, row=4, sticky=("W"))
        txt23 = tk.Text(self, width=60, height=5, bd=0, bg="#F0F0F0")
        txt23.grid(column=2, row=4, columnspan=2, sticky=("W"))
        txt23.insert("1.0", "Triple DES can only work with data that has of a multiple of 8 characters. So to\nensure that you can encrypt everything the app added semicolons to the end of\nyour message. To read the message correctly imagine the semicolons aren't\nthere.")
        txt23.configure(state="disabled", font=fo.Font(family="Arial"))

    def debutttr(self):
        self.txt22.configure(state="normal")
        self.txt22.delete("1.0", "end")
        self.txt22.configure(state="disabled")
        self.trueorfalse.get()
        if self.trueorfalse.get() == 0:
            try:
                data = self.txt2.get("1.0", "end-1c")
                data = bytes(data, "raw_unicode_escape")
                key = tripledes(unhex("1231231231234567FACEAABBCCDDFACE5E1001005E890098"), CBC)
                dd = key.decrypt(data)
                self.txt22.configure(state="normal")
                self.txt22.insert("1.0", dd)
                self.txt22.configure(state="disabled")
            except ValueError:
                raise ValueError("Data cannot be used")
        else:
            try:
                data = self.txt2.get("1.0", "end-1c")
                data = bytes(data, "raw_unicode_escape")
                key = tripledes(unhex("1231231231234567FACEAABBCCDDFACE5E1001005E890098"), ECB)
                dd = key.decrypt(data)
                self.txt22.configure(state="normal")
                self.txt22.insert("1.0", dd)
                self.txt22.configure(state="disabled")
            except ValueError:
                raise ValueError("Data cannot be used")
#Dit is weer een menu.
class trfile(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        tk.ttk.Label(self, text="Triple DES file menu", font=parent.titlefont).grid(column=1, row=1, columnspan=3)
        tk.ttk.Button(self, text="Go to triple DES encryption", command=lambda: parent.show_frame(tfen), width=30).grid(column=1, row=2, sticky=("W, E"))
        tk.ttk.Button(self, text="Go to triple DES decryption", command=lambda: parent.show_frame(tfde), width=30).grid(column=2, row=2, sticky=("W, E"))
        tk.ttk.Button(self, text="Go back to menu", command=lambda: parent.show_frame(Menu), width=30).grid(column=3, row=2, sticky=("W, E"))
#Dit frame is voor triple DES file encryptie.
#Het lijkt net zoals de andere triple DES veel op normale DES.
#Net zoals de triple DES decryptie komt hier ook niks nieuws naarvoren.
class tfen(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        tk.ttk.Label(self, text="Triple DES file encryption", font=parent.titlefont).grid(column=1, row=1, columnspan=2)
        tk.ttk.Button(self, text="Encrypt file", command=self.entrfile, width=30).grid(column=1, row=2, sticky=("W, E"))
        tk.ttk.Button(self, text="Go back to triple DES file menu", command=lambda: parent.show_frame(trfile), width=30).grid(column=2, row=2, sticky=("W, E"))
    
    def entrfile(self):
        filename = askopenfilename()
        f = open(filename, "rb+")
        data = f.read()
        f.close()
        key = tripledes(unhex("1231231231234567FACEAABBCCDDFACE5E1001005E890098"))
        data = key.encrypt(data, " ")
        f = open("TripleDESencryptedfile.enc", "wb+")
        f.write(data)
        f.close()
#Dit frame is voor triple DES file decryptie.
#Het lijkt net zoals de andere triple DES veel op normale DES.
#En net zoals de rest komt hier ook niets nieuws naar voren.
class tfde(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        tk.ttk.Label(self, text="Triple DES file decryption", font=parent.titlefont).grid(column=1, row=1, columnspan=2)
        tk.ttk.Button(self, text="Decrypt file", command=self.detrfile, width=30).grid(column=1, row=2, sticky=("W, E"))
        tk.ttk.Button(self, text="Go back to triple DES file menu", command=lambda: parent.show_frame(trfile), width=30).grid(column=2, row=2, sticky=("W, E"))

    def detrfile(self):
        filename = askopenfilename()
        f = open(filename, "rb+")
        data = f.read()
        f.close()
        key = tripledes(unhex("1231231231234567FACEAABBCCDDFACE5E1001005E890098"))
        data = key.decrypt(data, " ")
        f = open("TripleDESdecryptedfile.dec", "wb+")
        f.write(data)
        f.close()
#Dit is weer een menu.
class menig(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        tk.ttk.Label(self, text="Instruction manual menu", font=parent.titlefont).grid(column=1, row=1, columnspan=2)
        tk.ttk.Button(self, text="Keys and file directory", command=lambda: parent.show_frame(install)).grid(column=1, row=2, sticky=("W, E"))
        tk.ttk.Button(self, text="Instruction manual", command=lambda: parent.show_frame(useman)).grid(column=2, row=2, sticky=("W, E"))
#De twee classes hieronder staat alleen maar tekst in.
#Deze hebt ik eigenlijk een beetje voor de lol gemaakt.
#In deze twee classes staat meer over het product zelf en hoe het te gebruiken is.
#Hier worden ook de andere twee lettertypes gebruikt die waren beschreven in mainframes.
class install(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        tk.ttk.Label(self, text="Keys and file directory", font=parent.titlefont).grid(column=1, row=1)
        tk.ttk.Button(self, text="Go back to main menu", command=lambda: parent.show_frame(Menu), width=30).grid(column=2, row=1, sticky=("W, E"))
        tk.ttk.Label(self, text="Keys", font=parent.smalltitlefont).grid(column=1, row=2, sticky=("W"))
        tk.ttk.Label(self, text="File directory", font=parent.smalltitlefont).grid(column=2, row=2, sticky=("W"))
        itx1 = tk.Text(self, width=75, height=8, bd=0, bg="#F0F0F0", font=parent.normalfont)
        itx1.insert("1.0", "To change the keys of the applications you need to change the source code. You will firstly need to find the file named, Enapp.py. You can open this"
        " file with any text editor (like notepad or visual studio code). Then search for 'standard' (DES) and '1231231231234567FACEAABBCCDDFACE5E1001005E890098' (triple DES)," 
        " this are the keys for DES and triple DES. If you change the key for DES make sure it is 8 characters long and in unicode. If you change the key for triple DES, you will"
        " need to write 48 hexadecimal digits in unhex(""). These digits are 0 through 9 and A through F.")
        itx1.configure(state="disabled")
        itx1.grid(column=1, row=3, sticky=("W, E"))
        itx2 = tk.Text(self, width=75, height=8, bd=0, bg="#F0F0F0", font=parent.normalfont)
        itx2.insert("1.0", "To change the file directory of the encrypted and decrypted files. You will firstly need to make the folder you want the files to go to. Then copy the"
        " place of the map. You can do this by clicking on the name and then pressing Ctrl+c. Paste this before the file names (TripleDESencryptedfile.enc, Decyptedfile.dec, ect.)"
        "between the "". Make sure all the slashes are front slashes. You are also free to change the names of the file, just keep .enc and .dec.")
        itx2.configure(state="disabled")
        itx2.grid(column=2, row=3, sticky=("W, E"))

class useman(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        tk.ttk.Label(self, text="Instruction manual", font=parent.titlefont).grid(column=1, row=1)
        tk.ttk.Button(self, text="Go back to main menu", command=lambda: parent.show_frame(Menu), width=30).grid(column=2, row=1, sticky=("W, E"))
        tk.ttk.Label(self, text="DES manual", font=parent.smalltitlefont).grid(column=1, row=2)
        tk.ttk.Label(self, text="DES file manual", font=parent.smalltitlefont).grid(column=2, row=2)
        mtx1 = tk.Text(self, width=75, height=8, bd=0, bg="#F0F0F0", font=parent.normalfont)
        mtx1.insert("1.0", "DES is fairly simple, you type your message in the textbox on the DES encryption page and \nthen push the encrypt button." 
        " You can now copy this message and send it to anyone you \nwant. Every other person with this app and with the same keys as you can decrypt the" 
        " \nmessage. To decrypt a message you need to paste the encrypted message in the textbox on \nthe DES decryption page, and press the decrypt button."
        " Now you have the decrypted \nmessage. You can change the keys of DES (and all other applications in this app) in the \nsource code. For DES make"
        " sure your keys are 8 characters long, and don't mess with the \nother code.")
        mtx1.configure(state="disabled")
        mtx1.grid(column=1, row=3, sticky=("W, E"))
        mtx2 = tk.Text(self, width=75, height=8, bd=0, bg="#F0F0F0", font=parent.normalfont)
        mtx2.insert("1.0", "DES file can encrypt all files. You simply have to push the encrypt button and choose a file of  your liking. The encrypted file"
        " is always called Encyptedfile.enc. You are free to change its \nname but keep the .enc. If you want to decrypt a file you simply push the decrypt"
        " button and \nchoose the encrypted file. The decrypted file is always called Decryptedfile.dec. You are free \nto change its name and save it as the"
        " correct file type. Just change .dec to the right file type \nlike .docx. The keys work the same as with DES")
        mtx2.configure(state="disabled")
        mtx2.grid(column=2, row=3, sticky=("W, E"))
        tk.ttk.Label(self, text="Triple DES manual", font=parent.smalltitlefont).grid(column=1, row=4)
        tk.ttk.Label(self, text="Triple DES file manual", font=parent.smalltitlefont).grid(column=2, row=4)
        mtx3 = tk.Text(self, width=75, height=8, bd=0, bg="#F0F0F0", font=parent.normalfont)
        mtx3.insert("1.0", "Triple DES works the same as normal DES. There are only two differences. The first one is \nobviously the type of encryption. The"
        " second one is that, if your message is not a multiple of 8 characters long the app puts semicolons behind it. So if you are reading the message, make"
        " \nsure you think those away. There is also a waring on the page itself, so you don't have to \nworry that you will forget it. The keys from triple DES"
        " work a bit different from DES keys. Triple DES keys have to be 48 characters long and need to be written in hexadecimal digits. Those  digits are"
        " 0 through 9 and A through F")
        mtx3.configure(state="disabled")
        mtx3.grid(column=1, row=5, sticky=("W, E"))
        mtx4 = tk.Text(self, width=75, height=8, bd=0, bg="#F0F0F0", font=parent.normalfont)
        mtx4.insert("1.0", "Triple DES file works the same as DES file. Only the files aren't called Encyptedfile.enc and \nDecryptedfile.dec. They instead are"
        " called TripleDESencryptedfile.enc and \nTripleDESdecryptedfile.dec. As with DES file you can name these files whatever you want, \njust don't change"
        " the .enc. The keys for triple DES file work the exact same as the keys for \ntriple DES.")
        mtx4.configure(state="disabled")
        mtx4.grid(column=2, row=5, sticky=("W, E"))
#Dit is nodig om de app te laten runnen.        
if __name__ == "__main__":
    app = mainframes()
    app.mainloop()
