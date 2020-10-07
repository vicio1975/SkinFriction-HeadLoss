# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 20:05:37 2020

@author: vsamm
"""

import tkinter as tk


root = tk.Tk()
root.geometry("400x400+100+50")
root.title("test")
root.resizable(width=False, height=False)
root.iconbitmap('C:/Icons/roughness.ico')


##############main frames
leftFrame = tk.Frame(root,width=150)
leftFrame.grid(row=0,column=0, rowspan=2, sticky="nsew")

rightFrame=tk.Frame(root,width=250)
rightFrame.grid(row=0,column=1,rowspan=2,sticky="nesw")


##subframes left
menu_left_1 = tk.LabelFrame(leftFrame,text="frame0", width=150, height=250, bg="red")
menu_left_1.pack(side="top", fill="both", expand=True)

menu_left_2 = tk.LabelFrame(leftFrame,text="frame1", width=150, height=250, bg="blue")
menu_left_2.pack(side="top", fill="both", expand=True)

menu_left_3 = tk.LabelFrame(leftFrame,text="frame2", width=150, height=250, bg="green")
menu_left_3.pack(side="top", fill="both", expand=True)

tk.Label(menu_left_1,text="Sono nel frame 1").pack()
tk.Label(menu_left_2,text="Sono nel frame 2").pack()
tk.Label(menu_left_3,text="Sono nel frame 3").pack()

##subframes right
menu_right_1 = tk.LabelFrame(rightFrame,text="frame4", width=150, height=500, bg="yellow")
menu_right_1.pack(side="top", fill="both", expand=True)

tk.Label(menu_right_1,text="sono nel frame a destra\nciao\nciao\nciao").pack()



root.mainloop()
