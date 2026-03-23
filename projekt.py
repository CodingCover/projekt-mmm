
import numpy as np
import matplotlib.pyplot as plt

global B,b,typ_sygnalu, time, sygnal, czas_trwania, amplituda, okres, czestotliwosc_probkowania

### mój kod
#=============================================================================
typ_sygnalu = input("Wpisz typ sygnału na wejście\nP dla sygnału prostokątnego\nT dla sygnału trójkątnego\nH dla sygnału harmonicznego\n").upper()

while typ_sygnalu not in ['P', 'T', 'H']:
  print("wybrałeś niedostępny typ sygnału.\n")
  typ_sygnalu = input("Wpisz typ sygnału na wejście\nP dla sygnału prostokątnego\nT dla sygnału trójkątnego\nH dla sygnału harmonicznego\n").upper()


nazwa = "empty_nazwa" 
zakres = "empty_zakres" 
def poprawnaWartosc(nazwa, minW,maxW):
    while True:
     
     if nazwa == "czestotliwosc_sygnalu":
       wartosc = int(input(f"Podaj {nazwa}. Dostępny zakres to {minW} - {maxW}\n"))# = 2
     else:  
       wartosc = float(input(f"Podaj {nazwa}. Dostępny zakres to {minW} - {maxW}\n"))# = 2
       
     if wartosc > 0 and minW <= wartosc <= maxW:
      return wartosc
     else: 
        print("błąd, wpisz wartosc z zakresu\n")


czestotliwosc_sygnalu  = poprawnaWartosc("częstotliwość sygnału", 1,1000000)#dla czestotliwosci wiekszych niz 2 juz dziwnie male wyjscie sie robi. 
liczba_okresow = poprawnaWartosc("liczba okresów", 0.1,10)
czas_trwania = liczba_okresow / czestotliwosc_sygnalu

if typ_sygnalu == 'H':
    czestotliwosc_probkowania = czestotliwosc_sygnalu*10
else:
    czestotliwosc_probkowania = czestotliwosc_sygnalu*20
 


## warunki stabilnosci liniowej, zeby uklad "nie wariowal"(1+T*Kp) > 0, #Tp > 0 --> nie zostały użyte bo to już wykluczają ograniczenia 
# sensu fizycznego układu tzn. {T,Kp,T} > 0


amplituda = poprawnaWartosc("amplituda sygnału wejściowego", 0.5,5)
B = poprawnaWartosc("amplituda przekaźnika", 0.5*amplituda,5*amplituda)
b = poprawnaWartosc("histereza", 0.1*amplituda, 0.8*amplituda)
T = poprawnaWartosc("tłumienie?", 0.1, 2)
Kp = poprawnaWartosc("wzmocnienie filtra dolnoprzepustowego", 0.1, 5)
Tp = poprawnaWartosc("stała czasowa filtra dolnoprzepustowego", 0.01, 1) 


#===============================================================================
### tutaj zmienilem zmienne dalem do funkcji czestotliwosc sygnalu zamiast okresu i usunalem chyba nie używane parametry w funkcjach
# tak to jeszcze def sygnal prostakotny by trzeba bylo poprawic bo chat gpt pisze ze to skok jednostkowy.
# ja to moge potem od gpt skopiowac poprawne, #ty też możesz jak chcesz
#W tym kodzie zmienna TT = 1/fprobkowania bedzie miala inna wartosc bo nie jest jako stala zafixowana, bo u mnie fprobkowania to 10 lub 20 krotnosc 
#czestotliwosci sygnału wejściowego czyli u ciebie 1 / okres
sygnal=[]
time = np.linspace(0, czas_trwania, int(czas_trwania * czestotliwosc_probkowania))

def sygnal_prostokatny(czas_trwania,amplituda,czestotliwosc_probkowania):
    for i in range(czas_trwania*czestotliwosc_probkowania):
     return amplituda * np.sign(np.sin(2*np.pi*time/okres))

def sygnal_sinus(amplituda, czestotliwosc_sygnalu):
    return amplituda* np.sin(2 * np.pi * czestotliwosc_sygnalu * time)
   
def sygnal_trojkotny(amplituda, czestotliwosc_sygnalu):
    return   2*amplituda * np.abs(( czestotliwosc_sygnalu * 2 * time) % 2 - 1)-amplituda

   
def stworz_sygnal(typ_sygnalu):
    if typ_sygnalu==0:
        return sygnal_prostokatny(czas_trwania,amplituda,czestotliwosc_probkowania)
    elif typ_sygnalu==1:
        return sygnal_sinus(amplituda, czestotliwosc_sygnalu)
    elif typ_sygnalu==2:
        return sygnal_trojkotny(amplituda, czestotliwosc_sygnalu)


# inicjowanie wektorow zmiennych
r=stworz_sygnal(typ_sygnalu=1)
e=np.zeros(len(r))
e2=np.zeros(len(r))
u=np.zeros(len(r))
y=np.zeros(len(r))
y2=np.zeros(len(r))

# warunki poczatkowe
e[0]=r[0]-y[0]
e2[0]=e[0]-T*y2[0]
if e2[0]>b: u[0]=B
else: u[0]=-B
y2[0]=0
y[0]=0

TT=1/czestotliwosc_probkowania
for t in range (1,len(r)):
    e[t]=r[t]-y[t-1]
    e2[t]=e[t]-T*y2[t-1]
    
    # blok histerezy
    if e2[t]>b:
        u[t]=B
    elif e2[t]<-b:
        u[t]=-B
    else:
        u[t]=u[t-1] 
    
    y2[t]=(TT*u[t]*Kp+Tp*y2[t-1])/(TT+Tp) # blok kp/(1+tps)

    #y2[t]=y2[t-1] + (TT/Tp)*(Kp*u[t] - y2[t-1])

    y[t]=y[t-1]+y2[t]*TT # blok 1/s
    


plt.plot(time,r)
plt.plot(time,e)
plt.plot(time,e2)
plt.plot(time,u)
plt.plot(time,y)
plt.plot(time,y2)

plt.legend(["r(t)","e(t)","e2(t)","u(t)","y(t)","y2(t)"])
plt.xlabel("Czas [s]")
plt.ylabel("Wartość sygnału")
plt.grid()
plt.show()
