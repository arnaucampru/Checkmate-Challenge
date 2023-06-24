import tkinter as tk
from PIL import Image, ImageTk
import numpy as np

class Partida():
    def __init__(self,root):
        self._root=root
        self._root.geometry("640x640")
        self._root.bind_all("<Button-1>", self.Moviment)
        self._root.bind_all("<Button-2>", self.eliminaComp)
        
        self._turn=True#true-->torn jugador blanc
        #indica coordenades de ultima fitxa blanc/negre clicada
        self._tempx=0
        self._tempy=0
        self._expulsar=[]
             
        self._tauler_image = Image.open("ANTIALIAS.png")
        self._tauler_photo = ImageTk.PhotoImage(self._tauler_image)
        
        self._fitxa_image = Image.open("BLANCA.png")
        self._fitxa_photo = ImageTk.PhotoImage(self._fitxa_image)
        
        self._fitxa_image2 = Image.open("NEGRE.png")
        self._fitxa_photo2 = ImageTk.PhotoImage(self._fitxa_image2)
        
        self._fitxa_verdaa = Image.open("VERD.png")
        self._fitxa_verda = ImageTk.PhotoImage(self._fitxa_verdaa)
        
        self._tauler = tk.Label(self._root, image=self._tauler_photo) 
        self._tauler["bd"] = 0
        self._tauler.place(x = 0, y = 0) 
        
        self._fitxa = tk.Button(self._root, image=self._fitxa_photo)
        self._fitxa["bd"]=0
        
        self._llista=[[[0,0]for i in range(8)]for x in range(8)]
        a=np.zeros((8,8))
        a[0:3:2,::2]=2#-->negres
        a[1,1::2]=2
        a[5::2,1::2]=1
        a[6,::2]=1#-->blanques
        for files,valors in enumerate(a):
            for columnes,num in enumerate(valors):
                if a[files,columnes] == 2:
                     self._llista[files][columnes] = [2,tk.Button(self._root, image=self._fitxa_photo2)]
                     self._llista[files][columnes][1]["bd"]=0
                     self._llista[files][columnes][1].place(x = (columnes)*80, y = (files)*80)
                if a[files,columnes] == 1:
                    self._llista[files][columnes] = [1,tk.Button(self._root, image=self._fitxa_photo)]
                    self._llista[files][columnes][1]["bd"]=0
                    self._llista[files][columnes][1].place(x = (columnes)*80, y = (files)*80)
        
    
    def eliminafitxa(self,x,y):
        self._llista[y][x][1].destroy()
        self._llista[y][x]=[0,0]
    
    def afegeixfitxa(self,x,y,tipus):
        if self._llista[y][x][0]!=0:
            self.eliminafitxa(x,y)
        if tipus ==1:
            self._llista[y][x]=[tipus,tk.Button(self._root,image=self._fitxa_photo)]
        elif tipus ==2:
            self._llista[y][x]=[tipus,tk.Button(self._root,image=self._fitxa_photo2)]
        elif tipus ==3:
            self._llista[y][x]=[tipus,tk.Button(self._root,image=self._fitxa_verda)]
        self._llista[y][x][1].place(x=x*80,y=y*80)
        
    def eliminaComp(self,event):
        for f,valor in enumerate(self._llista):
            for c,num in enumerate(valor):
                if self._llista[f][c][0]==3:
                    self._llista[f][c][1].destroy()
                    self._llista[f][c]=[0,0]
                    
    
    def CompBlanca(self,x,y):
        self._expulsar=[]
        self.eliminaComp(0)
        if self._llista[y-1][x-1][0]==0:
            self.afegeixfitxa(x-1,y-1,3)
        elif self._llista[y-1][x-1][0]==2 and self._llista[y-2][x-2][0]==0:
            self.afegeixfitxa(x-2,y-2,3)
            self._expulsar.append((x-1,y-1))
        if self._llista[y-1][x+1][0]==0:
            self.afegeixfitxa(x+1,y-1,3)
        elif self._llista[y-1][x+1][0]==2 and self._llista[y-2][x+2][0]==0:
            self.afegeixfitxa(x+2,y-2,3)
            self._expulsar.append((x+1,y-1))
            
    def CompNegre(self,x,y):
        self._expulsar=[]
        self.eliminaComp(0)
        if self._llista[y+1][x+1][0]==0:
            self.afegeixfitxa(x+1,y+1,3)
        elif self._llista[y+1][x+1][0]==1 and self._llista[y+2][x+2][0]==0:
            self.afegeixfitxa(x+2,y+2,3)
            self._expulsar.append((x+1,y+1))
        if self._llista[y+1][x-1][0]==0:
            self.afegeixfitxa(x-1,y+1,3)
        elif self._llista[y+1][x-1][0]==1 and self._llista[y+2][x-2][0]==0:
            self.afegeixfitxa(x-2,y+2,3)
            self._expulsar.append((x-1,y+1))

    def MouBlanc(self,x,y):
        self.afegeixfitxa(x,y,1)
        self.eliminafitxa(self._tempx,self._tempy)
        self.eliminaComp(0)
    
    def MouNegre(self,x,y):
        self.afegeixfitxa(x,y,2)
        self.eliminafitxa(self._tempx,self._tempy)
        self.eliminaComp(0)
        
    def Moviment(self,event):
        cord_y=event.widget.winfo_y()//80
        cord_x=event.widget.winfo_x()//80        
        if self._llista[cord_y][cord_x][0]==1 and self._turn==True:
            self.CompBlanca(cord_x,cord_y)
            self._tempx=cord_x
            self._tempy=cord_y
        elif self._llista[cord_y][cord_x][0]==2 and self._turn==False:
            self.CompNegre(cord_x,cord_y)
            self._tempx=cord_x
            self._tempy=cord_y
        if self._llista[cord_y][cord_x][0]==3 and self._turn == True:
            self.MouBlanc(cord_x,cord_y)
            self._turn=False
            if abs(cord_y-self._tempy) >1 or abs(cord_x-self._tempx) >1:
                for num in self._expulsar:
                    self.eliminafitxa(num[0],num[1])
                
        elif self._llista[cord_y][cord_x][0]==3 and self._turn == False:
            self.MouNegre(cord_x,cord_y)
            self._turn=True
            if abs(cord_y-self._tempy) >1 or abs(cord_x-self._tempx) >1:
                for num in self._expulsar:
                    self.eliminafitxa(num[0],num[1])
        
        
     
if __name__ == "__main__":
    root= tk.Tk()
    root.geometry("640x640")
    p= Partida(root)
    root.mainloop()

