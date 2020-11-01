# -*- coding: utf-8 -*-
"""
Created by Vincenzo Sammartano
email:  v.sammartano@gmail.com
"""
import numpy as num
import tkinter as tk
from tkinter import  messagebox
#from PIL import ImageTk, Image
#import os

###spostare blocco parametri per inserire portata in cfm



#Tkinter Frame
root = tk.Tk()
root.geometry("700x550+100+50")
root.title("Skin Friction & Head Losses")
root.resizable(width=False, height=False)
root.iconbitmap('C:/Icons/roughness.ico')

#Fonts
f_8 = ("arial",8)
f_9 = ("arial",9)
f_10 = ("arial",10)
f_IT8 = ("arial",8,"italic")
f_IT8 = ("arial",8,"italic")
f_IT9 = ("arial",9,"italic")
f_IT11 = ("arial",11,"italic")
f_BO7 = ("arial",7,"bold")
f_BO9 = ("arial",9,"bold")
f_BO10 = ("arial",10,"bold")
f_BO12 = ("arial",12,"bold")
#Positions
xS=0

yS2=55
yS1=2+yS2/2
yS=yS2*2
yS3=180
yRes=yS3-100
XIN = 150

yR = 20

#Constants
Rf = 287.058 # Universal Constant of Gases [J/(Kg K)]
pAtm = 101325 # [Pa] atmospheric pressure
g = 9.806   # [m/s2] gravitational accelaration
###

##Functions
def fluid():
    Fp = []
    T = float(T_.get())
    t = T + 273.17 # Kelvin
    F = f.get()

    if F == 1:
        #Air
        rot = pAtm/(Rf*t) #Density as function of temperature in Kelvin [Kg/mc]
        gamma_t = rot * g  #specific weight at t°C
        #Sutherland Equation
        ba = 1.458*10**(-6) 
        sa = 110.4 #Kelvin
        mi = ba * (t**1.5)/(t+sa) #Dinamic Viscosity  Pa s = kg m^-1 s^-1
        ni = mi/rot         #Cinematic Viscosity  m2·s-1
        FpA = [rot,gamma_t,mi,ni]
        Fp = FpA

    if F == 2:
        #Water - Kell formulation
        ro = 999.83952
        At = 1 + (16.879850*10**-3)*T #constant to be used in the Kell formula
            #rot is the water density as function of temperature [Kg/e]
        rot =  (ro + (16.945176*T) - (7.987040*10**-3)*(T**2.0) -
             +(46.17046*10**-6)*(T**3.0) + (105.56302*10**-9)*(T**4.0)-
                    +(280.54253*10**-12)*(T**5.0))/At
        gamma_t = rot*g #specific weight at t°C
        # 0<t<370 Celsius
        mi = 2.414*(10**-5)*10**(247.8/(t-140)) #Dinamic Viscosity  Pa s = kg m^-1 s^-1
        ni = mi/rot         #Kinetic Viscosity  m2·s-1
        FpW = [rot,gamma_t,mi,ni]
        Fp = FpW

    L0 = tk.Label(root) #density
    L0.config(text="{:10.3f}".format(Fp[0]),font=f_BO10,bg="white",width=22)
    L0.place(x=455,y=yR+32)   
    L1 = tk.Label(root) #dynamic viscosity
    L1.config(text="{:10.4e}".format(Fp[2]),font=f_BO10,bg="white",width=22)
    L1.place(x=455,y=yR+91)   
    L2 = tk.Label(root) #kinematic viscosity
    L2.config(text="{:10.4e}".format(Fp[3]),font=f_BO10,bg="white",width=22)
    L2.place(x=455,y=yR+152)
    #print(Fp)
    return Fp
    
# def UFFF1(EPS,dc,Re,V0):
#     global lamb_,RE
#     lamb_= 0
    
#     #ColebrokWhite Equation
#     #First step - Hyp. fully turbulent flow
#     turbTerm =  EPS/(3.71*dc) #turbulent term
#     lambInf = 0.25 * (num.log10(turbTerm)**2)**-1
#     lamI = lambInf #First value for the friction coefficient
#     errLam = 999 
#     tol  = 1e-14
#     its = 0
#     while (errLam > tol):
#         lamTerm = 2.51/(Re*(lamI**0.5))   
#         lamII = 0.25 * (num.log10(turbTerm + lamTerm)**2)**-1 
#         errLam = num.abs((lamI - lamII)/lamI)
#         lamI = lamII
#         its += 1
#     lamb_ = lamI
#     LAMB = lamb_ 
#     lamb_ = "{:14.14f}".format(lamb_)
#     L5 = tk.Label(root,text=lamb_,font=f_BO10,bg="white",width=22)
#     L5.place(x=455,y=yR+213)
#     model = tk.Label(root,text="Colebrook equation", font=f_BO10)
#     model.place(x=45,y=yR+433)    
#     RE = "{:12.2f}".format(Re)
#     L6 = tk.Label(root,text=RE,font=f_BO10,bg="white",width=22)
#     L6.place(x=455,y=yR+270)
#     #Darcy Module for loss estimation
#     Darcy(LAMB,dc,V0)
   
def UFFF(EPS,dc,Re,V0):
    #A New Six Parameter Model to Estimate the Friction Factor
    global lamb_,RE
    
    l1 = 0.02 #residual stress from laminar to turbulent transition
    t1 = 3000 #Reynolds is number at first transition
    l2 = num.abs(l1-(1/(-2*num.log10(EPS/(3.7065*dc))))**2)
    t2 = (0.77505/(EPS/dc)**2) - (10.984/(EPS/dc)) + 7953.8     

    y0 = 64/Re  #laminar flow
    y1 = l1 / (1 + num.e**((t1-Re)/100))
    y2 = l2 / (1 + num.e**(((t2-Re)/600)*EPS/dc)) 
    
    lamb_ = y0 + y1 + y2
    
    LAMB = lamb_ 
    
    lamb_ = "{:14.14f}".format(lamb_)
    L5 = tk.Label(root,text=lamb_,font=f_BO10,bg="white",width=22)
    L5.place(x=455,y=yR+213)
    model = tk.Label(root,text="SixParam equation", font=f_BO10)
    model.place(x=45,y=yR+433)    
    RE = "{:12.2f}".format(Re)
    L6 = tk.Label(root,text=RE,font=f_BO10,bg="white",width=22)
    L6.place(x=455,y=yR+270)
    #Darcy Module for loss estimation
    Darcy(LAMB,dc,V0)    
    
def Darcy(lamb,D,V):
    # The Darcy function allows one to estimate the head Loss per unit lenght
    Loss = (lamb/D)* V**2/(2*g) 
    Loss_ = "{:12.10e}".format(Loss)
    L7 = tk.Label(root,text=Loss_,font=f_BO10,bg="white",width=22)
    L7.place(x=455,y=yR+330)
    TL(Loss)
    
def TL(Loss):
    # the head Loss
    ff = fluid()
    L = float(L_.get())
    LossPa = Loss*ff[1] #Pascal/m
    HeadLoss = "{:10.4e}".format((Loss*L))
    HeadLossPa = "{:10.4e}".format((LossPa*L)) #head loss in Pascal
    L8 = tk.Label(root,text=HeadLoss,font=f_BO10,bg="white",width=22)
    L8_2 = tk.Label(root,text=HeadLossPa,font=f_BO10,bg="white",width=22)

    L8.place(x=455,y=yR+390)
    L8_2.place(x=455,y=yR+450)
    
    
def calC():
    fp = fluid()
    ni = fp[3]
    modF_ = modF.get()
    EPS = float(eps_.get())
    D = float(D_.get())

    #Velocity selection
    if modF_ == 1:
        V0 = float(V0_.get())
        if V0 <= 0:
            messagebox.showwarning("Warning","The velocity has to be greater than 0!")
        else:
            if EPS<=0: 
                messagebox.showwarning("Warning","The absolute roughness has to be greater than 0!")
            if (D <= 0):
                messagebox.showwarning("Warning","The diameter has to be greater than 0!")
            else:
                dc = D
                Ac = 0.25 * num.pi * D**2
                Re = V0 * (dc/ni)
                UFFF(EPS,dc,Re,V0)
    #Flow rate                
    if modF_ == 2:
        Q0 = float(Q0_.get())
        if Q0 <= 0:
            messagebox.showwarning("Warning","The flow rate has to be greater than 0!")
        else:
            if EPS<=0: 
                messagebox.showwarning("Warning","The absolute roughness has to be greater than 0!")
            if D<=0:
                messagebox.showwarning("Warning","The diameter has to be greater than 0!")
            else:
                dc = D
                Ac = 0.25 * num.pi * D**2
                V0 = Q0/Ac
                Re = V0 * (dc/ni)
                UFFF(EPS,dc,Re,V0) 

def calR():
    fp = fluid()
    ni = fp[3]
    modF_ = modF.get()
    EPS = float(eps_.get())
    sA = float(W_.get())    
    sB = float(H_.get())    

    if modF_ == 1:
        V0 = float(V0_.get())
        if V0 <= 0:
            messagebox.showwarning("Warning","The velocity has to be greater than 0!")
        else:
            if EPS==0: 
                messagebox.showwarning("Warning","The absolute roughness has to be greater than 0!")
            else:    
                Ar = sA * sB   # area of the section
                if Ar<=0:
                    messagebox.showwarning("Warning","The width and height have be greater than 0!")
                else:
                    Pr = 2 * (sA + sB) # perimeter of the section
                    dc = 4 * (Ar/Pr) #hydraulic diameter
                    Re = V0 * (dc/ni)
                    UFFF(EPS,dc,Re,V0)
 
    if modF_ == 2:
        Q0 = float(Q0_.get())
        if Q0 <= 0:      
            messagebox.showwarning("Warning","The flow rate has to be greater than 0!")
        else:
            if EPS==0:
                messagebox.showwarning("Warning","The absolute roughness has to be greater than 0!")
            else:
                Ar = sA * sB   # area of the section
                if Ar<=0: 
                    messagebox.showwarning("Warning","The width and height have be greater than 0!")
                else:
                    V0 = Q0/Ar
                    Pr = 2 * (sA + sB) # perimeter of the section
                    dc = 4 * (Ar/Pr) #hydraulic diameter
                    Re = V0 * (dc/ni)
                    UFFF(EPS,dc,Re,V0)
    
    
def CAL():
    modF_ = modF.get()
    sec_ = sec.get()
    F_ = f.get()

    if F_== 0:
        messagebox.showwarning("Warning","Select the Fluid!")

    if modF_ == 0:
        messagebox.showwarning("Warning","You must select velocity\n or flow rate!")
        
    if  sec_  == 1:
        calC()
    elif sec_ == 2:
        calR()
    elif sec_  == 0:
        messagebox.showwarning("Warning","You must select the kind of section!")
    

def EXA():

    choices = """
- Flexible Rubber: 0.3 - 4;
- New cast iron:	0.25 - 0.8;
- Steel commercial pipe: 	0.045 - 0.09;
- Flexible Rubber Tubing Smooth: 0.006 - 0.07;
- Stainless steel: 0.0015;
- PVC and Plastic: 0.0015 - 0.007;
- Asphalted Cast Iron:	0.1 - 1;
- Cast Iron (new): 0.25;
- Cast Iron (old): 1.00;
- Galvanized Iron: 0.025 - 0.150;
- Wood Stave:	 0.180 - 0.91;
- Wood Stave (used): 0.250 - 1.0;
- Smooth Cement: 0.50;
- Concrete – Very Smooth: 0.025 - 0.2;
- Concrete – Fine (Floated, Brushed):	  0.200 - 0.8;
- Concrete – Rough, Form Marks:	0.8 - 3;
- Riveted Steel: 0.91-9.1;
- Water Mains with Tuberculations:	1.2;
- Brickwork, Mature Foul Sewers:3;
"""
    
    c = choices.replace("\t","")
    c = c.replace("\n","")
    DIC = c.split(";")
    
    DIC = [d.split(":") for d in DIC]
    tit = "Table of absolute roughness"
    DIC = DIC[:-1]
    root2 = tk.Tk()
    root2.title('Roughness Values')
    root2.geometry("360x390+450+50")
    
    label1 = tk.Label(root2,text=tit,font=f_BO9)
    label1.pack()
    
    for i in range(len(DIC)):
        st1 = str(DIC[i][0])
        st2 = str(DIC[i][1])
        st = st1 + " {}".format("--"*5+">") +st2
        lab = tk.Label(root2,text=st,font=f_9, justify="right")
        lab.pack()

    root2.mainloop()
##end of Functions

###########Main    
###Fluid Selection
frame00 = tk.Frame(width=240,height=152, colormap="new",relief="sunken",bd=2)
frame00.place(x=15,y=yS1-8)

frame01 = tk.Frame(width=240,height=220, colormap="new",relief="sunken",bd=2)
frame01.place(x=15,y=yS1+180)

w_0 = tk.Label(root,text='___ Physic and Kinetic Parameters ___',font=f_BO9)
w_0.place(x=8,y=2)

f = tk.IntVar()
f2 = tk.Radiobutton(root,text="Air",variable=f,value=1,command=fluid,font=f_BO9,
                    indicatoron=0,height=3,width=12)
f2.place(x=38,y=yS1*2)
f3 = tk.Radiobutton(root,text="Water",variable=f,value=2,command=fluid,font=f_BO9,
                    indicatoron=0,height=3,width=12)
f3.place(x=140,y=yS1*2)

t0 = tk.Radiobutton(root,text="Temperature",value=1,font=f_BO9)
t0.place(x=31,y=yS1)
t0.select()
t0_1 = tk.Label(root,text="[°C]",padx = 0,font=f_BO9)
t0_1.place(x=205,y=yS1)

T_ = tk.StringVar()
t1 = tk.Entry(root,textvariable=T_ , width=6,justify="center")
t1.place(x=XIN,y=yS1)
t1.insert("end", 25)

L0 = tk.Radiobutton(root,text="Duct Lenght",padx = 0,value=1,font=f_BO9)
L0.place(x=31,y=290+yS)
L0.select()
L00 = tk.Label(root,text="[m]",font=f_BO9,justify="right")
L00.place(x=205,y=290+yS)

L_ = tk.StringVar()
L1 = tk.Entry(root,textvariable=L_ , width=6,justify="center")
L1.place(x=XIN,y=290+yS)
L1.insert("end",1)


#Estimation Method V or Q
modF = tk.IntVar()
l2 = tk.Radiobutton(root,text="Mean Velocity",padx = 0,variable=modF,value=1,font=f_BO9)
l2.place(x=31,y=4*yS1)
l2_1 = tk.Label(root,text="[m/s]",padx = 0,font=f_BO9)
l2_1.place(x=205,y=4*yS1)

l3 = tk.Radiobutton(root,text="Flow Rate",padx = 0,variable=modF,value=2,font=f_BO9)
l3.place(x=31,y=5*yS1)
l3_1 = tk.Label(root,text="[m\xb3/s]",padx = 0,font=f_BO9)
l3_1.place(x=205,y=5*yS1)

V0_ = tk.StringVar()
v0 = tk.Entry(root,textvariable=V0_ , width=6,justify="center")
v0.place(x=XIN,y=4*yS1)
v0.insert("end", 0)

Q0_ = tk.StringVar()
Q0 = tk.Entry(root,textvariable=Q0_ , width=6,justify="center")
Q0.place(x=XIN,y=5*yS1)
Q0.insert("end", 0)


#Epsilon selection
l4_1 = tk.Label(root,text='_____ Geometric Parameters _______',font=f_BO9)
l4_1.place(x=14,y=4*yS2-30)

l4_2 = tk.Radiobutton(root,text="Wall roughness ",value=1,font=f_BO9)
l4_2.place(x=31,y=4*yS2+10)
l4_2.select()
l4_3 = tk.Label(root,text="[mm]",font=f_BO9)
l4_3.place(x=205,y=4*yS2+10)

eps_ = tk.StringVar()
eps = tk.Entry(root,textvariable=eps_ , width=6,justify="center")
eps.place(x=XIN,y=4*yS2+10)
eps.insert("end", 0)

###Geometry
#Circular Section
c = tk.Label(root,text="Diameter",font=f_BO9,justify="right")
c.place(x=XIN-65,y=175+yS)
c_1 = tk.Label(root,text="[m]",font=f_BO9)
c_1.place(x=205,y=175+yS)

D_ = tk.StringVar()
d = tk.Entry(root,textvariable=D_,justify="center",width=6)
d.place(x=XIN,y=175+yS)
d.insert("end", 0)

#Rectangular section 
#W
r0 = tk.Label(root,text="Width",font=f_BO9,justify="right")
r0.place(x=XIN-55,y=225+yS)
r1 = tk.Label(root,text="[m]",font=f_BO9,justify="right")
r1.place(x=205,y=225+yS)
W_ = tk.StringVar()
w = tk.Entry(root,textvariable=W_ , width=6,justify="center")
w.place(x=XIN,y=225+yS)
w.insert("end", 0)
#H
r2 = tk.Label(root,text="Height",font=f_BO9,justify="right")
r2.place(x=XIN-55,y=250+yS)
r3 = tk.Label(root,text="[m]",font=f_BO9,justify="right")
r3.place(x=205,y=250+yS)

H_ = tk.StringVar()
h = tk.Entry(root,textvariable=H_ , width=6,justify="center")
h.place(x=XIN,y=250+yS)
h.insert("end", 0)

###Section selection 
sec = tk.IntVar()
s1 = tk.Radiobutton(root,text="Circular Section",padx = 0,variable=sec,value=1,indicatoron=1)
s1.configure(font=f_BO9)
s1.place(x=31,y=150+yS)

s2 = tk.Radiobutton(root,text=" Rectangular Section ",padx = 0,variable=sec,value=2,indicatoron=1)
s2.configure(font=f_BO9)
s2.place(x=31,y=200+yS)

#Buttons
s3 = tk.Button(root,text="Calculate",command=CAL,font=f_BO9)
s3.config( height = 1, width = 15)
s3.place(x=280,y=240+yS1)

s4 = tk.Button(root,text="EXIT",command=root.destroy,font=f_BO9)
s4.config( height = 1, width = 15)
s4.place(x=280,y=280+yS1)

s5 = tk.Button(root,text='Roughness Table', command=EXA,font=f_BO9)
s5.place(x=280,y=200+yS1)
s5.config(height=1, width=15)

#Results
frame0 = tk.Frame(width=234,height=500, bg="grey", colormap="new",relief="sunken",bd=2)
frame0.place(x=435,y=yR)

lframe1 = tk.Label(root,text="Density [kg/m\xb3]",font=f_BO9, bg="grey")
lframe1.place(x=495,y=yR+5)
frame1 = tk.Frame(height=30,width=200, bg="white", colormap="new",relief="sunken",bd=2)
frame1.place(x=450,y=yR+25)

lframe2 = tk.Label(root,text="Dinamic viscosity [Pa s]",font=f_BO9, bg="grey")
lframe2.place(x=478,y=yR+65)
frame2 = tk.Frame(height=30,width=200, bg="white", colormap="new",relief="sunken",bd=2)
frame2.place(x=450,y=yR+85)

lframe3 = tk.Label(root,text="Kinematic viscosity [m\xb2/s]",font=f_BO9, bg="grey")
lframe3.place(x=468,y=yR+125)
frame3 = tk.Frame(height=30,width=200, bg="white", colormap="new",relief="sunken",bd=2)
frame3.place(x=450,y=yR+145)


lframe4 = tk.Label(root,text="Skin Friction Factor [-]",font=f_BO9, bg="grey")
lframe4.place(x=480,y=yR+185)
frame4 = tk.Frame(height=30,width=200, bg="white", colormap="new",relief="sunken",bd=2)
frame4.place(x=450,y=yR+205)

lframe5 = tk.Label(root,text="Reynolds Number [-]",font=f_BO9, bg="grey")
lframe5.place(x=492,y=yR+245)
frame6= tk.Frame(height=30,width=200, bg="white", colormap="new",relief="sunken",bd=2)
frame6.place(x=450,y=yR+265)

lframe7 = tk.Label(root,text="Specific Head-Loss [m/m]",font=f_BO9, bg="grey")
lframe7.place(x=480,y=yR+305)
frame7 = tk.Frame(height=30,width=200, bg="white", colormap="new",relief="sunken",bd=2)
frame7.place(x=450,y=yR+325)

lframe8 = tk.Label(root,text="Head-Loss [m]",font=f_BO9, bg="grey")
lframe8.place(x=508,y=yR+365)
frame8 = tk.Frame(height=30,width=200, bg="white", colormap="new",relief="sunken",bd=2)
frame8.place(x=450,y=yR+385)

lframe9 = tk.Label(root,text="Energy Loss [Pa]",font=f_BO9, bg="grey")
lframe9.place(x=508,y=yR+425)
frame9 = tk.Frame(height=30,width=200, bg="white", colormap="new",relief="sunken",bd=2)
frame9.place(x=450,y=yR+445)

root.mainloop()


