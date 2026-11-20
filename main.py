import json,os,sys,urllib.request as r
U=os.getenv("MAKEFUN_ENV_URL") or sys.exit("x")
V=[0,100,320,330,500,900,0]
N=[0];L=12e3;R=(5,4,3,2);I=-10**9;H="abcdefgh";K=[-33,-31,-18,-14,14,18,31,33];G=[-17,-16,-15,-1,1,15,16,17];D=[-17,-15,15,17,-16,-1,1,16]
def S(q):return H[q&7]+f"{q//16+1}"
def u(m):return S(m[0])+S(m[1])+("nbrq"[m[2]-2] if m[2] else "")
def P(f):
 b=[0]*128;p=f.split();w=0;l=0
 for c in p[0]:
  if c=="/":w+=1;l=0
  elif c.isdigit():l+=int(c)
  else:
   v="PNBRQK".index(c.upper())+1;b[(7-w)*16+l]=v if c.isupper() else -v;l+=1
 s=1 if p[1]=="w" else -1;c=p[2]
 t=sum(1<<i for i,ch in enumerate("KQkq") if ch in c)
 e=-1
 if p[3]!="-":e=(int(p[3][1])-1)*16+H.index(p[3][0])
 return b,s,t,e
def A(b,q,y):
 for O,v in((K,2),(G,6)):
  for o in O:
   if not(q+o)&0x88 and b[q+o]==y*v:return 1
 for d in D:
  t=q+d
  while not t&0x88:
   v=b[t]
   if v:
    if v*y>0 and (abs(v)==5 or (abs(v)==3 and abs(d) in(15,17)) or (abs(v)==4 and abs(d) in(1,16))):return 1
    break
   t+=d
 d=-16 if y>0 else 16
 for o in(d-1,d+1):
  if not(q+o)&0x88 and b[q+o]==y:return 1
 return 0
def k(b,s):return next(i for i,v in enumerate(b) if v==s*6)
def g(b,s,c,e):
 m=[]
 for f,v in enumerate(b):
  if v*s<=0:continue
  a=abs(v)
  if a==1:
   d=16*s;t=f+d
   if not t&0x88 and not b[t]:
    if t>>4 in(0,7):
     for p in R:m.append((f,t,p))
    else:
     m.append((f,t,0))
     if f>>4==(1 if s>0 else 6):
      if not b[f+d*2]:m.append((f,f+d*2,0))
   for o in(d-1,d+1):
    t=f+o
    if t&0x88:continue
    if b[t]*s<0:
     if t>>4 in(0,7):
      for p in R:m.append((f,t,p))
     else:m.append((f,t,0))
    elif t==e:m.append((f,t,0))
  elif a in(2,6):
   for o in(K if a==2 else G):
    t=f+o
    if not t&0x88 and b[t]*s<=0:m.append((f,t,0))
  else:
   z=D[:4] if a==3 else D[4:] if a==4 else D
   for d in z:
    t=f+d
    while not t&0x88:
     if b[t]*s>0:break
     m.append((f,t,0))
     if b[t]:break
     t+=d
 for F,T,W,C in((4,6,7,1),(4,2,0,2),(116,118,119,4),(116,114,112,8)):
  if c&C and b[W]==(4 if s>0 else -4) and all(not b[i] for i in range(min(F,W)+1,max(F,W))) and not A(b,F,-s) and not A(b,(F+T)//2,-s) and not A(b,T,-s):m.append((F,T,0))
 return m
def Y(b,s,c,e):
 m=[];j=k(b,s)
 for x in g(b,s,c,e):
  n=M(b,s,c,e,x)[0]
  if not A(n,x[1] if x[0]==j else j,-s):m.append(x)
 return m
def M(b,s,c,e,m):
 n=b[:];f,t,p=m;v=n[f];n[f]=0;n[t]=v
 if abs(v)==1 and t==e and not b[t]:n[t-16*s]=0
 if abs(v)==6 and abs(t-f)==2:
  if t>f:n[t-1]=n[t+1];n[t+1]=0
  else:n[t+1]=n[t-2];n[t-2]=0
 if p:n[t]=s*p
 o=c
 if f==4:o&=~3
 if f==116:o&=~12
 if f==0 or t==0:o&=~2
 if f==7 or t==7:o&=~1
 if f==112 or t==112:o&=~8
 if f==119 or t==119:o&=~4
 q=f+16*s if abs(v)==1 and abs(t-f)==32 else -1
 return n,o,q
def E(b,s):
 t=0
 for i,v in enumerate(b):
  if v:
   w=1 if v>0 else -1;a=abs(v);y=i>>4;x=i&7
   t+=w*(V[a]+((y if w>0 else 7-y)*6 if a==1 else 0)+((7-abs(x-3)-abs(y-3))*3 if a in(2,3) else 0))
 return t*s
def Q(b,s,c,e,a,z):
 t=E(b,s)
 if t>=z:return z
 if t>a:a=t
 m=[x for x in Y(b,s,c,e) if b[x[1]] or x[2]]
 m.sort(key=lambda x:-V[abs(b[x[1]])])
 for x in m:
  n,o,q=M(b,s,c,e,x)
  v=-Q(n,-s,o,q,-z,-a)
  if v>=z:return z
  if v>a:a=v
 return a
def T(b,s,c,e,d,a,z):
 N[0]+=1
 if N[0]>=L:raise TimeoutError
 if d==0:return Q(b,s,c,e,a,z)
 m=Y(b,s,c,e)
 if not m:return -9999 if A(b,k(b,s),-s) else 0
 m.sort(key=lambda x:-V[abs(b[x[1]])])
 for x in m:
  n,o,q=M(b,s,c,e,x)
  v=-T(n,-s,o,q,d-1,-z,-a)
  if v>=z:return z
  if v>a:a=v
 return a
def B(f,l):
 b,s,c,e=P(f);d={u(m):m for m in Y(b,s,c,e)}
 z=[d[x] for x in l if x in d]
 if not z:return l[0]
 N[0]=0;y=z[0];h=1
 try:
  while h<7:
   a=I;w=y
   for m in z:
    n,o,q=M(b,s,c,e,m)
    x=-T(n,-s,o,q,h-1,I,-a)
    if x>a:a=x;w=m
   y=w;h+=1
 except TimeoutError:pass
 return u(y)
def p(q,o):
 w=r.Request(U+q,json.dumps(o).encode(),{"content-type":"application/json"})
 try:
  with r.urlopen(w) as z:return json.load(z)
 except Exception:raise
while True:
 g=p("/game",{})
 if g["status"]=="done":break
 while g["status"]=="your_move":
  g=p("/move",{"game":g["game"],"move":B(g["fen"],g["legal_moves"])})
