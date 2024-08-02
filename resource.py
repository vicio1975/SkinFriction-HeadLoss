
##Functions

def fluid():
    Fp = []
    T = float(T_.get())
    t = T + 273.17 # Kelvin
    F = f_sel.get()

    if F == "Air":
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

    if F == "Water":
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

    return Fp
   
def UFFF1(EPS,dc,Re,V):
    lamb_= 0
    ff = fluid()
    L = float(L_.get())
    #ColebrokWhite Equation
    #First step - Hyp. fully turbulent flow
    turbTerm =  EPS/(3.71*dc) #turbulent term
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

    ####DarcyWeisbach Equation
    J = (LAMB/dc)* V**2/(2*g) #Specific Losses in m/m
    HeadLoss = J*L #Total Losses in m
    HeadLossPa = HeadLoss * ff[1] #Total losses in Pa

    global RES
    RES = [dc,Re,LAMB,J,HeadLoss,HeadLossPa]
    printOut()

def UFFF2(EPS,dc,Re,V):
    #A New Six Parameter Model to Estimate the Friction Factor
 
    ff = fluid()
    L = float(L_.get())

    l1 = 0.02 #residual stress from laminar to turbulent transition
    t1 = 3000 #Reynolds is number at first transition
    l2 = num.abs(l1-(1/(-2*num.log10(EPS/(3.7065*dc))))**2)
    t2 = (0.77505/(EPS/dc)**2) - (10.984/(EPS/dc)) + 7953.8     

    y0 = 64/Re  #laminar flow
    y1 = l1 / (1 + num.e**((t1-Re)/100))
    y2 = l2 / (1 + num.e**(((t2-Re)/600)*EPS/dc)) 
    
    LAMB = y0 + y1 + y2

    ####DarcyWeisbach Equation
    J = (LAMB/dc)* V**2/(2*g) #Specific Losses in m/m
    HeadLoss = J*L #Total Losses in m
    HeadLossPa = HeadLoss * ff[1] #Total losses in Pa

    global RES

    RES = [dc,Re,LAMB,J,HeadLoss,HeadLossPa]

    printOut()

def printOut():
   
    ff = fluid() #[rot,gamma_t,mi,ni]
    labflu = ["{:4.3f}".format(ff[0]),"{:4.3f}".format(ff[1]),"{:1.3e}".format(ff[2]),"{:1.3e}".format(ff[3])]
    labels = ["{:6.3f}".format(RES[0]),"{:8.0f}".format(RES[1]),"{:6.7f}".format(RES[2]),"{:6.7f}".format(RES[3]),"{:6.7f}".format(RES[4]),
             "{:3.4e}".format(RES[5])]
 
    for i,l in enumerate(labflu):
        tk.Label(frame03,text=l, bg="white",width=15,font=f_H12,anchor='center',borderwidth=2, relief="groove").grid(row=i,column=1,padx=3)
               
    for i,r in enumerate(labels):
        tk.Label(frame03,text=r, bg="white",width=15,font=f_H12,anchor='center',borderwidth=2, relief="groove").grid(row=i+4,column=1,padx=3)
        
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
                if modForm.get()==1: UFFF1(EPS,dc,Re,V0)
                elif modForm.get()==2: UFFF2(EPS,dc,Re,V0)
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
                if modForm.get()==1: UFFF1(EPS,dc,Re,V0)
                elif modForm.get()==2: UFFF2(EPS,dc,Re,V0)

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
                    if modForm.get()==1: UFFF1(EPS,dc,Re,V0)
                    elif modForm.get()==2: UFFF2(EPS,dc,Re,V0)
   
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
                    if modForm.get()==1: UFFF1(EPS,dc,Re,V0)
                    elif modForm.get()==2: UFFF2(EPS,dc,Re,V0)
    
def calGen():
    fp = fluid()#
    ni = fp[3]
    modF_ = modF.get()
    EPS = float(eps_.get())
    Ar = float(A_.get())    
    Pr = float(P_.get())
    
    if modF_ == 1:
        V0 = float(V0_.get())
        if V0 <= 0:
            messagebox.showwarning("Warning","The velocity has to be greater than 0!")
        else:
            if EPS==0: 
                messagebox.showwarning("Warning","The absolute roughness has to be greater than 0!")
            else:   
                if Ar<=0: 
                    messagebox.showwarning("Warning","Please, do check Area and Perimeter of the section!")
                else:
                    dc = 4 * (Ar/Pr) #hydraulic diameter
                    Re =V0*(dc/ni)
                    if modForm.get()==1: UFFF1(EPS,dc,Re,V0)
                    elif modForm.get()==2: UFFF2(EPS,dc,Re,V0)
                    
    if modF_ == 2:
        Q0 = float(Q0_.get())
        if Q0 <= 0:      
            messagebox.showwarning("Warning","The flow rate has to be greater than 0!")
        else:
            if EPS==0:
                messagebox.showwarning("Warning","The absolute roughness has to be greater than 0!")
            else:
                V0 = Q0/Ar
                if Ar<=0: 
                    messagebox.showwarning("Warning","Please, do check Area and Perimeter of the section!")
                else:
                    dc = 4 * (Ar/Pr) #hydraulic diameter
                    V0 = Q0/Ar
                    Re =V0*(dc/ni)
                    if modForm.get()==1: UFFF1(EPS,dc,Re,V0)
                    elif modForm.get()==2: UFFF2(EPS,dc,Re,V0)
      
def CAL():
    modF_ = modF.get()
    sec_ = sec.get()
    F_ = f_sel.get()

    if F_ not in flu_opt:
        messagebox.showwarning("Warning","Select the Fluid!")
    if modF_ == 0:
        messagebox.showwarning("Warning","You must select velocity\n or flow rate!")        
    if  sec_  == 1:
        calC()
    elif sec_ == 2:
        calR()
    elif sec_ == 3:
        calGen()
    elif sec_  == 0:
        messagebox.showwarning("Warning","You must select the kind of section!")

def ACT():
    if sec.get()==1:
        d.config(state='normal')
        d.delete(0,'end')
        d.insert('end',0)

        w.delete(0,'end')
        w.insert('end',0)
        w.config(state='disabled')

        h.delete(0,'end')
        h.insert('end',0)
        h.config(state='disabled')

        p.delete(0,'end')
        p.insert('end',0)
        p.config(state='disabled')

        a.delete(0,'end')
        a.insert('end',0)
        a.config(state='disabled')

        dd.config(fg='black')
        ddu.config(fg='black')
        ww.config(fg='gray')
        wwu.config(fg='gray')        
        hh.config(fg='gray')
        hhu.config(fg='gray')
        AA.config(fg='gray')
        AAU.config(fg='gray')
        PP.config(fg='gray')
        PPU.config(fg='gray')

      
    if sec.get()==2:
        w.config(state='normal')
        h.config(state='normal')
        w.delete(0,'end')
        w.insert('end',0)
        h.delete(0,'end')
        h.insert('end',0)

        d.delete(0,'end')
        d.insert('end',0)
        d.config(state='disabled')

        a.delete(0,'end')
        a.insert('end',0)
        a.config(state='disabled')

        p.delete(0,'end')
        p.insert('end',0)
        p.config(state='disabled')

        ww.config(fg='black')
        wwu.config(fg='black')
        hh.config(fg='black')
        hhu.config(fg='black')         
        d.config(state='disabled')
        dd.config(fg='gray')
        ddu.config(fg='gray')
        a.config(state='disabled')
        AA.config(fg='gray')
        AAU.config(fg='gray')        
        p.config(state='disabled')
        PP.config(fg='gray')
        PPU.config(fg='gray')       

    if sec.get()==3:
        a.config(state='normal')
        p.config(state='normal')
        a.delete(0,'end')
        a.insert('end',0)
        p.delete(0,'end')
        p.insert('end',0)

        d.delete(0,'end')
        d.insert('end',0)
        d.config(state='disabled')

        w.delete(0,'end')
        w.insert('end',0)
        w.config(state='disabled')

        h.delete(0,'end')
        h.insert('end',0)
        h.config(state='disabled')

        PP.config(fg='black')
        PPU.config(fg='black')
        AA.config(fg='black')
        AAU.config(fg='black')
        dd.config(fg='gray')
        ddu.config(fg='gray')        
        ww.config(fg='gray')
        wwu.config(fg='gray')
        hh.config(fg='gray')
        hhu.config(fg='gray')

def ACTF():
    if modF.get()==1:
        v0.config(state='normal')
        Q0.delete(0,'end')
        Q0.insert('end',0)
        Q0.config(state='disabled')

        v0.delete(0,'end')
        v0.insert('end',0)

        Q0.config(fg='black')
        l2.config(fg='black')
        l2_1.config(fg='black')
        f3.config(fg='gray')
        f3_1.config(fg='gray')
    
    if modF.get()==2:
        Q0.config(state='normal')
        v0.delete(0,'end')
        v0.insert('end',0)
        v0.config(state='disabled')

        Q0.delete(0,'end')
        Q0.insert('end',0)
        
        v0.config(fg='black')
        f3.config(fg='black')
        f3_1.config(fg='black')
        l2.config(fg='gray')
        l2_1.config(fg='gray')
        
def ACTF2():
    if modForm.get() == 1:
        for1.config(state='normal')
        for1.config(fg='black')
        for2.config(fg='gray')
    
    if modForm.get() == 2:
        for2.config(state='normal') 
        for1.config(fg='gray')
        for2.config(fg='black')

#Define a callback function
def callback(url):
   webbrowser.open_new_tab(url)

def table():

    choices = """
- Flexible Rubber: 0.3 - 4;\n
- New cast iron:	0.25 - 0.8;\n
- Steel commercial pipe: 	0.045 - 0.09;\n
- Flexible Rubber Tubing Smooth: 0.006 - 0.07;\n
- Stainless steel: 0.0015;\n
- PVC and Plastic: 0.0015 - 0.007;\n
- Asphalted Cast Iron:	0.1 - 1;\n
- Cast Iron (new): 0.25;\n
- Cast Iron (old): 1.00;\n
- Galvanized Iron: 0.025 - 0.150;\n
- Wood Stave:	 0.180 - 0.91;\n
- Wood Stave (used): 0.250 - 1.0;\n
- Smooth Cement: 0.50;\n
- Concrete – Very Smooth: 0.025 - 0.2;\n
- Concrete – Fine (Floated, Brushed):	  0.200 - 0.8;\n
- Concrete – Rough, Form Marks:	0.8 - 3;\n
- Riveted Steel: 0.91-9.1;\n
- Water Mains with Tuberculations:	1.2;\n
- Brickwork, Mature Foul Sewers: 3;\n
"""
    
    tit = "Table of absolute roughness"
    global root2, fin2

    root2 = tk.Tk()
    root2.title('Roughness Values')
    root2.geometry("450x550+900+50")
    root2.resizable(width=False, height=False)
    root2.iconbitmap('roughness.ico')
    
    label1 = tk.Label(root2,text=tit,font=('Helvetica', 14, 'normal'))
    label1.pack()
    
    T = tk.Text(root2, height=25, width=40,font=('Helvetica', 12, 'normal'))
    T.pack()
    T.config(state='normal')
    T.insert(tk.END, choices)
    T.config(state='disabled')
    fin2 = 1
    tk.Button(root2,text="EXIT",command=EX,font=('Helvetica', 12, 'normal','bold'),height = 1, width = 10).pack(pady=10)
    root2.mainloop()
    
def EX():
    #root.destroy()
    try:
        fin2
    except NameError:
        var_exists = False
        if var_exists: print("Window does not exist")
    else:
        root2.destroy()

def EX_out():
    root.destroy()
   
# ##end of Functions
# ##########################################

###########Main    
#INPUT
#fluid selection
f_sel = tk.StringVar()
f_sel.set(flu_opt[0])
f1 = tk.OptionMenu(frame00,f_sel, *flu_opt)
f1.config(width=8,font=f_H11)
f1.grid(row=0,column=1,sticky='W',pady=5)
tk.Label(frame00,text="Choose fluid",font=f_H12).grid(row=0,column=0,padx=15,sticky="W")

#temperature selection
tk.Label(frame00,text="Temperature",font=f_H12).grid(row=1,column=0,padx=15,pady=5,sticky='W')
tk.Label(frame00,text="[°C]",font=f_H12).grid(row=1, column=2,pady=5)
T_ = tk.StringVar()
t1 = tk.Entry(frame00,textvariable=T_ , width=6, justify="center",font=f_H12)
t1.grid(row = 1, column=1,pady=5)
t1.insert("end", 20)

#Method Velocity or Flow rate
modF = tk.IntVar()
l2 = tk.Radiobutton(frame00,text="Mean Velocity",padx = 10,variable=modF,value=1,font=f_H12)
l2.grid(row=2,column=0,sticky='W')
l2.configure(command=ACTF, indicatoron=1)

l2_1 = tk.Label(frame00,text="[m/s]",padx = 5,font=f_H12)
l2_1.grid(row=2,column=2,pady=5)
l2.select()

V0_ = tk.StringVar()
v0 = tk.Entry(frame00,textvariable=V0_ , width=6,justify="center",font=f_H12)
v0.grid(row=2,column=1,pady=5)
v0.insert('end',0)
v0.configure(state='normal')

f3 = tk.Radiobutton(frame00,text="Flow Rate",padx = 10,variable=modF,value=2,font=f_H12)
f3.grid(row=3,column=0,sticky='W')
f3.configure(command=ACTF)
f3_1 = tk.Label(frame00,text="[m\xb3/s]", padx = 5,font=f_H12)
f3_1.grid(row=3,column=2,pady=5)
f3.config(fg='gray')
f3_1.config(fg='gray')
    
Q0_ = tk.StringVar()
Q0 = tk.Entry(frame00,textvariable=Q0_ , width=6, justify="center",font=f_H12)
Q0.grid(row=3,column=1,pady=5)
Q0.insert('end',0)
Q0.configure(state='disabled')

#####Geometry settings
#Length
L0 = tk.Label(frame01,text="Duct Length",font=f_H12)
L0.grid(row = 0, column = 0,padx=10,pady =5)
L_ = tk.StringVar()
L1 = tk.Entry(frame01,textvariable = L_ , width = 6, justify="center",font=f_H12)
L1.grid(row = 0 , column=1,padx=10,pady=5)
L1.insert("end",1)
tk.Label(frame01,text="[m]",font=f_H12,justify="right").grid(row=0, column=2,padx=10,pady = 5)

# #Epsilon selection
tk.Label(frame01,text="Wall roughness",font=f_H12).grid(row=1,column=0,padx=10,pady = 5)
tk.Label(frame01,text="[mm]",font=f_H12).grid(row=1,column=2,padx=10,pady = 5)

eps_ = tk.StringVar()
eps = tk.Entry(frame01,textvariable=eps_,width=8,justify="center",font=f_H12)
eps.grid(row=1,column=1,padx=10,pady = 5)
eps.insert("end", 0.0015)
        
##Cross Section Geometry
sec = tk.IntVar()
s1 = tk.Radiobutton(frame02,text="Circular Section", padx=10,variable=sec,value=1,indicatoron=1)
s1.configure(font=f_H12,command=ACT)
s1.grid(row=0, column=0,sticky='W')
s1.select()
s2 = tk.Radiobutton(frame02,text="Rectangular Section",padx=10,variable=sec,value=2,indicatoron=1)
s2.configure(font=f_H12,command=ACT)
s2.grid(row=1, column=0,sticky='W')
s3 = tk.Radiobutton(frame02,text="Irregular Section",padx=10,variable=sec,value=3,indicatoron=1)
s3.configure(font=f_H12,command=ACT)
s3.grid(row=2, column=0,sticky='W')

###Geometry inputs
#Circular Section
dd = tk.Label(frame02,text="Diameter",font=f_H12,justify="left")
dd.grid(row=3,column=0,padx=20,pady = 5)
ddu = tk.Label(frame02,text="[m]",font=f_H12)
ddu.grid(row=3,column=2,padx=10,pady=5)
D_ = tk.StringVar()
d = tk.Entry(frame02,textvariable=D_,width=6,justify="center",font=f_H12)
d.grid(row=3,column=1,padx=10,pady=5)
d.insert('end',0)
d.config(state='normal')

#Rectangular section 
#Width
ww = tk.Label(frame02,text="Width",font=f_H12,justify="left")
ww.grid(row=5,column=0,padx=20,pady = 5)
wwu = tk.Label(frame02,text="[m]",font=f_H12)
wwu.grid(row=5,column=2,padx=20,pady=5)
W_ = tk.StringVar()
w = tk.Entry(frame02,textvariable=W_,width=6,justify="center",font=f_H12)
w.grid(row=5,column=1,padx=10,pady=5)
w.insert('end',0)
w.config(state='disabled')

#Height
hh = tk.Label(frame02,text="Height",font=f_H12,justify="left")
hh.grid(row=6,column=0,padx=20,pady = 5)
hhu = tk.Label(frame02,text="[m]",font=f_H12,justify="left")
hhu.grid(row=6,column=2,padx=20,pady = 5)
H_ = tk.StringVar()
h = tk.Entry(frame02,textvariable=H_ , width=6,justify="center",font=f_H12)
h.grid(row=6,column=1,padx=10,pady=5)
h.insert('end',0)
h.config(state='disabled')

#Irregular section 
#Area
AA = tk.Label(frame02,text="Area",font=f_H12,justify="left")
AA.grid(row=7,column=0,padx=20,pady = 5)
AAU = tk.Label(frame02,text="[m\xb2]",font=f_H12)
AAU.grid(row=7,column=2,padx=20,pady=5)
A_ = tk.StringVar()
a = tk.Entry(frame02,textvariable=A_,width=6,justify="center",font=f_H12)
a.grid(row=7,column=1,padx=10,pady=5)
a.insert('end',0)
a.config(state='disabled')

#Perimeter
PP = tk.Label(frame02,text="Perimeter",font=f_H12,justify="left")
PP.grid(row=8,column=0,padx=20,pady = 5)
PPU = tk.Label(frame02,text="[m]",font=f_H12,justify="left")
PPU.grid(row=8,column=2,padx=20,pady = 5)
P_ = tk.StringVar()
p = tk.Entry(frame02,textvariable=P_ , width=6,justify="center",font=f_H12)
p.grid(row=8,column=1,padx=10,pady=5)
p.insert('end',0)
p.config(state='disabled')
#label at startup
ww.config(fg='gray')
wwu.config(fg='gray')   
hh.config(fg='gray')
hhu.config(fg='gray')
PP.config(fg='gray')
PPU.config(fg='gray')
AA.config(fg='gray')
AAU.config(fg='gray')

#Formulation selection CooleBrookWhite or SixParamters equation
modForm = tk.IntVar()
for1 = tk.Radiobutton(frame04, text="Colebrook-White Equation", padx = 10, variable=modForm , value=1, font=f_H12)
for1.grid(row=4, column=0, sticky='W')
for1.configure(command=ACTF2, indicatoron=1)
for1.select()
for1.configure(state='normal')

for2 = tk.Radiobutton(frame04,text="Six-Factors Equation", padx = 10, variable=modForm, value=2,font=f_H12)
for2.grid(row=4,column=1,sticky='W')
for2.configure(command=ACTF2)
for2.config(fg='gray')
link = tk.Label(frame04,text="References", padx = 5, font = f_Ref, fg='#000080')
link.grid(row=4,column=2,sticky='W')
link.bind("<Button-1>", lambda e: callback("https://doi.org/10.1002/aic.16535"))

# #Results
VarList = ['Density [kg/m\xb3]','Specific weight [N/m\xb3]','Dinamic viscosity [Pa s]','Kinematic viscosity [m\xb2/s]',
            'Hydraulic Diameter [m]','Reynolds [-]','Skin Friction [-]','Specific Head-Loss [m/m]','Head-Loss [m]',
            'Head-Loss [Pa]']
for i,var in enumerate(VarList):
    tk.Label(frame03,text=var,font=f_H12).grid(row=i,column=0,sticky="E",pady=11)
    tk.Frame(frame03,height=35,width=150, colormap="new",relief="sunken",bd=2).grid(row=i,column=1,sticky="E",padx=18,pady=11)

