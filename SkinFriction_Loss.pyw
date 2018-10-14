# -*- coding: utf-8 -*-
"""
Created by Vincenzo Sammartano
email:  v.sammartano@gmail.com
"""
import numpy as num
from tkinter import  *
from tkinter import  messagebox
from PIL import ImageTk, Image
import os

#Tkinter Frame
root = Tk()
root.geometry("700x470+100+50")
root.title("Skin Friction & Head Losses")
root.resizable(width=False, height=False)
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
        FF = "Air"
        #print("Properties of {fluid}: {prop}".format(fluid=FF,prop=FpA))
        Fp = FpA

    if F == 2:
        #Water - Kell formulation
        ro = 999.83952
        At = 1 + (16.879850*10**-3)*T #constant to be used in the Kell formula
            #rot is the water density as function of temperature [Kg/mc]
        rot =  (ro + (16.945176*T) - (7.987040*10**-3)*(T**2.0) -
             +(46.17046*10**-6)*(T**3.0) + (105.56302*10**-9)*(T**4.0)-
                    +(280.54253*10**-12)*(T**5.0))/At
        gamma_t = rot*g #specific weight at t°C
        # 0<t<370 Celsius
        mi = 2.414*(10**-5)*10**(247.8/(t-140)) #Dinamic Viscosity  Pa s = kg m^-1 s^-1
        ni = mi/rot         #Kinetic Viscosity  m2·s-1
        FpW = [rot,gamma_t,mi,ni]
        FF = "Water"
        Fp = FpW

    L0 = Label(root)
    L0.config(text="{:10.4e}".format(Fp[0]),font=f_BO10,bg="white",width=22)
    L0.place(x=455,y=yR+32)   
    L1 = Label(root)
    L1.config(text="{:10.4e}".format(Fp[2]),font=f_BO10,bg="white",width=22)
    L1.place(x=455,y=yR+91)   
    L2 = Label(root)
    L2.config(text="{:10.4e}".format(Fp[3]),font=f_BO10,bg="white",width=22)
    L2.place(x=455,y=yR+152)
    #print(Fp)
    return Fp
    
def ColeBrook(EPS,dc,Re,V0):
    global lamb_,RE
    lamb_= 0

    #First step - Hyp. fully turbulent flow
    turbTerm =  EPS/(3.7*dc) #turbulent term
    lambInf = 0.25 * (num.log10(turbTerm)**2)**-1
    lamI = lambInf #First value for the friction coefficient
    errLam = 999 
    tol  = 1e-14
    its = 0
    while (errLam > tol):
        lamTerm = 2.51/(Re*(lamI**0.5))   
        lamII = 0.25 * (num.log10(turbTerm + lamTerm)**2)**-1 
        errLam = num.abs((lamI - lamII)/lamI)
        lamI = lamII
        its += 1

    lamb_ = lamI
    LAMB = lamb_ 
    lamb_ = "{:14.14f}".format(lamb_)
    L5 = Label(root,text=lamb_,font=f_BO10,bg="white",width=22)
    L5.place(x=455,y=yR+213)

    RE = "{:12.10e}".format(Re)
    L6 = Label(root,text=RE,font=f_BO10,bg="white",width=22)
    L6.place(x=455,y=yR+270)
    #Darcy Module for loss estimation
    Darcy(LAMB,dc,V0)
    
def Darcy(lamb,D,V):
    # The Darcy function allows one to estimate the head Loss per unit lenght
    Loss = (lamb/D)* V**2/(2*g) 
    Loss_ = "{:12.10e}".format(Loss)
    L7 = Label(root,text=Loss_,font=f_BO10,bg="white",width=22)
    L7.place(x=455,y=yR+330)
    TL(Loss)
    
def TL(Loss):
    # the head Loss
    L = float(L_.get())
    HeadLoss = "{:10.4e}".format((Loss*L))
    L8 = Label(root,text=HeadLoss,font=f_BO10,bg="white",width=22)
    L8.place(x=455,y=yR+390)

def calC():
    fp = fluid()
    ni = fp[3]
    modF_ = modF.get()
    Q0 = float(Q0_.get())
    D = float(D_.get())
    if D==0: 
        messagebox.showwarning("Warning","The diameter has to be greater than 0!")
    dc = D
    Ac = 0.25 * num.pi * D**2
    EPS = float(eps_.get())
    EPS = EPS * 1e-3 # absolute wall roughness
    if EPS==0: 
        messagebox.showwarning("Warning","The absolute roughness has to be greater than 0!")
        
    if modF_ == 1:
        #print("velocity mode!")
        V0 = float(V0_.get())
        if V0 == 0:
            messagebox.showwarning("Warning","The velocity has to be greater than 0!")
 
    if modF_ == 2:
        #print("flow rate mode!")
        V0 = Q0/Ac
        if V0 == 0:      
            messagebox.showwarning("Warning","The flow rate has to be greater than 0!")
    Re = V0 * (dc/ni)
    ColeBrook(EPS,dc,Re,V0)

def calR():
    fp = fluid()
    ni = fp[3]
    modF_ = modF.get()
    Q0 = float(Q0_.get())
    sA = float(W_.get())    
    sB = float(H_.get())    
    Ar = sA * sB   # area of the section
    if Ar==0: 
        messagebox.showwarning("Warning","The width and height have be greater than 0!")
    Pr = 2 * (sA + sB) # perimeter of the section
    dc = 4 * (Ar/Pr) #hydraulic diameter
    EPS = float(eps_.get())
    EPS = EPS * 1e-3 # absolute wall roughness
    if EPS==0: 
        messagebox.showwarning("Warning","The absolute roughness has to be greater than 0!")
    if modF_ == 1:
        #print("velocity mode!")
        V0 = float(V0_.get())
        if V0 == 0:
            messagebox.showwarning("Warning","The velocity has to be greater than 0!")
    if modF_ == 2:
       # print("flow rate mode!")
        V0 = Q0/Ar
        if V0 == 0:      
            messagebox.showwarning("Warning","The flow rate has to be greater than 0!")
    Re = V0 * (dc/ni)
    ColeBrook(EPS,dc,Re,V0)

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
    root2 = Tk()
    root2.title('Roughness Values')
    root2.geometry("360x390+450+50")
    
    label1 = Label(root2,text=tit,font=f_BO9)
    label1.pack()
    
    for i in range(len(DIC)):
        st1 = str(DIC[i][0])
        st2 = str(DIC[i][1])
        st = st1 + " {}".format("--"*5+">") +st2
        lab = Label(root2,text=st,font=f_9, justify="right")
        lab.pack()

    root2.mainloop()
##END of Functions

###########Main    
###Fluid Selection
frame00 = Frame(width=240,height=152, colormap="new",relief=SUNKEN,bd=2)
frame00.place(x=15,y=yS1-8)

frame01 = Frame(width=240,height=220, colormap="new",relief=SUNKEN,bd=2)
frame01.place(x=15,y=yS1+180)

w_0 = Label(root,text='___ Physic and Kinetic Parameters ___',font=f_BO9)
w_0.place(x=8,y=2)

f = IntVar()
f2 = Radiobutton(root,text="Air",variable=f,value=1,command=fluid,font=f_BO9)
f2.place(x=31,y=yS1*2)
f3 = Radiobutton(root,text="Water",variable=f,value=2,command=fluid,font=f_BO9)
f3.place(x=31,y=yS1*2+25)

t0 = Radiobutton(root,text="Temperature",value=1,font=f_BO9)
t0.place(x=31,y=yS1)
t0.select()
t0_1 = Label(root,text="[°C]",padx = 0,font=f_BO9)
t0_1.place(x=205,y=yS1)

T_ = StringVar()
t1 = Entry(root,textvariable=T_ , width=6,justify=CENTER)
t1.place(x=XIN,y=yS1)
t1.insert(END, 25)

L0 = Radiobutton(root,text="Duct Lenght",padx = 0,value=1,font=f_BO9)
L0.place(x=31,y=290+yS)
L0.select()
L00 = Label(root,text="[m]",font=f_BO9,justify=RIGHT)
L00.place(x=205,y=290+yS)

L_ = StringVar()
L1 = Entry(root,textvariable=L_ , width=6,justify=CENTER)
L1.place(x=XIN,y=290+yS)
L1.insert(END,1)


#Estimation Method V or Q
modF = IntVar()
l2 = Radiobutton(root,text="Mean Velocity",padx = 0,variable=modF,value=1,font=f_BO9)
l2.place(x=31,y=4*yS1)
l2_1 = Label(root,text="[m/s]",padx = 0,font=f_BO9)
l2_1.place(x=205,y=4*yS1)

l3 = Radiobutton(root,text="Flow Rate",padx = 0,variable=modF,value=2,font=f_BO9)
l3.place(x=31,y=5*yS1)
l3_1 = Label(root,text="[cms]",padx = 0,font=f_BO9)
l3_1.place(x=205,y=5*yS1)

V0_ = StringVar()
v0 = Entry(root,textvariable=V0_ , width=6,justify=CENTER)
v0.place(x=XIN,y=4*yS1)
v0.insert(END, 0)

Q0_ = StringVar()
Q0 = Entry(root,textvariable=Q0_ , width=6,justify=CENTER)
Q0.place(x=XIN,y=5*yS1)
Q0.insert(END, 0)

#Epsilon selection
l4_1 = Label(root,text='_____ Geometric Parameters _______',font=f_BO9)
l4_1.place(x=14,y=4*yS2-30)

l4_2 = Radiobutton(root,text="Wall roughness ",value=1,font=f_BO9)
l4_2.place(x=31,y=4*yS2+10)
l4_2.select()
l4_3 = Label(root,text="[mm]",font=f_BO9)
l4_3.place(x=205,y=4*yS2+10)

eps_ = StringVar()
eps = Entry(root,textvariable=eps_ , width=6,justify=CENTER)
eps.place(x=XIN,y=4*yS2+10)
eps.insert(END, 0)

###Geometry
#Circular Section
c = Label(root,text="Diameter",font=f_BO9,justify=RIGHT)
c.place(x=XIN-65,y=175+yS)
c_1 = Label(root,text="[m]",font=f_BO9)
c_1.place(x=205,y=175+yS)

D_ = StringVar()
d = Entry(root,textvariable=D_,justify=CENTER,width=6)
d.place(x=XIN,y=175+yS)
d.insert(END, 0)

#Rectangular section 
#W
r0 = Label(root,text="Width",font=f_BO9,justify=RIGHT)
r0.place(x=XIN-55,y=225+yS)
r1 = Label(root,text="[m]",font=f_BO9,justify=RIGHT)
r1.place(x=205,y=225+yS)
W_ = StringVar()
w = Entry(root,textvariable=W_ , width=6,justify=CENTER)
w.place(x=XIN,y=225+yS)
w.insert(END, 0)
#H
r2 = Label(root,text="Height",font=f_BO9,justify=RIGHT)
r2.place(x=XIN-55,y=250+yS)
r3 = Label(root,text="[m]",font=f_BO9,justify=RIGHT)
r3.place(x=205,y=250+yS)

H_ = StringVar()
h = Entry(root,textvariable=H_ , width=6,justify=CENTER)
h.place(x=XIN,y=250+yS)
h.insert(END, 0)

###Section selection 
sec = IntVar()
s1 = Radiobutton(root,text="Circular Section",padx = 0,variable=sec,value=1,indicatoron=1)
s1.configure(font=f_BO9)
s1.place(x=31,y=150+yS)

s2 = Radiobutton(root,text=" Rectangular Section ",padx = 0,variable=sec,value=2,indicatoron=1)
s2.configure(font=f_BO9)
s2.place(x=31,y=200+yS)

#Buttons
s3 = Button(root,text="Calculate",command=CAL,font=f_BO9)
s3.config( height = 1, width = 15)
s3.place(x=280,y=170+yS1)

s4 = Button(root,text="EXIT",command=root.destroy,font=f_BO9)
s4.config( height = 1, width = 15)
s4.place(x=280,y=210+yS1)

s5 = Button(root,text='Roughness Table', command=EXA,font=f_BO9)
s5.place(x=280,y=130+yS1)
s5.config(height=1, width=15)

#Results
frame0 = Frame(width=234,height=430, bg="grey", colormap="new",relief=SUNKEN,bd=2)
frame0.place(x=435,y=yR)

lframe1 = Label(root,text="Density [kg/m^3]",font=f_BO9, bg="grey")
lframe1.place(x=495,y=yR+5)
frame1 = Frame(height=30,width=200, bg="white", colormap="new",relief=SUNKEN,bd=2)
frame1.place(x=450,y=yR+25)

lframe2 = Label(root,text="Dinamic viscosity [Pa s]",font=f_BO9, bg="grey")
lframe2.place(x=478,y=yR+65)
frame2 = Frame(height=30,width=200, bg="white", colormap="new",relief=SUNKEN,bd=2)
frame2.place(x=450,y=yR+85)

lframe3 = Label(root,text="Kinematic viscosity [m^2/s]",font=f_BO9, bg="grey")
lframe3.place(x=468,y=yR+125)
frame3 = Frame(height=30,width=200, bg="white", colormap="new",relief=SUNKEN,bd=2)
frame3.place(x=450,y=yR+145)


lframe4 = Label(root,text="Skin Friction Factor [-]",font=f_BO9, bg="grey")
lframe4.place(x=480,y=yR+185)
frame4 = Frame(height=30,width=200, bg="white", colormap="new",relief=SUNKEN,bd=2)
frame4.place(x=450,y=yR+205)

lframe5 = Label(root,text="Reynolds Number [-]",font=f_BO9, bg="grey")
lframe5.place(x=492,y=yR+245)
frame6= Frame(height=30,width=200, bg="white", colormap="new",relief=SUNKEN,bd=2)
frame6.place(x=450,y=yR+265)

lframe7 = Label(root,text="Specific Head-Loss [m/m]",font=f_BO9, bg="grey")
lframe7.place(x=480,y=yR+305)
frame7 = Frame(height=30,width=200, bg="white", colormap="new",relief=SUNKEN,bd=2)
frame7.place(x=450,y=yR+325)

lframe7 = Label(root,text="Head-Loss [m]",font=f_BO9, bg="grey")
lframe7.place(x=508,y=yR+365)
frame7 = Frame(height=30,width=200, bg="white", colormap="new",relief=SUNKEN,bd=2)
frame7.place(x=450,y=yR+385)

root.mainloop()


