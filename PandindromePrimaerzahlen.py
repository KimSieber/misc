#####################################
##### Palindrome Primärzahlen
#####
##### Rätsel vom IT-Lab der SVI
#####
##### Rätsel - Primzahlen und Palindrome
##### Die kleinste Primzahl mit einer geraden Zahl von Stellen ist 11. 
##### Die Zahl 11 ist gleichzeitig ein Palindrom, also eine Zahl, die man 
##### von links nach rechts und auch von rechts nach links lesen kann, 
##### ohne dass sich ihr Wert ändert.
#####
##### Wie lautet die nächstgrößere Primzahl, die eine gerade Anzahl von 
##### Stellen hat und gleichzeitig ein Palindrom ist?
#####
##### @author    Kim Sieber
##### @create    18.11.2021
#####################################
import time

########################################
##### Primärzahl-Prüfung
#####
##### ermittelt, ob Zahl Primärzahl ist
##### @param     int   Ganzzahl, die geprüft werden soll
##### @return    bool  true/false
########################################
def isPrime(num):
    ### Vorabprüfungen, damit nicht so häufig zeitaufwendige Schleife verwendet werden muss
    if num < 2:              return False
    if num == 2 or num == 3: return True
    if num%2 == 0:           return False
    ### Schleife zur Prüfung Division
    for i in range(3, int(num/2)+1, 2):
        if num%i == 0:       return False
    return True


########################################
##### Palindrom-Prüfung
##### 
##### Prüft, ob Zahl ein Palindrom ist (rückwärts und Vorwärts gleich)
##### Bspw, 11, 131, 156651, 15851, ...
##### @param     int   Ganzzahl, die geprüft werden soll
##### @return    bool  True/False
########################################
def isPalindrom(num):
    ##### einstellige Zahlen zurückgeben
    if num < 10:     return True
    ##### Zahl in Array mit einzelnen Stellen zerlegen
    arr = [int(n) for n in str(num)]
    maxIdx = len(arr)-1
    for i in range(0,maxIdx):
        if arr[i] != arr[maxIdx-i]:   return False
    return True
        

#########################################
##### Suche Palindrome Primärzahlen
##### 
##### sucht Primärzahlen, prüft auf Palindrome und gibt diese aus
##### Begrenzung auf Zahl x
#########################################
x = 100000

t = time.time()

for i in range(0,x):
    if isPalindrom(i):
        if isPrime(i):
            print (i)
            
print ("finished: Laufzeit=", time.time()-t)            
