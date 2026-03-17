import numpy as np
import matplotlib.pyplot as plt

global B,b,typ_sygnalu, time, sygnal, czas_trwania, amplituda, okres, czestotliwosc_probkowania

### to wszystko trzeba zeby uzytkownik mogl zmieniac (?chyba)
#=============================================================================
typ_sygnalu=0 #0-prostokatny 1-sinus 2-trojkotny
czestotliwosc_probkowania=100
amplituda=2
okres=3
czas_trwania=10

B=2
b=1

Kp=0.5
Tp=0.1

T=0.3
#=============================================================================

sygnal=[]
time = np.linspace(0, czas_trwania, czas_trwania * czestotliwosc_probkowania)

def sygnal_prostokatny(czas_trwania,amplituda,czestotliwosc_probkowania):
    sygnal.append(0)
    for i in range(czas_trwania*czestotliwosc_probkowania-1):
        sygnal.append(amplituda)
    return sygnal

def sygnal_sinus(czas_trwania,amplituda, okres, czestotliwosc_probkowania):
    return amplituda* np.sin(2 * np.pi * 1/okres * time)
   
def sygnal_trojkotny(czas_trwania,amplituda, okres, czestotliwosc_probkowania):
    return   2*amplituda * np.abs(( 1/(okres/2) * time) % 2 - 1)-amplituda

   
def stworz_sygnal(typ_sygnalu):
    if typ_sygnalu==0:
        return sygnal_prostokatny(czas_trwania,amplituda,czestotliwosc_probkowania)
    elif typ_sygnalu==1:
        return sygnal_sinus(czas_trwania,amplituda, okres, czestotliwosc_probkowania)
    elif typ_sygnalu==2:
        return sygnal_trojkotny(czas_trwania,amplituda, okres, czestotliwosc_probkowania)


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