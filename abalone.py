import numpy as np
import matplotlib.pyplot as plt
plt.ion()

def create_jeu():
    M=np.zeros((11,11),int)
    M[0,:]=3
    M[-1,:]=3
    M[:,0]=3
    M[:,-1]=3
    for k in range(4,0,-1):
        M[5-k,len(M)-k-1:]=3
        M[len(M)-6+k ,1:k+1]=3
    M[1,1:6]=1
    M[2,1:7]=1
    M[3,3:6]=1
    
    M[9,5:10]=2
    M[8,4:10]=2
    M[7,5:8]=2
    return M
    
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
            
def croissant(a,b):
    m=min(a,b)
    M=max(a,b)
    return m,M

def selection(ligne,colonne):
    global S2,select
    S=M.copy()
    S2=[]
    ligne1,colonne1=first
    ligne,ligne1=croissant(ligne,ligne1)
    colonne,colonne1=croissant(colonne, colonne1)
    if colonne1-colonne>=3 or ligne1-ligne>=3:
        return
    if ligne==ligne1 or colonne==colonne1:
        if (S[ligne:ligne1+1,colonne:colonne1+1]==player).all():
            S[ligne:ligne1+1,colonne:colonne1+1]+=3
            select=False
            S2=[[ligne,colonne],[ligne1,colonne1]]
    elif ligne1-ligne==colonne1-colonne:
        for k in range(ligne1-ligne+1):
            if S[ligne+k,colonne+k]==player:
                S[ligne+k,colonne+k]+=3
            else:
                break
        else:
            select=False
            S2=[[ligne,colonne],[ligne1,colonne1]]
            
    print(first,ligne,colonne,M)
    affiche(S)

def autre(player):
    if player==1:
        return 2
    else:
        return 1
    
def deplacement(first):
    global player,gain
    print('deplacement')
    ligne,colonne=first
    MS=np.array(S2)
    if M[ligne,colonne]==0:
        print("déplacement simple")
        if (ligne==MS[:,0]).all():
            print("horizontal")
            if colonne==MS[1,1]+1:
                print("a droite")
                M[MS[0,0],MS[0,1]]=0
                M[ligne,colonne]=player
            elif colonne==MS[0,1]-1:
                M[MS[1,0],MS[1,1]]=0
                M[ligne,colonne]=player
        elif (colonne==MS[:,1]).all():
            print("vertical")
            if ligne==MS[1,0]+1:
                M[MS[0,0],MS[0,1]]=0
                M[ligne,colonne]=player
            elif ligne==MS[0,0]-1:
                M[MS[1,0],MS[1,1]]=0
                M[ligne,colonne]=player
        elif colonne-ligne==MS[0,1]-MS[0,0]==MS[1,1]-MS[1,0]:
            print("diagonal")
            if ligne==MS[1,0]+1:
                M[MS[0,0],MS[0,1]]=0
                M[ligne,colonne]=player
            elif ligne==MS[0,0]-1:
                M[MS[1,0],MS[1,1]]=0
                M[ligne,colonne]=player
        elif MS[0,0]==MS[1,0]:
            for dep in [(1,1,1),(1,0,0),(-1,0,1),(-1,-1,0)]:
                if ligne==MS[dep[2],0]+dep[0] and colonne==MS[dep[2],1]+dep[1]:
                    if (M[MS[0,0]+dep[0]:MS[1,0]+dep[0]+1,MS[0,1]+dep[1]:MS[1,1]+dep[1]+1]==0).all():
                        M[MS[0,0]:MS[1,0]+1,MS[0,1]:MS[1,1]+1]=0
                        M[MS[0,0]+dep[0]:MS[1,0]+dep[0]+1,MS[0,1]+dep[1]:MS[1,1]+dep[1]+1]=player
                        break
        elif MS[0,1]==MS[1,1]:
            print('cote')
            for dep in [(0,1,0),(0,-1,1),(1,1,1),(-1,-1,0)]:
                print(dep,MS)
                if ligne==MS[dep[2],0]+dep[0] and colonne==MS[dep[2],1]+dep[1]:
                    print('ok')
                    print(M[MS[0,0]+dep[0]:MS[1,0]+dep[0]+1,MS[0,1]+dep[1]:MS[1,1]+dep[1]+1])
                    if (M[MS[0,0]+dep[0]:MS[1,0]+dep[0]+1,MS[0,1]+dep[1]:MS[1,1]+dep[1]+1]==0).all():
                        M[MS[0,0]:MS[1,0]+1,MS[0,1]:MS[1,1]+1]=0
                        M[MS[0,0]+dep[0]:MS[1,0]+dep[0]+1,MS[0,1]+dep[1]:MS[1,1]+dep[1]+1]=player 
                        break        
        elif MS[1,1]-MS[0,1]==MS[1,0]-MS[0,0]:
            print('diag')
            for dep in [(0,1,1),(0,-1,0),(1,0,1),(-1,0,0)]:
                print(dep,MS)
                if ligne==MS[dep[2],0]+dep[0] and colonne==MS[dep[2],1]+dep[1]:
                    print('ok')
                    print(M[MS[0,0]+dep[0]:MS[1,0]+dep[0]+1,MS[0,1]+dep[1]:MS[1,1]+dep[1]+1])
                    ok=True
                    for k in range(MS[1,0]-MS[0,0]+1):
                        if M[MS[0,0]+dep[0]+k,MS[0,1]+dep[1]+k]!=0:
                            ok=False
                    if ok:
                        for k in range(MS[1,0]-MS[0,0]+1):
                            M[MS[0,0]+k,MS[0,1]+k]=0
                            M[MS[0,0]+dep[0]+k,MS[0,1]+dep[1]+k]=player 
                    
    elif M[ligne,colonne]==autre(player):
        print ('sumito')
        if (ligne==MS[:,0]).all():
            nb=MS[1,1]-MS[0,1]+1
            nb2=0
            sortie=False
            for k in range(nb):
                if colonne-MS[1,1]==1:
                    sig=1
                elif colonne-MS[0,1]==-1:
                    sig=-1
                else:
                    return
                if M[ligne,colonne+sig*k]==autre(player):
                    nb2+=1
                elif M[ligne,colonne+sig*k]==3:
                    sortie=True
                    break
                elif M[ligne,colonne+sig*k]==0:
                    break
                else:
                    print('sumito impossible')
                    affiche(M)
                    return
            if nb>nb2:
                if sig==1:
                    M[MS[0,0],MS[0,1]]=0
                else:
                    M[MS[1,0],MS[1,1]]=0
                M[ligne,colonne]=player
                if M[ligne,colonne+sig*nb2]==3:
                    gain[player]+=1
                else:
                    M[ligne,colonne+sig*nb2]=autre(player)
            else:
                print('sumito impossible')
                affiche(M)
                return
        elif (colonne==MS[:,1]).all():
            nb=MS[1,0]-MS[0,0]+1
            nb2=0
            sortie=False
            for k in range(nb):
                if ligne-MS[1,0]==1:
                    sig=1
                elif ligne-MS[0,0]==-1:
                    sig=-1
                else:
                    return
                if M[ligne+sig*k,colonne]==autre(player):
                    nb2+=1
                elif M[ligne+sig*k,colonne]==3:
                    sortie=True
                    break
                elif M[ligne+sig*k,colonne]==0:
                    break
                else:
                    print('sumito impossible')
                    affiche(M)
                    return
            if nb>nb2:
                if sig==1:
                    M[MS[0,0],MS[0,1]]=0
                else:
                    M[MS[1,0],MS[1,1]]=0
                M[ligne,colonne]=player
                if M[ligne+sig*nb2,colonne]==3:
                    gain[player]+=1
                else:
                    M[ligne+sig*nb2,colonne]=autre(player)
            else:
                print('sumito impossible')
                affiche(M)
                return                
        elif MS[1,1]-MS[0,1]==MS[1,0]-MS[0,0]:
            nb=MS[1,0]-MS[0,0]+1
            nb2=0
            sortie=False
            for k in range(nb):
                if ligne-MS[1,0]==1:
                    sig=1
                elif ligne-MS[0,0]==-1:
                    sig=-1
                else:
                    return
                if M[ligne+sig*k,colonne+sig*k]==autre(player):
                    nb2+=1
                elif M[ligne+sig*k,colonne+sig*k]==3:
                    sortie=True
                    break
                elif M[ligne+sig*k,colonne+sig*k]==0:
                    break
                else:
                    print('sumito impossible')
                    affiche(M)
                    return
            if nb>nb2:
                if sig==1:
                    M[MS[0,0],MS[0,1]]=0
                else:
                    M[MS[1,0],MS[1,1]]=0
                M[ligne,colonne]=player
                if M[ligne+sig*nb2,colonne+sig*nb2]==3:
                    gain[player]+=1
                else:
                    M[ligne+sig*nb2,colonne+sig*nb2]=autre(player)
            else:
                print('sumito impossible')
                affiche(M)
                return                
    else:
        print('impossible')
    affiche(M)
    player=autre(player)

def case(event):
    ligne=int(10-event.ydata+.5)
    colonne=int(event.xdata+(0.5*(5-event.ydata))+.5)
    return (ligne,colonne)
    

def onclick(event):
    global select,first
    ligne,colonne=case(event)
    first=ligne,colonne
    if select==False:
        deplacement(first)

def onrelease(event):
    global select
    ligne,colonne=case(event)
    if select==True:
        selection(ligne,colonne)
    else:
        select=True

fig, ax = plt.subplots(1, 1)
M=create_jeu()
S2=[]
first=[]
player=1
gain=[0,0,0]
select=True
affiche(M)
ax.set_aspect('equal')
ax.set_axis_off()
ax.axis([0,10,0,10])
cid = fig.canvas.mpl_connect('button_press_event', onclick)
cid2 = fig.canvas.mpl_connect('button_release_event', onrelease)
plt.show()
