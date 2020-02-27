import numpy as np
import matplotlib.pyplot as plt
plt.ion()

class Board():
    def __init__(self):
        self.M=np.zeros((11,11),int)
        self.M[0,:]=3
        self.M[-1,:]=3
        self.M[:,0]=3
        self.M[:,-1]=3
        for k in range(4,0,-1):
            self.M[5-k,len(M)-k-1:]=3
            self.M[len(M)-6+k ,1:k+1]=3
        self.M[1,1:6]=1
        self.M[2,1:7]=1
        self.M[3,3:6]=1
    
        self.M[9,5:10]=2
        self.M[8,4:10]=2
        self.M[7,5:8]=2
        
        self.player=1
        self.other=2
        self.state="Select" # "Move"
        self.first=[]
        self.last=[]
        self.select=[]
        self.sens=""
        
    def swap(self):
        self.select=[]
        self.player,self.other=self.other,self.player
        
    def case(self,event):
        if event.xdata!=None and event.ydata!=None:
            ligne=int(10-event.ydata+.5)
            colonne=int(event.xdata+(0.5*(5-event.ydata))+.5)
            return (ligne,colonne,self.M[ligne,colonne])
        return (None,None,None)
        
        
    def selection(self):
        if len(self.first)==2 and  len(self.last)==2:
            l1,l2=croissant(self.first[0],self.last[0])
            c1,c2=croissant(self.first[1],self.last[1])
            S=self.M.copy()
            if c2-c1>=3 or l2-l1>=3 :
                self.first=[]
                self.last=[]
                self.select=[]
                return
            if l1==l2:
                if c1==c2:
                    self.sens='point'
                    S[l1,c1]=4
                else:
                    self.sens='ligne'
                    S[l1,c1:c2+1]=4
            elif c1==c2:
                self.sens='colonne'
                S[l1:l2+1,c1]=4
            elif l2-l1==c2-c1:
                self.sens='diag'
                for k in range(l2-l1+1):
                    S[l1+k,c1+k]=4
            self.select=[(l1,c1),(l2,c2)]
            affiche(S)
            self.state="Move"
            return
            
    def move(self,event):
        dep=self.case(event)
        print(dep)
        if self.sens=='ligne' or self.sens=='diag':
            ind_var=1
            ind_fix=0
        if self.sens=='colonne':
            ind_var=0
            ind_fix=1
        if dep[2] in [0,self.other]:
            if self.sens=='point' and dep[2]==0:
                self.M[self.select[0]]=0
                self.M[dep[0],dep[1]]=self.player
                self.swap()
            elif self.sens in ['ligne','colonne','diag']:
                print('ligne')
                if dep[2]==0:
                    if dep[ind_var]==self.select[0][ind_var]-1:
                        point=1
                    elif dep[ind_var]==self.select[1][ind_var]+1:
                        point=0
                    else:
                        self.state="Select"
                        affiche(self.M)
                        return
                    if (dep[ind_fix]==self.select[point][ind_fix] and self.sens in ["ligne","colonne"]) or (dep[1]-dep[0]==self.select[1][1]-self.select[1][0] and self.sens=="diag"):
                        print(dep,point,self.select)
                        self.M[dep[0],dep[1]]=self.player
                        self.M[self.select[point]]=0
                        self.swap()
        self.state="Select"
        affiche(self.M)

def croissant(a,b):
    m=min(a,b)
    M=max(a,b)
    return m,M        

def affiche(M):
    ly,lx=M.shape
    for y in range(lx):
        for x in range(ly):
            if M[y,x]==1:
                col='red'
            elif M[y,x]==2:
                col='blue'
            elif M[y,x]==0:
                col='grey'
            elif M[y,x]==4 or M[y,x]==5:
                col='green'
            else:
                col='white'
            c=plt.Circle((x+0.5*(5-y),10-y),.45,color=col)
            ax.add_patch(c)

def onclick(event):
    if B.state=="Select":
        ligne,colonne,bille=B.case(event)
        if bille==B.player:
            B.first=[ligne,colonne]
    elif B.state=="Move":
        B.move(event)


def onrelease(event):
    if B.state=="Select":
        ligne,colonne,bille=B.case(event)
        if bille==B.player:
            B.last=[ligne,colonne]
            B.selection()
        else:
            affiche(B.M)
                
    

fig, ax = plt.subplots(1, 1)
B=Board()
affiche(B.M)
ax.set_aspect('equal')
ax.set_axis_off()
ax.axis([0,10,0,10])
cid = fig.canvas.mpl_connect('button_press_event', onclick)
cid2 = fig.canvas.mpl_connect('button_release_event', onrelease)
plt.show()
        