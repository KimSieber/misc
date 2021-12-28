######################################################################################################
### Projekt: Enigma
### 
### Ziel     : Nachbildung der Ver-/Entschlüsselungslogik
###            der Enigma-Maschine (Version I)
### Datum    : 23.12.2021 - 28.12.2021
### Autor    : Kim Sieber
###
### Quellen  : https://de.wikipedia.org/wiki/Enigma_(Maschine)
###            http://www.softdoc.de/mr/de/downloads/files/EnigmaTechnischeDetails.pdf
###            https://de.wikipedia.org/wiki/Enigma-Walzen
###            https://www.swisseduc.ch/informatik/daten/kryptologie_geschichte/docs/enigma_dokumentation.pdf
### Simulator: https://people.physik.hu-berlin.de/~palloks/js/enigma/enigma-u_v20.html
###            https://kryptografie.de/kryptografie/chiffre/enigma.htm
######################################################################################################

class enigma:
    ######################################################################################################
    ### Konstanten für die Abbildung der Umwandlungen
    ###
    ### ->ALPHA    : Bildet Alphabet ab, wandelt von Ziffer in Buchstabe und Buchstabe in Ziffer um
    ###                                => ALPHA[0..25]          = 'A'..'Z'
    ###                                => ALPHA.index['A'..'Z'] =  0...25
    ### ->WALZEN   : Stellt die verfügbaren Walzen mit Ihrer Umwandlung von A..Z dar sowie der Kerbe je Walze
    ###                                => WALZEN['I'..'VIII']   = ['EKMFLGDQVZNT...', ['N', ...]]
    ### ->UKWALZEN : Stellt die verfügbaren Umkehr-Walzen mit Ihrer Umwandlung von A..Z dar
    ###                                => UKWALZEN['A'..'C']    = ['YRUHQSLDPXNG...']
    ######################################################################################################
    '''                   0123456789+123456789+12345                '''
    ALPHA    =           'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    WALZEN   = {'I'   : ['EKMFLGDQVZNTOWYHXUSPAIBRCJ', ['Q']],
                'II'  : ['AJDKSIRUXBLHWTMCQGZNPYFVOE', ['E']],
                'III' : ['BDFHJLCPRTXVZNYEIWGAKMUSQO', ['V']],
                'IV'  : ['ESOVPZJAYQUIRHXLNFTGKDCMWB', ['J']],
                'V'   : ['VZBRGITYUPSDNHLXAWMJQOFECK', ['Z']],
                'VI'  : ['JPGVOUMFYQBENHZRDKASXLICTW', ['Z', 'M']],
                'VII' : ['NZJHGRCXMYSWBOUFAIVLPEKQDT', ['Z', 'M']],
                'VIII': ['FKQHTLXOCBJSPDZRAMEWNIUYGV', ['Z', 'M']] }
    UKWALZEN = {'A'   :  'EJMZALYXVBWFCRQUONTSPIKHGD',
                'B'   :  'YRUHQSLDPXNGOKMIEBFZCWVJAT',
                'C'   :  'FVPJIAOYEDRZXWGCTKUQSBNMHL' }
    WALZENNAMEN = [' ', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII']
    
    ######################################################################################################
    ### Konstruktor: Keine Funktion
    ###
    ### Erste aufzurufende Methode ist einstellen(), damit Einstellung der Enigma erfolgt
    ######################################################################################################
    def __init__ (self):
        pass

    ######################################################################################################
    ### Einstellen der Enigma mit folgenden Daten
    ###
    ### @Walzenlage_in   :  Walzen-Nr. an Positionen von links nach rechts  => Format: ['I','IV','III']
    ### @Ringstellung_in :  Ringstellungen der Walzen von links nach rechts => Format: [1, 17, 22]
    ### @Stecker_in      :  Steckerverbindungen                             => Format: [['AB'],['DZ'], ...]   
    ### @UKWalze_in      :  Buchstabe/Name der Umkehrwalze                  => Format: 'A'
    ### @Grundstellung_in:  Grundstellung / Start-Stellung der Walzen       => Format: ['E', 'W', 'G']
    ###
    ### Erzeugt folgende Klassenvariable:
    ### ->Walzenlage     :  Walzen-Nr. an der Position von links            => Format: ['I','IV','III']
    ### ->Ringstellung   :  Ringstellung wie oben, aber um -1 reduziert     => Format: [0, 16, 21]
    ### ->UKWalze_in     :  Buchstabe/Name der Umkehrwalze                  => Format: 'A'
    ### ->Stecker        :  Umwandlungs-Dictionary für Stecker, ganzes Alphabet abgebildet
    ###                         => Format: {'A':'D', 'C':'N', ..., 'B':'B', 'D':'D', ...}
    ######################################################################################################
    def einstellen (self, Walzenlage_in, Ringstellung_in , Stecker_in, UKWalze_in, Grundstellung_in = ''):
        self.Walzenlage   = Walzenlage_in
        self.Ringstellung = [(r-1) for r in Ringstellung_in]    # Reduktion um 1, da A=0 (kein Versatz)
        self.UKWalze      = UKWalze_in
        self.setze_Grundstellung(Grundstellung_in)              # Bleibt Funktion, da 
        ### Stecker in beide Richtungen darstellen sowie restlichen unumgestelltes Alphabet auffüllen
        self.Stecker = {}
        for steck in Stecker_in:
            self.Stecker[steck[0]] = steck[1]
            self.Stecker[steck[1]] = steck[0]
        for a in self.ALPHA:             # Auffüllen mit allen nicht umgestecketen Buchstaben
            if a not in self.Stecker:
                self.Stecker[a] = a
                
    ######################################################################################################
    ### Setzt die Grundstellung der Ringe von Buchstaben in Ziffern um
    ###
    ### @Grundstellung_in:  Grundstellung / Start-Stellung der Walzen       => Format: ['E', 'W', 'G']
    ### 
    ### Erzeugt folgende Klassenvariable:
    ### ->Grundstellung    :  Grundstellung in Ziffern                      => Format: [4, 22, 6]
    ######################################################################################################
    def setze_Grundstellung(self, Grundstellung_in):
        self.Grundstellung = [self.ALPHA.index(g) for g in Grundstellung_in]
        
    ######################################################################################################
    ### Druckt fürs debugging die Daten der Klassenvariablen, teils formatiert, an
    ######################################################################################################
    def drucke_Einstellungen(self):
        print ('UKWalze       = ', self.UKWalze)
        print ('Walzenlage    = ', ' '.join(self.Walzenlage), \
               ' => ', ''.join([str(self.WALZENNAMEN.index(w)) for w in self.Walzenlage]))
        print ('Ringstellung  = ', ' '.join([str(x+1) for x in self.Ringstellung]), \
               ' => ', ' '.join([self.ALPHA[r] for r in self.Ringstellung]))
#        print ('Stecker       = ',''.join(self.Stecker.keys()))
#        print ('                ',''.join(self.Stecker.values()))
        Stecker = [key+self.Stecker[key] for key in self.Stecker if key != self.Stecker[key]]
        print ('Stecker       = ',' '.join([Stecker[s] for s in range(0,len(Stecker),2)]))
        self.drucke_Grundstellung()
        print ()
        print ('Schlüssel     : ', self.UKWalze + \
                                   ''.join([str(self.WALZENNAMEN.index(w)) for w in self.Walzenlage]) + ',', \
                                   ''.join([self.ALPHA[r] for r in self.Ringstellung]) + ',', \
                                   ''.join([self.ALPHA[g] for g in self.Grundstellung]) + ',', \
                                   ' '.join([Stecker[s] for s in range(0,len(Stecker),2)]))
    def drucke_Grundstellung(self):
        print ('Grundstellung = ', ''.join([self.ALPHA[g] for g in self.Grundstellung]), \
               ' => ', ' '.join([str(x+1) for x in self.Grundstellung]), \
               '  (## AKTUELL ##)')

    ######################################################################################################
    ### Beschränkung einer Zahl auf einen definierten Wertebereich von 25 (A..Z => 0..25)
    ### genutzt, um rollierende Zahlen im Bereich 0..Skala zu halten
    ### Ist Ziffer < 0, wird von Skala heruntergezählt, ist Ziffer > Skala, von 0 hochgezählt
    ######################################################################################################
    def map(self, Ziffer):
        if Ziffer > 25:
            return (Ziffer - 26)
        if Ziffer < 0:
            return (26 + Ziffer)
        return Ziffer

    ######################################################################################################
    ### Setzt die Walze ganz rechts (Walzen[2]) um eins hoch
    ### Wenn Ringstellung einer Walze erreicht, nächste Walze weiterdrehen
    ###
    ### Veränderung der Klassenvariablen:
    ### +> Grundstellung[2..0] += 1 
    ######################################################################################################
    def weiterdrehen_Walze(self):
        if self.ALPHA[self.Grundstellung[2]] in self.WALZEN[self.Walzenlage[2]][1]:
            if self.ALPHA[self.Grundstellung[1]] in self.WALZEN[self.Walzenlage[1]][1]:
                self.Grundstellung[0] = self.map(self.Grundstellung[0] + 1)
            self.Grundstellung[1] = self.map(self.Grundstellung[1] + 1)
        self.Grundstellung[2] = self.map(self.Grundstellung[2] + 1)

    ######################################################################################################
    ### Text aufbereiten für Chifrierung
    ###
    ### Leerzeichen und Umbrüche entfernen, Großbuchstaben, Ziffern- und Sonderzeichen-Umwandlung
    ### CH/CK ändern, Eigennamen unverändert und doppelt darstellen
    ######################################################################################################
    def aufbereiten_Text(self, Text_in):
        ######################################
        ### Hilfsfunktion für nächsten Stelle
        ######################################
        def naechste_Stelle(Text, Stelle):
            if Stelle >= len(Text):     return ''
            else:                       return Text[Stelle+1]
            
        Text_in = Text_in.replace(' ', '')          # Leerzeichen entfernen
        Text_in = Text_in.replace('\n', '')         # Zeilenumbrüche entfernen
        Text_in = Text_in.upper()                   # Umwandlung in Großbuchstaben
        
        Eigennamen_start = None
        Text_aus         = ''
        i = 0
        while i < len(Text_in):
            if Text_in[i] in ['\'', '"']:
                if Eigennamen_start == None:        # None => Anfang des Eigennamens
                    if Text_aus[-1] != 'X':             Text_aus += 'X'
                    Eigennamen_start = len(Text_aus)
                else:
                    Text_aus        += 'X' + Text_aus[Eigennamen_start:] + 'X'
                    Eigennamen_start = None
            else:
                ### Zahlen in Text und X-voranstellen, abschließen mit X, wenn keine Ziffer folgt
                if Text_in[i].isdigit():
                    if Text_aus[-1] != 'X':             Text_aus += 'X'
                    Text_aus += ['NULL','EINS','ZWEI','DREI','VIER','FUENF','SEQS','SIEBEN','AQT','NEUN'][int(Text_in[i])]
                    if not naechste_Stelle(Text_in, i).isdigit():
                        Text_aus += 'X'
                ### CH und CK in Q umwandeln
                elif Text_in[i] == 'C':
                    if Eigennamen_start == None and naechste_Stelle(Text_in, i) in ['H', 'K']:
                        Text_aus += 'Q'
                        i += 1
                    else:
                        Text_aus += 'C'
                ### Umlaute umwanzeln
                elif Text_in[i] == 'Ä':
                    Text_aus += 'AE'
                elif Text_in[i] == 'Ö':
                    Text_aus += 'OE'
                elif Text_in[i] == 'Ü':
                    Text_aus += 'UE'
                elif Text_in[i] == 'ß':
                    Text_aus += 'SZ'
                ### Umwandlung alle unbekannten Zeichen
                elif Text_in[i] in self.ALPHA:
                    Text_aus += Text_in[i]
                else:
                    if Text_aus[-1] != 'X':
                        Text_aus += 'X'
            i += 1
        return Text_aus
    
    ######################################################################################################
    ### Chifriert / Dechifriert einen String
    ###
    ### Text muss vor Aufruf aufbereitet sein. ->Funktion aufbereiten_Text()
    ### @Text_in     :    String, aufbereitet
    ### @return      :    String, (de-)chifriert 
    ######################################################################################################
    def chifrieren_Text(self, Text_in):
        Text_in = Text_in.replace(' ', '')          # Leerzeichen entfernen
        Text_in = Text_in.replace('\n', '')         # Zeilenumbrüche entfernen
        Text_in = Text_in.upper()                   # Umwandlung in Großbuchstaben
        Text_aus = ''
        for a in Text_in:
            Text_aus += self.umwandeln_Buchstabe(a)
        return Text_aus

    ######################################################################################################
    ### Wandelt einen einzelnen Groß-Buchstaben um
    ###
    ### @Buchstabe:  Einzelner Groß-Buchstabe   => Format: 'A'..'Z'
    ###
    ### Reihenfolge der Bearbeitung:
    ### 1. Schaltet Walzendrehung um einen Schritt weiter
    ### 2. Wendet Stecker-Umsetzung an
    ### 3. Wendet die 3 Walzen von Rechts nach Links an -> 2, 1, 0
    ### 4. Wendet Umkehrwalze an
    ### 3. Wendet die 3 Walzen von Links nach Rechts an -> 0, 1, 2
    ### 4. Wendet Stecker-Umsetzung an
    ###
    ### @return   :  Umgesetzter Buchstabe     => Format: 'A'..'Z'
    ######################################################################################################
    def umwandeln_Buchstabe(self, Buchstabe):
        #####################################################
        ### Hilfsfunktionen,  Index <==> Buchstabe
        #####################################################    
        def idx(Buchstabe):
            return self.ALPHA.index(Buchstabe)
        def chr(Index):
            return self.ALPHA[Index]
        
        ### Walze um eins weiterdrehen
        self.weiterdrehen_Walze()
        ### Stecker
        Buchstabe = self.Stecker[Buchstabe]
        ### Walzen 2..0        => Vesatz ermitteln, Versatz anwenden, Walze anwenden, Versatz zurückrechnen, in Buchstabe
        for i in [2,1,0]:
            Versatz   = self.Grundstellung[i] - self.Ringstellung[i]
            Index     = self.map(idx(Buchstabe) + Versatz)
            Buchstabe = self.WALZEN[self.Walzenlage[i]][0][Index]
            Index     = self.map(idx(Buchstabe) - Versatz)
            Buchstabe = chr(Index)
        ### Umkehrwalze
        Buchstabe = self.UKWALZEN[self.UKWalze][ idx(Buchstabe) ]
        ### Walzen 0..2        => Versatz ermitteln, Versatz anwenden, Walze anwenden, Versatz zurückrechnen, in Buchstabe
        for i in [0,1,2]:
            Versatz   = self.Grundstellung[i] - self.Ringstellung[i]
            Index     = self.map(idx(Buchstabe) + Versatz)
            Buchstabe = chr(Index)
            Index     = self.WALZEN[self.Walzenlage[i]][0].index(Buchstabe)
            Index     = self.map(Index - Versatz)
            Buchstabe = chr(Index)
        ### Stecker
        Buchstabe = self.Stecker[Buchstabe]
        return Buchstabe
    
    ######################################################################################################
    ### Formatiert Text in 5er-Gruppen, 10 Gruppen je Zeile
    ######################################################################################################
    def formatieren_Text(self, Text_in):
        Text_aus = ' '.join([Text_in[t:t+5] for t in range(0,len(Text_in),5)])
        Text_aus = ''.join([(Text_aus[line:line+60]+'\n ') for line in range(0,len(Text_aus),60)])
        return Text_aus.strip()
        

######################################################################################################
### Klasse zum Laden der Schlüsseltafel und Ausgabe eines Tagesschlüssels
######################################################################################################
class schluesseltafel:    
    ######################################################################################################
    ### Konstruktor, optional mit Angabe Dateiname und gewünschter Tag
    ###
    ### @datei_name  : Name der einzulesenden Datei
    ### @tag_im_monat: Gewünschter Tag als Ziffer 0..31
    ######################################################################################################
    def __init__(self, Datei_Name = None, Tag_im_Monat = None):
        if Datei_Name:
            self.einlesen_Datei(Datei_Name)
            if Tag_im_Monat:
                self.setzen_Tag(Tag_im_Monat)
    
    ######################################################################################################
    ### Einlesen der Datei in die Klassenvariablen
    ###
    ### @datei_name  : Name der einzulesenden Datei
    ###
    ### Erzeugt Klassenvariablen:
    ### ->Schluesseltafel  : Schlüssel des gesamten Monats
    ###                          => Format:[0..n]={'Walzenlage'       : ['I','II','III'], 
    ###                                            'Ringstellung'     : [15, 26 , 8],
    ###                                            'Steckverbindungen': ['AD','ZV','HD', ... ]]}
    ######################################################################################################
    def einlesen_Datei(self, Datei_Name):
        with open(Datei_Name, "r") as Datei:
            datei_zeilen = [zeile.strip() for zeile in Datei.read().split('\n')]
            datei_inhalt = [daten.split(' ') for daten in datei_zeilen]
            datei_inhalt = [[daten for daten in zeile if daten!=''] for zeile in datei_inhalt] 
        self.Tagesschluessel = {}                # TS = Tagesschlüssel - geleert, wenn neue Schlüsseltafel eingelesen
        self.Schluesseltafel = {}                # ST = Schlüsseltafel     
        for schluessel in datei_inhalt:
            if schluessel[0].isdigit() == True:
                tagesschluessel = {'Walzenlage'       : [schluessel[1], schluessel[2], schluessel[3]],
                                   'Ringstellung'     : [int(schluessel[4]), int(schluessel[5]), int(schluessel[6])],
                                   'Steckverbindungen': [schluessel[i] for i in range(7,17)]                          }
                self.Schluesseltafel[int(schluessel[0])] = tagesschluessel
    
    ######################################################################################################
    ### Wählt einen Tag aus der Schlüsseltafel und bereitet Daten des Tages vor
    ###
    ### Erzeugt Klassenvariablen:
    ### ->Tagesschluessel: Chifre-Schlüssel des genannten Monatstages
    ###                                => Format: {'Walzenlage'       : ['I','II','III'], 
    ###                                            'Ringstellung'     : [15, 26 , 8],
    ###                                            'Steckverbindungen': ['AD','ZV','HD', ... ]]}
    ######################################################################################################
    def setzen_Tag(self, Tag_im_Monat):
        self.Tagesschluessel  = self.Schluesseltafel[Tag_im_Monat]          # TS = Tagesschlüssel
        
    ######################################################################################################
    ### Gibt Tagesschlüssel zurück, entweder vorher gewählter oder bei Bedarf neue gesetzter
    ###
    ### @tag_im_monat:  (optional)(int) Tag im Monat im Format 0..31
    ### @return      :  Tagesschlüssel => Format: {'Walzenlage'       : ['I','II','III'], 
    ###                                            'Ringstellung'     : [15, 26 , 8],
    ###                                            'Steckverbindungen': ['AD','ZV','HD', ... ]]}
    ######################################################################################################
    def gebe_Tagesschluessel(self, Tag_im_Monat = None):
        if Tag_im_Monat:
            self.setzen_Tag(Tag_im_Monat)
        return self.Tagesschluessel
        


###############################################################
### Verarbeitung
###
### Schlüsseltafel lesen und Enigma instanzieren
### Enigma einstellen, Grundstellung ermitteln und eingeben
###############################################################
ST = schluesseltafel('Enigma Schluesseltafel', 29)
Enigma = enigma()
Enigma.einstellen(ST.Tagesschluessel['Walzenlage'], \
                  ST.Tagesschluessel['Ringstellung'], \
                  ST.Tagesschluessel['Steckverbindungen'], 'B')
Grundstellung = 'QWE'
Funktripel    = 'EWG'
Enigma.setze_Grundstellung(Grundstellung)
Grundstellung = Enigma.chifrieren_Text(Funktripel).strip()
Enigma.setze_Grundstellung(Grundstellung)
Enigma.drucke_Einstellungen()

###############################################################
### Eingabe-Text lesen und umwandeln
###############################################################
with open('Enigma Text2', 'r') as Datei:
    Text = Datei.read()
print()
print('Text ORIGINAL     :\n', Text)
Text = Enigma.aufbereiten_Text(Text)
print('Text AUFBEREITET  : ', Text)
print('Text FORMATIERT   :\n', Enigma.formatieren_Text(Text))
Chifre = Enigma.chifrieren_Text(Text)
print()
print('Chifre ORIGINAL   : ', Chifre)
Chifre = Enigma.formatieren_Text(Chifre)
print('Chifre FORMATIERT:\n', Chifre)
print()
print('#############################################')
print()


###############################################################
### Chifre lesen und zurückwandeln
###############################################################
with open('Enigma Chifre', 'r') as Datei:
    Chifre = Datei.read()
Enigma.setze_Grundstellung(Grundstellung)
print('Chifre ORIGINAL    :\n', Chifre)
print('Chifre AUFBEREITET : ', Chifre.replace(' ','').replace('\n',''))
Text = Enigma.chifrieren_Text(Chifre)
print()
print('Text ORIGINAL      : ', Text)
Text = Enigma.formatieren_Text(Text)
print('Text AUFBEREITET   :\n', Text)
